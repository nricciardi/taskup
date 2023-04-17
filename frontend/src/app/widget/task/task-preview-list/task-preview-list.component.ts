import { Component, Input } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';

@Component({
  selector: 'app-task-preview-list',
  templateUrl: './task-preview-list.component.html',
  styleUrls: ['./task-preview-list.component.scss']
})
export class TaskPreviewListComponent {

  @Input("tasks") tasks: TaskModel[] | null = null;

  constructor() {
  }

  scrollTop() {
    window.scroll(0, 0);
  }

}
