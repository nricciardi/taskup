import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-badge',
  templateUrl: './badge.component.html',
  styleUrls: ['./badge.component.scss']
})
export class BadgeComponent {

  @Input("text") text?: string;
  @Input("icon") icon?: string;
  @Input("color") color?: string;
  @Input("textColor") textColor?: string;

}
