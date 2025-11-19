import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from "react-native";
import BottomNavbar from "../BottomNavbar/BottomNavbar";
import { RootStackParamList } from "../../../App";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { SafeAreaView } from "react-native-safe-area-context";
import AppLogo from "../AppLogo";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "HabitsStats">;
};

const HabitsStatsScreen = ({ navigation }: Props) => {
  const handleAdd = () => navigation.navigate("AddHabit");
  const handleFinishedHabits = () => navigation.navigate("FinishedHabits");
  const handleStats = () => navigation.navigate("HabitsStats");
  const handleHome = () => navigation.navigate("MainPage");

  return (
    <View style={styles.container}>

      <AppLogo />
      <Text style={styles.title}>Statistics</Text>

      <ScrollView style={styles.scrollView}>
        <View style={styles.statCard}>
          <Text style={styles.statLabel}>Active habits</Text>
          <Text style={styles.statValue}>5</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statLabel}>Average completion rate</Text>
          <Text style={styles.statValue}>76%</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statLabel}>Longest streak (days)</Text>
          <Text style={styles.statValue}>15</Text>
        </View>

        <View style={styles.statCard}>
          <Text style={styles.statLabel}>Completed habits</Text>
          <Text style={styles.statValue}>5</Text>
        </View>
      </ScrollView>

      <SafeAreaView edges={['bottom']} style={styles.navbarContainer}>
        <BottomNavbar
          onAdd={handleAdd}
          onFinishedHabits={handleFinishedHabits}
          onStats={handleStats}
          onHome={handleHome}
          currentScreen="HabitsStats"
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
    paddingBottom: 20,
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20,
  },
  statCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statLabel: {
    fontSize: 16,
    color: "#666666",
    marginBottom: 8,
  },
  statValue: {
    fontSize: 48,
    fontWeight: "bold",
    color: "#000000",
  },
  navbarContainer: {
    backgroundColor: "#000000",
  },
});

export default HabitsStatsScreen;
