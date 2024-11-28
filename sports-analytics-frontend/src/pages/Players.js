import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  SimpleGrid,
  Input,
  Select,
  Stack,
  Card,
  CardBody,
  Text,
  Button,
  Spinner,
  VStack,
  HStack,
  Badge,
} from '@chakra-ui/react';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [position, setPosition] = useState('');
  const { token } = useAuth();
  const showToast = useCustomToast();

  useEffect(() => {
    fetchPlayers();
  }, [position]);

  const fetchPlayers = async () => {
    try {
      let url = 'http://localhost:8000/players';
      const params = new URLSearchParams();
      if (position) params.append('position', position);
      if (params.toString()) url += `?${params.toString()}`;

      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setPlayers(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch players',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const addToFavorites = async (playerId) => {
    if (!token) {
      showToast({
        title: 'Error',
        description: 'Please login to add favorites',
        status: 'warning',
      });
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/users/me/favorites/players/${playerId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        showToast({
          title: 'Success',
          description: 'Player added to favorites',
          status: 'success',
        });
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to add player to favorites',
        status: 'error',
      });
    }
  };

  const filteredPlayers = players.filter(player =>
    player.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="80vh">
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box p={8}>
      <Heading mb={6}>Players</Heading>

      <Stack direction={['column', 'row']} spacing={4} mb={6}>
        <Select
          placeholder="Select Position"
          value={position}
          onChange={(e) => setPosition(e.target.value)}
        >
          <option value="G">Guard</option>
          <option value="F">Forward</option>
          <option value="C">Center</option>
        </Select>

        <Input
          placeholder="Search players..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </Stack>

      <SimpleGrid columns={[1, 2, 3, 4]} spacing={6}>
        {filteredPlayers.map((player) => (
          <Card key={player.player_id}>
            <CardBody>
              <VStack align="start" spacing={3}>
                <Heading size="md">{player.name}</Heading>
                <HStack>
                  <Badge colorScheme="blue">{player.position}</Badge>
                  <Badge colorScheme="green">{player.current_team?.team_name || 'Free Agent'}</Badge>
                </HStack>
                <Text fontSize="sm" noOfLines={3}>
                  {player.season_stats}
                </Text>
                <Button
                  size="sm"
                  colorScheme="blue"
                  onClick={() => addToFavorites(player.player_id)}
                  width="full"
                >
                  Add to Favorites
                </Button>
              </VStack>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default Players; 