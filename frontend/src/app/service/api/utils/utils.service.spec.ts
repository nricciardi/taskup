import { TestBed } from '@angular/core/testing';

import { BackEndUtilsService } from './utils.service';

describe('UtilsService', () => {
  let service: BackEndUtilsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BackEndUtilsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
