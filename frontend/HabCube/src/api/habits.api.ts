import { ICreateHabitDTO, IHabit } from "../types/habit.types";
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