import { useEffect, useState } from "react";
import { IHabit } from "../types/habit.types";
import { getHabits } from "../api/habits.api";

export const useHabits = () => {

  const [loading, setLoading] = useState<boolean>(false);
  const [habits, setHabits] = useState<IHabit[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHabits();
  }, [])

  const fetchHabits = async () => {
    setLoading(true);
    try {
      const data = await getHabits();
      setHabits(data);
    } catch (err) {
      setError("Failed to fetch habits.");
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    habits,
    error,
    fetchHabits,
  }
}