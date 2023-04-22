import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewAssignmentModalComponent } from './new-assignment-modal.component';

describe('NewAssignmentModalComponent', () => {
  let component: NewAssignmentModalComponent;
  let fixture: ComponentFixture<NewAssignmentModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewAssignmentModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewAssignmentModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
