import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from "react-native";
import BottomNavbar from "../BottomNavbar/BottomNavbar";
import { RootStackParamList } from "../../../App";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { SafeAreaView } from "react-native-safe-area-context";
import Icon from "react-native-vector-icons/Ionicons";
import AppLogo from "../AppLogo";
import { useFinishedHabits } from "../../hooks/useFinishedHabits";
import { IFinishedHabit } from "../../types/habit.types";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "FinishedHabits">;
};

const FinishedHabitsScreen = ({ navigation }: Props) => {
  const handleAdd = () => navigation.navigate("AddHabit");
  const handleFinishedHabits = () => navigation.navigate("FinishedHabits");
  const handleStats = () => navigation.navigate("HabitsStats");
  const handleHome = () => navigation.navigate("MainPage");

  const { habits, loading, error } = useFinishedHabits();

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };


  const renderHabitCard = (habit: IFinishedHabit) => (
    <View key={habit.id} style={styles.habitCard}>
      <View style={styles.habitHeader}>
        <View style={styles.iconContainer}>
          <Icon name={habit.icon} size={32} color="#000" />
        </View>
        <View style={styles.habitInfo}>
          <View style={styles.habitNameRow}>
            <Text style={styles.habitName}>{habit.name}</Text>
            <Icon
              name={habit.success_status ? "checkmark-circle" : "close-circle"}
              size={30}
              color={habit.success_status ? "#4CAF50" : "#F44336"}
            />
          </View>
          <Text style={styles.finishedDate}>
            Finished: {formatDate(habit.finish_date)}
          </Text>
        </View>
      </View>

      <View style={styles.progressBarContainer}>
        <View style={styles.progressBarBackground}>
          <View
            style={[
              styles.progressBarFill,
              { width: `${habit.best_streak >= 21 ? 100 : (habit.best_streak / 21) * 100}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {habit.best_streak} / 21 days
        </Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>

      <ScrollView style={styles.scrollView}>
        <AppLogo />
        <Text style={styles.title}>Finished Habits</Text>

        {habits.map(renderHabitCard)}
      </ScrollView>

      <SafeAreaView edges={["bottom"]} style={styles.navbarContainer}>
        <BottomNavbar
          onAdd={handleAdd}
          onFinishedHabits={handleFinishedHabits}
          onStats={handleStats}
          onHome={handleHome}
          currentScreen="FinishedHabits"
        />
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F7F7F7",
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
    marginBottom: 15,
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
  habitNameRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 4,
  },
  habitName: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#000000",
    flex: 1,
  },
  finishedDate: {
    fontSize: 13,
    color: "#666666",
  },
  progressBarContainer: {
    marginTop: 5,
  },
  progressBarBackground: {
    height: 8,
    backgroundColor: "#E0E0E0",
    borderRadius: 4,
    overflow: "hidden",
    marginBottom: 8,
  },
  progressBarFill: {
    height: "100%",
    backgroundColor: "#4CAF50",
    borderRadius: 4,
  },
  progressText: {
    fontSize: 12,
    color: "#666666",
    textAlign: "center",
  },
  navbarContainer: {
    backgroundColor: "#000000",
  },
});

export default FinishedHabitsScreen;
