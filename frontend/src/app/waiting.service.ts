import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class WaitingService {
	message: string;
	active: boolean = false;

	show(message)
	{
		this.message = message;
		this.active = true;
		this.emitWaitingSubject();
		
	}

	hide()
	{
		this.active = false;
		this.emitWaitingSubject();
	}

	waitingSubject = new Subject<any[]>();

   emitWaitingSubject() {
   	this.waitingSubject.next([{message:this.message, active:this.active}]);
   }




  constructor() { }
}
