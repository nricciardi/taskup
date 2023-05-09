import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { ProjectInformation } from 'src/app/model/project-information.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends EelService {

  readonly PATHS_STORED = "project_get_projects_paths_stored";
  readonly SET_PROJECT_PATH = "project_set_project_path";
  readonly PROJECT_INFORMATION = "project_project_information";


  public projectsPathsStored(): Promise<Observable<string[]>> {

    return this.call(this.PATHS_STORED);

  }

  public setProjectPath(path: string, refresh: boolean = true): Promise<Observable<boolean>> {

    return this.call(this.SET_PROJECT_PATH, path, refresh);

  }

  public getProjectInformation(): Promise<Observable<ProjectInformation>> {

    return this.call(this.PROJECT_INFORMATION);

  }
}
