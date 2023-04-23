import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TaskLabelModel } from 'src/app/model/entity/task-label.model';

@Component({
  selector: 'app-manage-task-label-modal',
  templateUrl: './manage-task-label-modal.component.html',
  styleUrls: ['./manage-task-label-modal.component.scss']
})
export class ManageTaskLabelModalComponent {

  @Input("target") target?: string;
  @Input("label") label?: TaskLabelModel;

  @Output() onRemoveFromTask = new EventEmitter<void>();
}
