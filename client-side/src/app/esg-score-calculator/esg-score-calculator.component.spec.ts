import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EsgScoreCalculatorComponent } from './esg-score-calculator.component';

describe('EsgScoreCalculatorComponent', () => {
  let component: EsgScoreCalculatorComponent;
  let fixture: ComponentFixture<EsgScoreCalculatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EsgScoreCalculatorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EsgScoreCalculatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
