import WelcomeScreen from "./src/components/WelcomeScreen";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NavigationContainer } from "@react-navigation/native";
import MainPageScreen from "./src/components/MainPage";
import AddHabitScreen from "./src/components/AddHabit";
import FinishedHabitsScreen from "./src/components/FinishedHabits";
import HabitsStatsScreen from "./src/components/HabitsStats";
import Toast from "react-native-toast-message";

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
      <Toast />
    </NavigationContainer>
  );
}
