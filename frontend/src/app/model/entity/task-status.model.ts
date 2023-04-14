export interface TaskStatusModel {
  id: number;
  name: string;
  description?: string;

  default_next_task_status_id: number;
  default_next_task_status: TaskStatusModel;

  default_prev_task_status_id: number;
  default_prev_task_status: TaskStatusModel;
}
