from typing import List, Optional
import json
from datetime import datetime
from ..database.dgraph import dgraph_db
import pydgraph

class DgraphService:
    @staticmethod
    async def create_player(player_data: dict) -> dict:
        mutation = {
            "set": [
                {
                    "uid": "_:player",
                    "dgraph.type": "Player",
                    **player_data
                }
            ]
        }
        try:
            txn = dgraph_db.client.txn()
            response = txn.mutate(set_obj=mutation)
            txn.commit()
            return {"uid": response.uids["player"]}
        finally:
            txn.discard()

    @staticmethod
    async def get_player(player_id: str) -> Optional[dict]:
        query = """
        query player($player_id: string) {
            player(func: eq(player_id, $player_id)) {
                uid
                player_id
                name
                position
                season_stats
                plays_for @facets(since) {
                    uid
                    team_id
                    name
                }
                participated_in @facets(stats) {
                    uid
                    game_id
                    date
                    stage
                    team1 { uid team_id name }
                    team2 { uid team_id name }
                }
            }
        }
        """
        variables = {"$player_id": player_id}
        try:
            txn = dgraph_db.client.txn(read_only=True)
            response = txn.query(query, variables=variables)
            players = json.loads(response.json)["player"]
            return players[0] if players else None
        finally:
            txn.discard()

    @staticmethod
    async def link_player_to_team(player_id: str, team_id: str, since: datetime):
        mutation = {
            "set": [
                {
                    "uid": player_id,
                    "plays_for": {
                        "uid": team_id,
                        "since": since.isoformat()
                    }
                }
            ]
        }
        try:
            txn = dgraph_db.client.txn()
            txn.mutate(set_obj=mutation)
            txn.commit()
        finally:
            txn.discard()

    @staticmethod
    async def execute_query(query: str, variables: dict = None) -> dict:
        try:
            txn = dgraph_db.client.txn(read_only=True)
            response = txn.query(query, variables=variables)
            return json.loads(response.json)
        finally:
            txn.discard()

dgraph_service = DgraphService() 