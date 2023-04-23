import { Component } from '@angular/core';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {

  constructor(private taskService: TaskService) {}

  ngOnInit() {
    this.allTasks();
  }

  allTasks() {
    this.taskService.all().then((response) => {
      response.subscribe({
        next: (value) => {
          console.log(value);

        }
      })
    })
  }
}
