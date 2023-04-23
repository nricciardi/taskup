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

  noUsers: boolean = false;

  usersCanBeAssign?: UserModel[];

  @Output() onAddAssignment = new EventEmitter<UserModel>();   // emit assigned user
  @Output() onClose = new EventEmitter<void>();

  ngOnInit() {
    // this.setUsersCanBeAssign();

  }

  ngOnDestroy() {
    this.onClose.emit();
  }

  selectUser(user: UserModel) {
    this.userSelected = user;
  }

  setUsersCanBeAssign() {

    this.noUsers = false;

    this.userService.all().then((response) => {

      response.subscribe({
        next: (value: UserModel[]) => {
          this.usersCanBeAssign = value.filter((item: UserModel) => {
            return !this.alreadyAssignedUsers.map(u => u.id).includes(item.id);
          });

          if(!this.usersCanBeAssign || this.usersCanBeAssign.length == 0)
            this.noUsers = true;

        }
      });

    });
  }
}
