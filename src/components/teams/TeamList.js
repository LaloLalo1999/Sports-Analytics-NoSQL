import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Container,
  Typography,
  Select,
  MenuItem,
} from '@mui/material';
import { getTeams } from '../../services/api';

const TeamList = () => {
  const [teams, setTeams] = useState([]);
  const [conference, setConference] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const data = await getTeams(conference);
        setTeams(data);
      } catch (error) {
        console.error('Error fetching teams:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, [conference]);

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 4 }}>
        Team Standings
      </Typography>
      <Select
        value={conference}
        onChange={(e) => setConference(e.target.value)}
        sx={{ mb: 2 }}
      >
        <MenuItem value="">All Conferences</MenuItem>
        <MenuItem value="EAST">Eastern</MenuItem>
        <MenuItem value="WEST">Western</MenuItem>
      </Select>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Team</TableCell>
              <TableCell>W</TableCell>
              <TableCell>L</TableCell>
              <TableCell>GB</TableCell>
              <TableCell>Last 10</TableCell>
              <TableCell>Streak</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teams.map((team) => (
              <TableRow key={team.id}>
                <TableCell>{team.team_name}</TableCell>
                <TableCell>{team.wins}</TableCell>
                <TableCell>{team.losses}</TableCell>
                <TableCell>{team.games_behind}</TableCell>
                <TableCell>{team.last_10}</TableCell>
                <TableCell>{team.streak}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default TeamList; 