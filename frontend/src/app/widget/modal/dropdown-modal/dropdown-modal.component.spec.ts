import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DropdownModalComponent } from './dropdown-modal.component';

describe('DropdownModalComponent', () => {
  let component: DropdownModalComponent;
  let fixture: ComponentFixture<DropdownModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DropdownModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DropdownModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
