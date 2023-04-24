import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeadlineBadgeComponent } from './deadline-badge.component';

describe('DeadlineBadgeComponent', () => {
  let component: DeadlineBadgeComponent;
  let fixture: ComponentFixture<DeadlineBadgeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeadlineBadgeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DeadlineBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
