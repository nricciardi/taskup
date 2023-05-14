import { Component, ElementRef, ViewChild } from '@angular/core';
import { RepoNode } from 'src/app/model/entity/repo.model';
import { RepoService } from 'src/app/service/api/repo/repo.service';
import { Branch, createGitgraph } from "@gitgraph/js";
import { LoggerService } from 'src/app/service/logger/logger.service';

@Component({
  selector: 'app-repo',
  templateUrl: './repo.component.html',
  styleUrls: ['./repo.component.scss']
})
export class RepoComponent {

  root: RepoNode | null = null;
  branches: any = {};     // object key-value: key is branch name, value is ref of branch
  gitgraph: any;

  constructor(private repoService: RepoService) {}

  ngOnInit() {
    this.loadTree();
  }

  loadTree() {

    this.repoService.getTree().then((response) => {

      response.subscribe({
        next: (value) => {
          this.root = value;

          if(!!this.root)
            setTimeout(() => this.createGraph(this.root!), 1000);
        }
      })

    })

  }

  generateTree(node: RepoNode) {

    // if there is NOT branch => create it
    if(!(node.of_branch in this.branches))  {
      let branch_ref = this.gitgraph.branch(node.of_branch)

      this.branches[node.of_branch] = branch_ref;
    }


    if(node.children && node.children.length == 2) {

      if(node.parents) {

        let same_branch_parent: any;
        let other_branch_parent: any;

        for (let index = 0; index < node.parents.length; index++) {
          const parent = node.parents[index];

          if(parent.of_branch == node.of_branch) {
            same_branch_parent = parent
          } else {
            other_branch_parent = parent;
          }

        }

        const same_branch = this.branches[same_branch_parent.of_branch];
        const other_branch = this.branches[other_branch_parent.of_branch];


        same_branch.merge(other_branch, node.message);
      }

    } else {
      let branch = this.branches[node.of_branch];

      branch.commit({
        subject: `${node.message}`,
        author: `${node.author.name} <${node.author.email}>`,
        hashAbbrev: node.hexsha
      });

    }

    let children = node.children ?? [];

    for (let index = 0; index < children.length; index++) {
      const child = children[index];

      this.generateTree(child);
    }

  }

  createGraph(node: RepoNode) {

    let graphContainer = document.getElementById("graph-container");

    if(!graphContainer) {
      LoggerService.logError("graph container not found");
      return;
    }


    this.gitgraph = createGitgraph(graphContainer);

    this.generateTree(node);

  }
}
