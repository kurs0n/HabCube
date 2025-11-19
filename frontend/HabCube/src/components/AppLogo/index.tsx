import React from "react";
import { Image, ImageStyle, StyleSheet, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";

type Props = {
  style?: ImageStyle;
};

const AppLogo: React.FC<Props> = ({ style }) => {
  const navigation = useNavigation<any>();
  const handlePress = () => {
    navigation.navigate("MainPage");
  };

  return (
    <TouchableOpacity onPress={handlePress} activeOpacity={0.7}>
      <Image
        source={require("../../../assets/iconNoBg1.png")}
        style={[styles.logo, style]}
        resizeMode="contain"
      />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  logo: {
    width: 100,
    height: 100,
    top: 10,
    left: 10,
    zIndex: 10,
    paddingBottom: 20,
  },
});

export default AppLogo;