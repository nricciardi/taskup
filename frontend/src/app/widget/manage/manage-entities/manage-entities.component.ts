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

  entities?: E[];
  entitiesFiltered: E[] = [];

  constructor(public utilsService: UtilsService) {}

  ngOnInit() {

    this.loadEntities();

  }

  loadEntities() {
    this.manager?.all().then((response) => {

      response.subscribe({
        next: (values: E[]) => {
          if(!!values) {
            this.entities = values;
            this.entitiesFiltered = [...this.entities];
          }
        }
      })

    });
  }

}
