import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './page/page-not-found/page-not-found.component';
import { DashboardComponent } from './page/dashboard/dashboard.component';
import { LoginComponent } from './page/login/login.component';
import { HomeComponent } from './page/home/home.component';
import { TestComponent } from './page/test/test.component';
import { MyProfileComponent } from './page/my-profile/my-profile.component';
import { ManageTaskStatusComponent } from './page/manage-task-status/manage-task-status.component';
import { ManageTaskLabelsComponent } from './page/manage-task-labels/manage-task-labels.component';
import { ManageUsersComponent } from './page/manage-users/manage-users.component';

const routes: Routes = [

  {
    path: "",
    redirectTo: "/home",
    pathMatch: "full"
  },
  {
    path: "home",
    component: HomeComponent
  },
  {
    path: "dashboard",
    component: DashboardComponent
  },
  {
    path: "login",
    component: LoginComponent
  },
  {
    path: "test",
    component: TestComponent
  },
  {
    path: "my-profile",
    component: MyProfileComponent
  },
  {
    path: "manage-task-status",
    component: ManageTaskStatusComponent
  },
  {
    path: "manage-task-labels",
    component: ManageTaskLabelsComponent
  },
  {
    path: "manage-users",
    component: ManageUsersComponent
  },


  {
    path: "**",
    component: PageNotFoundComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
