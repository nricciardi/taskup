import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends EelService {

  readonly PATHS_STORED = "project_projects_paths_stored";
  readonly SET_PROJECT_PATH = "project_set_project_path";


  public projectsPathsStored(): Promise<Observable<string[]>> {

    return this.call(this.PATHS_STORED);

  }

  public setProjectPath(path: string, refresh: boolean = true): Promise<Observable<boolean>> {

    return this.call(this.SET_PROJECT_PATH, path, refresh);

  }
}
