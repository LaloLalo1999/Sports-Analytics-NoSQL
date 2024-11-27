from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ..config import get_settings
import time

settings = get_settings()

class CassandraDB:
    def __init__(self):
        self.cluster = None
        self.session = None

    def connect(self):
        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                self.cluster = Cluster([settings.CASSANDRA_HOSTS])
                # First connect without keyspace to create it
                session = self.cluster.connect()
                
                # Create keyspace if it doesn't exist
                session.execute("""
                    CREATE KEYSPACE IF NOT EXISTS sports_analytics 
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
                """)
                
                # Now connect with the keyspace
                self.session = self.cluster.connect(settings.CASSANDRA_KEYSPACE)
                
                # Create tables
                self._create_tables()
                print("Successfully connected to Cassandra")
                break
            except Exception as e:
                print(f"Failed to connect to Cassandra (attempt {retries + 1}/{max_retries}): {str(e)}")
                retries += 1
                if retries < max_retries:
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    raise e

    def _create_tables(self):
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS gamedetails (
                date date,
                game_id uuid,
                stage text,
                team1_id uuid,
                team1_name text,
                team1_score int,
                team2_id uuid,
                team2_name text,
                team2_score int,
                highlight_video_link text,
                PRIMARY KEY ((date), game_id)
            )
        """)

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS teamgames (
                team_id uuid,
                date date,
                game_id uuid,
                opponent_team_id uuid,
                opponent_team_name text,
                team_score int,
                opponent_score int,
                highlight_video_link text,
                PRIMARY KEY ((team_id), date, game_id)
            )
        """)

    def close(self):
        if self.cluster:
            self.cluster.shutdown()

cassandra_db = CassandraDB() 