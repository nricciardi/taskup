export interface TaskModel {
  id: number;
  name: string;
  description: string;
  deadline: Date;
  priority: number;
  created_at: Date;
  updated_at: Date;
  author_id: number;
  task_status_id: number;
}
