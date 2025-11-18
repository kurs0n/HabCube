import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import AppLogo from "./AppLogo";

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
      <View style={styles.logoWrapper}>
        <AppLogo style={styles.bigLogo} />
      </View>
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
    fontSize: 28,
    color: "#000",
  },
  appName: {
    fontSize: 36,
    fontWeight: "bold",
    color: "#000",
  },
  logoWrapper: {
    alignItems: "center",
    justifyContent: "center",
    width: "100%",
  },
  bigLogo: {
    width: 200,
    height: 200,
    marginTop: 10,
    marginBottom: 20,
    alignSelf: "center",
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
