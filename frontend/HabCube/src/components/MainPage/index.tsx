import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";

import { SafeAreaView } from "react-native-safe-area-context";

import BottomNavbar from "../BottomNavbar/BottomNavbar";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../../App";
import Icon from "react-native-vector-icons/Ionicons";
import AppLogo from "../AppLogo";
import { useHabits } from "../../hooks/useHabits";
import { IHabit } from "../../types/habit.types";
import { useFocusEffect } from "@react-navigation/native";

type MainPageNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "MainPage"
>;

type Props = {
  navigation: MainPageNavigationProp;
};

const MainPageScreen = ({ navigation }: Props) => {
  const handleAdd = () => navigation.navigate("AddHabit");
  const handleFinishedHabits = () => navigation.navigate("FinishedHabits");
  const handleStats = () => navigation.navigate("HabitsStats");
  const handleHome = () => navigation.navigate("MainPage");

  const handleCompleteHabit = (habitId: number) => {
    console.log(`Completing habit ${habitId}`);
  };

  const { fetchHabits } = useHabits();

  useFocusEffect(
    React.useCallback(() => {
      fetchHabits();
    }, [])
  );

  const { habits, loading, error } = useHabits();

  const renderHabitItem = (habit: IHabit) => (
    <View key={habit.id} style={styles.habitCard}>
      <View style={styles.habitHeader}>
        <View style={styles.iconContainer}>
          <Icon name={habit.icon} size={28} color="#000" />
        </View>
        <View style={styles.habitInfo}>
          <Text style={styles.habitName}>{habit.name}</Text>
          <Text style={styles.habitDescription}>{habit.description}</Text>
          <Text style={styles.habitFrequency}>
            {habit.frequency.charAt(0).toUpperCase() + habit.frequency.slice(1)} •
            Streak: {habit.statistics?.current_streak} days
          </Text>
        </View>
        <TouchableOpacity
          style={[
            styles.checkButton,
            habit.statistics?.last_completed === new Date().toISOString().split('T')[0] && styles.checkButtonCompleted,
          ]}
          onPress={() => handleCompleteHabit(habit.id)}
        >
          <Icon
            name={habit.statistics?.last_completed === new Date().toISOString().split('T')[0] ? "checkmark" : "ellipse-outline"}
            size={24}
            color={habit.statistics?.last_completed === new Date().toISOString().split('T')[0] ? "#FFF" : "#000"}
          />
        </TouchableOpacity>
      </View>

      <View style={styles.progressContainer}>
        <View style={styles.progressBarBackground}>
          <View
            style={[
              styles.progressBarFill,
              { width: `${(habit.statistics?.total_completions / 21) * 100}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {habit.statistics?.total_completions} / ${21} days
        </Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>

      <ScrollView style={styles.scrollView}>
        <AppLogo />
        <Text style={styles.title}>Active Habits</Text>

        {habits.map(renderHabitItem)}
      </ScrollView>

      <SafeAreaView edges={['bottom']} style={styles.navbarContainer}>
        <BottomNavbar
          onAdd={handleAdd}
          onFinishedHabits={handleFinishedHabits}
          onStats={handleStats}
          onHome={handleHome}
          currentScreen="MainPage"
        />
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F7F7F7",
    width: "100%",
    paddingTop: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#000000",
    paddingHorizontal: 20,
    paddingTop: 5,
    paddingBottom: 15,
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20,
  },
  habitCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  habitHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
  },
  habitDescription: {
    fontSize: 14,
    marginVertical: 6,
    marginRight: 4,
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: "#F0F0F0",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  habitInfo: {
    flex: 1,
  },
  habitName: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#000000",
    marginBottom: 4,
  },
  habitFrequency: {
    fontSize: 13,
    color: "#666666",
  },
  checkButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 2,
    borderColor: "#000",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#FFF",
  },
  checkButtonCompleted: {
    backgroundColor: "#4CAF50",
    borderColor: "#4CAF50",
  },
  progressContainer: {
    marginTop: 8,
  },
  progressBarBackground: {
    height: 6,
    backgroundColor: "#E0E0E0",
    borderRadius: 3,
    overflow: "hidden",
    marginBottom: 6,
  },
  progressBarFill: {
    height: "100%",
    backgroundColor: "#2196F3",
    borderRadius: 3,
  },
  progressText: {
    fontSize: 11,
    color: "#666666",
    textAlign: "right",
  },
  navbarContainer: {
    backgroundColor: "#000000",
  },
});

export default MainPageScreen;
