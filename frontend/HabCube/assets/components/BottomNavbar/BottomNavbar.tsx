import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Icon from "react-native-vector-icons/Ionicons";

const NavItem = ({ iconName, label, onPress }) => (
  <TouchableOpacity style={styles.navItem} onPress={onPress}>
    <Icon name={iconName} size={24} color="#FFFFFF" />
    <Text style={styles.navText}>{label}</Text>
  </TouchableOpacity>
);

const BottomNavbar = ({ onAdd, onFinishedHabits, onStats }) => {
  return (
    <SafeAreaView>
      <View style={styles.bottomNav}>
        <NavItem iconName="add-circle-outline" label="Add" onPress={onAdd} />
        <NavItem
          iconName="checkmark-circle-outline"
          label="Finished Habits"
          onPress={onFinishedHabits}
        />
        <NavItem iconName="bar-chart-outline" label="Stats" onPress={onStats} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  bottomNav: {
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    backgroundColor: "#000000",
    paddingVertical: 15,
  },
  navItem: {
    alignItems: "center",
    paddingHorizontal: 10,
  },
  navText: {
    color: "#FFFFFF",
    fontSize: 12,
    marginTop: 5,
    fontWeight: "500",
  },
});

export default BottomNavbar;
