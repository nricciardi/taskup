import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageAssignedUserModalComponent } from './manage-assigned-user-modal.component';

describe('ManageAssignedUserModalComponent', () => {
  let component: ManageAssignedUserModalComponent;
  let fixture: ComponentFixture<ManageAssignedUserModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageAssignedUserModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageAssignedUserModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
