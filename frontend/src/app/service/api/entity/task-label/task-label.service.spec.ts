import { TestBed } from '@angular/core/testing';

import { TaskLabelService } from './task-label.service';

describe('TaskLabelService', () => {
  let service: TaskLabelService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TaskLabelService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
