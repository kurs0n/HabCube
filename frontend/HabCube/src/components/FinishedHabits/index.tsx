import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from "react-native";
import BottomNavbar from "../BottomNavbar/BottomNavbar";
import { RootStackParamList } from "../../../App";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { SafeAreaView } from "react-native-safe-area-context";
import Icon from "react-native-vector-icons/Ionicons";
import AppLogo from "../AppLogo";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "FinishedHabits">;
};

interface FinishedHabit {
  id: number;
  name: string;
  icon: string;
  totalDays: number;
  completedDays: number;
  finishedDate: string;
  isSuccess: boolean;
}

const FINISHED_HABITS: FinishedHabit[] = [
  {
    id: 1,
    name: "Morning Run",
    icon: "fitness",
    totalDays: 21,
    completedDays: 21,
    finishedDate: "2025-10-20",
    isSuccess: true,
  },
  {
    id: 2,
    name: "Read 30 Minutes",
    icon: "book",
    totalDays: 21,
    completedDays: 21,
    finishedDate: "2025-10-15",
    isSuccess: true,
  },
  {
    id: 3,
    name: "Drink 8 Glasses Water",
    icon: "water",
    totalDays: 21,
    completedDays: 20,
    finishedDate: "2025-10-10",
    isSuccess: false,
  },
  {
    id: 4,
    name: "Meditation",
    icon: "leaf",
    totalDays: 21,
    completedDays: 21,
    finishedDate: "2025-10-05",
    isSuccess: true,
  },
  {
    id: 5,
    name: "Early Sleep",
    icon: "bed",
    totalDays: 21,
    completedDays: 4,
    finishedDate: "2025-09-28",
    isSuccess: false,
  },
];

const FinishedHabitsScreen = ({ navigation }: Props) => {
  const handleAdd = () => navigation.navigate("AddHabit");
  const handleFinishedHabits = () => navigation.navigate("FinishedHabits");
  const handleStats = () => navigation.navigate("HabitsStats");
  const handleHome = () => navigation.navigate("MainPage");

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };

  const renderHabitCard = (habit: FinishedHabit) => (
    <View key={habit.id} style={styles.habitCard}>
      <View style={styles.habitHeader}>
        <View style={styles.iconContainer}>
          <Icon name={habit.icon} size={32} color="#000" />
        </View>
        <View style={styles.habitInfo}>
          <View style={styles.habitNameRow}>
            <Text style={styles.habitName}>{habit.name}</Text>
            <Icon
              name={habit.isSuccess ? "checkmark-circle" : "close-circle"}
              size={30}
              color={habit.isSuccess ? "#4CAF50" : "#F44336"}
            />
          </View>
          <Text style={styles.finishedDate}>
            Finished: {formatDate(habit.finishedDate)}
          </Text>
        </View>
      </View>

      <View style={styles.progressBarContainer}>
        <View style={styles.progressBarBackground}>
          <View
            style={[
              styles.progressBarFill,
              { width: `${(habit.completedDays / habit.totalDays) * 100}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {habit.completedDays} / {habit.totalDays} days
        </Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>

      <AppLogo />
      <Text style={styles.title}>Finished Habits</Text>

      <ScrollView style={styles.scrollView}>
        {FINISHED_HABITS.map(renderHabitCard)}
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
    paddingTop: 20,
    paddingBottom: 10,
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
