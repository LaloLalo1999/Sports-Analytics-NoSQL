Functional Requirements 
User Account Management (MongoDB)
1.	User Registration: Allow users to create new accounts with a unique username, email, and password.
2.	User Authentication: Authenticate users during login using their email and password.
3.	Password Security: Securely store user passwords by hashing them before saving them to the database.
4.	User Profile Retrieval: Retrieve and display user profile information upon successful login.
5.	User Logout: Allow users to securely log out of their accounts.
6.	User Deletion: Allow users to erase their data.
7.	Forgot my password: Allow the users to securely restore their password through their email.

League Standings and Team Information (MongoDB)
8.	View League Standings: Display current league standings for both the Eastern and Western conferences.
9.	Team Details: Provide detailed information about each team, including wins, losses, games behind, conference record, home and away records, last 10 games, and current streak.
10.	Search Teams: Allow users to search for teams by name.
11.	Filter Standings by Conference: Enable users to filter league standings based on the selected conference.

 
Game Details and Scheduling (Cassandra)
12.	View Scheduled Games: Display a list of scheduled games for a selected date.
13.	Game Details Retrieval: Provide detailed information for each game, including teams involved, scores, date, stage, and highlight video link.
14.	Search Games by Date: Allow users to search for games based on a specific date.
15.	Highlight Videos Access: Provide links to highlight videos for completed games.

Player Information and Statistics (Dgraph)
16.	View Player Profiles: Display detailed profiles for players, including name, position, team, and season statistics.
17.	Search Players: Allow users to search for players by name or team.
18.	Player Game Participation: Show a list of games in which a specific player has participated.
19.	Aggregate Player Statistics: Provide aggregated season statistics for players.
20.	Top Performers: Display a list of top-performing players based on selected statistical categories.

Team and Player Relationships (Dgraph)
21.	Team Roster Display: Display all players associated with a specific team.
22.	Player-Team Associations: Maintain and display relationships between players and their respective teams.
23.	Game Participation Links: Illustrate relationships between players and the games they have participated in.
24.	Team Game History: Display all games that a specific team has competed in.
25.	Graphical Relationship Maps: Provide graphical representations of relationships between players, teams, and games.

User Personalization and Interaction (MongoDB & Dgraph)
26.	Favorite Teams: Allow users to mark teams as favorites for quick access.
27.	Favorite Players: Allow users to mark players as favorites.
28.	Personalized Notifications: Send notifications to users about upcoming games or news related to their favorite teams and players.
29.	User Dashboard: Provide a personalized dashboard displaying favorite teams’ standings and upcoming games.

Advanced Queries and Analytics
30.	Head-to-Head Team Stats: Allow users to view head-to-head statistics between two selected teams.
31.	Player Performance Over Time: Enable users to view a player’s performance trends over the season.
32.	Team Performance Trends: Allow users to analyze team performance over the last games.

Performance Optimization
33.	Indexing for Fast Retrieval (MongoDB): Use indexes on frequently queried fields like team_name and position to optimize query performance.
34.	Efficient Query Execution (Cassandra): Design tables with appropriate partition and clustering keys to satisfy query requirements efficiently.
35.	Graph Indexing (Dgraph): The system shall utilize Dgraph’s indexing strategies on fields like player_id and game_id for faster traversal.
