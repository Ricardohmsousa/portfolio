import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { register } from '../services';
import {RootStackParamList} from '../NavigationProps'


// Define the types for the navigation prop
type RegisterScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  'Register'
>;

// Define the props for the RegisterScreen component
interface RegisterScreenProps {
  navigation: RegisterScreenNavigationProp;
}

// RegisterScreen component with types
const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleRegister = async () => {
    try {
      await register (username, password);
      Alert.alert('Success', 'User registered successfully');
      navigation.navigate('Login');
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.error || 'Registration failed');
    }
  };

  return (
    <View>
      <Text>Register</Text>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
};

export default RegisterScreen;
