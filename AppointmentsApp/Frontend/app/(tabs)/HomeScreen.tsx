import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, Alert } from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { getSalons } from '../services'; // Adjust the import path as needed
import { RootStackParamList } from '../NavigationProps';

// Define the type for the salon item
interface Salon {
  id: number;    // Assuming id is a number. Change it to string if needed.
  name: string;
}

// Define the types for the navigation prop
type HomeScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  'Home'  // Replace 'Home' with the actual name of the screen if different
>;

// Define the props for the HomeScreen component
interface HomeScreenProps {
  navigation: HomeScreenNavigationProp;
}

// Define the HomeScreen component with typed props
const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  // Type the state as an array of Salon objects
  const [salons, setSalons] = useState<Salon[]>([]);

  useEffect(() => {
    fetchSalons();
  }, []);

  const fetchSalons = async () => {
    try {
      const response = await getSalons();
      setSalons(response.data.data); // Ensure this matches the actual response structure
    } catch (error: any) {
      Alert.alert('Error', 'Failed to fetch salons');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Salon List</Text>
      <FlatList
        data={salons}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ padding: 10, borderBottomWidth: 1, borderBottomColor: '#ddd' }}>
            <Text>{item.name}</Text>
          </View>
        )}
      />
      <Button title="Add Salon" onPress={() => navigation.navigate('AddSalon')} />
    </View>
  );
};

export default HomeScreen;
