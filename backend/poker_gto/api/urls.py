from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Hand analysis
    path('analyze-hand/', views.analyze_hand, name='analyze_hand'),
    
    # Training endpoints
    path('random-situation/', views.generate_random_situation, name='generate_random_situation'),
    path('validate-action/', views.validate_user_action, name='validate_user_action'),
    
    # Range information
    path('position-ranges/', views.get_position_ranges, name='get_position_ranges'),
    path('scenarios/', views.get_available_scenarios, name='get_available_scenarios'),
]
