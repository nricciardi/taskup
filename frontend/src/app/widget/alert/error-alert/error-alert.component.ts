import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-error-alert',
  templateUrl: './error-alert.component.html',
  styleUrls: ['./error-alert.component.scss']
})
export class ErrorAlertComponent {
  @Input("title") title?: string;
  // @Input("description") description?: string;
  @Input("dismissable") dismissable: boolean = true;

}
