import { Component, Input } from '@angular/core';
import { environment } from 'src/environments/environment.development';


export enum DeadlineStatus {
  PRIMARY,
  WARNING,
  DANGER
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

  getDeadlineStatus(): DeadlineStatus | null {

    if(!this.deadline)
      return null;

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
