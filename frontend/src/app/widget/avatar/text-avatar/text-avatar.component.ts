import { Component, Input } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';

@Component({
  selector: 'app-text-avatar',
  templateUrl: './text-avatar.component.html',
  styleUrls: ['./text-avatar.component.scss']
})
export class TextAvatarComponent {

  @Input("user") user?: UserModel;

  getText(): string {
    if(this.user?.name && this.user?.surname) {
      return this.user.name.substring(0, 1) + this.user.surname.substring(0, 1)
    } else {
      return this.user ? this.user.username.substring(0, 2) : "-";
    }
  }
}
