import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageDeadlineComponent } from './manage-deadline.component';

describe('ManageDeadlineComponent', () => {
  let component: ManageDeadlineComponent;
  let fixture: ComponentFixture<ManageDeadlineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageDeadlineComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageDeadlineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
