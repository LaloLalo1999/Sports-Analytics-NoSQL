import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  SimpleGrid,
  Input,
  Stack,
  Card,
  CardBody,
  Text,
  Button,
  Spinner,
  HStack,
  Badge,
} from '@chakra-ui/react';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Games = () => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const { token } = useAuth();
  const showToast = useCustomToast();

  useEffect(() => {
    fetchGames();
  }, [date]);

  const fetchGames = async () => {
    try {
      const response = await fetch(`http://localhost:8000/games?date=${date}`);
      if (response.ok) {
        const data = await response.json();
        setGames(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch games',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const viewHighlights = async (gameId) => {
    try {
      const response = await fetch(`http://localhost:8000/games/${gameId}/highlights`);
      if (response.ok) {
        const data = await response.json();
        window.open(data.highlight_video_link, '_blank');
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch highlights',
        status: 'error',
      });
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
      <Heading mb={6}>Games</Heading>

      <Stack spacing={4} mb={6}>
        <Input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          max={new Date().toISOString().split('T')[0]}
        />
      </Stack>

      <SimpleGrid columns={[1, 2, 3]} spacing={6}>
        {games.map((game) => (
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

                {game.stage === 'FINAL' && (
                  <Button
                    size="sm"
                    colorScheme="blue"
                    onClick={() => viewHighlights(game.game_id)}
                  >
                    View Highlights
                  </Button>
                )}
              </Stack>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default Games; 