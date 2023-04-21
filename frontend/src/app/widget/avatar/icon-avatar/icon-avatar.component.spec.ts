import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IconAvatarComponent } from './icon-avatar.component';

describe('IconAvatarComponent', () => {
  let component: IconAvatarComponent;
  let fixture: ComponentFixture<IconAvatarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IconAvatarComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IconAvatarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
