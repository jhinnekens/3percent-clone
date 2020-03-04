import { Input, Component, OnInit, Output, EventEmitter } from '@angular/core';
import {trigger, sequence,state, transition, style, animate} from '@angular/animations';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss'],
})
export class ToastComponent implements OnInit {

  @Output()
  onClose: EventEmitter<boolean> = new EventEmitter();

  @Input() message : string;
  @Input() type : string;
  
show: boolean = true;
  
  ngOnInit() {

  	var that = this;
  	 setTimeout(function(){
  		that.onClose.emit();
  	}, 2000);
  }

}
