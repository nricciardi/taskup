import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { ProjectInformation } from 'src/app/model/project-information.model';

@Injectable({
  providedIn: 'root'
})
export class ProjectService extends EelService {

  readonly PROJECT_INFORMATION = "project_project_information";


  public getProjectInformation(): Promise<Observable<ProjectInformation>> {

    return this.call(this.PROJECT_INFORMATION);

  }
}
