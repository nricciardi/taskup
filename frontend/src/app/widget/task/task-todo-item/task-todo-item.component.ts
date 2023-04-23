import { Component, Input } from '@angular/core';
import { TodoItemModel } from 'src/app/model/entity/todo-item.model';

@Component({
  selector: 'app-task-todo-item',
  templateUrl: './task-todo-item.component.html',
  styleUrls: ['./task-todo-item.component.scss']
})
export class TaskTodoItemComponent {

  @Input("item") item?: TodoItemModel;
}
