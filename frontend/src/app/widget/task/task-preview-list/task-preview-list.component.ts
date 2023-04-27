import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UpdateTaskModel } from 'src/app/model/entity/update-task.model';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';

@Component({
  selector: 'app-task-preview-list',
  templateUrl: './task-preview-list.component.html',
  styleUrls: ['./task-preview-list.component.scss']
})
export class TaskPreviewListComponent {

  @Input("tasks") tasks: TaskModel[] | null = null;
  @Input("loggedUser") loggedUser?: UserModel;

  @Output() onDeletion = new EventEmitter<number>();
  @Output() onModify = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onAddAssignment = new EventEmitter<UpdateTaskModel>();
  @Output() onRemoveLabel = new EventEmitter<UpdateTaskModel>();
  @Output() onAddLabel = new EventEmitter<UpdateTaskModel>();

  constructor(private authService: AuthService) {
    this.authService.refreshMe();   // so after i can use .loggedUser
  }

  scrollTop() {
    window.scroll(0, 0);
  }

}
