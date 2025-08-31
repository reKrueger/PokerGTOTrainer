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

def create_poker_table_visual(current_position=None):
    """Create poker table that highlights current position clearly"""
    fig = go.Figure()
    
    # Draw the poker table (elliptical)
    theta = [i * 2 * math.pi / 100 for i in range(101)]
    table_x = [2.2 * math.cos(t) for t in theta]
    table_y = [1.2 * math.sin(t) for t in theta]
    
    # Add poker table
    fig.add_trace(go.Scatter(
        x=table_x, y=table_y,
        fill='toself',
        fillcolor='rgba(34, 139, 34, 0.4)',  # Darker green
        line=dict(color='rgba(34, 139, 34, 0.9)', width=5),
        mode='lines',
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Position data: [x, y, name, short_name]
    positions_data = [
        (0, 2.0, "Under The Gun", "UTG"),      # Top
        (2.0, 1.0, "Middle Position", "MP"),   # Top Right
        (2.0, -1.0, "Cut Off", "CO"),         # Bottom Right
        (0, -2.0, "Button", "BTN"),           # Bottom
        (-2.0, -1.0, "Small Blind", "SB"),    # Bottom Left
        (-2.0, 1.0, "Big Blind", "BB")        # Top Left
    ]
    
    # Add position markers with enhanced highlighting
    for x, y, full_name, short_name in positions_data:
        is_current = (current_position and current_position.upper() == short_name)
        
        if is_current:
            # Current position - large red circle with pulse effect
            circle_color = "#FF1122"
            circle_size = 35
            text_color = 'white'
            border_width = 4
            border_color = '#FF6666'
        else:
            # Other positions - smaller green circles
            circle_color = "#4CAF50"
            circle_size = 22
            text_color = 'white'
            border_width = 2
            border_color = '#66BB6A'
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=circle_size, 
                color=circle_color, 
                line=dict(color=border_color, width=border_width)
            ),
            text=short_name,
            textposition="middle center",
            textfont=dict(
                size=14 if is_current else 11, 
                color=text_color,
                family='Arial Black' if is_current else 'Arial'
            ),
            name=full_name,
            hovertemplate=f"<b>{full_name}</b><br>({short_name})" + 
                         ("<br><b>← YOU ARE HERE</b>" if is_current else "") + "<extra></extra>",
            showlegend=False
        ))
        
        # Add position labels outside circles
        if is_current:
            # Big red arrow pointing to your position
            fig.add_annotation(
                x=x, y=y + (0.8 if y > 0 else -0.8),
                text="<b>↓ YOU ↓</b>" if y > 0 else "<b>↑ YOU ↑</b>",
                showarrow=False,
                font=dict(size=16, color='#FF1122', family='Arial Black'),
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#FF1122',
                borderwidth=2
            )
    
    # Add dealer button if BTN is current position
    if current_position and current_position.upper() == "BTN":
        fig.add_trace(go.Scatter(
            x=[0.4], y=[-1.6],
            mode='markers+text',
            marker=dict(
                size=18,
                color='white',
                line=dict(color='black', width=3)
            ),
            text="DEALER",
            textposition="middle center",
            textfont=dict(size=8, color='black', family='Arial Black'),
            name="Dealer Button",
            showlegend=False,
            hovertemplate="Dealer Button<extra></extra>"
        ))
    
    # Add title in center with position info
    center_text = "<b>6-MAX<br>POKER TABLE</b>"
    if current_position:
        center_text += f"<br><span style='color: #FF1122; font-size: 14px;'>You: {current_position}</span>"
    
    fig.add_annotation(
        x=0, y=0,
        text=center_text,
        showarrow=False,
        font=dict(size=16, color='white'),
        bgcolor='rgba(34, 139, 34, 0.9)',
        bordercolor='rgba(255, 255, 255, 0.4)',
        borderwidth=2
    )
    
    # Layout with better sizing
    title_text = "🎰 Poker Table"
    if current_position:
        title_text += f" - <span style='color: #FF1122;'>YOU ARE {current_position}</span>"
    
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            range=[-3.2, 3.2], 
            showgrid=False, 
            showticklabels=False, 
            zeroline=False
        ),
        yaxis=dict(
            range=[-3.2, 3.2], 
            showgrid=False, 
            showticklabels=False, 
            zeroline=False, 
            scaleanchor="x", 
            scaleratio=1
        ),
        plot_bgcolor='rgba(240, 248, 255, 0.1)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def main():
    st.title("🎰 Poker GTO Trainer - Position Training Mode")
    st.markdown("**Jede neue Hand zeigt dir sofort deine Position am Tisch!**")
    
    if not POKER_AVAILABLE:
        st.error("❌ Poker modules not found!")
        return
    
    # Initialize
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = GTOAnalyzer()
    if 'score' not in st.session_state:
        st.session_state.score = {'correct': 0, 'total': 0}
    
    # Sidebar with prominent NEW HAND button
    st.sidebar.title("🎮 Training Controls")
    
    # Big prominent button
    if st.sidebar.button("🎲 NEUE HAND", key="new_hand", help="Generate new situation", type="primary"):
        generate_new_hand()
        st.rerun()  # Force immediate redraw
    
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
    1. Klicke 'NEUE HAND'
    2. Sieh deine rote Position
    3. Schaue deine Karten an
    4. Wähle deine Aktion
    5. Lerne aus GTO-Feedback
    """)
    
    # Main content
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
