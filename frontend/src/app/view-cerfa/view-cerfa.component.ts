import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { ConnectService } from '../connect.service'

@Component({
  selector: 'app-view-cerfa',
  templateUrl: './view-cerfa.component.html',
  styleUrls: ['./view-cerfa.component.scss']
})
export class ViewCerfaComponent implements OnInit {

declarations : any[];

declarationSubscription: Subscription;

d3Visible : boolean = false;

IDgraph: string;

  constructor(private data: ConnectService) {}

  ngOnInit(): void {

		this.declarationSubscription = this.data.fichierCollecteSubject.subscribe((declarations: any[]) => 
		{
			this.declarations = declarations;
		}
		)
		
	this.data.getFichierCollecte();


  }

  showD3(id:string)
  {
    this.IDgraph = id;
    this.d3Visible = true;
  }

  hideD3()
  {
    this.d3Visible = false;
  }

}
