# FastAPI Graph Query Service

A FastAPI-based service that provides graph query capabilities using Google Cloud Spanner.

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

## Configure Samples(Optional)

### samples.yaml
Create a `samples.yaml` file to define your graph query samples:

```yaml
samples:
  - name: "Sample Query Name"
    command: "(n:Label)-[:RELATIONSHIP]->(m:Label)"
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

## Development

The application uses FastAPI with automatic reload enabled in development mode. Any changes to the Python files will trigger an automatic restart of the application.

## Security Notes

- The application currently allows all CORS origins (`*`)
- Ensure your `credentials.json` is properly secured and not committed to version control
- Review the `.gitignore` file to ensure sensitive files are not tracked
