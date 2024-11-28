import asyncio
import os
from dotenv import load_dotenv
from app.services.serpapi_service import serpapi_service

# Load environment variables
load_dotenv()

async def test_fetch_games():
    try:
        # Fetch games using the SerpAPIService without storing in DB
        games = await serpapi_service.fetch_games(store_in_db=False)
        
        if not games:
            print("No games found")
            return
            
        # Print the fetched games
        print(f"Found {len(games)} games:")
        for game in games:
            print(f"\n{game['team1_name']} ({game['team1_score']}) vs "
                  f"{game['team2_name']} ({game['team2_score']})")
            print(f"Stage: {game['stage']}")
            print(f"Date: {game['date']}")
            if game['highlight_video_link']:
                print(f"Highlights: {game['highlight_video_link']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error fetching games: {e}")

async def test_fetch_teams():
    try:
        # Test both conferences
        for conf in ["eastern", "western", None]:
            print(f"\nTesting conference: {conf if conf else 'ALL'}")
            teams = await serpapi_service.fetch_teams(conf)
            
            if not teams:
                print("No teams found")
                continue
                
            print(f"Found {len(teams)} teams:")
            for team in teams:
                print(f"\n{team['team_name']} ({team['conference']})")
                print(f"Position: {team['position']}")
                print(f"Record: {team['wins']}-{team['losses']}")
                print(f"Games Behind: {team['games_behind']}")
                print(f"Last 10: {team['last_10']}")
                print(f"Streak: {team['streak']}")
                print("-" * 50)
                
    except Exception as e:
        print(f"Error fetching teams: {e}")
        raise  # Re-raise to see full traceback

# Run the test
if __name__ == "__main__":
    if not os.getenv('SERPAPI_API_KEY'):
        print("Error: SERPAPI_API_KEY not found in environment variables")
    else:
        asyncio.run(test_fetch_games())
        asyncio.run(test_fetch_teams())
