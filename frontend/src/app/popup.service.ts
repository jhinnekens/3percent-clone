import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class PopupService {
	type: string;
	message: string;
	active: boolean = false;

	show(type, message)
	{
		this.type = type;
		this.message = message;
		this.active = true;
		this.emitPopupSubject();
	}

	hide()
	{
		this.active = false;
	}

	popupSubject = new Subject<any[]>();

   emitPopupSubject() {
   	this.popupSubject.next([{type:this.type, message:this.message, active:this.active}]);
   }


  constructor() { }
}
