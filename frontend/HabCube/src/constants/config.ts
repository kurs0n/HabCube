import { Platform } from 'react-native';

const getBaseUrl = () => {
  // if (Platform.OS === 'android') {
  //   // Android emulator
  //   return 'http://10.0.2.2:5000';
  // } else if (Platform.OS === 'ios') {
  //   // iOS simulator
  //   return 'http://localhost:5000';
  // } else {
  //   // Web (przeglądarka)
  //   return 'http://localhost:5000';
  // }
  return 'https://backend-1089871134307.europe-west1.run.app';
};

export const API_CONFIG = {
  BASE_URL: getBaseUrl(),
  API_VERSION: 'v1',
  TIMEOUT: 10000,
}

export const API_URL = `${API_CONFIG.BASE_URL}/api/${API_CONFIG.API_VERSION}`;
