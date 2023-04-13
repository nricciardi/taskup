import { TaskStatusModel } from "./task-status.model";
import { TaskModel } from "./task.model";

export interface DashboardModel {
  task_status: TaskStatusModel[];
  default_task_status_id: number;
  tasks: TaskModel[];
}
