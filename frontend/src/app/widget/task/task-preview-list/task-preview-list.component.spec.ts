import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskPreviewListComponent } from './task-preview-list.component';

describe('TaskPreviewListComponent', () => {
  let component: TaskPreviewListComponent;
  let fixture: ComponentFixture<TaskPreviewListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TaskPreviewListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskPreviewListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
