import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Select,
  Input,
  Stack,
  Button,
  Spinner,
  Card,
  CardBody,
  Text,
  SimpleGrid,
} from '@chakra-ui/react';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [conference, setConference] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const { token } = useAuth();
  const showToast = useCustomToast();

  useEffect(() => {
    fetchTeams();
  }, [conference]);

  const fetchTeams = async () => {
    try {
      let url = 'http://localhost:8000/teams/standings';
      if (conference) {
        url += `?conference=${conference}`;
      }
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setTeams(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch teams',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const addToFavorites = async (teamId) => {
    if (!token) {
      showToast({
        title: 'Error',
        description: 'Please login to add favorites',
        status: 'warning',
      });
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/users/me/favorites/teams/${teamId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        showToast({
          title: 'Success',
          description: 'Team added to favorites',
          status: 'success',
        });
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to add team to favorites',
        status: 'error',
      });
    }
  };

  const filteredTeams = teams.filter(team => 
    team.team_name.toLowerCase().includes(searchQuery.toLowerCase())
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
      <Heading mb={6}>Teams</Heading>
      
      <Stack direction={['column', 'row']} spacing={4} mb={6}>
        <Select
          placeholder="Select Conference"
          value={conference}
          onChange={(e) => setConference(e.target.value)}
        >
          <option value="EAST">Eastern Conference</option>
          <option value="WEST">Western Conference</option>
        </Select>
        
        <Input
          placeholder="Search teams..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </Stack>

      <SimpleGrid columns={[1, 2, 3]} spacing={6}>
        {filteredTeams.map((team) => (
          <Card key={team.id}>
            <CardBody>
              <Stack spacing={3}>
                <Text fontWeight="bold" fontSize="xl">{team.team_name}</Text>
                <Text>Conference: {team.conference}</Text>
                <Text>Record: {team.wins}-{team.losses}</Text>
                <Text>Home: {team.home_record}</Text>
                <Text>Away: {team.away_record}</Text>
                <Text>Last 10: {team.last_10}</Text>
                <Button
                  size="sm"
                  colorScheme="blue"
                  onClick={() => addToFavorites(team.id)}
                >
                  Add to Favorites
                </Button>
              </Stack>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default Teams; 