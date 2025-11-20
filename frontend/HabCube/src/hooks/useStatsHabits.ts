import { useEffect, useState } from "react"
import { IHabitsStats } from "../types/habit.types"
import { getHabitsStats } from "../api/habits.api"

export const useStatsHabits = () => {
  const [stats, setStats] = useState<IHabitsStats | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatsHabits = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await getHabitsStats();
        setStats(response);
      } catch (err: any) {
        setError("Failed to fetch finished habits.")
      } finally {
        setLoading(false)
      }
    }
    fetchStatsHabits();
  }, [])
  return { stats, loading, error }
}