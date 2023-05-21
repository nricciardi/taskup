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
import { RoleGuardService } from './service/api/auth/role-guard.service';
import { SettingsComponent } from './page/settings/settings.component';
import { ServerErrorComponent } from './page/server-error/server-error.component';

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
    path: "settings",
    component: SettingsComponent
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
    canActivate: [AuthGuardService, RoleGuardService],
    data: { roleRequired: "permission_manage_task_status" }
  },
  {
    path: "manage-task-labels",
    component: ManageTaskLabelsComponent,
    canActivate: [AuthGuardService, RoleGuardService],
    data: { roleRequired: "permission_manage_task_labels" }
  },
  {
    path: "manage-users",
    component: ManageUsersComponent,
    canActivate: [AuthGuardService, RoleGuardService],
    data: { roleRequired: "permission_manage_users" }
  },
  {
    path: "manage-roles",
    component: ManageRolesComponent,
    canActivate: [AuthGuardService, RoleGuardService],
    data: { roleRequired: "permission_manage_roles" }
  },

  {
    path: "server-error",
    component: ServerErrorComponent
  },
  {
    path: "**",
    component: PageNotFoundComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule],
  providers: [AuthGuardService, RoleGuardService]
})
export class AppRoutingModule { }
