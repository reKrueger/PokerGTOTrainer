from typing import Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import Position
from .ranges import GTORange, Action


class GTOChartParser:
    """Parses GTO charts from the provided spreadsheet data"""
    
    def __init__(self):
        self.charts: Dict[Position, GTORange] = {}
        self._initialize_charts()
    
    def _initialize_charts(self):
        """Initialize all GTO charts based on the provided data"""
        self._create_utg_chart()
        self._create_mp2_chart()
        self._create_mp3_chart() 
        self._create_co_chart()
        self._create_btn_sb_chart()
        self._create_sb_chart()
        self._create_bb_vs_sb_btn_chart()
        self._create_bb_vs_co_chart()
        self._create_bb_vs_mp3_chart()
    
    def _create_utg_chart(self):
        """Create UTG (Under The Gun) opening range - tightest range"""
        utg_range = GTORange(Position.UTG, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            utg_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold  
        strong_hands = ["AQs", "AQo", "AJs", "KQs", "TT"]
        for hand in strong_hands:
            utg_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "KJs", "QJs", "99"]
        for hand in medium_hands:
            utg_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Limited weaker raises - raise/fold
        weak_raise_hands = ["A9s", "A8s", "KTs", "88", "77"]
        for hand in weak_raise_hands:
            utg_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.UTG] = utg_range
    
    def _create_mp2_chart(self):
        """Create MP2 (Middle Position 2) opening range"""
        mp_range = GTORange(Position.MP, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold  
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"]
        for hand in strong_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "ATo", "KJs", "KJo", "QJs", "QJo", "JTs", "99"]
        for hand in medium_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold
        weak_raise_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "K9s", "KTs", "QTs", "T9s", "88", "77"]
        for hand in weak_raise_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.MP] = mp_range
    
    def _create_mp3_chart(self):
        """Create MP3 (Middle Position 3) opening range - slightly wider than MP2"""
        mp3_range = GTORange(Position.MP, "first_in_mp3")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"] 
        for hand in strong_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "ATo", "KJs", "KJo", "QJs", "QJo", "JTs", "99", "88"]
        for hand in medium_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold (wider than MP2)
        weak_raise_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "K9s", "KTs", "QTs", "Q9s", 
                           "JTs", "J9s", "T9s", "T8s", "98s", "87s", "77", "66"]
        for hand in weak_raise_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.MP] = mp3_range
    
    def _create_co_chart(self):
        """Create Cutoff opening range - wider than MP"""
        co_range = GTORange(Position.CO, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "ATs", "KQs", "KQo", "KJs", "TT", "99"]
        for hand in strong_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATo", "A9s", "KJo", "KTs", "QJs", "QJo", "QTs", "JTs", "JTo", "88", "77"]
        for hand in medium_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold (much wider range)
        weak_raise_hands = ["A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s", "K9s", "K8s", "K7s",
                           "Q9s", "Q8s", "J9s", "J8s", "T9s", "T8s", "98s", "97s", "87s", "76s",
                           "66", "55", "44", "33", "22"]
        for hand in weak_raise_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.CO] = co_range
    
    def _create_btn_sb_chart(self):
        """Create Button/SB opening range - widest range"""
        btn_range = GTORange(Position.BTN, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "ATs", "ATo", "A9s", "KQs", "KQo", "KJs", 
                       "KJo", "KTs", "QJs", "QJo", "QTs", "TT", "99", "88"]
        for hand in strong_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call  
        medium_hands = ["A8s", "A7s", "A6s", "A5s", "K9s", "Q9s", "JTs", "JTo", "J9s", "T9s", "77", "66"]
        for hand in medium_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Very wide raising range - raise/fold
        weak_raise_hands = ["A4s", "A3s", "A2s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                           "Q8s", "Q7s", "Q6s", "J8s", "J7s", "T8s", "T7s", "98s", "97s", "96s", 
                           "87s", "86s", "76s", "75s", "65s", "55", "44", "33", "22"]
        for hand in weak_raise_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        # Some offsuit broadway - raise/fold
        offsuit_broadway = ["A9o", "KTo", "QTo", "JTo"]
        for hand in offsuit_broadway:
            btn_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.BTN] = btn_range
    
    def _create_sb_chart(self):
        """Create Small Blind opening range - similar to BTN but slightly tighter"""
        sb_range = GTORange(Position.SB, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            sb_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "ATs", "ATo", "KQs", "KQo", "KJs", 
                       "KJo", "KTs", "QJs", "QJo", "QTs", "TT", "99", "88"]
        for hand in strong_hands:
            sb_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call  
        medium_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "K9s", "Q9s", "JTs", "J9s", "T9s", "77", "66"]
        for hand in medium_hands:
            sb_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Wide raising range - raise/fold (slightly tighter than BTN)
        weak_raise_hands = ["A4s", "A3s", "A2s", "K8s", "K7s", "K6s", "K5s", "K4s", 
                           "Q8s", "Q7s", "J8s", "J7s", "T8s", "T7s", "98s", "97s", 
                           "87s", "86s", "76s", "65s", "55", "44", "33", "22"]
        for hand in weak_raise_hands:
            sb_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        # Some offsuit broadway - raise/fold
        offsuit_broadway = ["A9o", "KTo", "QTo"]
        for hand in offsuit_broadway:
            sb_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts[Position.SB] = sb_range
    
    def _create_bb_vs_sb_btn_chart(self):
        """Create BB defense vs SB+BTN"""
        bb_range = GTORange(Position.BB, "vs_btn_sb")
        
        # Reraise/all in hands
        reraise_all_in = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in reraise_all_in:
            bb_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Reraise/fold hands
        reraise_fold = ["AQs", "AQo", "AJs", "AJo", "ATs", "KQs", "KQo", "KJs", "TT"]
        for hand in reraise_fold:
            bb_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Call hands (wide defense)
        call_hands = ["ATo", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s", "KJo", "KTs",
                     "K9s", "K8s", "K7s", "K6s", "QJs", "QJo", "QTs", "Q9s", "Q8s", "JTs", "JTo",
                     "J9s", "J8s", "T9s", "T8s", "98s", "97s", "87s", "76s", "65s", "54s",
                     "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in call_hands:
            bb_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts[Position.BB] = bb_range
    
    def _create_bb_vs_co_chart(self):
        """Create BB defense vs CO - tighter than vs BTN"""
        bb_co_range = GTORange(Position.BB, "vs_co")
        
        # Reraise/all in hands
        reraise_all_in = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in reraise_all_in:
            bb_co_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Reraise/fold hands
        reraise_fold = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"]
        for hand in reraise_fold:
            bb_co_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Call hands (tighter than vs BTN)
        call_hands = ["ATs", "ATo", "A9s", "A8s", "A7s", "A6s", "A5s", "KJs", "KJo", "KTs", "K9s",
                     "QJs", "QJo", "QTs", "Q9s", "JTs", "JTo", "J9s", "T9s", "T8s", "98s", "87s",
                     "76s", "65s", "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in call_hands:
            bb_co_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts[Position.BB] = bb_co_range
    
    def _create_bb_vs_mp3_chart(self):
        """Create BB defense vs MP3 - tightest defense"""
        bb_mp3_range = GTORange(Position.BB, "vs_mp3")
        
        # Reraise/all in hands
        reraise_all_in = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in reraise_all_in:
            bb_mp3_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Reraise/fold hands  
        reraise_fold = ["AQs", "AQo", "AJs", "KQs", "TT"]
        for hand in reraise_fold:
            bb_mp3_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Call hands (tightest range)
        call_hands = ["AJo", "ATs", "ATo", "A9s", "A8s", "A7s", "A6s", "A5s", "KQo", "KJs", "KJo", 
                     "KTs", "QJs", "QJo", "QTs", "JTs", "JTo", "T9s", "98s", "87s", "76s",
                     "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in call_hands:
            bb_mp3_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts[Position.BB] = bb_mp3_range
    
    def get_gto_range(self, position: Position, scenario: str = "first_in") -> GTORange:
        """Get GTO range for a specific position"""
        return self.charts.get(position)
    
    def get_action_for_hand(self, position: Position, hand_notation: str, scenario: str = "first_in") -> Action:
        """Get recommended action for a specific hand in a position"""
        gto_range = self.get_gto_range(position, scenario)
        if gto_range:
            action = gto_range.get_action_for_hand(hand_notation)
            return action if action else Action.FOLD
        return Action.FOLD
    
    def get_all_positions(self) -> list[Position]:
        """Get all positions with GTO data"""
        return list(self.charts.keys())
