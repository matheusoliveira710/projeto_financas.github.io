from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from ml.project_recommender import ProjectRecommender
from services.analytics import AnalyticsService
from services.report_generator import ReportGenerator

app = Flask(__name__)
CORS(app)

# Initialize services
analytics_service = AnalyticsService()
report_generator = ReportGenerator()
recommender = ProjectRecommender()


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Provide analytics data for dashboard"""
    try:
        # Mock data - replace with actual data processing
        analytics_data = {
            'performance_metrics': {
                'completion_rate': 78,
                'on_time_delivery': 85,
                'team_efficiency': 92
            },
            'trends': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'completion_data': [65, 70, 68, 75, 78, 80],
                'efficiency_data': [85, 82, 88, 90, 92, 95]
            },
            'recommendations': recommender.get_recommendations()
        }

        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/analyze', methods=['POST'])
def analyze_project():
    """Analyze project data and provide insights"""
    try:
        project_data = request.json

        # Generate insights using ML
        insights = analytics_service.generate_insights(project_data)

        # Generate risk assessment
        risk_assessment = analytics_service.assess_risks(project_data)

        # Get recommendations
        recommendations = recommender.get_project_recommendations(project_data)

        response = {
            'insights': insights,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Generate comprehensive project reports"""
    try:
        report_type = request.json.get('type', 'progress')
        project_data = request.json.get('data', {})

        report = report_generator.generate_report(report_type, project_data)

        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/completion', methods=['POST'])
def predict_completion():
    """Predict project completion date"""
    try:
        project_data = request.json

        # Mock prediction - replace with actual ML model
        current_progress = project_data.get('progress', 0)
        start_date = datetime.fromisoformat(project_data.get('start_date'))
        deadline = datetime.fromisoformat(project_data.get('deadline'))

        # Simple linear prediction
        if current_progress > 0:
            days_elapsed = (datetime.now() - start_date).days
            total_days_needed = (days_elapsed / current_progress) * 100
            predicted_completion = start_date + timedelta(days=total_days_needed)
        else:
            predicted_completion = deadline

        is_on_track = predicted_completion <= deadline

        response = {
            'predicted_completion': predicted_completion.isoformat(),
            'is_on_track': is_on_track,
            'confidence': 0.85
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'python-backend'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)