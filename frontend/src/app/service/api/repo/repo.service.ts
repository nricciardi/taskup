import { Injectable } from '@angular/core';
import { EelService } from '../../eel/eel.service';
import { Observable } from 'rxjs';
import { RepoNode } from 'src/app/model/entity/repo.model';

@Injectable({
  providedIn: 'root'
})
export class RepoService extends EelService {

  readonly TREE = "repo_tree";

  public getTree(): Promise<Observable<RepoNode | null>> {
    return this.call(this.TREE);
  }
}
