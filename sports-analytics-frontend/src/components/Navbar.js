import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Flex,
  Text,
  Button,
  Stack,
  Link,
} from '@chakra-ui/react';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  
  return (
    <Box bg="gray.100" px={4}>
      <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
        <Box>
          <Text fontSize="lg" fontWeight="bold">
            Sports Analytics
          </Text>
        </Box>

        <Flex alignItems={'center'}>
          <Stack direction={'row'} spacing={7}>
            <Link as={RouterLink} to="/">Home</Link>
            <Link as={RouterLink} to="/teams">Teams</Link>
            <Link as={RouterLink} to="/players">Players</Link>
            <Link as={RouterLink} to="/games">Games</Link>
            <Link as={RouterLink} to="/analytics">Analytics</Link>
            
            {user ? (
              <>
                <Link as={RouterLink} to="/profile">Profile</Link>
                <Button onClick={logout}>Logout</Button>
              </>
            ) : (
              <>
                <Link as={RouterLink} to="/login">Login</Link>
                <Link as={RouterLink} to="/register">Register</Link>
              </>
            )}
          </Stack>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navbar; 