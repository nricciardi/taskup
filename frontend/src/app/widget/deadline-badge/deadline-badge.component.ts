import { Component, EventEmitter, Input, Output } from '@angular/core';
import { environment } from 'src/environments/environment.development';


export enum DeadlineStatus {
  PRIMARY,
  WARNING,
  DANGER,
  DONE
};


@Component({
  selector: 'app-deadline-badge',
  templateUrl: './deadline-badge.component.html',
  styleUrls: ['./deadline-badge.component.scss']
})
export class DeadlineBadgeComponent {

  dateFormat: string = environment.fullDateFormat;

  DeadlineStatus = DeadlineStatus;

  @Input("deadline") deadline: Date | null = null;
  @Input("done") done: boolean = false;   // flag to set done
  @Input("editable") editable: boolean = false;   // enable modal to modify
  @Input("id") id?: string;     // unique id to prevent mismatch on edit modal

  @Output() onDeadlineModified = new EventEmitter<Date>();


  getDeadlineStatus(): DeadlineStatus | null {

    if(!this.deadline)
      return null;

    if(this.done) {
      return DeadlineStatus.DONE;
    }

    const now = new Date(Date.now());
    const dealine: Date = new Date(this.deadline);

    const dangerDate = new Date(dealine);
    dangerDate.setDate(dangerDate.getDate() - environment.dangerDateDayBefore);
    if(now > dangerDate) {
      return DeadlineStatus.DANGER;
    }

    const warningDate = new Date(dealine);
    warningDate.setDate(warningDate.getDate() - environment.warningDateDayBefore);
    if(now > warningDate) {
      return DeadlineStatus.WARNING;
    }

    return DeadlineStatus.PRIMARY;
  }
}
