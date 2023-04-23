import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UpdateTaskModel } from 'src/app/model/entity/update-task.model';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
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

  @Output() onDeletion = new EventEmitter<number>();
  @Output() onRemoveAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onAddAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveLabel = new EventEmitter<UpdateTaskModel>();
  @Output() onAddLabel = new EventEmitter<UpdateTaskModel>();

  DeadlineStatus = DeadlineStatus;

  dateFormat: string = environment.fullDateFormat;

  constructor(private taskService: TaskService, public authService: AuthService) {
  }

  ngOnInit() {
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


    let result = this.task.assigned_users?.map(au => au.user.id).includes(userId);

    if(result)
      return result;

    return false;
  }

  getAssignedUsers(): UserModel[] {

    return this.task?.assigned_users?.map(au => au.user) ?? [];

  }

  getAvatarText(user: UserModel): string {
    if(user?.name && user?.surname) {
      return user.name.substring(0, 1) + user.surname.substring(0, 1)
    } else {
      return user ? user.username.substring(0, 2) : "-";
    }
  }

  async removeUserFromTask(userId: number): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Removing user with id ${userId} from task: ${this.task.id} - ${this.task.name}`);

    this.taskService.removeAssignment(this.task.id, userId).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.taskService.find(this.task!.id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
                this.onRemoveAssignment.emit({
                  target: this.task.id,
                  new: t
                });
              }
            })
          })

        }
      })
    });


  }

  async addAssignment(user: UserModel): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Add user ${user.username} to task: ${this.task.id} - ${this.task.name}`);

    this.taskService.addAssignment(this.task.id, user.id).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.taskService.find(this.task!.id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
              }
            });
          })

        }
      })
    });


  }

  delete() {

    if(!this.task)
      return;

    LoggerService.logInfo("Remove task " + this.task?.name);

    this.taskService.deleteById(this.task.id).then((response) => {
      response.subscribe({
        next: (value) => {
          this.onDeletion.emit(this.task!.id);
        }
      })
    })
  }

  canDelete(): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_delete_all)
      return true;

    if(this.task?.author_id == loggedUser.id && !!loggedUser.role?.permission_delete_own)
      return true;


    return false;

  }

  canModify(): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_edit_all)
      return true;

    if(this.task?.author_id == loggedUser.id && !!loggedUser.role?.permission_edit_own)
      return true;


    return false;

  }

  removeLabelFromTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Remove label");

    this.taskService.removeLabel(this.task.id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {

          // refresh task
          this.taskService.find(this.task!.id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;
                this.onRemoveAssignment.emit({
                  target: this.task.id,
                  new: t
                });
              }
            })
          })
        }
      })
    });
  }

  addLabelFromTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Add label");

    this.taskService.addLabel(this.task.id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {


          // refresh task
          this.taskService.find(this.task!.id).then((respose) => {
            respose.subscribe({
              next: (t) => {
                this.task = t;

              }
            })
          })
        }
      })
    });
  }

}
