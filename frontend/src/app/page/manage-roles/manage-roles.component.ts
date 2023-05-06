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
      placeholder: "Create",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_read_all",
      type: "checkbox",
      placeholder: "Read all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move_backward",
      type: "checkbox",
      placeholder: "Move backward",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move_forward",
      type: "checkbox",
      placeholder: "Move forward",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_move",
      type: "checkbox",
      placeholder: "Move",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_edit_own",
      type: "checkbox",
      placeholder: "Edit own",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_edit_all",
      type: "checkbox",
      placeholder: "Edit all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_change_role",
      type: "checkbox",
      placeholder: "Change role",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_change_assignment",
      type: "checkbox",
      placeholder: "Change assigment",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_delete_own",
      type: "checkbox",
      placeholder: "Edit own",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "permission_delete_all",
      type: "checkbox",
      placeholder: "Edit all",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
  ]
}
