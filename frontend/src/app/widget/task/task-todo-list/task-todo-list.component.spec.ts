import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskTodoListComponent } from './task-todo-list.component';

describe('TaskTodoListComponent', () => {
  let component: TaskTodoListComponent;
  let fixture: ComponentFixture<TaskTodoListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TaskTodoListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskTodoListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
