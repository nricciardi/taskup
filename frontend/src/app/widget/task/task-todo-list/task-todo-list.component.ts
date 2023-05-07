import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { NewTodoItemModel, TodoItemModel } from 'src/app/model/entity/todo-item.model';
import { AuthService } from 'src/app/service/api/auth/auth.service';
import { TodoService } from 'src/app/service/api/entity/todo/todo.service';
import { UtilsService } from 'src/app/service/utils/utils.service';

@Component({
  selector: 'app-task-todo-list',
  templateUrl: './task-todo-list.component.html',
  styleUrls: ['./task-todo-list.component.scss']
})
export class TaskTodoListComponent {

  constructor(private todoService: TodoService, private authService: AuthService) {}

  @Input("taskId") taskId?: number;
  @Input("todoCollapseStatus") todoCollapseStatus: boolean = false;

  @Output() onRefresh = new EventEmitter<void>();

  @ViewChild('showTodoBtn') showTodoBtn?: ElementRef;

  todoItems: TodoItemModel[] = [];

  ngOnInit() {
    this.loadTodoItems();
  }

  ngAfterViewInit() {

    // if on init todoCollapseStatus is true => show todo list
    if(this.todoCollapseStatus) {
      this.showTodoBtn?.nativeElement.click();

      this.todoCollapseStatus = true;
    }
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

  newTodo(todo: NewTodoItemModel) {

    if(!this.taskId || !this.authService.loggedUser)
      return;

    this.todoService.create({
      description: todo.description,
      deadline: todo.deadline,
      task_id: this.taskId,
      author_id: this.authService.loggedUser.id

    }).then((response) => {
      response.subscribe({
        next: (value) => {
          this.loadTodoItems();   // refresh todos
        }
      })
    })

  }
}
