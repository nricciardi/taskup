import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { ProjectInformation } from 'src/app/model/project-information.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends EelService {

  readonly PATHS_STORED = "project_get_projects_paths_stored";
  readonly PROJECT_INFORMATION = "project_project_information";


  public projectsPathsStored(): Promise<Observable<string[]>> {

    return this.call(this.PATHS_STORED);

  }

  public getProjectInformation(): Promise<Observable<ProjectInformation>> {

    return this.call(this.PROJECT_INFORMATION);

  }
}
