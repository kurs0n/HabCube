import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  TextInput,
  Platform,
  ScrollView,
} from "react-native";
import React from "react";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../../App";
import BottomNavbar from "../BottomNavbar/BottomNavbar";
import { SafeAreaView } from "react-native-safe-area-context";
import { Picker } from "@react-native-picker/picker";
import Icon from "react-native-vector-icons/Ionicons";

import DateTimePicker from "@react-native-community/datetimepicker";

import { AVAILABLE_ICONS } from "../../assets/data/icons";

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, "AddHabit">;
};


const AddHabitScreen = ({ navigation }: Props) => {
  const handleAdd = () => navigation.navigate("AddHabit");
  const handleFinishedHabits = () => navigation.navigate("FinishedHabits");
  const handleStats = () => navigation.navigate("HabitsStats");
  const handleHome = () => navigation.navigate("MainPage");

  const [habitName, setHabitName] = React.useState("");
  const [habitDescription, setHabitDescription] = React.useState("");
  const [habitFrequency, setHabitFrequency] = React.useState("daily");
  const [habitStartDate, setHabitStartDate] = React.useState(new Date());
  const [showDatePicker, setShowDatePicker] = React.useState(false);
  const [habitIcon, setHabitIcon] = React.useState(AVAILABLE_ICONS[0].name);

  const handleSubmit = () => {
    console.log({
      name: habitName,
      description: habitDescription,
      frequency: habitFrequency,
      startDate: habitStartDate.toISOString(),
    });
  };

  const onDateChange = (event: any, selectedDate?: Date) => {
    const currentDate = selectedDate || habitStartDate;
    setShowDatePicker(false);
    setHabitStartDate(currentDate);
  };

  return (
    <View style={styles.container}>
      <ScrollView>
        <Text style={styles.title}>Create New Habit</Text>

        <Text style={styles.title}>Habit Name:</Text>
        <TextInput
          placeholder="Habit Name"
          value={habitName}
          onChangeText={setHabitName}
          style={styles.input}
        />

        <Text style={styles.title}>Description:</Text>
        <TextInput
          placeholder="Description (optional)"
          value={habitDescription}
          onChangeText={setHabitDescription}
          style={styles.input}
        />

        <Text style={styles.label}>Choose Icon:</Text>
        <View style={styles.iconGrid}>
          {AVAILABLE_ICONS.map((icon) => (
            <TouchableOpacity
              key={icon.name}
              style={[
                styles.iconOption,
                habitIcon === icon.name && styles.selectedIcon,
              ]}
              onPress={() => setHabitIcon(icon.name)}
            >
              <Icon
                name={icon.name}
                size={32}
                color={habitIcon === icon.name ? "#FFF" : "#000"}
              />
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.title}>Frequency:</Text>
        <Picker
          selectedValue={habitFrequency}
          onValueChange={(itemValue) => setHabitFrequency(itemValue)}
          style={styles.pickerContainer}
        >
          <Picker.Item label="Daily" value="daily" />
          <Picker.Item label="Weekly" value="weekly" />
          <Picker.Item label="Monthly" value="monthly" />
        </Picker>

        <Text style={styles.title}>Start Date:</Text>
        <TouchableOpacity
          style={styles.input}
          onPress={() => setShowDatePicker(true)}
        >
          <Text style={styles.dateText}>
            {habitStartDate.toLocaleDateString("en-GB")}
          </Text>
        </TouchableOpacity>

        {showDatePicker && (
          <DateTimePicker
            value={habitStartDate}
            mode="date"
            display={Platform.OS === "ios" ? "spinner" : "default"}
            onChange={onDateChange}
          />
        )}
        <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
          <Text style={styles.submitButtonText}>Add Habit</Text>
        </TouchableOpacity>
      </ScrollView>

      <SafeAreaView edges={['bottom']} style={styles.navbarContainer}>
        <BottomNavbar
          onAdd={handleAdd}
          onFinishedHabits={handleFinishedHabits}
          onStats={handleStats}
          onHome={handleHome}
          currentScreen="AddHabit"
        />
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F7F7F7",
    paddingTop: 50,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#000000",
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  label: {
    fontSize: 16,
    fontWeight: "600",
    color: "#000000",
    paddingHorizontal: 20,
    marginBottom: 8,
    marginTop: 10,
  },
  input: {
    height: 50,
    borderColor: "#CCCCCC",
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 15,
    marginHorizontal: 20,
    marginBottom: 15,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
  },
  pickerContainer: {
    borderColor: "#CCCCCC",
    borderWidth: 1,
    borderRadius: 8,
    marginHorizontal: 20,
    marginBottom: 15,
    backgroundColor: "#FFFFFF",
    height: 60,
  },
  dateText: {
    fontSize: 16,
    color: "#000",
    paddingVertical: 5,
  },
  spacer: {
    flex: 1,
  },
  iconGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    paddingHorizontal: 15,
    marginBottom: 20,
  },
  iconOption: {
    width: 60,
    height: 60,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 12,
    margin: 5,
    backgroundColor: "#FFF",
    borderWidth: 2,
    borderColor: "#CCCCCC",
  },
  selectedIcon: {
    backgroundColor: "#000",
    borderColor: "#000",
  },
  submitButton: {
    backgroundColor: "#000",
    padding: 15,
    borderRadius: 8,
    marginHorizontal: 20,
    marginTop: 20,
    marginBottom: 20,
    alignItems: "center",
  },
  submitButtonText: {
    color: "#FFF",
    fontSize: 16,
    fontWeight: "600",
  },
  navbarContainer: {
    backgroundColor: "#000000",
  },
});

export default AddHabitScreen;
