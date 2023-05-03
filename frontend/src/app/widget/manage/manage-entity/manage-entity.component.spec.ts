import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageEntityComponent } from './manage-entity.component';

describe('ManageEntityComponent', () => {
  let component: ManageEntityComponent;
  let fixture: ComponentFixture<ManageEntityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageEntityComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageEntityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
