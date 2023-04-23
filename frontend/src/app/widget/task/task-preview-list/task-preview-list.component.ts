import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { UserModel } from 'src/app/model/entity/user.model';

@Component({
  selector: 'app-task-preview-list',
  templateUrl: './task-preview-list.component.html',
  styleUrls: ['./task-preview-list.component.scss']
})
export class TaskPreviewListComponent {

  @Input("tasks") tasks: TaskModel[] | null = null;
  @Input("loggedUser") loggedUser?: UserModel;

  @Output() onDeletion = new EventEmitter<number>();

  constructor() {
  }

  scrollTop() {
    window.scroll(0, 0);
  }

}
