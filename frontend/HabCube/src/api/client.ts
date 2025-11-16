import axios from "axios";
import { API_CONFIG, API_URL } from "../constants/config";

const apiClient = axios.create({
  baseURL: API_URL,
  // timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  }
})

export default apiClient;