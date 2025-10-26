import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import WelcomeScreen from "./assets/components/WelcomeScreen";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NavigationContainer } from "@react-navigation/native";
import MainPageScreen from "./assets/components/MainPage";
import AddHabitScreen from "./assets/components/AddHabit";
import FinishedHabitsScreen from "./assets/components/FinishedHabits";
import HabitsStatsScreen from "./assets/components/HabitsStats";

export type RootStackParamList = {
  Welcome: undefined;
  MainPage: undefined;
  AddHabit: undefined;
  FinishedHabits: undefined;
  HabitsStats: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Welcome"
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Welcome" component={WelcomeScreen} />
        <Stack.Screen name="MainPage" component={MainPageScreen} />
        <Stack.Screen name="AddHabit" component={AddHabitScreen} />
        <Stack.Screen name="FinishedHabits" component={FinishedHabitsScreen} />
        <Stack.Screen name="HabitsStats" component={HabitsStatsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
