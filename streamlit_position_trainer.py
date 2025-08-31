#!/usr/bin/env python3
"""
Optimized Streamlit App - Table redraws every hand to show your position
Perfect for position awareness training
"""

import streamlit as st
import sys
import os
import random
import plotly.graph_objects as go
import math

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import poker table UI components
try:
    from poker_table_ui import PokerTableController, PokerTableModel, PokerTableView
    TABLE_UI_AVAILABLE = True
except ImportError:
    TABLE_UI_AVAILABLE = False

# Try to import poker modules
try:
    from poker_gto.core import Card, Deck, Hand, Position, Rank, Suit
    from poker_gto.gto import GTOAnalyzer
    POKER_AVAILABLE = True
except ImportError:
    POKER_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="🎰 Poker GTO Trainer",
    page_icon="🎰",
    layout="wide"
)

def create_hand_range_table(position_str: str):
    """Create a poker hand range table for the given position"""
    if not POKER_AVAILABLE:
        st.error("❌ Poker modules not available!")
        return
    
    # Map position string to Position enum
    position_map = {
        "UTG": Position.UTG,
        "MP": Position.MP,
        "CO": Position.CO,
        "BTN": Position.BTN,
        "SB": Position.SB,
        "BB": Position.BB
    }
    
    position = position_map.get(position_str)
    if not position:
        st.error(f"❌ Unknown position: {position_str}")
        return
        
    analyzer = st.session_state.analyzer
    
    # Get range based on position
    if position_str in ["UTG", "MP", "CO", "BTN", "SB"]:
        scenario = "first_in"
    else:  # BB
        scenario = "vs_btn_sb"  # Default BB scenario
        
    # Special handling for position mappings
    if position_str == "MP":
        # The analyzer uses mp3_first_in, so we need to get that specifically
        chart_key = "mp3_first_in"
        gto_range = analyzer.chart_parser.charts.get(chart_key)
    elif position_str == "UTG":
        # UTG uses same range as MP2 (tighter)
        chart_key = "mp2_first_in"
        gto_range = analyzer.chart_parser.charts.get(chart_key)
    else:
        gto_range = analyzer._get_range_for_scenario(position, scenario)
    if not gto_range:
        st.warning(f"⚠️ No GTO data available for {position_str} in scenario {scenario}")
        return
    
    # Create 13x13 hand matrix (standard poker hand matrix)
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    
    # Create HTML table
    html_table = "<table style='border-collapse: collapse; width: 100%; font-family: monospace;'>"
    
    # Header row
    html_table += "<tr><th style='border: 1px solid #333; padding: 8px; background: #f0f0f0;'></th>"
    for rank in ranks:
        html_table += f"<th style='border: 1px solid #333; padding: 8px; background: #f0f0f0; text-align: center;'>{rank}</th>"
    html_table += "</tr>"
    
    # Data rows
    for i, rank1 in enumerate(ranks):
        html_table += f"<tr><th style='border: 1px solid #333; padding: 8px; background: #f0f0f0; text-align: center;'>{rank1}</th>"
        
        for j, rank2 in enumerate(ranks):
            if i < j:
                # Upper right: suited hands (e.g., AKs)
                hand = f"{rank1}{rank2}s"
            elif i > j:
                # Lower left: offsuit hands (e.g., AKo)
                hand = f"{rank2}{rank1}o"
            else:
                # Diagonal: pairs (e.g., AA)
                hand = f"{rank1}{rank1}"
            
            # Check if hand is in any action range and get color
            action_found = None
            for action, hand_range in gto_range.action_ranges.items():
                if hand_range.get_frequency(hand) > 0:
                    action_found = action
                    break
            
            # Color coding based on action
            if action_found:
                if "ALL_IN" in action_found.name:
                    color = "#FF4444"  # Red for premium hands
                    text_color = "white"
                elif "RERAISE" in action_found.name:
                    color = "#FF8844"  # Orange for reraise
                    text_color = "white"
                elif "RAISE" in action_found.name:
                    color = "#44AA44"  # Green for raise
                    text_color = "white"
                elif "CALL" in action_found.name:
                    color = "#4488FF"  # Blue for call
                    text_color = "white"
                else:
                    color = "#DDDDDD"  # Light gray for other actions
                    text_color = "black"
            else:
                color = "#FFFFFF"  # White for fold/not in range
                text_color = "black"
            
            cell_style = f"border: 1px solid #333; padding: 8px; text-align: center; background-color: {color}; color: {text_color}; font-weight: bold;"
            html_table += f"<td style='{cell_style}'>{hand}</td>"
        
        html_table += "</tr>"
    
    html_table += "</table>"
    
    return html_table, gto_range


