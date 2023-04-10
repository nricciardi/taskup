import { Component } from '@angular/core';
import { TaskModel } from 'src/app/model/entity/task.model';
import { TaskService } from 'src/app/service/api/entity/task/task.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  public tasks?: TaskModel[];

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {

    this.taskService.all().then((response) => {
      response.subscribe({
        next: (value) => {
          this.tasks = value;

        }
      })
    })

  }
}
