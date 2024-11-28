import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Text,
  SimpleGrid,
  Card,
  CardBody,
  Stack,
  Button,
  VStack,
  HStack,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Spinner,
  Badge,
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Home = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    todayGames: [],
    recentResults: [],
    topTeams: [],
  });
  const showToast = useCustomToast();

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      // Get today's date in YYYY-MM-DD format
      const today = new Date().toISOString().split('T')[0];

      // Common fetch options
      const fetchOptions = {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      };

      // Fetch today's games
      const gamesResponse = await fetch(
        `http://localhost:8000/games?date=${today}`,
        fetchOptions
      );
      
      if (!gamesResponse.ok) {
        const errorData = await gamesResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch games');
      }
      const gamesData = await gamesResponse.json();

      // Fetch recent results
      const resultsResponse = await fetch(
        'http://localhost:8000/games/recent',
        fetchOptions
      );
      
      if (!resultsResponse.ok) {
        const errorData = await resultsResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch recent results');
      }
      const resultsData = await resultsResponse.json();

      // Fetch top teams
      const teamsResponse = await fetch(
        'http://localhost:8000/teams/standings?limit=5',
        fetchOptions
      );
      
      if (!teamsResponse.ok) {
        const errorData = await teamsResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch teams');
      }
      const teamsData = await teamsResponse.json();

      setStats({
        todayGames: gamesData || [],
        recentResults: resultsData || [],
        topTeams: teamsData || [],
      });
    } catch (error) {
      console.error('Error fetching home data:', error);
      showToast({
        title: 'Error',
        description: error.message || 'Failed to fetch home page data',
        status: 'error',
        duration: 5000,
      });
      // Set empty arrays as fallback
      setStats({
        todayGames: [],
        recentResults: [],
        topTeams: [],
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="80vh">
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box p={8}>
      <VStack spacing={8} align="stretch">
        {/* Welcome Section */}
        <Box textAlign="center" py={10}>
          <Heading size="2xl" mb={4}>
            Welcome to Sports Analytics
          </Heading>
          <Text fontSize="xl" color="gray.600">
            Your comprehensive platform for sports statistics and analysis
          </Text>
          {!user && (
            <HStack justify="center" mt={6} spacing={4}>
              <Button
                as={RouterLink}
                to="/register"
                colorScheme="blue"
                size="lg"
              >
                Get Started
              </Button>
              <Button
                as={RouterLink}
                to="/login"
                variant="outline"
                size="lg"
              >
                Sign In
              </Button>
            </HStack>
          )}
        </Box>

        {/* Today's Games */}
        <Box>
          <Heading size="lg" mb={4}>Today's Games</Heading>
          {stats.todayGames.length > 0 ? (
            <SimpleGrid columns={[1, 2, 3]} spacing={6}>
              {stats.todayGames.map((game) => (
                <Card key={game.game_id}>
                  <CardBody>
                    <Stack spacing={3}>
                      <Badge colorScheme={game.stage === 'FINAL' ? 'red' : 'green'}>
                        {game.stage}
                      </Badge>
                      <HStack justify="space-between">
                        <Box>
                          <Text fontWeight="bold">{game.team1_name}</Text>
                          <Text fontSize="2xl">{game.team1_score}</Text>
                        </Box>
                        <Text fontSize="lg">VS</Text>
                        <Box>
                          <Text fontWeight="bold">{game.team2_name}</Text>
                          <Text fontSize="2xl">{game.team2_score}</Text>
                        </Box>
                      </HStack>
                    </Stack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          ) : (
            <Text textAlign="center" color="gray.500">No games scheduled for today</Text>
          )}
        </Box>

        {/* Top Teams */}
        <Box>
          <Heading size="lg" mb={4}>Top Teams</Heading>
          {stats.topTeams.length > 0 ? (
            <SimpleGrid columns={[1, 2, 3, 5]} spacing={6}>
              {stats.topTeams.map((team) => (
                <Card key={team.id}>
                  <CardBody>
                    <VStack spacing={2}>
                      <Text fontWeight="bold" fontSize="lg">{team.team_name}</Text>
                      <HStack>
                        <Stat>
                          <StatLabel>Record</StatLabel>
                          <StatNumber>{team.wins}-{team.losses}</StatNumber>
                          <StatHelpText>{team.conference}</StatHelpText>
                        </Stat>
                      </HStack>
                    </VStack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          ) : (
            <Text textAlign="center" color="gray.500">No team data available</Text>
          )}
        </Box>

        {/* Quick Links */}
        <SimpleGrid columns={[1, null, 3]} spacing={6}>
          <Card>
            <CardBody>
              <VStack>
                <Heading size="md">Team Analysis</Heading>
                <Text>Compare team statistics and performance trends</Text>
                <Button
                  as={RouterLink}
                  to="/analytics"
                  colorScheme="blue"
                  variant="outline"
                >
                  View Analytics
                </Button>
              </VStack>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <VStack>
                <Heading size="md">Player Stats</Heading>
                <Text>Explore detailed player statistics and profiles</Text>
                <Button
                  as={RouterLink}
                  to="/players"
                  colorScheme="blue"
                  variant="outline"
                >
                  View Players
                </Button>
              </VStack>
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <VStack>
                <Heading size="md">Game Schedule</Heading>
                <Text>Check upcoming games and recent results</Text>
                <Button
                  as={RouterLink}
                  to="/games"
                  colorScheme="blue"
                  variant="outline"
                >
                  View Games
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </SimpleGrid>
      </VStack>
    </Box>
  );
};

export default Home; 