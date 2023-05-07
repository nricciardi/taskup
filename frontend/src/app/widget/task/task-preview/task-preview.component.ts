import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';
import { BlueprintTaskModel, TaskModel } from 'src/app/model/entity/task.model';
import { UpdateTaskModel } from 'src/app/model/entity/update-task.model';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { TaskAssignmentService } from 'src/app/service/api/entity/task-assignment/task-assignment.service';
import { TaskStatusService } from 'src/app/service/api/entity/task-status/task-status.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';
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

  taskStatusMaskFn(taskStatus: TaskStatusModel) {
    return taskStatus.name;
  }

  compareTaskStatusFn(a: TaskStatusModel, b: TaskStatusModel) {
    return a.id == b.id;
  }


  @Input('task') task?: TaskModel;
  @Input("todoCollapseStatus") todoCollapseStatus: boolean = false;
  @Input("taskStatus") taskStatus: TaskStatusModel[] | null = null;

  @Output() onDeletion = new EventEmitter<number>();
  @Output() onModify = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onAddAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveLabel = new EventEmitter<UpdateTaskModel>();
  @Output() onAddLabel = new EventEmitter<UpdateTaskModel>();

  constructor(private taskService: TaskService, public authService: AuthService, public utilsService: UtilsService,
     public taskStatusService: TaskStatusService, private taskAssignmentService: TaskAssignmentService) {
  }

  nextStatus?: Promise<TaskStatusModel>;
  prevStatus?: Promise<TaskStatusModel>;

  blueprintModificateTask?: BlueprintTaskModel;   // task object used as blueprint for modification (primaly app modifies it, then send update request)

  private _hasNews: boolean = false;

  get hasNews() {
    return this._hasNews;
  }

  set hasNews(value: boolean) {

    this._hasNews = value;
  }

  ngOnInit() {

    if(this.task) {

      if(this.task.task_status) {

        if(this.task.task_status.default_next_task_status_id)
          this.nextStatus = this.taskStatusService.getTaskById(this.task.task_status.default_next_task_status_id);

        if(this.task.task_status.default_prev_task_status_id)
          this.prevStatus = this.taskStatusService.getTaskById(this.task.task_status.default_prev_task_status_id);
      }

    }

    this.refreshHasNews();
  }

  private _inModify: boolean = false;

  get inModify() {
    return this._inModify;
  }

  set inModify(value: boolean) {
    this._inModify = value;

    if(this.task && value) {

      this.initBlueprintTask();

    }
  }

  initBlueprintTask() {
    if(!this.task)
      return;

    this.blueprintModificateTask = {
      id: this.task.id,
      name: this.task.name,
      description: this.task.description,
      priority: this.task.priority,
    }
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

  async removeUserFromTask(userId: number): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Removing user with id ${userId} from task: ${this.task.id} - ${this.task.name}`);

    const id = this.task.id;

    this.taskService.removeAssignment(id, userId).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.refreshTask(() => {
            this.onRemoveAssignment.emit({
              target: id,
              new: this.task!
            });
          });

        }
      })
    });


  }

  async addAssignment(user: UserModel): Promise<void> {

    if(!this.task)
      return

    LoggerService.logInfo(`Add user ${user.username} to task: ${this.task.id} - ${this.task.name}`);

    const id = this.task.id;

    this.taskService.addAssignment(id, user.id).then((response) => {
      response.subscribe({
        next: (value: boolean) => {

          // refresh task
          this.refreshTask();

        }
      })
    });


  }

  delete() {

    if(!this.task)
      return;

    LoggerService.logInfo("Remove task " + this.task?.name);

    const id = this.task.id;

    this.taskService.deleteById(id).then((response) => {
      response.subscribe({
        next: (value) => {
          this.onDeletion.emit(id);
        }
      })
    })
  }

  removeLabelFromTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Remove label");

    const id = this.task.id;

    this.taskService.removeLabel(id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {

          // refresh task
          this.refreshTask(() => {
            this.onRemoveLabel.emit({
              target: id,
              new: this.task!
            });
          });

        }
      })
    });
  }

  addLabelToTask(label: TaskLabelModel) {
    if(!this.task)
      return;

    LoggerService.logInfo("Add label");

    const id = this.task.id;

    this.taskService.addLabel(id, label.id).then((response) => {
      response.subscribe({
        next: (value) => {

         this.refreshTask();
        }
      })
    });
  }

  modify(values: Object) {

    if(!this.task)
      return;

    LoggerService.logInfo("Modify task " + this.task?.name);

    const id = this.task.id;

    this.taskService.update(id, values).then((response) => {
      response.subscribe({
        next: (value) => {

          // refresh task
          this.refreshTask(() => {
            this.onModify.emit({
              target: id,
              new: this.task!
            });
          });

        }
      })
    })

  }

  refreshHasNews(): boolean {

    if(!this.authService.loggedUser || !this.task) {
      this.hasNews = false;
      return this.hasNews;
    }

    if(this.userAssignedToTask(this.authService.loggedUser.id)) {
      // logged user is assigned

      const assignment = this.task.assigned_users?.find((au) => {
        return au.user.id == this.authService.loggedUser!.id;
      });

      if(!assignment) {
        this.hasNews = false;
        return this.hasNews;
      }

      if(assignment.last_watched_at == null) {
        this.hasNews = true;
        return this.hasNews;
      }

      this.hasNews = this.task.updated_at > assignment.last_watched_at;
      return this.hasNews;

    } else {
      // logged user is NOT assigned

      if(this.authService.loggedUser.last_visit_at == null) {
        this.hasNews =  true;
        return this.hasNews;
      }

      this.hasNews = this.task.updated_at > this.authService.loggedUser.last_visit_at;
      return this.hasNews;
    }


  }

  updateLastWatched(): void {

    if(!this.authService.loggedUser || !this.task)
      return;

    if(!this.userAssignedToTask(this.authService.loggedUser.id)) {
      // if logged user is not assigned at this task: update last_visit and refresh

      this.hasNews = false;
      this.authService.updateLastVisit();

    } else {
      this.taskAssignmentService.updateByTaskUserId(this.task.id, this.authService.loggedUser.id, {
        last_watched_at: this.utilsService.datetimeNow()
      }).then((response) => {

        response.subscribe({
          next: (value: any) => {

            LoggerService.logInfo("Updated last watched");

            this.refreshTask(() => {
              this.refreshHasNews();
            });

          }
        })

      })
    }

  }

  refreshTask(runAfter: Function = () => {}): void {

    if(!this.task)
      return;

    // refresh task
    this.taskService.find(this.task.id).then((respose) => {
      respose.subscribe({
        next: (t) => {
          this.task = t;

          runAfter();
        }
      })
    })
  }

  changeStatus(taskStatus: TaskStatusModel | null) {

    if(!this.task || !taskStatus)
      return;

    this.modify({
      "task_status_id": taskStatus.id
    });
  }
}
