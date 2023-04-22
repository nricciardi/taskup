import { Component, EventEmitter, Input, Output } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';

@Component({
  selector: 'app-new-assignment-modal',
  templateUrl: './new-assignment-modal.component.html',
  styleUrls: ['./new-assignment-modal.component.scss']
})
export class NewAssignmentModalComponent {
  constructor(private userService: UserService) {}

  @Input("target") target?: string;
  @Input("alreadyAssignedUsers") alreadyAssignedUsers: UserModel[] = [];

  userSelected?: UserModel;

  usersCanBeAssign?: UserModel[];

  @Output() onAddAssignment = new EventEmitter<UserModel>();   // emit assigned user

  ngOnInit() {
    // this.setUsersCanBeAssign();

  }

  selectUser(user: UserModel) {
    this.userSelected = user;
  }

  setUsersCanBeAssign() {

    this.userService.all().then((response) => {

      response.subscribe({
        next: (value: UserModel[]) => {
          this.usersCanBeAssign = value.filter((item: UserModel) => {
            return !this.alreadyAssignedUsers.map(u => u.id).includes(item.id);
          });

        }
      });

    });
  }
}
