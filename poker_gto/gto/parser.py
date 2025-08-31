from typing import Dict
from ..core import Position
from .ranges import GTORange, Action


class GTOChartParser:
    """Parses GTO charts from the provided spreadsheet data"""
    
    def __init__(self):
        self.charts: Dict[str, GTORange] = {}
        self._initialize_charts()
    
    def _initialize_charts(self):
        """Initialize all GTO charts based on the provided data"""
        self._create_mp2_chart()
        self._create_mp3_chart() 
        self._create_co_chart()
        self._create_btn_sb_chart()
        self._create_bb_vs_sb_btn_chart()
        self._create_bb_vs_co_chart()
        self._create_bb_vs_mp3_chart()
    
    def _create_mp2_chart(self):
        """Create MP2 (Middle Position 2) opening range"""
        mp_range = GTORange(Position.MP, "first_in")
        
        # Premium hands - raise/4-bet/all in  
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "KQs", "TT"]
        for hand in strong_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "KJs", "QJs", "JTs", "99"]
        for hand in medium_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold
        weak_raise_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "KTs", "K9s", "QTs", "Q9s", 
                           "T9s", "98s", "88", "77", "66", "55"]
        for hand in weak_raise_hands:
            mp_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts["mp2_first_in"] = mp_range
    
    def _create_mp3_chart(self):
        """Create MP3 opening range - slightly wider"""
        mp3_range = GTORange(Position.MP, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"]
        for hand in strong_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "ATo", "KJs", "KJo", "QJs", "QJo", "JTs", "99"]
        for hand in medium_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold (wider than MP2)
        weak_raise_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                           "KTs", "K9s", "K8s", "QTs", "Q9s", "Q8s", "JTs", "J9s", "J8s",
                           "T9s", "T8s", "98s", "97s", "87s", "76s", "88", "77", "66", "55", "44"]
        for hand in weak_raise_hands:
            mp3_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts["mp3_first_in"] = mp3_range
    def _create_co_chart(self):
        """Create CO (Cut Off) opening range - wider than MP"""
        co_range = GTORange(Position.CO, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"]
        for hand in strong_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Medium hands - raise/call
        medium_hands = ["ATs", "ATo", "A9o", "KJs", "KJo", "KTo", "QJs", "QJo", "QTo", 
                       "JTs", "JTo", "T9o", "99"]
        for hand in medium_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Weaker raises - raise/fold
        weak_raise_hands = ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                           "A8o", "A7o", "A6o", "A5o", "KTs", "K9s", "K8s", "K7s", "K9o", "K8o",
                           "QTs", "Q9s", "Q8s", "Q7s", "Q9o", "Q8o", "JTs", "J9s", "J8s", "J7s",
                           "J9o", "J8o", "T9s", "T8s", "T7s", "T8o", "T7o", "98s", "97s", "96s",
                           "98o", "87s", "86s", "85s", "87o", "76s", "75s", "76o", "65s", "54s",
                           "88", "77", "66", "55", "44", "33", "22"]
        for hand in weak_raise_hands:
            co_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts["co_first_in"] = co_range
    
    def _create_btn_sb_chart(self):
        """Create BTN/SB opening range - widest range"""
        btn_range = GTORange(Position.BTN, "first_in")
        
        # Premium hands - raise/4-bet/all in
        premium_hands = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_4BET_ALL_IN)
        
        # Strong hands - raise/4-bet/fold
        strong_hands = ["AQs", "AQo", "AJs", "AJo", "KQs", "KQo", "TT"]
        for hand in strong_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_4BET_FOLD)
        
        # Most hands are raise/call on BTN (very wide)
        medium_hands = ["ATs", "ATo", "A9s", "A9o", "A8s", "A8o", "A7s", "A7o", "A6s", "A6o",
                       "A5s", "A5o", "A4s", "A4o", "A3s", "A3o", "A2s", "A2o",
                       "KJs", "KJo", "KTs", "KTo", "K9s", "K9o", "K8s", "K8o", "K7s", "K7o",
                       "K6s", "K6o", "K5s", "K5o", "K4s", "K4o", "K3s", "K3o", "K2s", "K2o",
                       "QJs", "QJo", "QTs", "QTo", "Q9s", "Q9o", "Q8s", "Q8o", "Q7s", "Q7o",
                       "JTs", "JTo", "J9s", "J9o", "J8s", "J8o", "J7s", "J7o",
                       "T9s", "T9o", "T8s", "T8o", "T7s", "T7o", "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in medium_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_CALL)
        
        # Rest are raise/fold (suited connectors etc)
        weak_raise_hands = ["98s", "98o", "97s", "97o", "96s", "96o", "87s", "87o", 
                           "86s", "86o", "76s", "76o", "75s", "75o", "65s", "65o", "54s", "54o"]
        for hand in weak_raise_hands:
            btn_range.add_hand_to_action(hand, Action.RAISE_FOLD)
        
        self.charts["btn_first_in"] = btn_range
        
        # SB uses same range as BTN for now
        sb_range = GTORange(Position.SB, "first_in")
        for action, hand_range in btn_range.action_ranges.items():
            sb_range.action_ranges[action] = hand_range
        self.charts["sb_first_in"] = sb_range
    
    def _create_bb_vs_sb_btn_chart(self):
        """Create BB vs SB/BTN defending range"""
        bb_range = GTORange(Position.BB, "vs_btn_sb")
        
        # Premium reraises - reraise/all in
        premium_reraise = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Strong reraises - reraise/fold  
        strong_reraise = ["AQs", "AQo", "AJs", "AJo", "KQs", "TT"]
        for hand in strong_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Wide calling range vs BTN/SB
        calling_hands = ["ATs", "ATo", "A9s", "A9o", "A8s", "A8o", "A7s", "A7o", "A6s", "A6o",
                        "A5s", "A5o", "A4s", "A4o", "A3s", "A3o", "A2s", "A2o",
                        "KJs", "KJo", "KTs", "KTo", "K9s", "K9o", "K8s", "K8o", "K7s", "K7o",
                        "QJs", "QJo", "QTs", "QTo", "Q9s", "Q9o", "Q8s", "Q8o", "Q7s", "Q7o",
                        "JTs", "JTo", "J9s", "J9o", "J8s", "J8o", "J7s", "J7o",
                        "T9s", "T9o", "T8s", "T8o", "T7s", "T7o", "98s", "98o", "97s", "97o",
                        "87s", "87o", "86s", "86o", "76s", "76o", "75s", "75o", "65s", "65o",
                        "54s", "54o", "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in calling_hands:
            bb_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts["bb_vs_btn_sb"] = bb_range
    
    def _create_bb_vs_co_chart(self):
        """Create BB vs CO defending range - tighter than vs BTN"""
        bb_range = GTORange(Position.BB, "vs_co")
        
        # Premium reraises - reraise/all in
        premium_reraise = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Strong reraises - reraise/fold
        strong_reraise = ["AQs", "AQo", "AJs", "AJo", "KQs", "TT"]
        for hand in strong_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Calling hands - call (tighter than vs BTN)
        calling_hands = ["ATs", "ATo", "A9s", "A9o", "A8s", "A8o", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                        "KJs", "KJo", "KTs", "KTo", "K9s", "K9o", "K8s", "K7s",
                        "QJs", "QJo", "QTs", "QTo", "Q9s", "Q9o", "Q8s", "Q7s",
                        "JTs", "JTo", "J9s", "J9o", "J8s", "J7s", "T9s", "T9o", "T8s", "T8o", "T7s",
                        "98s", "97s", "87s", "86s", "76s", "75s", "65s", "54s",
                        "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in calling_hands:
            bb_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts["bb_vs_co"] = bb_range
    
    def _create_bb_vs_mp3_chart(self):
        """Create BB vs MP3 defending range - tightest"""
        bb_range = GTORange(Position.BB, "vs_mp3")
        
        # Premium reraises - reraise/all in
        premium_reraise = ["AA", "KK", "QQ", "JJ", "AKs", "AKo"]
        for hand in premium_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_ALL_IN)
        
        # Strong reraises - reraise/fold
        strong_reraise = ["AQs", "AQo", "AJs", "AJo", "KQs", "TT"]
        for hand in strong_reraise:
            bb_range.add_hand_to_action(hand, Action.RERAISE_FOLD)
        
        # Calling hands - call (tightest defend range)
        calling_hands = ["ATs", "ATo", "A9s", "A9o", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                        "KJs", "KJo", "KTs", "K9s", "K8s", "QJs", "QJo", "QTs", "Q9s", "Q8s",
                        "JTs", "J9s", "J8s", "T9s", "T8s", "98s", "97s", "87s", "76s", "65s", "54s",
                        "99", "88", "77", "66", "55", "44", "33", "22"]
        for hand in calling_hands:
            bb_range.add_hand_to_action(hand, Action.CALL)
        
        self.charts["bb_vs_mp3"] = bb_range
    
    def get_gto_range(self, position: Position, scenario: str) -> GTORange:
        """Get GTO range for position and scenario"""
        key = f"{position.short_name.lower()}_{scenario}"
        return self.charts.get(key)
    
    def get_all_charts(self) -> Dict[str, GTORange]:
        """Get all available charts"""
        return self.charts
    
    def to_dict(self) -> dict:
        """Convert all charts to dictionary for JSON serialization"""
        return {
            chart_name: gto_range.to_dict()
            for chart_name, gto_range in self.charts.items()
        }
