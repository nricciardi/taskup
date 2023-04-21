import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TextAvatarComponent } from './text-avatar.component';
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('TextAvatarComponent', () => {
  let component: TextAvatarComponent;
  let fixture: ComponentFixture<TextAvatarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TextAvatarComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TextAvatarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
