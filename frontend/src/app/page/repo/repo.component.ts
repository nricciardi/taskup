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
    // this.loadTree();

    this.test();
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

  test() {

    this.repoService.getCommits().then((response) => {

      response.subscribe({
        next: (commits) => {

          console.log(commits);

          if(commits?.length == 0)
            return;

          let graphContainer = document.getElementById("graph-container");

          if(!graphContainer) {
            LoggerService.logError("graph container not found");
            return;
          }


          this.gitgraph = createGitgraph(graphContainer);

          const MASTER = this.gitgraph.branch("master");


          MASTER.commit({
            hash: "1",
            subject: "C1"
          })

          MASTER.commit({
            hash: "2",
            subject: "C2"
          });

          const B2 = MASTER.branch("B2");

          B2.commit({
            hash: "3",
            subject: "C3"
          })

          const B3 = MASTER.branch("B3");

          B3.commit({
            hash: "4",
            subject: "C4",
            parentCommit: "1"
          })

          /*B3.commit({
            hash: "1",
            subject: "C1"
          })*/

          return;
          let branches: any = {};
          commits?.forEach((commit: RepoNode) => {

            let parentsToAdd = [];

            for (let index = 0; commit.parents && index < commit.parents.length; index++) {
              const parent = commit.parents[index]

              for (let j = 0; j < this.gitgraph._graph.commits.length; j++) {
                const c = this.gitgraph._graph.commits[j];

                if(parent.hexsha == c.hash)
                  parentsToAdd.push(c);

              }

            }



            const nodeCommit = {
              hash: commit.hexsha,
              subject: commit.message,
              author: `${commit.author.name} <${commit.author.email}>`,
              parent: parentsToAdd[0]
            };

            let branch;
            if(commit.of_branch in Object.keys(branches)) {

              branch = branches[commit.of_branch];

            } else {

              branch = this.gitgraph.branch(commit.of_branch);
              branches[commit.of_branch] = branch;

            }

            branch.commit(nodeCommit);

          })

          console.log(this.gitgraph);



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
