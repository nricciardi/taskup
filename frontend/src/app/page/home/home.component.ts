import { Component } from '@angular/core';
import { TaskService } from 'src/app/service/api/task/task.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(private taskService: TaskService) {
  }

  ngOnInit() {
    this.taskService.all().then((subscriber) => {

      subscriber.subscribe({
        next: (value) => {
          console.log(value);

        }
      })
    })
  }

}
