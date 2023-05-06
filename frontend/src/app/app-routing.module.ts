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
import { ManageRolesComponent } from './page/manage-roles/manage-roles.component';
import { AuthGuardService } from './service/api/auth/auth-guard.service';

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
    component: DashboardComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "login",
    component: LoginComponent
  },
  {
    path: "test",
    component: TestComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "my-profile",
    component: MyProfileComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "manage-task-status",
    component: ManageTaskStatusComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "manage-task-labels",
    component: ManageTaskLabelsComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "manage-users",
    component: ManageUsersComponent,
    canActivate: [AuthGuardService]
  },
  {
    path: "manage-roles",
    component: ManageRolesComponent,
    canActivate: [AuthGuardService]
  },

  {
    path: "**",
    component: PageNotFoundComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuardService]
})
export class AppRoutingModule { }
