import React, { useState } from 'react';
import {
  Box,
  Heading,
  Select,
  Stack,
  Card,
  CardBody,
  Text,
  Button,
  Spinner,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Stat,
  StatLabel,
  StatNumber,
  StatGroup,
} from '@chakra-ui/react';
import useCustomToast from '../hooks/useCustomToast';

const Analytics = () => {
  const [loading, setLoading] = useState(false);
  const [team1, setTeam1] = useState('');
  const [team2, setTeam2] = useState('');
  const [headToHeadStats, setHeadToHeadStats] = useState(null);
  const [teamPerformance, setTeamPerformance] = useState(null);
  const showToast = useCustomToast();

  const fetchHeadToHead = async () => {
    if (!team1 || !team2) {
      showToast({
        title: 'Error',
        description: 'Please select both teams',
        status: 'warning',
      });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/analytics/teams/head-to-head/${team1}/${team2}`
      );
      if (response.ok) {
        const data = await response.json();
        setHeadToHeadStats(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch head-to-head statistics',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamPerformance = async (teamId) => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/analytics/teams/performance/${teamId}`
      );
      if (response.ok) {
        const data = await response.json();
        setTeamPerformance(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch team performance',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={8}>
      <Heading mb={6}>Analytics</Heading>

      <Tabs>
        <TabList>
          <Tab>Head-to-Head</Tab>
          <Tab>Team Performance</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Stack spacing={4}>
              <Stack direction={['column', 'row']} spacing={4}>
                <Select
                  placeholder="Select Team 1"
                  value={team1}
                  onChange={(e) => setTeam1(e.target.value)}
                >
                  {/* Add team options */}
                </Select>
                <Select
                  placeholder="Select Team 2"
                  value={team2}
                  onChange={(e) => setTeam2(e.target.value)}
                >
                  {/* Add team options */}
                </Select>
                <Button
                  colorScheme="blue"
                  onClick={fetchHeadToHead}
                  isLoading={loading}
                >
                  Compare
                </Button>
              </Stack>

              {headToHeadStats && (
                <Card>
                  <CardBody>
                    <StatGroup>
                      <Stat>
                        <StatLabel>Total Games</StatLabel>
                        <StatNumber>{headToHeadStats.total_games}</StatNumber>
                      </Stat>
                      <Stat>
                        <StatLabel>Team 1 Wins</StatLabel>
                        <StatNumber>{headToHeadStats.team1_wins}</StatNumber>
                      </Stat>
                      <Stat>
                        <StatLabel>Team 2 Wins</StatLabel>
                        <StatNumber>{headToHeadStats.team2_wins}</StatNumber>
                      </Stat>
                    </StatGroup>
                  </CardBody>
                </Card>
              )}
            </Stack>
          </TabPanel>

          <TabPanel>
            <Stack spacing={4}>
              <Select
                placeholder="Select Team"
                onChange={(e) => fetchTeamPerformance(e.target.value)}
              >
                {/* Add team options */}
              </Select>

              {teamPerformance && (
                <Table>
                  <Thead>
                    <Tr>
                      <Th>Date</Th>
                      <Th>Opponent</Th>
                      <Th isNumeric>Score</Th>
                      <Th isNumeric>Opponent Score</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {teamPerformance.map((game) => (
                      <Tr key={game.game_id}>
                        <Td>{new Date(game.date).toLocaleDateString()}</Td>
                        <Td>{game.opponent_team_name}</Td>
                        <Td isNumeric>{game.team_score}</Td>
                        <Td isNumeric>{game.opponent_score}</Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              )}
            </Stack>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default Analytics; 