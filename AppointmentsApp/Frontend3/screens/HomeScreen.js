import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, ImageBackground, TextInput, SafeAreaView, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import Carousel from 'react-native-reanimated-carousel'; // Import Carousel from reanimated-carousel

const categories = [
  { id: '1', title: 'Salões perto de si' },
  { id: '2', title: 'Os mais visitados' },
];

const carouselItems = [
  { title: "Item 1", text: "Text 1", image: 'https://via.placeholder.com/300x200?text=Item+1' },
  { title: "Item 2", text: "Text 2", image: 'https://via.placeholder.com/300x200?text=Item+2' },
  { title: "Item 3", text: "Text 3", image: 'https://via.placeholder.com/300x200?text=Item+3' },
  { title: "Item 4", text: "Text 4", image: 'https://via.placeholder.com/300x200?text=Item+4' },
  { title: "Item 5", text: "Text 5", image: 'https://via.placeholder.com/300x200?text=Item+5' },
];

const PAGE_WIDTH = 300; // Adjust this to match your design
const HomeScreen = ({ navigation }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const [isFast, setIsFast] = useState(false);
  const [isAutoPlay, setIsAutoPlay] = useState(false);
  const [isPagingEnabled, setIsPagingEnabled] = useState(true);
  const [data, setData] = useState(carouselItems);
  const carouselRef = useRef(null);

  const handleToggleSpeed = () => setIsFast(!isFast);
  const handleToggleAutoPlay = () => setIsAutoPlay(!isAutoPlay);
  const handleTogglePaging = () => setIsPagingEnabled(!isPagingEnabled);
  const handleChangeDataLength = () => {
    setData(data.length === 6 ? carouselItems.concat(carouselItems) : carouselItems);
  };
  const handleScrollPrev = () => carouselRef.current?.scrollTo({ count: -1, animated: true });
  const handleScrollNext = () => carouselRef.current?.scrollTo({ count: 1, animated: true });
  const handleLogIndex = () => console.log(carouselRef.current?.getCurrentIndex());

  const renderCategory = ({ item }) => (
    <TouchableOpacity style={styles.categoryItem} onPress={() => alert(`Selected: ${item.title}`)}>
      <Text style={styles.categoryTitle}>{item.title}</Text>
    </TouchableOpacity>
  );

  const renderCarouselItem = ({ item }) => (
    <View style={styles.carouselItemContainer}>
      <ImageBackground
        source={{ uri: item.image }}
        style={styles.carouselImage}
        imageStyle={styles.carouselImageStyle}
      >
        {/* The image will fill the whole container */}
      </ImageBackground>
      <View style={styles.carouselTextContainer}>
        <Text style={styles.carouselTitle}>{item.title}</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerText}>Saloons</Text>
      </View> 
      <View style={styles.subheader}>
        <Text style={styles.subheaderText}>Lets do a makeover today</Text>
      </View>
      {/* Search Box */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchBox}
          placeholder=""
          value={searchTerm}
          onChangeText={setSearchTerm}
        />
        <Icon name="search" size={20} color="#333" style={styles.searchIcon} />
      </View>
      <View style={styles.categoryheader}>
        <Text style={styles.subheaderText}>Near you</Text>
      </View>
      {/* Carousel */}
      <View style={styles.carouselContainer}>
        <Carousel
          loop={false}
          width={PAGE_WIDTH * 0.85}
          height={PAGE_WIDTH / 2}
          autoPlay={isAutoPlay}
          style={{ width: "100%" }}
          autoPlayInterval={isFast ? 100 : 2000}
          data={data}
          scrollAnimationDuration={1000}
          onSnapToItem={(index) => setActiveIndex(index)}
          renderItem={renderCarouselItem}
          ref={carouselRef}
        />
      </View>
      {/* Action Buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.primaryButton} onPress={() => navigation.navigate('AnotherScreen')}>
          <Text style={styles.buttonText}>Explore Now</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.secondaryButton} onPress={() => navigation.navigate('Login')}>
          <Text style={styles.buttonText}>Log Out</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  header: {
    padding: 5,
    borderRadius: 10,
    marginBottom: 5,
    alignItems: 'center',
  },
  subheader: {
    borderRadius: 10,
    marginBottom: 20,
    alignItems: 'center',
  },
  categoryheader: {
    borderRadius: 10,
    marginTop:10, 
    marginLeft: 30,
    marginBottom:10,
    alignItems: 'left',
  },
  subheaderText: {
    color: '#000',
    fontSize: 20,
  },
  headerText: {
    color: '#000',
    fontSize: 30,
    fontWeight: 'bold',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  searchBox: {
    height: 40,
    borderColor: '#d3d3d3',
    borderWidth: 2,
    borderRadius: 10,
    paddingHorizontal: 10,
    flex: 1,
    backgroundColor: '#fff',
  },
  searchIcon: {
    marginLeft: 10,
  },
  banner: {
    width: '100%',
    height: 150,
    borderRadius: 10,
    marginBottom: 20,
  },
  carouselContainer: {
    margin:20,
    marginBottom: 20,
  },
  carouselItemContainer: {
    borderRadius: 5,
    overflow: 'hidden',
    height: PAGE_WIDTH / 2,
    marginLeft: 5,
    marginRight: 5,
  },
  carouselImage: {
    flex: 1,
    justifyContent: 'center',
  },
  carouselImageStyle: {
    borderRadius: 5,
  },
  carouselTextContainer: {
    backgroundColor: '#fff',
    padding: 10,
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  carouselTitle: {
    fontSize: 18,
    color: '#000',
    fontWeight: 'bold',
  },
  carouselText: {
    fontSize: 14,
    color: '#000',
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  controlButton: {
    backgroundColor: '#ddd',
    padding: 10,
    borderRadius: 5,
    margin: 5,
    alignItems: 'center',
  },
  categoryList: {
    flexGrow: 1,
    marginBottom: 20,
  },
  categoryItem: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  categoryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  primaryButton: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 10,
    width: '48%',
    alignItems: 'center',
  },
  secondaryButton: {
    backgroundColor: '#ff4d4d',
    padding: 15,
    borderRadius: 10,
    width: '48%',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default HomeScreen;
