import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { HttpClient } from '@angular/common/http';
import {BehaviorSubject, catchError, Observable} from 'rxjs';
import {AsyncPipe} from '@angular/common';

@Component({
  selector: 'app-esg-score-calculator',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, FormsModule, AsyncPipe],
  templateUrl: './esg-score-calculator.component.html',
  styleUrls: ['./esg-score-calculator.component.scss']
})

export class EsgScoreCalculatorComponent {
  // Create the private BehaviorSubject to hold the ESG score
  private esgScoreSubject: BehaviorSubject<number> = new BehaviorSubject<number>(0);

  inputFields: number[] = Array(7).fill(0); // Initialize 7 decimal inputs

  constructor(private http: HttpClient) {}

  // Getter to expose esgScoreSubject as a public observable
  get esgScore$() {
    return this.esgScoreSubject.asObservable();
  }

  onSubmit() {
    const data = {
      controv_src_score: this.inputFields[0],
      environmental_pillar_score: this.inputFields[1],
      governance_pillar_score: this.inputFields[2],
      social_pillar_score: this.inputFields[3],
      climate_change_theme_score: this.inputFields[4],
      industry_adjusted_score: this.inputFields[5],
      business_ethics_theme_score: this.inputFields[6],
    };

    this.http.post<any>('http://127.0.0.1:5000/predict', data).subscribe(
      (response) => {
        // Update the esgScoreSubject with the value returned from the server
        this.esgScoreSubject.next(response.esg_score);
      },
      (error) => {
        console.error('Error:', error);
        this.esgScoreSubject.next(0); // If there's an error, default to 0
      }
    );
  }
}
