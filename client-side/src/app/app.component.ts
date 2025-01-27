import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { EsgScoreCalculatorComponent } from './esg-score-calculator/esg-score-calculator.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MatInputModule, MatFormFieldModule, FormsModule, EsgScoreCalculatorComponent],  // Add EsgScoreCalculatorComponent to imports
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {}
