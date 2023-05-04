import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-success-alert',
  templateUrl: './success-alert.component.html',
  styleUrls: ['./success-alert.component.scss']
})
export class SuccessAlertComponent {
  @Input("title") title?: string;
  // @Input("description") description?: string;
  @Input("dismissable") dismissable: boolean = true;

}
