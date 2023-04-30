import { Component, Input, NO_ERRORS_SCHEMA, Output } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';

@Component({
  selector: 'app-text-avatar',
  templateUrl: './text-avatar.component.html',
  styleUrls: ['./text-avatar.component.scss']
})
export class TextAvatarComponent {

  @Input("color") color?: string;
  @Input("text") text?: string;
  @Input("tooltip") tooltip: string = "";

  darkTxt(): boolean {
    if(!this.color)
      return false;

    return parseInt(this.color, 16) > (0.75 * parseInt("ffffff", 16));
  }
}
