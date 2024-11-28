import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Text,
  Link,
} from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const showToast = useCustomToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Convert form data to URLSearchParams (required for OAuth2 password flow)
      const formData = new URLSearchParams();
      formData.append('username', email);  // OAuth2 expects 'username' field
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        await login(data.access_token, data.user);
        showToast({
          title: 'Success',
          description: 'Logged in successfully',
          status: 'success',
        });
      } else {
        const error = await response.json();
        showToast({
          title: 'Error',
          description: error.detail || 'Invalid email or password',
          status: 'error',
        });
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'An error occurred during login',
        status: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box maxW="md" mx="auto" mt={8} p={6} borderWidth={1} borderRadius={8}>
      <Text fontSize="2xl" mb={4}>Login</Text>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormControl>
          <Button
            type="submit"
            colorScheme="blue"
            width="full"
            isLoading={isLoading}
          >
            Login
          </Button>
          <Text>
            Don't have an account?{' '}
            <Link as={RouterLink} to="/register" color="blue.500">
              Register here
            </Link>
          </Text>
        </VStack>
      </form>
    </Box>
  );
};

export default Login; 