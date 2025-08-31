from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
import json
from typing import Dict, Any

from ..core import Card, Deck, Hand, Position, Rank, Suit
from ..gto import GTOAnalyzer


# Initialize analyzer once
analyzer = GTOAnalyzer()


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Poker GTO Trainer API is running'
    })


@api_view(['POST'])
def analyze_hand(request):
    """Analyze a specific hand for GTO recommendation"""
    try:
        data = request.data
        
        # Parse position
        position_str = data.get('position', 'BTN')
        try:
            position = Position.from_string(position_str)
        except ValueError:
            return Response(
                {'error': f'Invalid position: {position_str}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse scenario
        scenario = data.get('scenario', 'first_in')
        
        # Generate random hand for demo (in real app, parse from request)
        deck = Deck()
        cards = deck.deal_cards(2)
        hand = Hand(cards[0], cards[1])
        
        # Analyze the hand
        analysis = analyzer.analyze_preflop_hand(hand, position, scenario)
        
        # Add hand data to response
        response_data = {
            **analysis,
            'hand_data': hand.to_dict()
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def generate_random_situation(request):
    """Generate a random poker situation for training"""
    try:
        # Generate random position
        positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
        position = random.choice(positions)
        
        # Generate random hand
        deck = Deck()
        cards = deck.deal_cards(2)
        hand = Hand(cards[0], cards[1])
        
        # Determine scenario based on position
        if position == Position.BB:
            scenarios = ["vs_btn_sb", "vs_co", "vs_mp3"]
            scenario = random.choice(scenarios)
        else:
            scenario = "first_in"
        
        # Get GTO analysis
        analysis = analyzer.analyze_preflop_hand(hand, position, scenario)
        
        situation = {
            'situation_id': random.randint(1000, 9999),
            'position': position.to_dict(),
            'hand': hand.to_dict(),
            'scenario': scenario,
            'scenario_description': _get_scenario_description(position, scenario),
            'gto_analysis': analysis
        }
        
        return Response(situation)
        
    except Exception as e:
        return Response(
            {'error': f'Could not generate situation: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_position_ranges(request):
    """Get opening ranges for all positions"""
    try:
        position_param = request.GET.get('position')
        scenario_param = request.GET.get('scenario', 'first_in')
        
        if position_param:
            # Get range for specific position
            try:
                position = Position.from_string(position_param)
                range_summary = analyzer.get_opening_range_summary(position, scenario_param)
                return Response({
                    'position': position.to_dict(),
                    'scenario': scenario_param,
                    'range_summary': range_summary
                })
            except ValueError:
                return Response(
                    {'error': f'Invalid position: {position_param}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Get ranges for all positions
            ranges = {}
            positions = [Position.MP, Position.CO, Position.BTN, Position.SB]  # Opening positions
            
            for pos in positions:
                range_summary = analyzer.get_opening_range_summary(pos, scenario_param)
                ranges[pos.short_name] = {
                    'position': pos.to_dict(),
                    'range_summary': range_summary
                }
            
            return Response({
                'scenario': scenario_param,
                'ranges': ranges
            })
        
    except Exception as e:
        return Response(
            {'error': f'Could not get ranges: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_available_scenarios(request):
    """Get all available scenarios"""
    try:
        scenarios = analyzer.get_all_available_scenarios()
        
        return Response({
            'scenarios': scenarios,
            'positions': [pos.to_dict() for pos in [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]]
        })
        
    except Exception as e:
        return Response(
            {'error': f'Could not get scenarios: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def validate_user_action(request):
    """Validate user's action against GTO recommendation"""
    try:
        data = request.data
        
        # Parse situation
        situation_data = data.get('situation', {})
        user_action = data.get('user_action', 'fold')
        
        # Recreate the situation
        position = Position.from_string(situation_data['position']['short_name'])
        scenario = situation_data['scenario']
        hand = Hand.from_dict(situation_data['hand'])
        
        # Get GTO recommendation
        gto_analysis = analyzer.analyze_preflop_hand(hand, position, scenario)
        gto_action = gto_analysis['recommended_action']
        
        # Simple validation (you could make this more sophisticated)
        is_correct = user_action.lower() == gto_action.lower()
        
        # Map actions for more flexible matching
        action_mapping = {
            'fold': ['fold'],
            'call': ['call', 'call_ip'],
            'raise': ['raise', 'raise_fold', 'raise_call', 'raise_4_bet_fold', 'raise_4_bet_all_in'],
            'reraise': ['reraise_fold', 'reraise_all_in']
        }
        
        # Check if user action maps to GTO action
        if not is_correct:
            for user_mapped, gto_mapped_list in action_mapping.items():
                if user_action.lower() == user_mapped:
                    is_correct = any(gto_action.lower().replace('_', ' ').replace('-', ' ') in gto_mapped.replace('_', ' ').replace('-', ' ') for gto_mapped in gto_mapped_list)
                    break
        
        validation = {
            'is_correct': is_correct,
            'user_action': user_action,
            'gto_action': gto_action,
            'gto_explanation': gto_analysis['explanation'],
            'feedback': _get_feedback(is_correct, user_action, gto_action)
        }
        
        return Response(validation)
        
    except Exception as e:
        return Response(
            {'error': f'Could not validate action: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _get_scenario_description(position: Position, scenario: str) -> str:
    """Get human-readable scenario description"""
    if scenario == "first_in":
        return f"You are {position.short_name} and no one has raised yet."
    elif scenario == "vs_btn_sb":
        return f"You are {position.short_name} and the Button/SB has raised."
    elif scenario == "vs_co":
        return f"You are {position.short_name} and the CO has raised."
    elif scenario == "vs_mp3":
        return f"You are {position.short_name} and MP has raised."
    else:
        return f"You are {position.short_name}."


def _get_feedback(is_correct: bool, user_action: str, gto_action: str) -> str:
    """Generate feedback message"""
    if is_correct:
        return f"Correct! {user_action.capitalize()} is the GTO play here."
    else:
        return f"Not quite. GTO recommends {gto_action} instead of {user_action}."
