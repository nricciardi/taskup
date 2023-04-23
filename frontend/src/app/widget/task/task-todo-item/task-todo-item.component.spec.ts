import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskTodoItemComponent } from './task-todo-item.component';

describe('TaskTodoItemComponent', () => {
  let component: TaskTodoItemComponent;
  let fixture: ComponentFixture<TaskTodoItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TaskTodoItemComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskTodoItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
