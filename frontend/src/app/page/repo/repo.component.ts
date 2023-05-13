import { Component } from '@angular/core';
import { RepoNode } from 'src/app/model/entity/repo.model';
import { RepoService } from 'src/app/service/api/repo/repo.service';

@Component({
  selector: 'app-repo',
  templateUrl: './repo.component.html',
  styleUrls: ['./repo.component.scss']
})
export class RepoComponent {

  tree: RepoNode | null = null;

  constructor(private repoService: RepoService) {}

  ngOnInit() {
    this.loadTree();
  }

  loadTree() {

    this.repoService.getTree().then((response) => {

      response.subscribe({
        next: (value) => {
          this.tree = value;
        }
      })

    })

  }
}
