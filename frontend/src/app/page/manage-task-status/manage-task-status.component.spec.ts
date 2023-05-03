import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTaskStatusComponent } from './manage-task-status.component';

describe('ManageTaskStatusComponent', () => {
  let component: ManageTaskStatusComponent;
  let fixture: ComponentFixture<ManageTaskStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageTaskStatusComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageTaskStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
