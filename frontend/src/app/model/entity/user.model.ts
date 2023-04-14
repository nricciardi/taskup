import { RoleModel } from "./role.model";

export interface UserModel {
  id: number;
  username: string;
  name?: string;
  surname?: string;
  email: string;
  // password: string;    hidden
  role_id: number;
  role?: RoleModel;
}
