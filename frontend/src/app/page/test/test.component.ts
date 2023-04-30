import { Component } from '@angular/core';
import { TaskStatusService } from 'src/app/service/api/entity/task-status/task-status.service';
import { TaskService } from 'src/app/service/api/entity/task/task.service';
import { UserService } from 'src/app/service/api/entity/user/user.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent {

  constructor(public taskStatusService: TaskStatusService) {}

  ngOnInit() {

  }


  async test() {
    return this.taskStatusService.getTaskById(1);

    // return r.name;
  }
}
