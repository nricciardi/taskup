import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTaskLabelsComponent } from './manage-task-labels.component';

describe('ManageTaskLabelsComponent', () => {
  let component: ManageTaskLabelsComponent;
  let fixture: ComponentFixture<ManageTaskLabelsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageTaskLabelsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageTaskLabelsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
