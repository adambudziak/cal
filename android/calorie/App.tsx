import 'react-native-gesture-handler';
import React from 'react';
import IngredientSearchScreen from './src/screens/IngredientSearchScreen';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import CreateMeal from './src/screens/CreateMeal';

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Create Meal" component={CreateMeal} />
        <Stack.Screen name="Find Ingredient" component={IngredientSearchScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
