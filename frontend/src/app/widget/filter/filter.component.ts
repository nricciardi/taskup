import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { LoggerService } from 'src/app/service/logger/logger.service';

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent<E> {

  @Input("filterFields") filterFields?: string[];
  @Input("title") title?: string;
  @Input("entities") entities: E[] = [];

  @Output() entitiesChange = new EventEmitter<E[]>();
  @Output() onFilter = new EventEmitter<void>();
  @Output() onReset = new EventEmitter<void>();



  private entitiesBackup?: E[];

  filterForm?: FormGroup;

  private _filterMode: boolean = false;    // false = AND, true = OR

  get filterMode() {
    return this._filterMode;
  }

  set filterMode(value) {
    this._filterMode = value;

    this.onFilter.emit();
  }

  ngOnInit() {
    // create dynamically filter form
    if(this.filterFields) {

      this.filterForm = new FormGroup({});

      for (let index = 0; index < this.filterFields.length; index++) {
        const filterField = this.filterFields[index];

        this.filterForm.addControl(filterField, new FormControl(''));

      }

    }

    this.entitiesBackup = this.entities;

  }

  filter(): void {
    if(!this.entitiesBackup || !this.filterFields)
      return;

    this.entities = this.entitiesBackup;    // reset entities

    // or filter function
    const OR = (entity: E) => {

      for (let index = 0; index < this.filterFields!.length; index++) {
        const filterField = this.filterFields![index];

        const filteredValue = String((this.filterForm?.controls as any)[filterField].value).toLowerCase();
        const associatedEntityValue = String((entity as any)[filterField]).toLowerCase();

        console.log(filterField, associatedEntityValue, filteredValue, filteredValue !== "" && associatedEntityValue.includes(filteredValue));


        if(filteredValue !== "" && associatedEntityValue.includes(filteredValue))
          return true;
      }

      return false;

    }

    // or filter function
    const AND = (entity: E) => {

      for (let index = 0; index < this.filterFields!.length; index++) {
        const filterField = this.filterFields![index];

        const filteredValue = String((this.filterForm?.controls as any)[filterField].value).toLowerCase();
        const associatedEntityValue = String((entity as any)[filterField]).toLowerCase();

        if(filteredValue == "" )
          continue;

        if(!associatedEntityValue.includes(filteredValue))
          return false;
      }

      return true;

    }

    // filter entities
    if(this.filterMode)
      this.entities = this.entities.filter(OR);
    else
      this.entities = this.entities.filter(AND);

    LoggerService.logInfo("Filtered");

    this.onFilter.emit();
    this.entitiesChange.emit(this.entities);

  }

  reset() {
    this.entities = this.entitiesBackup ?? [];
    this.onReset.emit();
    this.entitiesChange.emit(this.entities);
  }
}
