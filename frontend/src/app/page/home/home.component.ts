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

  async ngOnInit() {

    console.log(await this.taskService.all());
  }

}
