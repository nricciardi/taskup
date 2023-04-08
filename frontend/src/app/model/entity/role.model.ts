export interface RoleModel {
  id: number;
  name: string;
  permission_create: number;
  permission_read_all: number;
  permission_move_backward: number;
  permission_move_forward: number;
  permission_edit: number;
  permission_change_role: number;
  permission_change_assignment: number;
}