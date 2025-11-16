import { useState } from "react";
import { createHabit } from "../api/habits.api";
import { ICreateHabitDTO, IHabit } from "../types/habit.types";

export const useCreateHabit = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addHabit = async (habitData: ICreateHabitDTO): Promise<IHabit | null> => {
    setLoading(true);
    setError(null);
    try {
      const newHabit = await createHabit(habitData);
      return newHabit;
    } catch (err: any) {
      setError("Failed to create habit.");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { addHabit, loading, error };
};