def show_range_display():
    """Display the range table for selected position"""
    if 'show_range_for' not in st.session_state:
        return
        
    position = st.session_state.show_range_for
    st.markdown(f"## 📊 Starting Hand Ranges - {position}")
    
    # Show table with focus on selected position
    if TABLE_UI_AVAILABLE:
        model = PokerTableModel()
        controller = PokerTableController(model)
        view = PokerTableView(controller)
        
        controller.setup_range_display_scenario(position)
        fig = view.render_range_table(position)
        st.plotly_chart(fig, use_container_width=True, key=f"range_table_{position}")
        
        st.markdown("---")
    
    # Get scenario options for position
    if position in ["UTG", "MP", "CO", "BTN", "SB"]:
        scenarios = ["first_in"]
    else:  # BB
        scenarios = ["vs_btn_sb", "vs_co", "vs_mp3"]
    
    # Scenario selector for BB
    if position == "BB":
        selected_scenario = st.selectbox(
            "Scenario wählen:",
            scenarios,
            format_func=lambda x: {
                "vs_btn_sb": "vs Button/Small Blind",
                "vs_co": "vs Cut Off", 
                "vs_mp3": "vs Middle Position"
            }.get(x, x),
            key="bb_scenario"
        )
    else:
        selected_scenario = "first_in"
        st.info(f"**Scenario**: First in (Opening)")
    
    try:
        # Create position enum
        position_map = {
            "UTG": Position.UTG,
            "MP": Position.MP,
            "CO": Position.CO,
            "BTN": Position.BTN,
            "SB": Position.SB,
            "BB": Position.BB
        }
        
        pos_enum = position_map[position]
        analyzer = st.session_state.analyzer
        
        # Special handling for position mappings
        if position == "MP":
            chart_key = "mp3_first_in"
            gto_range = analyzer.chart_parser.charts.get(chart_key)
        elif position == "UTG":
            # UTG uses same range as MP2 (tighter)
            chart_key = "mp2_first_in" 
            gto_range = analyzer.chart_parser.charts.get(chart_key)
        else:
            gto_range = analyzer._get_range_for_scenario(pos_enum, selected_scenario)
        
        if not gto_range:
            st.error(f"❌ No range data found for {position} in scenario {selected_scenario}")
            return
        
        # Legend
        st.markdown("### 🎨 Legende:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="background-color: #FF4444; padding: 10px; text-align: center; color: white; font-weight: bold;">🔴 Premium (All-in)</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="background-color: #FF8844; padding: 10px; text-align: center; color: white; font-weight: bold;">🟠 Reraise</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="background-color: #44AA44; padding: 10px; text-align: center; color: white; font-weight: bold;">🟢 Raise</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="background-color: #4488FF; padding: 10px; text-align: center; color: white; font-weight: bold;">🔵 Call</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display the range table
        html_table, gto_range = create_hand_range_table(position)
        st.markdown(html_table, unsafe_allow_html=True)
        
        # Statistics
        st.markdown("### 📈 Range Statistiken:")
        total_hands_in_range = 0
        action_stats = {}
        
        for action, hand_range in gto_range.action_ranges.items():
            hand_count = len(hand_range.get_all_hands())
            action_stats[action.value] = hand_count
            total_hands_in_range += hand_count
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Gesamte Hände in Range", f"{total_hands_in_range}/169")
            st.metric("VPIP (%)", f"{(total_hands_in_range/169)*100:.1f}%")
        
        with col2:
            if action_stats:
                st.write("**Action Breakdown:**")
                for action, count in action_stats.items():
                    percentage = (count / 169) * 100
                    st.write(f"• {action}: {count} Hände ({percentage:.1f}%)")
        
    except Exception as e:
        st.error(f"❌ Error displaying range: {str(e)}")


def create_poker_table_visual(current_position=None):
    """Create poker table using new MVC architecture"""
    if not TABLE_UI_AVAILABLE:
        st.error("❌ Table UI components not available!")
        return None
    
    # Create table components
    model = PokerTableModel()
    controller = PokerTableController(model)
    view = PokerTableView(controller)
    
    if current_position:
        # Setup training scenario with hero position
        position_map = {
            "UTG": "UTG", "MP": "MP", "CO": "CO", 
            "BTN": "BTN", "SB": "SB", "BB": "BB"
        }
        hero_pos = position_map.get(current_position.upper(), "BTN")
        controller.setup_training_scenario(hero_pos, "Hero")
        
        # Render training table
        fig = view.render_training_table(hero_pos)
    else:
        # Empty table for start screen
        controller.setup_full_table()  # Show full table layout
        fig = view.render_simple()
    
    return fig

def main():
    st.title("🎰 Poker GTO Trainer - Position Training Mode")
    st.markdown("**Jede neue Hand zeigt dir sofort deine Position am Tisch!**")
    
    if not POKER_AVAILABLE:
        st.error("❌ Poker modules not found!")
        return
        
    if not TABLE_UI_AVAILABLE:
        st.error("❌ Table UI components not found!")
        return
    
    # Initialize
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = GTOAnalyzer()
    if 'score' not in st.session_state:
        st.session_state.score = {'correct': 0, 'total': 0}
    
    # Sidebar with prominent NEW HAND button
    st.sidebar.title("🎮 Training Controls")
    
    # Big prominent button
    if st.sidebar.button("🎲 FLOP TRAINING", key="new_hand", help="Generate new situation", type="primary"):
        generate_new_hand()
        st.rerun()  # Force immediate redraw
    
    st.sidebar.markdown("---")
    
    # Flop Ranges Section
    st.sidebar.markdown("### 📊 Flop Ranges")
    
    # Position selection for range display
    positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    position_names = {
        "UTG": "Under The Gun",
        "MP": "Middle Position", 
        "CO": "Cut Off",
        "BTN": "Button",
        "SB": "Small Blind",
        "BB": "Big Blind"
    }
    
    # Position selector
    selected_position = st.sidebar.selectbox(
        "Position wählen:",
        positions,
        key="range_position",
        help="Wähle eine Position um die Starting Hand Ranges zu sehen"
    )
    
    if selected_position:
        if st.sidebar.button(f"📋 Zeige {selected_position} Range", key="show_range"):
            st.session_state.show_range_for = selected_position
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Show score in sidebar
    score = st.session_state.score
    if score['total'] > 0:
        percentage = (score['correct'] / score['total']) * 100
        st.sidebar.metric("Erfolgsquote", f"{score['correct']}/{score['total']}", f"{percentage:.1f}%")
    else:
        st.sidebar.info("Klicke 'NEUE HAND' um zu starten!")
    
    # Reset button
    if st.sidebar.button("🔄 Score Zurücksetzen"):
        st.session_state.score = {'correct': 0, 'total': 0}
        st.sidebar.success("Score zurückgesetzt!")
        st.rerun()
    
    # Instructions
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **🎯 Anleitung:**
    1. Klicke 'FLOP TRAINING'
    2. Sieh deine rote Position
    3. Schaue deine Karten an
    4. Wähle deine Aktion
    5. Lerne aus GTO-Feedback
    
    **📊 Range Anzeige:**
    - Wähle Position aus Liste
    - Klicke 'Zeige Range'
    - Studiere die Starthände
    """)
    
    # Clear range display button
    if 'show_range_for' in st.session_state:
        if st.sidebar.button("❌ Range ausblenden", key="clear_range"):
            del st.session_state.show_range_for
            st.rerun()
        
        st.sidebar.info(f"📋 Zeige Range für: **{st.session_state.show_range_for}**")
    
    # Main content
    if 'show_range_for' in st.session_state:
        # Show range display
        show_range_display()
        st.markdown("---")
    
    if 'current_hand' in st.session_state:
        situation = st.session_state.current_hand
        current_pos = situation['position'].short_name
        
        # ALWAYS redraw table for current position - this is the key!
        st.markdown("### 🎯 Deine Position am Tisch:")
        fig = create_poker_table_visual(current_pos)
        st.plotly_chart(fig, use_container_width=True, key=f"table_{current_pos}_{hash(str(situation['hand']))}")
        
        # Position summary bar
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.error(f"**DEINE POSITION: {current_pos}**")
        with col2:
            ranges = {"UTG": "~12%", "MP": "~15%", "CO": "~25%", "BTN": "~45%", "BB": "Defend", "SB": "~35%"}
            st.info(f"**Typical Range**: {ranges.get(current_pos, 'N/A')}")
        with col3:
            types = {"UTG": "Early", "MP": "Middle", "CO": "Late", "BTN": "Best", "BB": "Defend", "SB": "Blind"}
            st.success(f"**Position**: {types.get(current_pos, 'Unknown')}")
        with col4:
            st.warning(f"**Full Name**: {situation['position'].full_name}")
        
        # Show current situation
        show_current_situation()
        
        # Two column layout for cards and actions
        col1, col2 = st.columns([1, 1])
        
        with col1:
            show_hand_details()
        
        with col2:
            show_action_buttons()
            
        # Show feedback if action was taken
        if 'last_action_feedback' in st.session_state:
            st.markdown("---")
            feedback = st.session_state.last_action_feedback
            if feedback['is_correct']:
                st.success(f"✅ **RICHTIG!** GTO empfiehlt: {feedback['gto_action']}")
            else:
                st.error(f"❌ **FALSCH!** GTO empfiehlt: {feedback['gto_action']}")
            
            st.info(f"**Erklärung**: {feedback['explanation']}")
            
            # Auto-clear feedback after showing
            if st.button("➡️ Nächste Hand", type="primary"):
                if 'last_action_feedback' in st.session_state:
                    del st.session_state.last_action_feedback
                generate_new_hand()
                st.rerun()
    
    else:
        # Show empty table as invitation
        fig = create_poker_table_visual()
        st.plotly_chart(fig, use_container_width=True)
        
        # Big call to action
        st.markdown("### 🎯 Bereit für GTO Training?")
        st.info("👆 **Klicke 'NEUE HAND' in der Sidebar um zu beginnen!**")
        
        # Feature overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🎰 Position Training**\nSiehe sofort wo du sitzt")
        with col2:
            st.markdown("**🃏 Visual Cards**\nSchöne Karten-Darstellung")
        with col3:
            st.markdown("**🧠 GTO Feedback**\nLerne die optimale Strategie")

def generate_new_hand():
    """Generate new random poker situation"""
    positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.BB, Position.SB]
    position = random.choice(positions)
    
    deck = Deck()
    cards = deck.deal_cards(2)
    hand = Hand(cards[0], cards[1])
    
    if position == Position.BB:
        scenarios = ["vs_btn_sb", "vs_co", "vs_mp3"]
        scenario = random.choice(scenarios)
    else:
        scenario = "first_in"
    
    analyzer = st.session_state.analyzer
    analysis = analyzer.analyze_preflop_hand(hand, position, scenario)
    
    st.session_state.current_hand = {
        'position': position,
        'hand': hand,
        'scenario': scenario,
        'analysis': analysis
    }
    
    # Clear any previous feedback
    if 'last_action_feedback' in st.session_state:
        del st.session_state.last_action_feedback

def show_current_situation():
    """Display current hand situation"""
    if 'current_hand' not in st.session_state:
        return
    
    situation = st.session_state.current_hand
    
    st.markdown("---")
    st.markdown("### 🎯 Aktuelle Situation")
    
    # Scenario description with better formatting
    scenario_desc = get_scenario_description(situation['position'], situation['scenario'])
    st.info(f"**Szenario**: {scenario_desc}")

def show_hand_details():
    """Show hand details with enhanced card visualization"""
    if 'current_hand' not in st.session_state:
        return
    
    situation = st.session_state.current_hand
    hand = situation['hand']
    card1, card2 = hand.get_cards()
    
    st.markdown("### 🃏 Deine Karten")
    
    # Enhanced card display with bigger cards
    col1, col2 = st.columns(2)
    
    with col1:
        suit_color = "red" if card1.suit.value in ["H", "D"] else "black"
        st.markdown(f"""
            <div style='
                text-align: center; 
                padding: 20px; 
                border: 3px solid #333; 
                border-radius: 15px; 
                background: white; 
                color: {suit_color}; 
                margin: 5px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                font-family: Arial Black;
            '>
                <h1 style='margin: 0; font-size: 2.5em;'>{card1.rank.symbol}{suit_to_emoji(card1.suit.value)}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        suit_color = "red" if card2.suit.value in ["H", "D"] else "black"
        st.markdown(f"""
            <div style='
                text-align: center; 
                padding: 20px; 
                border: 3px solid #333; 
                border-radius: 15px; 
                background: white; 
                color: {suit_color}; 
                margin: 5px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                font-family: Arial Black;
            '>
                <h1 style='margin: 0; font-size: 2.5em;'>{card2.rank.symbol}{suit_to_emoji(card2.suit.value)}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    # Hand notation prominently displayed
    st.markdown(f"<h3 style='text-align: center; color: #4CAF50;'>Hand: {hand.get_hand_notation()}</h3>", unsafe_allow_html=True)

def show_action_buttons():
    """Show large, prominent action buttons"""
    if 'current_hand' not in st.session_state:
        return
    
    st.markdown("### 🎮 Deine Aktion wählen")
    
    # Large buttons in 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛑 FOLD", key="fold", use_container_width=True, type="secondary"):
            process_action("fold")
        if st.button("📞 CALL", key="call", use_container_width=True, type="secondary"):
            process_action("call")
    
    with col2:
        if st.button("⬆️ RAISE", key="raise", use_container_width=True, type="secondary"):
            process_action("raise")
        if st.button("🚀 ALL-IN", key="allin", use_container_width=True, type="secondary"):
            process_action("all-in")

def process_action(user_action):
    """Process user action and store feedback"""
    situation = st.session_state.current_hand
    analysis = situation['analysis']
    gto_action = analysis['recommended_action']
    
    # Validation
    is_correct = validate_action(user_action, gto_action)
    
    # Update score
    st.session_state.score['total'] += 1
    if is_correct:
        st.session_state.score['correct'] += 1
    
    # Store feedback for display
    st.session_state.last_action_feedback = {
        'is_correct': is_correct,
        'user_action': user_action,
        'gto_action': gto_action,
        'explanation': analysis['explanation']
    }
    
    st.rerun()

def validate_action(user_action, gto_action):
    """Enhanced action validation"""
    action_map = {
        'fold': ['fold'],
        'call': ['call', 'call_ip'],
        'raise': ['raise', 'raise_fold', 'raise_call', 'raise_4_bet'],
        'all-in': ['all_in', 'all-in', 'reraise_all_in', 'raise_4_bet_all_in']
    }
    user_keywords = action_map.get(user_action, [])
    return any(keyword in gto_action.lower().replace('-', '_').replace('/', '_') for keyword in user_keywords)

def suit_to_emoji(suit):
    """Convert suit to emoji"""
    return {'H': '♥️', 'D': '♦️', 'C': '♣️', 'S': '♠️'}.get(suit, suit)

def get_scenario_description(position, scenario):
    """Get detailed scenario description"""
    descriptions = {
        "first_in": f"Noch niemand hat erhöht. Du bist {position.short_name} und bist als erster dran.",
        "vs_btn_sb": f"Button oder SB hat erhöht. Du bist {position.short_name} und musst entscheiden.",
        "vs_co": f"CO hat erhöht. Du bist {position.short_name} und stehst vor der Entscheidung.",
        "vs_mp3": f"MP hat erhöht. Du bist {position.short_name} und bist am Zug."
    }
    return descriptions.get(scenario, f"Du bist {position.short_name} und am Zug.")

if __name__ == "__main__":
    main()
