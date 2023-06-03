import { Component, ElementRef, ViewChild } from '@angular/core';
import { RepoNode } from 'src/app/model/entity/repo.model';
import { RepoService } from 'src/app/service/api/repo/repo.service';
import { Branch, createGitgraph } from "@gitgraph/js";
import { LoggerService } from 'src/app/service/logger/logger.service';
import { AuthService } from 'src/app/service/api/auth/auth.service';

@Component({
  selector: 'app-repo',
  templateUrl: './repo.component.html',
  styleUrls: ['./repo.component.scss']
})
export class RepoComponent {

  @ViewChild("showCommitInfoBtn") showCommitInfoBtn?: ElementRef;

  validRepo?: boolean;
  branches: any = {};     // object key-value: key is branch name, value is ref of branch
  gitgraph: any;
  generationError: boolean = false;

  nodeSelected?: RepoNode;

  constructor(private repoService: RepoService, private authService: AuthService) {
    authService.refreshMe();
  }

  ngOnInit() {

    this.loadGraph();
  }

  loadGraph() {

    this.repoService.getCommits().then((response) => {

      this.validRepo = undefined;
      this.gitgraph = undefined;
      this.branches = {};

      response.subscribe({
        next: (nodes) => {

          if(!!nodes) {
            setTimeout(() => {
              this.loadGitGraph();
              this.generateGraphFromCommits(nodes);
            }, 250);

            this.validRepo = true;

          } else {
            this.validRepo = false;
          }


        }
      })

    })

  }

  generateGraphFromCommits(nodes: RepoNode[]) {

    this.generationError = false;

    try {

      const showInfoOfCommit = (commit: any) => {


        if(this.showCommitInfoBtn && !!this.authService.loggedUser) {

          try {
            this.nodeSelected = nodes.find((node) => {
              return node.hexsha == commit.hash;
            });

            // show modal
            this.showCommitInfoBtn.nativeElement.click();
          } catch (error) {
            LoggerService.logError("error during showCommitInfo");
          }
        }

      }

      for (let index = 0; index < nodes.length; index++) {
        const node: RepoNode = nodes[index];

        // if there is NOT branch => create it
        if(!(node.of_branch in this.branches))  {
          let branch_ref = this.gitgraph.branch(node.of_branch)

          this.branches[node.of_branch] = branch_ref;
        }

        if(node.parents) {

          // ============ MERGE ==================
          if(node.parents.length > 1) {

            const currentBranch = node.of_branch;

            node.parents.forEach((parent: RepoNode) => {    // for each parent with different branch, using it to merge

              if(parent.of_branch != currentBranch) {

                const parentBranch = this.branches[parent.of_branch];

                this.branches[currentBranch].merge({
                  commitOptions: {
                    hash: node.hexsha,
                    subject: node.message,
                    author: `${node.author.name} <${node.author.email}>`,
                    onMessageClick(commit: any) {
                      showInfoOfCommit(commit);
                    },
                    onClick(commit: any) {
                      showInfoOfCommit(commit);

                    }
                  },
                  branch: parentBranch
                });

              }
            })


          // ============ NORMAL COMMIT ===========
          } else {

            // add commit to branch
            this.branches[node.of_branch].commit({
              hash: node.hexsha,
              subject: node.message,
              author: `${node.author.name} <${node.author.email}>`,
              onMessageClick(commit: any) {
                showInfoOfCommit(commit);
              },
              onClick(commit: any) {
                showInfoOfCommit(commit);

              }
            });

            // add tag to commit
            if(!!node.tag)
              this.branches[node.of_branch].tag(node.tag);

          }
        }

        if(node.children) {

          // branching
          node.children.forEach((child: RepoNode) => {

            if(child.of_branch != node.of_branch) {
              const newBranch = this.branches[node.of_branch].branch(child.of_branch);

              // add branch in branches
              this.branches[child.of_branch] = newBranch;
            }

          });
        }


      }
    } catch (error) {
      this.generationError = true;
      console.log(error);

    }

  }

  loadGitGraph() {

    let graphContainer = document.getElementById("graph-container");

    if(!graphContainer) {
      LoggerService.logError("graph container not found");
      return;
    }


    this.gitgraph = createGitgraph(graphContainer);

  }

}
