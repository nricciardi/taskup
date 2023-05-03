import { Component, Input } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { FormField } from 'src/app/model/form-field.model';
import { EntityApiService } from 'src/app/service/api/entity/entity-api.service';
import { LoggerService } from 'src/app/service/logger/logger.service';

@Component({
  selector: 'app-manage-entities',
  templateUrl: './manage-entities.component.html',
  styleUrls: ['./manage-entities.component.scss']
})
export class ManageEntitiesComponent<T> {

  @Input("entities") entities?: T[];
  @Input("title") title?: string;
  @Input("editableFields") editableFields: FormField[] = [];
  @Input("filterFields") filterFields?: string[];
  @Input("entityTitleField") entityTitleField?: string;

  filterForm?: FormGroup;

  entitiesManagable: T[] = [];

  ngOnInit() {


    // create dynamically filter form
    if(this.filterFields) {

      this.filterForm = new FormGroup({});

      for (let index = 0; index < this.filterFields.length; index++) {
        const filterField = this.filterFields[index];

        this.filterForm.addControl(filterField, new FormControl(''));

      }

    }

    // add all entities passed as input in entitiesManagable
    this.entitiesManagable = this.entities ?? [];

  }

  filter(): void {
    if(!this.entities || !this.filterFields)
      return;

    this.entitiesManagable = this.entities.filter((entity) => {

      return true;

      for (let index = 0; index < this.filterFields!.length; index++) {
        const filterField = this.filterFields![index];

        if((entity as any)[filterField] == (this.filterForm?.controls as any)[filterField].value)
          return true;
      }

      return false;

    });

    LoggerService.logInfo("Filtered");
    console.log(this.entitiesManagable);

  }
}
