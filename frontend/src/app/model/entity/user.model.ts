import { RoleModel } from "./role.model";

export interface UserModel {
  id: number;
  username: string;
  email: string;
  // password: string;    hidden
  role_id: number;
  role?: RoleModel;
}
