import { TaskStatusModel } from "./task-status.model";
import { TaskModel } from "./task.model";
import { UserModel } from "./user.model";

export interface DashboardModel {
  task_status: TaskStatusModel[];
  default_task_status_id: number;
  tasks: TaskModel[];
  of_user: UserModel;
}
