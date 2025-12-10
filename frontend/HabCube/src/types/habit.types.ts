export type FrequencyType = "daily" | "weekly" | "monthly";

export interface IHabit {
  id: number;
  name: string;
  description?: string;
  icon: string;
  frequency: FrequencyType;
  created_at: string;
  active: boolean;
  deadline_time?: string;
  statistics: IHabitStatistics;
  is_completed: boolean;
}

export interface ICreateHabitDTO {
  name: string;
  description?: string;
  icon: string;
  frequency: FrequencyType;
  created_at: string;
  deadline_time?: string;
  type: string;
}

export interface IHabitStatistics {
  id: number;
  habit_id: number;
  total_completions: number;
  current_streak: number;
  best_streak: number;
  success_rate: number;
  last_completed: string | null;
  updated_at: string;
}

export interface IFinishedHabit {
  id: number;
  name: string;
  description?: string;
  icon: string;
  best_streak: number;
  success_status: boolean;
  finish_date: string;
  color: string;
}

export interface IHabitsStats {
  active_habits_count: number;
  average_completion_rate: number;
  completed_habits_count: number;
  longest_streak: number;
  total_habits: number;
}
