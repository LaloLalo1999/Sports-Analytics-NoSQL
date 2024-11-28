import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  VStack,
  HStack,
  Text,
  Button,
  Card,
  CardBody,
  SimpleGrid,
  IconButton,
  FormControl,
  FormLabel,
  Input,
  Badge,
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';
import useCustomToast from '../hooks/useCustomToast';

const Profile = () => {
  const { user, token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [favoriteTeams, setFavoriteTeams] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
  });
  const showToast = useCustomToast();

  useEffect(() => {
    if (user) {
      fetchFavoriteTeams();
      fetchNotifications();
      setFormData({
        username: user.username,
        email: user.email,
      });
    }
  }, [user]);

  const fetchFavoriteTeams = async () => {
    try {
      const promises = user.favorite_teams.map(async (teamId) => {
        const response = await fetch(`http://localhost:8000/teams/${teamId}`);
        if (response.ok) {
          return response.json();
        }
        return null;
      });

      const teams = await Promise.all(promises);
      setFavoriteTeams(teams.filter(team => team !== null));
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch favorite teams',
        status: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await fetch('http://localhost:8000/users/me/notifications', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to fetch notifications',
        status: 'error',
      });
    }
  };

  const removeFavoriteTeam = async (teamId) => {
    try {
      const response = await fetch(`http://localhost:8000/users/me/favorites/teams/${teamId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setFavoriteTeams(favoriteTeams.filter(team => team.id !== teamId));
        showToast({
          title: 'Success',
          description: 'Team removed from favorites',
          status: 'success',
        });
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to remove team from favorites',
        status: 'error',
      });
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/users/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        showToast({
          title: 'Success',
          description: 'Profile updated successfully',
          status: 'success',
        });
        setEditMode(false);
      }
    } catch (error) {
      showToast({
        title: 'Error',
        description: 'Failed to update profile',
        status: 'error',
      });
    }
  };

  return (
    <Box p={8}>
      <Heading mb={6}>Profile</Heading>

      <SimpleGrid columns={[1, null, 2]} spacing={6}>
        <Card>
          <CardBody>
            <VStack align="start" spacing={4}>
              {editMode ? (
                <form onSubmit={handleUpdateProfile} style={{ width: '100%' }}>
                  <VStack spacing={4}>
                    <FormControl>
                      <FormLabel>Username</FormLabel>
                      <Input
                        value={formData.username}
                        onChange={(e) => setFormData({
                          ...formData,
                          username: e.target.value
                        })}
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Email</FormLabel>
                      <Input
                        value={formData.email}
                        onChange={(e) => setFormData({
                          ...formData,
                          email: e.target.value
                        })}
                      />
                    </FormControl>
                    <HStack>
                      <Button type="submit" colorScheme="blue">
                        Save
                      </Button>
                      <Button onClick={() => setEditMode(false)}>
                        Cancel
                      </Button>
                    </HStack>
                  </VStack>
                </form>
              ) : (
                <>
                  <Box>
                    <Text fontWeight="bold">Username</Text>
                    <Text>{user?.username}</Text>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Email</Text>
                    <Text>{user?.email}</Text>
                  </Box>
                  <Button onClick={() => setEditMode(true)}>
                    Edit Profile
                  </Button>
                </>
              )}
            </VStack>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <Heading size="md" mb={4}>Favorite Teams</Heading>
            <VStack align="stretch" spacing={4}>
              {favoriteTeams.map((team) => (
                <HStack key={team.id} justify="space-between">
                  <Text>{team.team_name}</Text>
                  <IconButton
                    icon={<DeleteIcon />}
                    colorScheme="red"
                    variant="ghost"
                    onClick={() => removeFavoriteTeam(team.id)}
                  />
                </HStack>
              ))}
            </VStack>
          </CardBody>
        </Card>

        <Card gridColumn="span 2">
          <CardBody>
            <Heading size="md" mb={4}>Notifications</Heading>
            <VStack align="stretch" spacing={4}>
              {notifications.map((notification) => (
                <Card key={notification.date} variant="outline">
                  <CardBody>
                    <HStack justify="space-between">
                      <VStack align="start" spacing={1}>
                        <Text>{notification.message}</Text>
                        <Text fontSize="sm" color="gray.500">
                          {new Date(notification.date).toLocaleString()}
                        </Text>
                      </VStack>
                      <Badge colorScheme={notification.read ? 'green' : 'red'}>
                        {notification.read ? 'Read' : 'Unread'}
                      </Badge>
                    </HStack>
                  </CardBody>
                </Card>
              ))}
            </VStack>
          </CardBody>
        </Card>
      </SimpleGrid>
    </Box>
  );
};

export default Profile; 