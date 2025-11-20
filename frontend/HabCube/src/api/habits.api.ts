import { ICreateHabitDTO, IFinishedHabit, IHabit, IHabitsStats } from "../types/habit.types";
import apiClient from "./client";
import { ENDPOINTS } from "./endpoints";

export const getHabits = async (): Promise<IHabit[]> => {
  const response = await apiClient.get(ENDPOINTS.HABITS);
  return response.data.habits;
}

export const createHabit = async (habitData: ICreateHabitDTO): Promise<IHabit> => {
  const response = await apiClient.post(ENDPOINTS.CREATE_HABIT, habitData);
  return response.data.habit;
}

export const getFinishedHabits = async (): Promise<IFinishedHabit[]> => {
  const response = await apiClient.get(`${ENDPOINTS.FINISHED_HABITS}`);
  return response.data.habits;
}

export const getHabitsStats = async (): Promise<IHabitsStats> => {
  const response = await apiClient.get(`${ENDPOINTS.STATS_HABITS}`);
  console.log("Stats API Response:", response.data);
  return response.data;
}