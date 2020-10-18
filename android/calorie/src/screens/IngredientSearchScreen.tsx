import { TouchableHighlight, View } from 'react-native';
import React, { useEffect, useState } from 'react';
import styled from 'styled-components/native';
import { IngredientType } from '../types';
import { Feather } from '@expo/vector-icons';

const Background = styled.View`
  width: 100%;
  height: 100%;
  background: rgba(7, 98, 16, 0.5);
`;

const SearchHeader = styled.View`
  top: 80px;
  flex: 1;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding-left: 20px;
  padding-right: 20px;
`;

const SearchTextField = styled.View`
  height: 20px;
  line-height: 20px;
  width: 250px;
  height: 52px;

  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(0, 0, 0, 0.15);
  box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.03);
  border-radius: 20px;
  padding-left: 20px;
  flex: 1;
  justify-content: center;
`;

const SearchTextInput = styled.TextInput`
  font-size: 20px;
`;

const ResultsPane = styled.View`
  width: 100%;
  height: 100%;
  top: 120px;
  background: #ffffff;
  border-radius: 30px;
`;

const FoundResultsHeader = styled.View`
  height: 20px;
  align-items: center;
`;

const FoundResultsHeaderText = styled.Text`
  position: absolute;
  font-size: 33px;
  top: 44px;
`;

const SearchResult = styled.View`
  height: 212px;
  background: #ffffff;
  box-shadow: 0px 30px 60px rgba(57, 57, 57, 0.1);
  border-radius: 30px;
  elevation: 10;
  flex: 1;
  align-items: center;
  justify-content: center;
  margin-top: 15px;
  margin-bottom: 15px;
  margin-left: 15px;
  margin-right: 15px;
`;

const SearchResults = styled.FlatList`
  padding-top: 100px;
  padding-left: 15px;
  padding-right: 15px;
  padding-bottom: 200px;
`;

const SearchResultName = styled.Text`
  font-size: 20px;
  font-family: Roboto;
  text-align: center;
`;

const SearchResultCalories = styled.Text`
  font-size: 15px;
  color: #516717;
`;

const IngredientResultList = ({ ingredients }: { ingredients: Array<IngredientType> }) => {
  const renderResult = ({ item }: { item: IngredientType }) => (
    <SearchResult>
      <SearchResultName>{item.name.toLocaleUpperCase()}</SearchResultName>
      <SearchResultCalories>{item.calories} CAL</SearchResultCalories>
    </SearchResult>
  );

  return (
    <View>
      <SearchResults
        data={ingredients}
        renderItem={renderResult}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
      />
    </View>
  );
};

const IngredientSearchScreen = ({ navigation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (searchQuery) {
      fetch(`http://192.168.0.123:9900/meals/ingredients/?search=${searchQuery}`)
        .then((response) => response.json())
        .then(setResults)
        .catch(console.error);
    }
  }, [searchQuery]);

  return (
    <Background>
      <SearchHeader>
        <Feather name="chevron-left" size={30} onPress={() => navigation.pop()} />
        <SearchTextField>
          <SearchTextInput placeholder="Type here" onChangeText={setSearchQuery} autoFocus={true} />
        </SearchTextField>
      </SearchHeader>
      <ResultsPane>
        {results.length > 0 && (
          <>
            <FoundResultsHeader>
              <FoundResultsHeaderText>Found {results.length} results</FoundResultsHeaderText>
            </FoundResultsHeader>
            <IngredientResultList ingredients={results} />
          </>
        )}
      </ResultsPane>
    </Background>
  );
};

export default IngredientSearchScreen;
