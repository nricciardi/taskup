import { TestBed } from '@angular/core/testing';

import { EelService } from './eel.service';

describe('EelService', () => {
  let service: EelService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EelService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
