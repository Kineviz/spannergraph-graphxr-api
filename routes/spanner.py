from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.item import Item, ItemCreate
from google.cloud import spanner
import json
import os
from dotenv import load_dotenv
import yaml
from pydantic import BaseModel

class ExecuteRequest(BaseModel):
    command: str

# Load environment variables
load_dotenv()

router = APIRouter()

s = spanner.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
instance = s.instance(os.getenv('SPANNER_INSTANCE', 'transit'))
client = instance.database(os.getenv('SPANNER_DATABASE', 'transitdb'))

@router.get("/schema")
async def get_items(request: Request):
    # Query to get all tables
    tables_query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_CATALOG = '' AND TABLE_TYPE = 'BASE TABLE'
    """
    
    # Query to get relationships between tables
    relationships_query = """
        SELECT
            fk.TABLE_NAME AS fk_table,
            fk.COLUMN_NAME AS fk_column, 
            pk.TABLE_NAME AS pk_table,
            pk.COLUMN_NAME AS pk_column
        FROM
            INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS rc
        JOIN
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS fk
            ON rc.CONSTRAINT_NAME = fk.CONSTRAINT_NAME
        JOIN
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS pk
            ON rc.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME
        WHERE
            fk.TABLE_NAME != pk.TABLE_NAME
    """
    
    # Use separate snapshots for each query to avoid re-use
    with client.snapshot() as snapshot1:
        # Get all tables
        tables_result = snapshot1.execute_sql(tables_query)
        tables = [row[0] for row in tables_result]
    
    with client.snapshot() as snapshot2:    
        # Get relationships
        relationships_result = snapshot2.execute_sql(relationships_query)
        relationships = []
        for row in relationships_result:
            relationships.append(row[0])
        
        # Remove relationship tables from tables list
        tables = [t for t in tables if t not in relationships]
        
        return {
            "categories": tables,
            "relationships": relationships
        }

@router.post("/execute")
async def execute(request: ExecuteRequest):
    try:
        command = request.command
        # Use environment variable with fallback to request value
        graphName = os.getenv('GRAPH_NAME', 'TransitGraph')
        query = """GRAPH {}
            MATCH p={}
            RETURN SAFE_TO_JSON(p) as thepath
            """.format(graphName, command)
        print("query:",query)
        with client.snapshot() as snapshot:
            results = snapshot.execute_sql(query)
            # Flatten the nested array structure
            all_rows = []
            for row in results:
                # Extract just the inner array values
                row_data = row[0].__dict__["_array_value"]
                all_rows.append(row_data)
            return all_rows
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return []

@router.get("/samples")
async def get_samples():
    try:
        config_path = os.getenv('SAMPLES_PATH', 'samples.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        if not config or 'samples' not in config:
            return {"samples": []}
            
        return {"samples": config['samples']}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Configuration file not found"
        )
    except yaml.YAMLError:
        raise HTTPException(
            status_code=500,
            detail="Error parsing configuration file"
        )