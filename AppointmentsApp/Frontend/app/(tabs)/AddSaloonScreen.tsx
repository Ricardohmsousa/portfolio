import React, { useState } from 'react';
import { View, TextInput, Button, Alert } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { createSalon } from '../services';
import {RootStackParamList} from '../NavigationProps'
// Define the type for the navigation prop
type AddSalonScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  'AddSalon'
>;

// Define the props for the AddSalonScreen component
interface AddSalonScreenProps {
  navigation: AddSalonScreenNavigationProp;
}

// Define the AddSalonScreen component with typed props
const AddSalonScreen: React.FC<AddSalonScreenProps> = ({ navigation }) => {
  // Define state variables with string types
  const [name, setName] = useState<string>('');
  const [address, setAddress] = useState<string>('');
  const [phone, setPhone] = useState<string>('');

  const handleAddSalon = async () => {
    try {
      await createSalon(name, address, phone);
      Alert.alert('Success', 'Salon added successfully');
      navigation.navigate('Home');  // Navigate to 'Home' screen
    } catch (error: any) {
      Alert.alert('Error', 'Failed to add salon');
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        placeholder="Address"
        value={address}
        onChangeText={setAddress}
      />
      <TextInput
        placeholder="Phone"
        value={phone}
        onChangeText={setPhone}
      />
      <Button title="Add Salon" onPress={handleAddSalon} />
    </View>
  );
};

export default AddSalonScreen;
