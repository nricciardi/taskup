import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-show-info-of-commit-modal',
  templateUrl: './show-info-of-commit-modal.component.html',
  styleUrls: ['./show-info-of-commit-modal.component.scss']
})
export class ShowInfoOfCommitModalComponent {
  @Input("target") target?: string;
  @Input("commiterEmail") commiterEmail?: string;
  @Input("branchesOfCommit") branchesOfCommit?: string[];
  @Input("message") message?: string;
  @Input("hash") hash?: string;
  @Input("commiterName") commiterName?: string;

  @Output() onClose = new EventEmitter<void>();


  ngAfterContentInit() {
  }

}
