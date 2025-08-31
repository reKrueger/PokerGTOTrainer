"""
Poker Table Controller
======================

Controller class for managing poker table logic and state changes.
Acts as intermediary between Model and View.
"""

from typing import Optional, List, Dict, Any, Callable
from .model import PokerTableModel, PlayerInfo, Card, BetType, TableStage


class PokerTableController:
    """
    Controller for poker table interactions and state management
    
    Responsibilities:
    - Handle user interactions
    - Update model state
    - Coordinate between model and view
    - Manage game flow logic
    """
    
    def __init__(self, model: PokerTableModel):
        self.model = model
        self._observers: List[Callable] = []
    
    def add_observer(self, callback: Callable):
        """Add observer for model changes"""
        self._observers.append(callback)
    
    def _notify_observers(self):
        """Notify all observers of model changes"""
        for callback in self._observers:
            callback()
    
    # Player Management
    def add_player(self, position: str, name: str, stack: float = 100.0):
        """Add player to table"""
        try:
            self.model.add_player(position, name, stack)
            self._notify_observers()
            return True
        except ValueError as e:
            print(f"Error adding player: {e}")
            return False
    
    def remove_player(self, position: str):
        """Remove player from table"""
        self.model.remove_player(position)
        self._notify_observers()
    
    def set_current_player(self, position: str):
        """Set current acting player"""
        self.model.set_current_player(position)
        self._notify_observers()
    
    # Card Management
    def set_flop(self, card1: Card, card2: Card, card3: Card):
        """Set flop cards"""
        self.model.set_flop([card1, card2, card3])
        self._notify_observers()
    
    def set_turn(self, card: Card):
        """Set turn card"""
        self.model.set_turn(card)
        self._notify_observers()
    
    def set_river(self, card: Card):
        """Set river card"""
        self.model.set_river(card)
        self._notify_observers()
    
    def clear_community_cards(self):
        """Clear all community cards"""
        self.model.community_cards.flop = []
        self.model.community_cards.turn = None
        self.model.community_cards.river = None
        self.model.current_stage = TableStage.PREFLOP
        self._notify_observers()
    
    # Betting Actions
    def player_fold(self, position: str):
        """Player folds"""
        self.model.set_player_action(position, BetType.FOLD, 0.0)
        self._notify_observers()
    
    def player_check(self, position: str):
        """Player checks"""
        self.model.set_player_action(position, BetType.CHECK, 0.0)
        self._notify_observers()
    
    def player_call(self, position: str, amount: float):
        """Player calls"""
        self.model.set_player_action(position, BetType.CALL, amount)
        self._update_pot(amount)
        self._notify_observers()
    
    def player_bet(self, position: str, amount: float):
        """Player bets"""
        self.model.set_player_action(position, BetType.BET, amount)
        self._update_pot(amount)
        self._notify_observers()
    
    def player_raise(self, position: str, amount: float):
        """Player raises"""
        self.model.set_player_action(position, BetType.RAISE, amount)
        self._update_pot(amount)
        self._notify_observers()
    
    def player_all_in(self, position: str, amount: float):
        """Player goes all-in"""
        self.model.set_player_action(position, BetType.ALL_IN, amount)
        self._update_pot(amount)
        self._notify_observers()
    
    def _update_pot(self, amount: float):
        """Update pot with bet amount"""
        self.model.pot_size += amount
    
    # Game Flow
    def start_new_hand(self):
        """Start a new hand"""
        self.model.reset_hand()
        self._notify_observers()
    
    def next_betting_round(self):
        """Move to next betting round"""
        self.model.reset_betting_round()
        
        # Advance stage if possible
        if self.model.current_stage == TableStage.PREFLOP and self.model.community_cards.flop:
            self.model.current_stage = TableStage.FLOP
        elif self.model.current_stage == TableStage.FLOP and self.model.community_cards.turn:
            self.model.current_stage = TableStage.TURN
        elif self.model.current_stage == TableStage.TURN and self.model.community_cards.river:
            self.model.current_stage = TableStage.RIVER
        
        self._notify_observers()
    
    # Utility Methods
    def get_table_state(self) -> Dict[str, Any]:
        """Get current table state"""
        return self.model.to_dict()
    
    def get_active_players(self) -> List[PlayerInfo]:
        """Get active players"""
        return self.model.get_active_players()
    
    def get_current_player(self) -> Optional[PlayerInfo]:
        """Get current acting player"""
        if self.model.current_player_position:
            return self.model.get_player_by_position(self.model.current_player_position)
        return None
    
    def is_preflop(self) -> bool:
        """Check if currently preflop"""
        return self.model.current_stage == TableStage.PREFLOP
    
    def is_postflop(self) -> bool:
        """Check if currently postflop"""
        return self.model.current_stage != TableStage.PREFLOP
    
    def get_community_cards_count(self) -> int:
        """Get number of community cards"""
        return len(self.model.community_cards.get_all_cards())
    
    def get_stage_display(self) -> str:
        """Get display string for current stage"""
        stage_names = {
            TableStage.PREFLOP: "Pre-Flop",
            TableStage.FLOP: "Flop",
            TableStage.TURN: "Turn", 
            TableStage.RIVER: "River"
        }
        return stage_names.get(self.model.current_stage, "Unknown")
    
    # Setup Methods for Different Scenarios
    def setup_training_scenario(self, hero_position: str, hero_name: str = "Hero"):
        """Setup table for training scenario with hero in specified position"""
        self.start_new_hand()
        
        # Add hero
        self.add_player(hero_position, hero_name, 100.0)
        self.set_current_player(hero_position)
        
        # Add opponents at other positions (for context)
        opponent_positions = [pos for pos in self.model.positions if pos != hero_position]
        for i, pos in enumerate(opponent_positions[:3]):  # Add up to 3 opponents
            self.add_player(pos, f"Opponent{i+1}", 100.0)
    
    def setup_range_display_scenario(self, focus_position: str):
        """Setup table for range display with focus on specific position"""
        self.start_new_hand()
        
        # Add player at focus position
        self.add_player(focus_position, "Hero", 100.0)
        
        # Add minimal opponents for context
        other_positions = [pos for pos in self.model.positions if pos != focus_position]
        for pos in other_positions[:2]:
            self.add_player(pos, "Opp", 100.0)
    
    def setup_full_table(self):
        """Setup full 6-player table"""
        self.start_new_hand()
        
        player_names = ["UTG_Player", "MP_Player", "CO_Player", "BTN_Player", "SB_Player", "BB_Player"]
        
        for position, name in zip(self.model.positions, player_names):
            self.add_player(position, name, 100.0)
