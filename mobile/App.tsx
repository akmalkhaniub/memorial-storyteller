import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';

import MediaVaultScreen from './src/screens/MediaVaultScreen';
import StoryStudioScreen from './src/screens/StoryStudioScreen';
import GuardianGateScreen from './src/screens/GuardianGateScreen';
import ChildVaultScreen from './src/screens/ChildVaultScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName="MediaVault"
        screenOptions={{
          headerStyle: { backgroundColor: '#0F172A' },
          headerTintColor: '#F8FAFC',
          headerTitleStyle: { fontWeight: '600' },
          contentStyle: { backgroundColor: '#0F172A' }
        }}
      >
        <Stack.Screen 
          name="MediaVault" 
          component={MediaVaultScreen} 
          options={{ title: 'Memory Vault' }} 
        />
        <Stack.Screen 
          name="StoryStudio" 
          component={StoryStudioScreen} 
          options={{ title: 'Story Studio' }} 
        />
        <Stack.Screen 
          name="GuardianGate" 
          component={GuardianGateScreen} 
          options={{ title: 'Guardian Review' }} 
        />
        <Stack.Screen 
          name="ChildVault" 
          component={ChildVaultScreen} 
          options={{ title: "Dad's Storybook" }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
