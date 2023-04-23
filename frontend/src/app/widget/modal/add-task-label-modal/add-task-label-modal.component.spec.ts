import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddTaskLabelModalComponent } from './add-task-label-modal.component';

describe('AddTaskLabelModalComponent', () => {
  let component: AddTaskLabelModalComponent;
  let fixture: ComponentFixture<AddTaskLabelModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddTaskLabelModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddTaskLabelModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
