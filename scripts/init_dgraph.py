import pydgraph
import json

def set_schema():
    client = pydgraph.DgraphClient(pydgraph.DgraphClientStub('localhost:9080'))
    
    schema = """
    type Player {
        player_id: string @index(exact) .
        name: string @index(exact) .
        position: string @index(exact) .
        season_stats: string .
        plays_for: [Team] @reverse .
        participated_in: [Game] @reverse .
    }

    type Team {
        team_id: string @index(exact) .
        name: string @index(exact) .
        has_players: [Player] .
        competed_in: [Game] .
    }

    type Game {
        game_id: string @index(exact) .
        date: datetime @index(hour) .
        stage: string @index(exact) .
        team1_score: int .
        team2_score: int .
        team1: Team .
        team2: Team .
        players: [Player] .
    }
    """
    
    return client.alter(pydgraph.Operation(schema=schema))

if __name__ == "__main__":
    set_schema() 