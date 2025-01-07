#  GraphXR Spanner Connector

A FastAPI-based service that enables GraphXR to connect and visualize graph data stored in Google Cloud Spanner. This API service acts as a bridge between GraphXR and Spanner Graph, allowing interactive graph data exploration and visualization.

## Prerequisites

- Docker and Docker Compose
- Google Cloud Platform account
- Google Cloud Spanner instance
- Google Cloud credentials (credentials.json)

## Project Setup

1. Clone the repository
2. Place your `credentials.json` file in the project root directory
3. Create a `.env` file with the following variables or set them in the docker-compose.yml file:

```
ENVIRONMENT=development
SPANNER_INSTANCE=transit
SPANNER_DATABASE=transitdb
GOOGLE_CLOUD_PROJECT=code4demo
GRAPH_NAME=TransitGraph
```


## Running the Application

### Using Docker Compose (Recommended)

1. Build and start the container:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Connect with GraphXR Grove

To connect the API with GraphXR Grove, follow these steps:

1. Access GraphXR Grove through one of these options:
   - Use the shared demo link: [Spanner Graph Transit Demo](https://graphxr.kineviz.com/share/677ce4fc63df25e71340f471/spanner-graph-transit-demo?userID=5c020fe520f1ed00216552c3&groveProjectId=677ce4fc63df25e71340f471&groveFileKey=spanner-graph&groveVersion=0&groveFullscreen=true&groveReadonly=true&groveBlockMode=hide)
   > **Notice:** The demo link uses a trial database which may not always be accessible. If you encounter connection issues, please set up your own project following the instructions below.
   - Create your own project in GraphXR Grove

2. If creating your own project:
   - Open GraphXR(https://graphxr.kineviz.com/)
   - Create a new project
   - Navigate to the Grove panel
   - Drag and drop the Grove connector to connect to your API endpoint (http://localhost:8000)
   - Import the provided Grove connector file: [spanner-graph.grove](https://github.com/Kineviz/spannergraph-graphxr-api/blob/master/spanner-graph.grove)
   - Set the server address to http://localhost:8000

3. You should see a UI like this:

![Spanner Graph UI](https://github.com/Kineviz/spannergraph-graphxr-api/blob/master/images/spanner-graph.jpg?raw=true)

## API Endpoints

- `GET /api/v1/spanner/schema`: Retrieve database schema information
- `POST /api/v1/spanner/execute`: Execute graph queries
- `GET /api/v1/spanner/samples`: Get predefined query samples
## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| ENVIRONMENT | Application environment | development |
| SPANNER_INSTANCE | Google Cloud Spanner instance name | transit |
| SPANNER_DATABASE | Spanner database name | transitdb |
| GOOGLE_CLOUD_PROJECT | Google Cloud project ID | - |
| GRAPH_NAME | Name of the graph in Spanner | TransitGraph |

## Project Structure

```
.
├── main.py              # FastAPI application entry point
├── routes/              # API route handlers
├── models/              # Pydantic models
├── docker-compose.yml   # Docker compose configuration
├── Dockerfile          # Docker build instructions
├── requirements.txt    # Python dependencies
└── samples.yaml        # Sample queries configuration
```
## Data Source

The transit data used in this project is sourced from [TransitFraudDemo](https://github.com/maguec/TransitFraudDemo), which provides sample transit data for demonstration purposes.




## Development

The application uses FastAPI with automatic reload enabled in development mode. Any changes to the Python files will trigger an automatic restart of the application.

## Security Notes

- The application currently allows all CORS origins (`*`)
- Ensure your `credentials.json` is properly secured and not committed to version control
- Review the `.gitignore` file to ensure sensitive files are not tracked
