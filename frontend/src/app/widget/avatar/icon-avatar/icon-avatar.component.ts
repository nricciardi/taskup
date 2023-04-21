import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-icon-avatar',
  templateUrl: './icon-avatar.component.html',
  styleUrls: ['./icon-avatar.component.scss']
})
export class IconAvatarComponent {
  @Input("color") color?: string;
  @Input("iconClass") iconClass?: string;
  @Input("tooltip") tooltip: string = "";
}
