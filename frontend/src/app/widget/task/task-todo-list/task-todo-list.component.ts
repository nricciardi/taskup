import { Component, Input } from '@angular/core';
import { TodoItemModel } from 'src/app/model/entity/todo-item.model';
import { TodoService } from 'src/app/service/api/entity/todo/todo.service';

@Component({
  selector: 'app-task-todo-list',
  templateUrl: './task-todo-list.component.html',
  styleUrls: ['./task-todo-list.component.scss']
})
export class TaskTodoListComponent {

  constructor(private todoService: TodoService) {}

  @Input("taskId") taskId?: number;

  todoItems: TodoItemModel[] = [];

  ngOnInit() {
    this.loadTodoItems();
  }

  loadTodoItems(): void {
    if(!this.taskId)
      return;

    this.todoService.allOf(this.taskId).then((response) => {
      response.subscribe({
        next: (value: TodoItemModel[]) => {
          if(value)
            this.todoItems = value;
        }
      })
    })
  }
}
