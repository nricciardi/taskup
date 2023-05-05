import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { FormField, SelectOption } from 'src/app/model/form-field.model';
import { RoleService } from 'src/app/service/api/entity/role/role.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';

@Component({
  selector: 'app-manage-users',
  templateUrl: './manage-users.component.html',
  styleUrls: ['./manage-users.component.scss']
})
export class ManageUsersComponent {
  constructor(public userService: UserService, private roleSerivice: RoleService) {}

  fields: FormField[] = [
    {
      name: "username",
      type: "text",
      placeholder: "Username",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "name",
      type: "text",
      placeholder: "Name",
      blueprintFormControl: new FormControl<string | null>(null)
    },
    {
      name: "surname",
      type: "text",
      placeholder: "Surname",
      blueprintFormControl: new FormControl<string | null>(null)
    },
    {
      name: "avatar_hex_color",
      type: "color",
      placeholder: "Color",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "email",
      type: "email",
      placeholder: "Email",
      blueprintFormControl: new FormControl('', [Validators.required])
    },
    {
      name: "phone",
      type: "text",
      placeholder: "Phone",
      blueprintFormControl: new FormControl('')
    },
  ]

  ngOnInit() {
    this.appendRoleOptions();   // append role options on list of fields
  }

  appendRoleOptions() {

    this.roleSerivice.all().then((response) => {

      response.subscribe({
        next: (values) => {

          if(!!values) {

            this.fields.push(
              {
                title: "role",
                name: "role_id",
                type: "selectbox",
                placeholder: "role",
                blueprintFormControl: new FormControl('', [Validators.required]),
                selectOptions: values.map((role) => {
                  return {
                    value: role.id,
                    text: role.name
                  }
                })
              });
          }

        }
      })

    })

  }

}
