import { Component, Input } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';

@Component({
  selector: 'app-task-preview',
  templateUrl: './task-preview.component.html',
  styleUrls: ['./task-preview.component.scss']
})
export class TaskPreviewComponent {

  @Input('task') task?: TaskModel;

}
