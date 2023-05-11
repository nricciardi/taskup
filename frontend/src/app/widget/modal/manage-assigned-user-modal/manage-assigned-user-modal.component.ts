import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { RoleModel } from 'src/app/model/entity/role.model';
import { UserModel } from 'src/app/model/entity/user.model';
import { RoleService } from 'src/app/service/api/entity/role/role.service';

@Component({
  selector: 'app-manage-assigned-user-modal',
  templateUrl: './manage-assigned-user-modal.component.html',
  styleUrls: ['./manage-assigned-user-modal.component.scss']
})
export class ManageAssignedUserModalComponent {
  @Input("user") user?: UserModel;
  @Input("target") target?: string;
  @Input("assignmentDate") assignmentDate?: Date;
  @Input("editable") editable: boolean = false;

  @Output() onRemoveFromTask = new EventEmitter<void>();

  role?: RoleModel;

  constructor(private roleService: RoleService) {}

  ngOnInit() {

    const userId = this.user?.role_id;
    if(userId) {
      this.roleService.find(userId).then((response) => {

        response.subscribe({
          next: (role) => {
            this.role = role;
          }
        })

      })
    }

    }

}
