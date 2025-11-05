import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";

type WelcomeScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  "Welcome"
>;

type Props = {
  navigation: WelcomeScreenNavigationProp;
};

const WelcomeScreen: React.FC<Props> = ({ navigation }) => {
  const handleStart = () => {
    navigation.navigate("MainPage");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to</Text>
      <Text style={styles.appName}>HabCube</Text>

      <TouchableOpacity style={styles.button} onPress={handleStart}>
        <Text style={styles.buttonText}>Start</Text>
      </TouchableOpacity>
    </View>
  );
};

export default WelcomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 24,
    color: "#000",
    marginBottom: 6,
  },
  appName: {
    fontSize: 36,
    fontWeight: "bold",
    color: "#000",
    marginBottom: 40,
  },
  button: {
    backgroundColor: "#000",
    paddingVertical: 14,
    paddingHorizontal: 60,
    borderRadius: 25,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "600",
  },
});
