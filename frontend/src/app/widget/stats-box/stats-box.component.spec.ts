import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatsBoxComponent } from './stats-box.component';

describe('StatsBoxComponent', () => {
  let component: StatsBoxComponent;
  let fixture: ComponentFixture<StatsBoxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StatsBoxComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StatsBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
