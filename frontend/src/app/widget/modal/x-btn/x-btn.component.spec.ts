import { ComponentFixture, TestBed } from '@angular/core/testing';

import { XBtnComponent } from './x-btn.component';

describe('XBtnComponent', () => {
  let component: XBtnComponent;
  let fixture: ComponentFixture<XBtnComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ XBtnComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(XBtnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
