import { Component, OnInit, HostListener } from '@angular/core';
import { NgForm } from '@angular/forms';
import { PopupService } from '../popup.service'
import { ConnectService } from '../connect.service'
import { WaitingService } from '../waiting.service'
import { Subscription } from 'rxjs';
import  {Router} from '@angular/router';

@Component({
  selector: 'app-upload-cerfa',
  templateUrl: './upload-cerfa.component.html',
  styleUrls: ['./upload-cerfa.component.scss']
})
export class UploadCerfaComponent implements OnInit {

    @HostListener('document:click', ['$event'])
    documentClick(event: MouseEvent) {

      if((<Element>event.target).classList[0] != "associeProposition")
        this.focusAssocieOnOff("off")

    }
emailValid : boolean = false;
associeValid: boolean = false;
groupeValid: boolean = false;
fileChoosed: boolean = false;

postCollecteSubscription: Subscription;

postCollecteData;

fileName: string = "";
fileBody;

associeChoosed : string ="";
emailChoosed : string ="";

selectedFile: File = null;
fd = new FormData();


associes: any[];

focusAssocie: boolean = false;


  constructor(
    private toast: PopupService,
    private data: ConnectService,
    private waiting: WaitingService,
    private router: Router
  ) { }

  ngOnInit(): void {
      this.associes = 
      [
          {name:"Sandra Aron", email:"sandra.aron@pwcavocats.com"},
          {name:"Bruno Lunghi", email:"bruno.lunghi@pwcavocats.com"}
      ]
  }

chooseAssocieInList(name, email)
{
   this.associeChoosed = name;
   this.emailChoosed = email;
   
   this.emailValid = true;
   this.associeValid = true;

   this.focusAssocieOnOff("off");
  }

  onSubmit(form: NgForm) {

    this.waiting.show("Chargement du fichier de collecte en cours");

    this.postCollecteSubscription = this.data.postCollecteSubject.subscribe((postCollecteData: any[]) => 
		{
      console.log("uploadDone");
     // this.postCollecteData = postCollecteData;
     this.waiting.hide();
     this.router.navigateByUrl("/view-cerfa")
      this.toast.show("success","Fichier de collecte importé avec succès");
		}
		)


    this.data.postFichierCollecte(form, this.fileBody);
}


testEmail(email: string)
{
	 var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@(pwcavocats\.com|avocats\.pwc\.com)$/;

	 if (re.test(email))
	 this.emailValid = true;

	 else
	 this.emailValid = false;
}

testAssocie(associe: string)
{
  if (associe.length >= 2)
  this.associeValid = true;
  else
  this.associeValid = false;
  
}

focusAssocieOnOff(on: string)
{

    if (on == "on")
      this.focusAssocie = true;
    else
      this.focusAssocie = false;
}

testGroupe(groupe: string)
{

  if (groupe.length >= 2)
  this.groupeValid = true;
  else
  this.groupeValid = false;
}


handleFileInput(file) {
      
      this.selectedFile = <File>file.target.files[0];
      this.fd.append('file', this.selectedFile, this.selectedFile.name);

      console.log(<Blob>this.selectedFile);

      let reader = new FileReader();
   reader.readAsDataURL(this.selectedFile);

   var that = this;

   reader.onload = function () {
      that.fileBody = reader.result;
      that.fileChoosed = true;
   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
   };




  if (this.selectedFile.type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    this.fileChoosed = false;
  
  else
    this.fileChoosed = true;
    this.fileName = this.selectedFile.name;

}


}
