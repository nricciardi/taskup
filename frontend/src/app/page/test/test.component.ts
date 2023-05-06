import { Component } from '@angular/core';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { TaskStatusService } from 'src/app/service/api/entity/task-status/task-status.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {


  constructor(public taskStatusService: TaskStatusService, private authService: AuthService) {}

  ngOnInit() {

  }


  async test() {
    this.authService.isLogged().then((response) => {

      response.subscribe({
        next: (value) => {
          console.log("value: ", value);

        }
      })

    })
  }
}
