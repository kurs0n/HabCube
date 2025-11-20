import { useEffect, useState } from "react"
import { IFinishedHabit } from "../types/habit.types"
import { getFinishedHabits } from "../api/habits.api"

export const useFinishedHabits = () => {
  const [habits, setHabits] = useState<IFinishedHabit[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFinishedHabits = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await getFinishedHabits();
        setHabits(response);
      } catch (err: any) {
        setError("Failed to fetch finished habits.")
      } finally {
        setLoading(false)
      }
    }
    fetchFinishedHabits();
  }, [])
  return { habits, loading, error }
}