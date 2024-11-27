import pydgraph
from ..config import get_settings

settings = get_settings()

class DgraphDB:
    def __init__(self):
        self.client = None
        self.stub = None

    def connect(self):
        self.stub = pydgraph.DgraphClientStub(settings.DGRAPH_HOSTS)
        self.client = pydgraph.DgraphClient(self.stub)
        self._set_schema()

    def _set_schema(self):
        schema = """
            # Define types
            type Player {
                player_id
                name
                position
                season_stats
                plays_for
                participated_in
            }

            type Team {
                team_id
                name
                has_players
                competed_in
            }

            type Game {
                game_id
                date
                stage
                team1_score
                team2_score
                team1
                team2
                players
            }

            # Define predicates
            player_id: string @index(exact) .
            name: string @index(exact) .
            position: string @index(exact) .
            season_stats: string .
            plays_for: [uid] @reverse .
            participated_in: [uid] @reverse .
            
            team_id: string @index(exact) .
            has_players: [uid] @reverse .
            competed_in: [uid] @reverse .
            
            game_id: string @index(exact) .
            date: datetime @index(hour) .
            stage: string @index(exact) .
            team1_score: int .
            team2_score: int .
            team1: uid .
            team2: uid .
            players: [uid] .
        """
        
        try:
            self.client.alter(pydgraph.Operation(schema=schema))
            print("Successfully initialized Dgraph schema")
        except Exception as e:
            print(f"Error initializing Dgraph schema: {str(e)}")
            raise

    def close(self):
        if self.stub:
            self.stub.close()

dgraph_db = DgraphDB() 