import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTaskLabelModalComponent } from './manage-task-label-modal.component';

describe('ManageTaskLabelModalComponent', () => {
  let component: ManageTaskLabelModalComponent;
  let fixture: ComponentFixture<ManageTaskLabelModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageTaskLabelModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageTaskLabelModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
