import { Component, OnInit, AfterViewInit } from '@angular/core';
import { AuthService } from '../../service/auth-service.service';
import { Router } from '@angular/router';
import { Title, Meta } from '@angular/platform-browser';
import { Chart } from 'chart.js';
import * as d3 from 'd3';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  selfLoading = true;
  successMessage = "";
  errorMessage = "";
  data:any;
  filteredData:any;

  selectedYear: string = "";
  selectedSector: string = "";
  selectedCountry: string = "";
  
  uniqueYears: string[] = [];
  uniqueSectors: string[] = [];
  uniqueCountries: string[] = [];

  // Chart Data
  barChart: any ;
  pieChart: any ;
  lineChart: any;

  colorScheme = { domain: ['#5AA454', '#C7B42C', '#AAAAAA'] };


  constructor(private authService: AuthService, private router: Router, private titleService: Title, private metaService: Meta)
  {

    // this.authService.logout();
    // this.redirect();

    this.selfLoading = true;

    this.updateMetadata(); 

    if(this.isEmpty(this.authService.getData()) )
    {
      this.authService.fetchData().subscribe(
      (response:any) => {
        this.selfLoading = false;
        this.authService.saveData(response.data);
        this.data = response.data;
        this.filteredData = this.data;
        this.successMessage = 'Data loaded successfully (from API) !'; // JSON.stringify(this.data);
        this.extractUniqueValues();
        this.prepareChartData();
        
      },
      (response:any) => {
        this.selfLoading = false;
        if (response.status == 0)
          this.errorMessage =  "Cross Origin Issue, Check your API server program and allow this domain make request!";
        else if (response.status == 401)
          this.errorMessage = "Connexion refused!, Invalid connexion details";
        else
          this.errorMessage =  response.message ?? 'Error occured while loading the data';

        // this.authService.logout();
        // this.redirect();
      }
      );  
    }
    else
    {
      this.selfLoading = false;
      this.data = this.authService.getData();
      this.filteredData = this.data;
      this.successMessage = 'Data loaded successfully from cache (fetched only once from API) !';
      this.extractUniqueValues();
      this.prepareChartData();
    }

  }
//-----------------------------------
  ngOnInit() {
    

  }

  // ngAfterViewInit() {
  //   if ( !this.isEmpty(this.data) ) {
  //     this.createCharts();
  //   }
  // }
//-----------------------------------


  extractUniqueValues() {
    this.uniqueYears = [];
    this.uniqueSectors = [];
    this.uniqueCountries = [];

    const yearSet = new Set<string>();
    const sectorSet = new Set<string>();
    const countrySet = new Set<string>();

    for (const d of this.data) {
      if (d.end_year) {
        yearSet.add(String(d.end_year)); // Ensure values are stored as strings
      }
      if (d.sector) {
        sectorSet.add(String(d.sector));
      }
      if (d.country) {
        countrySet.add(String(d.country));
      }
    }

    this.uniqueYears = Array.from(yearSet);
    this.uniqueSectors = Array.from(sectorSet);
    this.uniqueCountries = Array.from(countrySet);

  } 


  prepareChartData() {
    if ( !this.isEmpty(this.data) ) {
      this.filteredData = this.data;
      // this.updateCharts();
      this.createCharts(); // Ensure charts are created when data is ready
    }
  }

  applyFilters() {
    this.selfLoading = true;
    this.filteredData = this.data.filter((d: any) =>
      (!this.selectedYear || d.end_year === this.selectedYear) &&
      (!this.selectedSector || d.sector === this.selectedSector) &&
      (!this.selectedCountry || d.country === this.selectedCountry)
    );

    if (!this.barChart || !this.pieChart || !this.lineChart) {
      this.createCharts(); // Create charts if they don't exist
    } else {
      this.updateCharts(); // Update if charts already exist
    }

    this.selfLoading = false;
  }

  createCharts() {

    const barCanvas = document.getElementById("barChart") as HTMLCanvasElement;
    const pieCanvas = document.getElementById("pieChart") as HTMLCanvasElement;
    const lineCanvas = document.getElementById("lineChart") as HTMLCanvasElement;

    if (!barCanvas || !pieCanvas || !lineCanvas) {
      console.warn("Chart canvas elements not found.");
      return;
    }


    this.barChart = new Chart(barCanvas, {
      type: "bar",
      data: {
        labels: this.filteredData.map((d: any) => d.end_year),
        datasets: [{
          label: "Intensity",
          data: this.filteredData.map((d: any) => d.intensity),
          backgroundColor: ["#5AA454", "#C7B42C", "#AAAAAA"]
        }]
      },
      options: { responsive: true, plugins: { legend: { display: true } } }
    });

    this.pieChart = new Chart(pieCanvas, {
      type: "pie",
      data: {
        labels: [...new Set(this.filteredData.map((d: any) => d.sector))],
        datasets: [{
          label: "Sector Distribution",
          data: this.filteredData.reduce((acc: any, d: any) => {
            acc[d.sector] = (acc[d.sector] || 0) + 1;
            return acc;
          }, {}),
          backgroundColor: ["#5AA454", "#C7B42C", "#AAAAAA"]
        }]
      },
      options: { responsive: true }
    });

    this.lineChart = new Chart(lineCanvas, {
      type: "line",
      data: {
        labels: this.filteredData.map((d: any) => d.end_year),
        datasets: [{
          label: "Relevance",
          data: this.filteredData.map((d: any) => d.relevance),
          borderColor: "#C7B42C",
          fill: false
        }]
      },
      options: { responsive: true, plugins: { legend: { display: true } } }
    });
  }

  updateCharts() {
    if (this.barChart) {
      this.barChart.data.labels = this.filteredData.map((d: any) => d.end_year);
      this.barChart.data.datasets[0].data = this.filteredData.map((d: any) => d.intensity);
      this.barChart.update();
    }

    if (this.pieChart) {
      this.pieChart.data.labels = [...new Set(this.filteredData.map((d: any) => d.sector))];
      this.pieChart.data.datasets[0].data = Object.values(this.filteredData.reduce((acc: any, d: any) => {
        acc[d.sector] = (acc[d.sector] || 0) + 1;
        return acc;
      }, {}));
      this.pieChart.update();
    }

    if (this.lineChart) {
      this.lineChart.data.labels = this.filteredData.map((d: any) => d.end_year);
      this.lineChart.data.datasets[0].data = this.filteredData.map((d: any) => d.relevance);
      this.lineChart.update();
    }
  }


//-----------------------------------
  updateMetadata() {
    this.titleService.setTitle("Admin - Dashboard");  // 🔹 Change Page Title
    this.metaService.updateTag({ name: 'description', content: "Admin dashboard." }); // 🔹 Change Meta Description
    this.metaService.updateTag({ name: 'keywords', content: "admin, dashboard" }); // 🔹 Change Meta Keywords
    this.metaService.updateTag({ name: 'robots', content: "no-index,no-follow" });
  }
//-----------------------------------
  async redirect()
  {
    this.router.navigate(['/']);  // Redirect to dashboard after login
  }
//-----------------------------------
  async logout()
  {
    this.authService.logout();
    await this.sleep(500);
    this.router.navigate(['/login']);
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
