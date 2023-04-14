import { Component, Input } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { environment } from 'src/environments/environment.development';

enum DeadlineStatus {
  PRIMARY,
  WARNING,
  DANGER
}


@Component({
  selector: 'app-task-preview',
  templateUrl: './task-preview.component.html',
  styleUrls: ['./task-preview.component.scss']
})
export class TaskPreviewComponent {

  @Input('task') task?: TaskModel;

  DeadlineStatus = DeadlineStatus;

  dateFormat: string = environment.fullDateFormat;

  constructor() {
  }

  getDeadlineStatus(): DeadlineStatus | undefined {

    if(!this.task)
      return undefined;

    if(!this.task.deadline)
      return undefined;

    let now = new Date(Date.now());
    let dealine: Date = new Date(this.task.deadline);

    now.setDate(now.getDate() - environment.warningDateDayBefore);
    if(dealine > now) {
      return this.DeadlineStatus.WARNING;
    }

    now = new Date(Date.now());
    now.setDate(now.getDate() - environment.dangerDateDayBefore);
    if(dealine > now) {
      return this.DeadlineStatus.DANGER;
    }

    return this.DeadlineStatus.PRIMARY;
  }

}
