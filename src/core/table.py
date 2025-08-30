from typing import List, Optional, Dict
from .deck import Deck, Card
from .position import Position, PositionManager
from .hand import Hand


class Player:
    """Represents a player at the poker table"""
    
    def __init__(self, name: str, position: Position, stack: float = 100.0):
        self.name = name
        self.position = position
        self.stack = stack
        self.hole_cards: Optional[Hand] = None
        self.is_active = True
        self.current_bet = 0.0
        self.total_invested = 0.0
    
    def deal_hand(self, card1: Card, card2: Card):
        """Deal hole cards to player"""
        self.hole_cards = Hand(card1, card2)
    
    def fold(self):
        """Player folds"""
        self.is_active = False
    
    def bet(self, amount: float) -> bool:
        """Player bets/calls amount. Returns True if successful"""
        if amount <= self.stack:
            self.stack -= amount
            self.current_bet += amount
            self.total_invested += amount
            return True
        return False
    
    def reset_for_new_hand(self):
        """Reset player state for new hand"""
        self.hole_cards = None
        self.is_active = True
        self.current_bet = 0.0
        self.total_invested = 0.0
    
    def __str__(self) -> str:
        cards_str = str(self.hole_cards) if self.hole_cards else "No cards"
        return f"{self.name} ({self.position}) - Stack: ${self.stack:.2f} - {cards_str}"



class Table:
    """Represents a poker table with players and game state"""
    
    def __init__(self, max_players: int = 6, small_blind: float = 0.5, big_blind: float = 1.0):
        self.max_players = max_players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.position_manager = PositionManager(max_players)
        self.players: List[Player] = []
        self.community_cards: List[Card] = []
        self.pot = 0.0
        self.current_bet = 0.0
        self.dealer_position = 0
    
    def add_player(self, name: str, position: Position, stack: float = 100.0) -> bool:
        """Add a player to the table"""
        if len(self.players) >= self.max_players:
            return False
        
        # Check if position is already taken
        for player in self.players:
            if player.position == position:
                return False
        
        player = Player(name, position, stack)
        self.players.append(player)
        return True
    
    def remove_player(self, name: str) -> bool:
        """Remove a player from the table"""
        for i, player in enumerate(self.players):
            if player.name == name:
                self.players.pop(i)
                return True
        return False
    
    def get_player_by_position(self, position: Position) -> Optional[Player]:
        """Get player by position"""
        for player in self.players:
            if player.position == position:
                return player
        return None
    
    def deal_preflop(self):
        """Deal two cards to each player"""
        self.deck.reset()
        for player in self.players:
            if player.is_active:
                cards = self.deck.deal_cards(2)
                if len(cards) == 2:
                    player.deal_hand(cards[0], cards[1])
    
    def deal_flop(self):
        """Deal the flop (3 community cards)"""
        if len(self.community_cards) == 0:
            self.deck.deal_card()  # Burn card
            self.community_cards.extend(self.deck.deal_cards(3))
    
    def post_blinds(self):
        """Post small and big blinds"""
        sb_player = self.get_player_by_position(Position.SB)
        bb_player = self.get_player_by_position(Position.BB)
        
        if sb_player:
            sb_player.bet(self.small_blind)
            self.pot += self.small_blind
        
        if bb_player:
            bb_player.bet(self.big_blind)
            self.pot += self.big_blind
            self.current_bet = self.big_blind
    
    def reset_for_new_hand(self):
        """Reset table state for new hand"""
        for player in self.players:
            player.reset_for_new_hand()
        self.community_cards = []
        self.pot = 0.0
        self.current_bet = 0.0
    
    def get_active_players(self) -> List[Player]:
        """Get list of active players"""
        return [player for player in self.players if player.is_active]
    
    def __str__(self) -> str:
        community_str = " ".join(str(card) for card in self.community_cards) if self.community_cards else "No community cards"
        players_str = "\n".join(str(player) for player in self.players)
        return f"Table - Pot: ${self.pot:.2f}\nCommunity: {community_str}\nPlayers:\n{players_str}"
