import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Subject } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class ConnectService {

  private serverUrl = 'https://percent-f141b.firebaseio.com';
  
  fichierCollectes;
  PostCollecteData;


  getFichierCollecte() {
    this.httpClient
      .get<any[]>('http://0.0.0.0:5000/declarations')
      .subscribe(
        (response) => {
          this.fichierCollectes = response;
          this.emitFichierCollecte();
        },
        (error) => {
          console.log('Erreur ! : ' + error);
        }
      );
   }

 fichierCollecteSubject = new Subject<any[]>();

   emitFichierCollecte() {
   	this.fichierCollecteSubject.next(this.fichierCollectes.slice());
   }



   graphData;


   getGraphData(ID:string) {
     this.httpClient
       .get<any[]>('http://0.0.0.0:5000/organigramme/' + ID)
       .subscribe(
         (response) => {
           this.graphData = response;
           this.emitGraphData();
         },
         (error) => {
           console.log('Erreur ! : ' + error);
         }
       );
    }
 
    graphDataSubject = new Subject<any[]>();
 
    emitGraphData() {
      this.graphDataSubject.next(this.graphData);
    }
 


 postFichierCollecte(formData, file) {

let headers = new HttpHeaders();
headers.set('Content-Type', null);
headers.set('Accept', "multipart/form-data");


var fd = new FormData();
fd.append("associe", formData.form.value.associe);
fd.append("email", formData.form.value.email);
fd.append("groupe", formData.form.value.groupe);
fd.append("OTP", formData.form.value.OTP);

fd.append('file', file);


   this.httpClient
   .post<any[]>('http://0.0.0.0:5000/upload',fd)
      .subscribe(
        () => {
          this.PostCollecteData = 1;
          this.emitPostCollecte();
          console.log('Enregistrement terminé !');
        },
        (error) => {
          console.log('Erreur ! : ' + error);
        }
     );

  }


  postCollecteSubject = new Subject<any[]>();
 
  emitPostCollecte() {
    this.postCollecteSubject.next([this.PostCollecteData]);
  }



  constructor(private httpClient: HttpClient) { }
}
