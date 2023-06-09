import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageEntitiesComponent } from './manage-entities.component';

describe('ManageEntitiesComponent', () => {
  let component: ManageEntitiesComponent;
  let fixture: ComponentFixture<ManageEntitiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageEntitiesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageEntitiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
