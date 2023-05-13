import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-warning-alert',
  templateUrl: './warning-alert.component.html',
  styleUrls: ['./warning-alert.component.scss']
})
export class WarningAlertComponent {

  @Input("title") title?: string;
  // @Input("description") description?: string;
  @Input("dismissable") dismissable: boolean = true;

}
