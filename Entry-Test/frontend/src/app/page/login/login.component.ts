import { Component } from '@angular/core';
import { AuthService } from '../../service/auth-service.service';
import { Router } from '@angular/router';
import { Title, Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  email:any = '';
  password = '';
  errorMessage = '';
  successMessage = '';
  selfLoading = false;

  constructor(private authService: AuthService, private router: Router, private titleService: Title, private metaService: Meta) {
   
   this.updateMetadata(); 
  }
//-----------------------------------
  updateMetadata() {
    this.titleService.setTitle("Admin Login - Dashboard");  // 🔹 Change Page Title
    this.metaService.updateTag({ name: 'description', content: "Login to access admin dashboard." }); // 🔹 Change Meta Description
    this.metaService.updateTag({ name: 'keywords', content: "admin, login, dashboard, authentication" }); // 🔹 Change Meta Keywords
    this.metaService.updateTag({ name: 'robots', content: "no-index,no-follow" });
  }
//-----------------------------------
  async login() {
    this.errorMessage = '';
    this.successMessage = '';
    this.selfLoading = true;

    await this.sleep(2000);

    if(!this.isEmpty(this.email) && !this.isEmpty(this.password))
    {
      this.authService.login(this.email, this.password).subscribe(
      (response:any) => {
        this.authService.saveToken(response.access_token);
        this.successMessage =  response.message ?? 'Logged in successfully !';
        this.redirect();
      },
      (response:any) => {
        this.selfLoading = false;
        if (response.status == 0)
          this.errorMessage =  "Cross Origin Issue, Check your API server program and allow this domain make request!";
        else if (response.status == 401)
          this.errorMessage = "Connexion refused!, Invalid connexion details";
        else
          this.errorMessage =  response.message ?? 'Invalid email or password';

      }
      );  
    }
    else
    {
      this.selfLoading = false;
      this.errorMessage = "Please enter a valid email and password !";
    }
    
  }

//-----------------------------------
  async redirect()
  {
    await this.sleep(2000);
    this.router.navigate(['/']);  // Redirect to dashboard after login
  }

//-----------------------------------
  isEmpty(obj:any)
  {
    return  obj == null || obj.length == 0 || obj == "";
  }
//-----------------------------------
  async sleep(ms: number)
  {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

}
