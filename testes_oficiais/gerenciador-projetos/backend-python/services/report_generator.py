import json
from datetime import datetime
import pandas as pd


class ReportGenerator:
    def generate_report(self, report_type, project_data):
        """Generate different types of reports"""
        if report_type == 'progress':
            return self._generate_progress_report(project_data)
        elif report_type == 'risk':
            return self._generate_risk_report(project_data)
        elif report_type == 'performance':
            return self._generate_performance_report(project_data)
        else:
            return self._generate_summary_report(project_data)

    def _generate_progress_report(self, project_data):
        """Generate progress report"""
        progress = project_data.get('progress', 0)
        tasks_completed = project_data.get('tasks_completed', 0)
        total_tasks = project_data.get('total_tasks', 1)

        report = {
            'type': 'progress',
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'overall_progress': progress,
                'tasks_completed': tasks_completed,
                'tasks_remaining': total_tasks - tasks_completed,
                'completion_rate': (tasks_completed / total_tasks) * 100
            },
            'recommendations': self._get_progress_recommendations(progress)
        }

        return report

    def _generate_risk_report(self, project_data):
        """Generate risk assessment report"""
        report = {
            'type': 'risk',
            'generated_at': datetime.now().isoformat(),
            'risk_assessment': {
                'overall_risk': 'medium',
                'identified_risks': [
                    {
                        'category': 'timeline',
                        'description': 'Possível atraso na entrega',
                        'probability': 'medium',
                        'impact': 'high'
                    },
                    {
                        'category': 'resources',
                        'description': 'Alocação de equipe limitada',
                        'probability': 'low',
                        'impact': 'medium'
                    }
                ]
            },
            'mitigation_strategies': [
                'Revisar cronograma semanalmente',
                'Alocar recursos adicionais se necessário'
            ]
        }

        return report

    def _generate_performance_report(self, project_data):
        """Generate performance report"""
        report = {
            'type': 'performance',
            'generated_at': datetime.now().isoformat(),
            'metrics': {
                'efficiency': 85,
                'productivity': 78,
                'quality': 92,
                'adherence_to_schedule': 75
            },
            'team_performance': {
                'average_task_completion_time': '2.3 dias',
                'bug_rate': '2.1%',
                'customer_satisfaction': '4.2/5.0'
            }
        }

        return report

    def _generate_summary_report(self, project_data):
        """Generate summary report"""
        return {
            'type': 'summary',
            'generated_at': datetime.now().isoformat(),
            'project_overview': {
                'status': 'in_progress',
                'start_date': project_data.get('start_date'),
                'deadline': project_data.get('deadline'),
                'budget_utilization': '65%'
            },
            'key_achievements': [
                'Fase 1 concluída com sucesso',
                'Equipe totalmente integrada',
                'Metas de qualidade atingidas'
            ],
            'next_steps': [
                'Iniciar fase 2 de desenvolvimento',
                'Revisão de código agendada',
                'Testes de integração planejados'
            ]
        }

    def _get_progress_recommendations(self, progress):
        """Get recommendations based on progress"""
        if progress < 25:
            return ['Focar em estabelecer base sólida', 'Definir marcos claros']
        elif progress < 50:
            return ['Manter momentum atual', 'Revisar alocação de recursos']
        elif progress < 75:
            return ['Preparar para fase final', 'Antecipar possíveis obstáculos']
        else:
            return ['Focar em finalização', 'Preparar documentação']