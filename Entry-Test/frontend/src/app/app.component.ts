import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './service/auth-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';

  constructor(private authService: AuthService, private router: Router)
  {
    if(this.authService.isAuthenticated())
    {
      this.router.navigate(['/']);
    }
    else
    {
      this.router.navigate(['/login']);
    }
  }

}
