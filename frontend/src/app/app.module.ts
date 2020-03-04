import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule }   from '@angular/forms';


import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';
import { UploadCerfaComponent } from './upload-cerfa/upload-cerfa.component';
import { ViewCerfaComponent } from './view-cerfa/view-cerfa.component';
import { ToastComponent } from './toast/toast.component'

import { Routes, RouterModule} from '@angular/router';

import { ConnectService } from './connect.service'

import { HttpClientModule } from '@angular/common/http';


import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { D3GraphComponent } from './d3-graph/d3-graph.component';
import { WaitingComponent } from './waiting/waiting.component';

const appRoutes: Routes = [
  { path: '', component: MenuComponent},
  { path: 'upload-cerfa', component: UploadCerfaComponent},
  { path: 'view-cerfa', component: ViewCerfaComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    UploadCerfaComponent,
    ViewCerfaComponent,
    ToastComponent,
    D3GraphComponent,
    WaitingComponent
  ],
  imports: [
    BrowserModule, 
    RouterModule.forRoot(appRoutes), 
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule
  ],
  providers: [ConnectService],
  bootstrap: [AppComponent]
})


export class AppModule { 





}
