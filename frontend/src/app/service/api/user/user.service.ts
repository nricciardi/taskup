import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { UserModel } from 'src/app/model/entity/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService extends EntityApiService<UserModel> {
  override ALL: string = "user_all_as_dict";
  override FIND: string = "user_find";
}
