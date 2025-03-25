import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { env } from '../../env/env';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = env.apiUrl;  // Flask API endpoint

  constructor(private http: HttpClient) {}

  login(email: string, password: string) {
    return this.http.post(env.apiUrl, { 'email': email, 'password':password });
  }

  fetchData() {
    return this.http.get(env.apiData);
  }

  saveToken(token: string): void {
    localStorage.setItem('auth_token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getData(): string | null {
    return localStorage.getItem('data') != null ? JSON.parse(localStorage.getItem('data') ?? "{}") : null;
     
  }

  saveData(token: string): void {
    localStorage.setItem('data', JSON.stringify(token) ) ;
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.clear();
  }
}
