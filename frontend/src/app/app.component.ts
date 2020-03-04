import { Component } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';

import { map, filter, scan, mergeMap } from 'rxjs/operators';
import { PopupService } from './popup.service'
import { WaitingService } from './waiting.service'
import { Subscription} from 'rxjs'

import {trigger, sequence,state, transition, style, animate} from '@angular/animations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations:[
    trigger('FadeOut',[
    state('out', style({opacity: 1})),
      transition(':leave', [
      style({opacity: 1 }),
        animate('2s ease', style({
          opacity: 0
        }))
    
  
    ])
  ])]
})
export class AppComponent  {
  	pageTitle;
  	toastSuscription: Subscription;

  	toastActive: boolean = false;

  	toastType: string;
	  toastMessage: string;
	  

	waitingSuscription: Subscription;

  	waitingActive: boolean = false;

  	waitingType: string;
  	waitingMessage: string;

  		constructor(private router: Router,
    				private activatedRoute: ActivatedRoute,
					private toast : PopupService,
					private waiting : WaitingService
    				) {}


		ngOnInit() 
		{
			this.router.events
			  .pipe(filter<NavigationEnd>((event) => event instanceof NavigationEnd))
			
			  .subscribe((event) => {
			    if (event.url == '/')
			     this.pageTitle = "Menu";

			    else if (event.url == '/upload-cerfa')
			     this.pageTitle = "Nouvelle déclaration";

			    else if (event.url == '/view-cerfa')
			     this.pageTitle = "Mes déclarations";

			    else
			     this.pageTitle = "Erreur 404";

			  }); 


			   this.toastSuscription = this.toast.popupSubject.subscribe(
			      (popup: any[]) => {
			        this.toastActive = popup[0].active;
			        this.toastType = popup[0].type;
			        this.toastMessage = popup[0].message;
			      }
				)
				
				this.waitingSuscription = this.waiting.waitingSubject.subscribe(
					(waiting: any[]) => {
					  this.waitingActive = waiting[0].active;
					  this.waitingMessage = waiting[0].message;
					}
				  )

		}

		hideToast()
		{
			this.toastActive = false;
		}

		hideWaiting()
		{
			this.waitingActive = false;
		}

}



