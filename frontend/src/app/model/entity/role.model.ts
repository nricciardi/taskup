import { BaseEntity } from "./base-entity.model";

export interface RoleModel extends BaseEntity {
  id: number;
  name: string;
  permission_create: boolean;
  permission_read_all: boolean;
  permission_move_backward: boolean;
  permission_move_forward: boolean;
  permission_move: boolean;
  permission_edit_own: boolean;
  permission_edit_all: boolean;
  permission_edit_task_deadline: boolean;
  permission_change_role: boolean;
  permission_change_assignment: boolean;
  permission_delete_own: boolean;
  permission_delete_all: boolean;
  permission_manage_roles: boolean;
  permission_manage_task_status: boolean;
  permission_manage_task_labels: boolean;
  permission_manage_users: boolean;
}
