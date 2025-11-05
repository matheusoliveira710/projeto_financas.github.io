import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class AnalyticsService:
    def __init__(self):
        self.historical_data = self.load_historical_data()

    def load_historical_data(self):
        """Load sample historical project data"""
        return pd.DataFrame({
            'project_id': range(1, 21),
            'complexity': np.random.randint(1, 6, 20),
            'team_size': np.random.randint(2, 10, 20),
            'duration_weeks': np.random.randint(4, 26, 20),
            'success': np.random.choice([True, False], 20, p=[0.7, 0.3]),
            'completion_rate': np.random.uniform(0.5, 1.0, 20)
        })

    def generate_insights(self, project_data):
        """Generate insights based on project data"""
        complexity = project_data.get('complexity', 3)
        team_size = project_data.get('team_size', 5)
        duration = project_data.get('duration_weeks', 12)

        # Calculate success probability based on historical data
        similar_projects = self.historical_data[
            (self.historical_data['complexity'] == complexity) &
            (self.historical_data['team_size'] == team_size)
            ]

        if len(similar_projects) > 0:
            success_rate = similar_projects['success'].mean()
            avg_completion = similar_projects['completion_rate'].mean()
        else:
            success_rate = 0.7
            avg_completion = 0.8

        insights = {
            'success_probability': round(success_rate * 100, 1),
            'expected_completion_rate': round(avg_completion * 100, 1),
            'risk_level': self.calculate_risk_level(complexity, team_size, duration),
            'key_factors': self.identify_key_factors(complexity, team_size, duration)
        }

        return insights

    def calculate_risk_level(self, complexity, team_size, duration):
        """Calculate project risk level"""
        risk_score = (complexity * 0.4) + (team_size * 0.2) + (duration * 0.1)

        if risk_score >= 3.5:
            return 'high'
        elif risk_score >= 2.5:
            return 'medium'
        else:
            return 'low'

    def identify_key_factors(self, complexity, team_size, duration):
        """Identify key success factors"""
        factors = []

        if complexity >= 4:
            factors.append('Gerenciamento de escopo crítico')
        if team_size >= 8:
            factors.append('Comunicação entre equipes essencial')
        if duration >= 20:
            factors.append('Manutenção de momentum importante')

        return factors

    def assess_risks(self, project_data):
        """Assess project risks"""
        risks = []

        complexity = project_data.get('complexity', 3)
        deadline = project_data.get('deadline')

        if complexity >= 4:
            risks.append({
                'type': 'complexity',
                'description': 'Alta complexidade pode levar a atrasos',
                'severity': 'high',
                'mitigation': 'Dividir em fases menores com entregas incrementais'
            })

        if deadline:
            deadline_date = datetime.fromisoformat(deadline)
            days_until_deadline = (deadline_date - datetime.now()).days

            if days_until_deadline < 30:
                risks.append({
                    'type': 'timeline',
                    'description': 'Prazo curto detectado',
                    'severity': 'medium',
                    'mitigation': 'Priorizar funcionalidades essenciais'
                })

        return risks