import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-task-status-side-banner',
  templateUrl: './task-status-side-banner.component.html',
  styleUrls: ['./task-status-side-banner.component.scss']
})
export class TaskStatusSideBannerComponent {

  @Input("title") title?: string;

}
