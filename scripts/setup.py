import subprocess
import time
import os

def setup_databases():
    # Start Docker containers
    print("Starting Docker containers...")
    subprocess.run(["docker-compose", "up", "-d"])
    
    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(30)
    
    # Initialize MongoDB
    print("Initializing MongoDB...")
    subprocess.run(["python", "scripts/init_mongodb.py"])
    
    # Initialize Dgraph schema
    print("Initializing Dgraph schema...")
    subprocess.run(["python", "scripts/init_dgraph.py"])
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    setup_databases() 