from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.mongodb import mongodb
from .database.cassandra import cassandra_db
from .database.dgraph import dgraph_db
from .routers import auth, users, teams, games, players, analytics
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Sports Analytics API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(games.router, prefix="/games", tags=["Games"])
app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup():
    try:
        logger.info("Connecting to MongoDB...")
        await mongodb.connect()
        
        logger.info("Connecting to Cassandra...")
        cassandra_db.connect()
        
        logger.info("Connecting to Dgraph...")
        dgraph_db.connect()
        
        logger.info("All database connections established successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown():
    await mongodb.close()
    cassandra_db.close()
    dgraph_db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Sports Analytics API"} 