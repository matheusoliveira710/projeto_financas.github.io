import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class ProjectRecommender:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.load_sample_data()

    def load_sample_data(self):
        """Load sample project data for recommendations"""
        # Sample project data
        self.projects_data = pd.DataFrame({
            'complexity': [3, 5, 2, 4, 1, 5, 3, 4],
            'team_size': [5, 8, 3, 6, 2, 7, 4, 5],
            'duration_weeks': [12, 20, 8, 16, 6, 24, 10, 18],
            'success_rate': [0.85, 0.65, 0.95, 0.75, 0.98, 0.60, 0.88, 0.72]
        })

        # Train recommendation model
        self.train_model()

    def train_model(self):
        """Train the recommendation model"""
        try:
            # Prepare features
            features = self.projects_data[['complexity', 'team_size', 'duration_weeks']]

            # Scale features
            scaled_features = self.scaler.fit_transform(features)

            # Train K-means clustering
            self.model = KMeans(n_clusters=3, random_state=42)
            self.model.fit(scaled_features)

        except Exception as e:
            print(f"Error training model: {e}")

    def get_recommendations(self):
        """Get general project recommendations"""
        recommendations = [
            {
                'title': 'Otimizar Alocação de Recursos',
                'description': 'Redistribuir equipes baseado em habilidades',
                'priority': 'high',
                'impact': 'Aumento de 15% na produtividade'
            },
            {
                'title': 'Revisar Prazos de Entrega',
                'description': 'Ajustar cronogramas baseado em dados históricos',
                'priority': 'medium',
                'impact': 'Melhoria de 20% na pontualidade'
            },
            {
                'title': 'Implementar Revisões Regulares',
                'description': 'Agendar checkpoints semanais de progresso',
                'priority': 'low',
                'impact': 'Identificação precoce de problemas'
            }
        ]

        return recommendations

    def get_project_recommendations(self, project_data):
        """Get specific recommendations for a project"""
        complexity = project_data.get('complexity', 3)
        team_size = project_data.get('team_size', 5)
        duration = project_data.get('duration_weeks', 12)

        recommendations = []

        # Complexity-based recommendations
        if complexity >= 4:
            recommendations.append({
                'type': 'complexity',
                'message': 'Projeto de alta complexidade detectado',
                'suggestion': 'Considere dividir em fases menores e aumentar a frequência de revisões',
                'priority': 'high'
            })

        # Team size recommendations
        if team_size > 10:
            recommendations.append({
                'type': 'team_size',
                'message': 'Equipe muito grande pode impactar comunicação',
                'suggestion': 'Implemente sub-equipes com líderes dedicados',
                'priority': 'medium'
            })

        # Duration recommendations
        if duration > 20:
            recommendations.append({
                'type': 'duration',
                'message': 'Projeto de longa duração identificado',
                'suggestion': 'Estabeleça marcos intermediários para manter o momentum',
                'priority': 'medium'
            })

        return recommendations