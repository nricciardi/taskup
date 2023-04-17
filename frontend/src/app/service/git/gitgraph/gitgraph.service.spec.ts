import { TestBed } from '@angular/core/testing';

import { GitgraphService } from './gitgraph.service';

describe('GitgraphService', () => {
  let service: GitgraphService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GitgraphService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
