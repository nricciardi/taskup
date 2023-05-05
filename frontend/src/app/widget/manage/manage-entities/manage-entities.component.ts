import { Component, Input } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BaseEntity } from 'src/app/model/entity/base-entity.model';
import { FormField } from 'src/app/model/form-field.model';
import { EntityApiService } from 'src/app/service/api/entity/entity-api.service';
import { LoggerService } from 'src/app/service/logger/logger.service';
import { UtilsService } from 'src/app/service/utils/utils.service';


@Component({
  selector: 'app-manage-entities',
  templateUrl: './manage-entities.component.html',
  styleUrls: ['./manage-entities.component.scss']
})
export class ManageEntitiesComponent<M extends EntityApiService<E>, E extends BaseEntity> {

  @Input("title") title?: string;
  @Input("editableFields") editableFields: FormField[] = [];
  @Input("filterFields") filterFields?: string[];
  @Input("entityTitleField") entityTitleField?: string;
  @Input("manager") manager?: M;
  @Input("additionalFieldOnCreation") additionalFieldOnCreation: FormField[] = [];

  filterForm?: FormGroup;

  private _filterMode: boolean = false;    // false = AND, true = OR

  get filterMode() {
    return this._filterMode;
  }

  set filterMode(value) {
    this._filterMode = value;

    this.filter();
  }

  entities?: E[];
  private entitiesBackup?: E[];

  constructor(public utilsService: UtilsService) {}

  ngOnInit() {


    // create dynamically filter form
    if(this.filterFields) {

      this.filterForm = new FormGroup({});

      for (let index = 0; index < this.filterFields.length; index++) {
        const filterField = this.filterFields[index];

        this.filterForm.addControl(filterField, new FormControl(''));

      }

    }


    this.loadEntities();

  }

  loadEntities() {
    this.manager?.all().then((response) => {

      response.subscribe({
        next: (values: E[]) => {
          if(!!values) {
            this.entities = values;
            this.entitiesBackup = this.entities;
          }
        }
      })

    });
  }

  reset() {
    this.entities = this.entitiesBackup;
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

        console.log(filterField, associatedEntityValue, filteredValue, filteredValue !== "" && associatedEntityValue.includes(filteredValue));

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

  }
}
