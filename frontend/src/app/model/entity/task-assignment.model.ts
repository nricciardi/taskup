export interface TaskAssignmentModel {
  id: number;
  assigned_at: Date;

  user_id: number;
  task_id: number;
}
