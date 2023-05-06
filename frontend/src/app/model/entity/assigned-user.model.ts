import { UserModel } from "./user.model";

export interface AssignedUserModel {
  user: UserModel;
  assigned_at: Date;
  last_watched_at: Date | null;
}
