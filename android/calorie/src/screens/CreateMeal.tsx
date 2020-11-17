import styled from 'styled-components/native';
import { IngredientType } from '../types';
import { FlatList, Text } from 'react-native';
import React, { useState } from 'react';
import { EvilIcons } from '@expo/vector-icons';

const Page = styled.View`
  flex: 1;
  padding: 10px;
  padding-top: 50px;
  background: #f7fcf9;
`;

const IngredientSearch = styled.View`
  height: 52px;
  background: #ffffff;
  border-radius: 20px;
  justify-content: center;
  padding-left: 20px;
  padding-right: 20px;
`;

const IngredientSearchContent = styled.TouchableOpacity`
  flex: 1;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const IngredientSearchText = styled.Text`
  font-size: 18px;
  color: #4f6665;
`;

const IngredientName = styled.View`
  width: 220px;
  height: 52px;
  background: #ffffff;
  border-radius: 20px;
  flex: 1;
  justify-content: center;
  padding-left: 20px;
`;

const IngredientGrams = styled.View`
  position: absolute;
  width: 101px;
  height: 52px;
  left: 230px;
  right: 16px;
  background: #ffffff;
  border-radius: 20px;
  flex: 1;
  justify-content: center;
  padding-left: 20px;
`;

const IngredientSeparator = styled.View`
  height: 30px;
`;

const IngredientsView = ({ ingredients }: { ingredients: Array<IngredientType> }) => {
  const renderItem = ({ item }: { item: IngredientType }) => (
    <>
      <IngredientName>
        <Text>
          {item.name} {item.calories}
        </Text>
      </IngredientName>
      <IngredientGrams>
        <Text>123</Text>
      </IngredientGrams>
    </>
  );

  return (
    <FlatList
      data={ingredients}
      renderItem={renderItem}
      keyExtractor={(item) => item.id.toString()}
      ItemSeparatorComponent={() => <IngredientSeparator />}
    />
  );
};

const CreateMeal = ({ navigation }) => {
  return (
    <Page>
      <IngredientSearch>
        <IngredientSearchContent onPress={() => navigation.navigate('Find Ingredient')}>
          <>
            <IngredientSearchText>Find ingredient</IngredientSearchText>
            <EvilIcons name="search" size={20} color="black" />
          </>
        </IngredientSearchContent>
      </IngredientSearch>
      <IngredientsView ingredients={[]} />
    </Page>
  );
};

export default CreateMeal;
