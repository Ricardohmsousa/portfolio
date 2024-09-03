import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { login } from '../services'; // Adjust the import path as needed
import AsyncStorage from '@react-native-async-storage/async-storage';

interface LoginScreenProps {
  navigation: {
    navigate: (screen: string) => void;
  };
}

// Define the response type for the login function
interface LoginResponse {
  access_token: string;
}

const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleLogin = async () => {
    try {
      const response = await login(username, password);
      const data: LoginResponse = response.data;
      await AsyncStorage.setItem('token', data.access_token);
      navigation.navigate('Home');
    } catch (error: any) {
      // Improved error handling
      const errorMessage = error.response?.data?.error || 'Login failed';
      Alert.alert('Error', errorMessage);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Login</Text>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        style={{ marginBottom: 10, padding: 10, borderColor: '#ddd', borderWidth: 1 }}
      />
      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{ marginBottom: 20, padding: 10, borderColor: '#ddd', borderWidth: 1 }}
      />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
};

export default LoginScreen;
