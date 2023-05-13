import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';
import { RoleService } from 'src/app/service/api/entity/role/role.service';

@Component({
  selector: 'app-manage-roles',
  templateUrl: './manage-roles.component.html',
  styleUrls: ['./manage-roles.component.scss']
})
export class ManageRolesComponent {
  constructor(public roleService: RoleService) {}

  fields: FormField[] = [
    {
      name: "name",
      type: "text",
      placeholder: "name",
      blueprintFormControl: new FormControl('', [Validators.required]),
      unique: true
    },
    {
      name: "permission_create",
      type: "checkbox",
      placeholder: "permission_create",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_read_all",
      type: "checkbox",
      placeholder: "permission_read_all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move_backward",
      type: "checkbox",
      placeholder: "permission_move_backward",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move_forward",
      type: "checkbox",
      placeholder: "permission_move_forward",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move",
      type: "checkbox",
      placeholder: "permission_move",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_edit_own",
      type: "checkbox",
      placeholder: "permission_edit_own",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_edit_all",
      type: "checkbox",
      placeholder: "permission_edit_all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_change_role",
      type: "checkbox",
      placeholder: "permission_change_role",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_change_assignment",
      type: "checkbox",
      placeholder: "permission_change_assignment",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_delete_own",
      type: "checkbox",
      placeholder: "permission_delete_own",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_delete_all",
      type: "checkbox",
      placeholder: "permission_delete_all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_manage_task_status",
      type: "checkbox",
      placeholder: "permission_manage_task_status",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_manage_task_labels",
      type: "checkbox",
      placeholder: "permission_manage_task_labels",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_manage_users",
      type: "checkbox",
      placeholder: "permission_manage_users",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_edit_task_deadline",
      type: "checkbox",
      placeholder: "permission_edit_task_deadline",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_manage_roles",
      type: "checkbox",
      placeholder: "permission_manage_roles",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_remove_work",
      type: "checkbox",
      placeholder: "permission_remove_work",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
  ]
}
