# Sports Analytics API

A FastAPI-based application that provides sports analytics data using a multi-database architecture with MongoDB, Cassandra, and Dgraph.

## Features

- User Account Management
  - Registration and Authentication
  - Profile Management
  - Favorite Teams and Players
  - Notifications System

- League Standings and Team Information
  - View League Standings
  - Team Details and Statistics
  - Conference-based Filtering
  - Search Teams

- Game Details and Scheduling
  - View Scheduled Games
  - Game Details and Scores
  - Highlight Videos Access
  - Search Games by Date

- Player Information and Statistics
  - Player Profiles
  - Performance Statistics
  - Game Participation History
  - Search Players

- Advanced Analytics
  - Head-to-Head Team Statistics
  - Player Performance Trends
  - Team Performance Analysis

## Technology Stack

- **FastAPI**: Modern Python web framework
- **MongoDB**: User data and team information
- **Cassandra**: Game details and scheduling
- **Dgraph**: Player-team-game relationships
- **Docker**: Containerization and deployment
- **JWT**: Authentication and authorization

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

## Installation

1. Clone the repository: 

```bash
git clone https://github.com/your-repo/sports-analytics-api.git
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```env
MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=sports_analytics
Cassandra
CASSANDRA_HOSTS=localhost
CASSANDRA_KEYSPACE=sports_analytics
Dgraph
DGRAPH_HOSTS=localhost:9080
JWT
JWT_SECRET_KEY=your-256-bit-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start the databases:

```bash
docker-compose up -d
```

2. Wait for about 30 seconds for the databases to initialize.

3. Run the application:

```bash
uvicorn app.main:app --reload
```

4. Access the API documentation at `http://localhost:8000/docs`

## Project Structure

```plaintext
sports-analytics/
├── app/
│ ├── database/ # Database connections
│ ├── models/ # Data models
│ ├── routers/ # API routes
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ ├── config.py # Configuration
│ └── main.py # Application entry point
├── scripts/ # Initialization scripts
├── tests/ # Test files
├── .env # Environment variables
├── .gitignore
├── docker-compose.yml # Docker services
├── requirements.txt # Python dependencies
└── README.md
```

## API Documentation

The API documentation is automatically generated and can be accessed at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Design

### MongoDB

- Users collection: User profiles and preferences
- Teams collection: Team information and standings

### Cassandra

- GameDetails table: Game-specific information
- TeamGames table: Team-specific game records

### Dgraph

- Player nodes: Player information and relationships
- Team nodes: Team relationships
- Game nodes: Game participation relationships

## Acknowledgments

- FastAPI documentation
- MongoDB documentation
- Cassandra documentation
- Dgraph documentation
