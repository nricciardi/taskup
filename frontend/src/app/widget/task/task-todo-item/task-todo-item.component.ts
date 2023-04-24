import { Component, Input } from '@angular/core';
import { TodoItemModel } from 'src/app/model/entity/todo-item.model';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-task-todo-item',
  templateUrl: './task-todo-item.component.html',
  styleUrls: ['./task-todo-item.component.scss']
})
export class TaskTodoItemComponent {

  constructor(public utilsService: UtilsService) {}

  @Input("item") item?: TodoItemModel;
}
