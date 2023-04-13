import { Component, Input } from '@angular/core';
import { TaskStatusModel } from 'src/app/model/entity/task-status.model';

@Component({
  selector: 'app-task-status-side-banner',
  templateUrl: './task-status-side-banner.component.html',
  styleUrls: ['./task-status-side-banner.component.scss']
})
export class TaskStatusSideBannerComponent {

  @Input("taskStatus") taskStatus?: TaskStatusModel;

}
