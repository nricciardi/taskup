import { Component } from '@angular/core';
import { TaskService } from 'src/app/service/api/task/task.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {

    this.taskService.all().then((response) => {
      response.subscribe({
        next: (value) => {
          console.log(value);

        }
      })
    })

  }
}
