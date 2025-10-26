import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import Icon from "react-native-vector-icons/Ionicons";

type NavItemProps = {
  iconName: string;
  label: string;
  onPress: () => void;
};

const NavItem = ({ iconName, label, onPress }: NavItemProps) => (
  <TouchableOpacity style={styles.navItem} onPress={onPress}>
    <Icon name={iconName} size={24} color="#FFFFFF" />
    <Text style={styles.navText}>{label}</Text>
  </TouchableOpacity>
);

type BottomNavbarProps = {
  onAdd: () => void;
  onFinishedHabits: () => void;
  onStats: () => void;
  onHome: () => void;
  currentScreen?: string;
};

const BottomNavbar = ({ onAdd, onFinishedHabits, onStats, onHome, currentScreen }: BottomNavbarProps) => {
  return (
      <View style={styles.bottomNav}>
        {currentScreen !== "MainPage" && (
          <NavItem iconName="home-outline" label="Home" onPress={onHome} />
        )}
        {currentScreen !== "AddHabit" && (
          <NavItem iconName="add-circle-outline" label="Add Habit" onPress={onAdd} />
        )}
        {currentScreen !== "FinishedHabits" && (
          <NavItem
            iconName="checkmark-circle-outline"
            label="Finished"
            onPress={onFinishedHabits}
          />
        )}
        {currentScreen !== "HabitsStats" && (
          <NavItem iconName="bar-chart-outline" label="Stats" onPress={onStats} />
        )}
      </View>
  );
};

const styles = StyleSheet.create({
  bottomNav: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    alignItems: "center",
    backgroundColor: "#000000",
    paddingVertical: 8,
  },
  navItem: {
    alignItems: "center",
    paddingHorizontal: 5,
    justifyContent: "center",
  },
  navText: {
    color: "#FFFFFF",
    fontSize: 12,
    fontWeight: "500",
  },
});

export default BottomNavbar;
