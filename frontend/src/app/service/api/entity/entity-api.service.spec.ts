import { TestBed } from '@angular/core/testing';

import { EntityApiService } from './entity-api.service';

describe('EntityApiService', () => {
  let service: EntityApiService<any>;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EntityApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
