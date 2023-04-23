import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { UserModel } from 'src/app/model/entity/user.model';

@Component({
  selector: 'app-manage-assigned-user-modal',
  templateUrl: './manage-assigned-user-modal.component.html',
  styleUrls: ['./manage-assigned-user-modal.component.scss']
})
export class ManageAssignedUserModalComponent {
  @Input("user") user?: UserModel;
  @Input("target") target?: string;
  @Input("assignmentDate") assignmentDate?: Date;

  @Output() onRemoveFromTask = new EventEmitter<void>();

  ngOnDestroy() {

  }
}
