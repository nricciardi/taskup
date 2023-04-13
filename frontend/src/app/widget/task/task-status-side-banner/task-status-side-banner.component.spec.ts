import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskStatusSideBannerComponent } from './task-status-side-banner.component';

describe('TaskStatusSideBannerComponent', () => {
  let component: TaskStatusSideBannerComponent;
  let fixture: ComponentFixture<TaskStatusSideBannerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TaskStatusSideBannerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskStatusSideBannerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
