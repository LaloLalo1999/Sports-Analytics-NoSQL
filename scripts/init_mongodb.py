from pymongo import MongoClient
import json

def init_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.sports_analytics
    
    # Create collections
    db.create_collection('users')
    db.create_collection('teams')
    
    # Create indexes
    db.users.create_index('email', unique=True)
    db.users.create_index('username')
    db.teams.create_index('team_name')
    db.teams.create_index([('conference', 1), ('position', 1)])
    
    print("MongoDB initialized successfully")

if __name__ == "__main__":
    init_mongodb() 