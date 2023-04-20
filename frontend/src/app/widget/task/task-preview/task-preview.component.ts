import { Component, Input } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UserModel } from 'src/app/model/entity/user.model';
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
  @Input("loggedUser") loggedUser?: UserModel;

  DeadlineStatus = DeadlineStatus;

  dateFormat: string = environment.fullDateFormat;

  constructor() {
  }

  getDeadlineStatus(): DeadlineStatus | undefined {

    if(!this.task)
      return undefined;

    if(!this.task.deadline)
      return undefined;

    const now = new Date(Date.now());
    const dealine: Date = new Date(this.task.deadline);

    const dangerDate = new Date(dealine);
    dangerDate.setDate(dangerDate.getDate() - environment.dangerDateDayBefore);
    if(now > dangerDate) {
      return this.DeadlineStatus.DANGER;
    }

    const warningDate = new Date(dealine);
    warningDate.setDate(warningDate.getDate() - environment.warningDateDayBefore);
    if(now > warningDate) {
      return this.DeadlineStatus.WARNING;
    }

    return this.DeadlineStatus.PRIMARY;
  }

  userAssignedToTask(userId: number | undefined): boolean {

    if(!userId || !this.task)
      return false;


    let result = this.task.users?.map(u => u.id).includes(userId);


    if(result)
      return result;

    return false;
  }
}
