import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowInfoOfCommitModalComponent } from './show-info-of-commit-modal.component';

describe('ShowInfoOfCommitModalComponent', () => {
  let component: ShowInfoOfCommitModalComponent;
  let fixture: ComponentFixture<ShowInfoOfCommitModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowInfoOfCommitModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShowInfoOfCommitModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
