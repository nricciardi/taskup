import { Injectable } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  getAvatarText(user: UserModel): string {
    if(user?.name && user?.surname) {
      return user.name.substring(0, 1) + user.surname.substring(0, 1)
    } else {
      return user ? user.username.substring(0, 2) : "-";
    }
  }
}
