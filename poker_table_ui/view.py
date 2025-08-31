"""
Poker Table View
================

Streamlit-based UI component for poker table visualization.
Renders rectangular table with positions, cards, and betting information.
"""

import streamlit as st
import plotly.graph_objects as go
import math
from typing import Optional, Dict, List, Any
from .controller import PokerTableController
from .model import PokerTableModel, PlayerInfo, Card, TableStage


class PokerTableView:
    """
    Streamlit-based view component for poker table
    
    Features:
    - Rectangular table layout
    - Position-based player display
    - Community cards (Flop, Turn, River)
    - Betting information display
    - Responsive and interactive
    """
    
    def __init__(self, controller: PokerTableController):
        self.controller = controller
        self.model = controller.model
        
        # UI Configuration
        self.table_width = 800
        self.table_height = 400
        self.position_colors = {
            "UTG": "#FF6B6B",    # Red
            "MP": "#4ECDC4",     # Teal  
            "CO": "#45B7D1",     # Blue
            "BTN": "#96CEB4",    # Green
            "SB": "#FECA57",     # Yellow
            "BB": "#FF9FF3"      # Pink
        }
    
    def render(self, show_community_cards: bool = True, show_betting: bool = True, 
               table_title: str = "Poker Table") -> go.Figure:
        """
        Render the complete poker table
        
        Args:
            show_community_cards: Whether to show flop/turn/river
            show_betting: Whether to show betting information
            table_title: Title for the table
        """
        fig = go.Figure()
        
        # Draw table base
        self._draw_table_base(fig)
        
        # Draw player positions
        self._draw_player_positions(fig, show_betting)
        
        # Draw community cards if enabled
        if show_community_cards:
            self._draw_community_cards(fig)
        
        # Draw pot information
        if show_betting and self.model.pot_size > 0:
            self._draw_pot_info(fig)
        
        # Configure layout
        self._configure_layout(fig, table_title)
        
        return fig
    
    def _draw_table_base(self, fig: go.Figure):
        """Draw the rectangular table base"""
        # Outer table border (rectangular)
        table_x = [0, self.table_width, self.table_width, 0, 0]
        table_y = [0, 0, self.table_height, self.table_height, 0]
        
        fig.add_trace(go.Scatter(
            x=table_x, y=table_y,
            fill='toself',
            fillcolor='rgba(34, 139, 34, 0.3)',  # Green felt
            line=dict(color='rgba(139, 69, 19, 0.8)', width=4),  # Brown border
            mode='lines',
            showlegend=False,
            hoverinfo='none',
            name='Table'
        ))
        
        # Inner playing area
        margin = 40
        inner_x = [margin, self.table_width - margin, self.table_width - margin, margin, margin]
        inner_y = [margin, margin, self.table_height - margin, self.table_height - margin, margin]
        
        fig.add_trace(go.Scatter(
            x=inner_x, y=inner_y,
            fill='toself',
            fillcolor='rgba(34, 139, 34, 0.1)',
            line=dict(color='rgba(34, 139, 34, 0.4)', width=2),
            mode='lines',
            showlegend=False,
            hoverinfo='none',
            name='Playing Area'
        ))
    
    def _get_position_coordinates(self, position: str) -> tuple:
        """Get x, y coordinates for player position"""
        # Rectangular table positioning
        coords = {
            "UTG": (100, self.table_height - 100),   # Top left
            "MP": (300, self.table_height - 60),     # Top middle-left
            "CO": (500, self.table_height - 60),     # Top middle-right
            "BTN": (self.table_width - 100, self.table_height - 100),  # Top right
            "SB": (self.table_width - 100, 100),     # Bottom right
            "BB": (100, 100)                         # Bottom left
        }
        return coords.get(position, (400, 200))
    
    def _draw_player_positions(self, fig: go.Figure, show_betting: bool = True):
        """Draw all player positions with information"""
        for position in self.model.positions:
            player = self.model.get_player_by_position(position)
            if player and player.is_active:
                self._draw_player(fig, player, show_betting)
            else:
                self._draw_empty_seat(fig, position)
    
    def _draw_player(self, fig: go.Figure, player: PlayerInfo, show_betting: bool):
        """Draw individual player with information"""
        x, y = self._get_position_coordinates(player.position)
        
        # Player circle
        is_current = player.is_current_player
        circle_size = 35 if is_current else 25
        circle_color = self.position_colors.get(player.position, "#888888")
        border_color = "#FF0000" if is_current else "#FFFFFF"
        border_width = 4 if is_current else 2
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=circle_size,
                color=circle_color,
                line=dict(color=border_color, width=border_width)
            ),
            text=player.position,
            textposition="middle center",
            textfont=dict(
                size=12 if is_current else 10,
                color='white',
                family='Arial Black' if is_current else 'Arial'
            ),
            name=f"{player.name} ({player.position})",
            hovertemplate=f"<b>{player.name}</b><br>{player.position}<br>Stack: {player.stack:.0f}" +
                         (f"<br>Bet: {player.current_bet:.1f}" if show_betting and player.current_bet > 0 else "") +
                         "<extra></extra>",
            showlegend=False
        ))
        
        # Player name and stack
        name_text = f"<b>{player.name}</b><br>Stack: {player.stack:.0f}"
        fig.add_annotation(
            x=x, y=y - 45,
            text=name_text,
            showarrow=False,
            font=dict(size=10, color='white'),
            bgcolor='rgba(0, 0, 0, 0.7)',
            bordercolor='rgba(255, 255, 255, 0.3)',
            borderwidth=1
        )
        
        # Betting information
        if show_betting and player.current_bet > 0:
            bet_text = f"{player.current_bet:.1f}x"
            if player.last_action:
                bet_text = f"{player.last_action.value.upper()}<br>{bet_text}"
            
            fig.add_annotation(
                x=x + 40, y=y + 20,
                text=bet_text,
                showarrow=True,
                arrowhead=2,
                arrowcolor="#FFD700",
                font=dict(size=12, color='black', family='Arial Black'),
                bgcolor='rgba(255, 215, 0, 0.9)',
                bordercolor='black',
                borderwidth=2
            )
        
        # Current player indicator
        if is_current:
            fig.add_annotation(
                x=x, y=y + 50,
                text="<b>← YOUR TURN →</b>",
                showarrow=False,
                font=dict(size=14, color='#FF0000', family='Arial Black'),
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#FF0000',
                borderwidth=2
            )
    
    def _draw_empty_seat(self, fig: go.Figure, position: str):
        """Draw empty seat placeholder"""
        x, y = self._get_position_coordinates(position)
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=20,
                color='rgba(128, 128, 128, 0.3)',
                line=dict(color='rgba(128, 128, 128, 0.5)', width=1)
            ),
            text=position,
            textposition="middle center",
            textfont=dict(size=8, color='gray'),
            name=f"Empty ({position})",
            hovertemplate=f"Empty Seat<br>{position}<extra></extra>",
            showlegend=False
        ))
    
    def _draw_community_cards(self, fig: go.Figure):
        """Draw community cards in center of table"""
        center_x = self.table_width // 2
        center_y = self.table_height // 2
        
        # Get community cards
        cards = self.model.community_cards.get_all_cards()
        
        if not cards:
            # No cards yet - show placeholders for preflop
            self._draw_card_placeholders(fig, center_x, center_y)
            return
        
        # Draw actual cards
        card_width = 60
        card_spacing = 70
        start_x = center_x - (len(cards) * card_spacing) // 2
        
        for i, card in enumerate(cards):
            card_x = start_x + (i * card_spacing)
            self._draw_single_card(fig, card, card_x, center_y)
        
        # Stage label
        stage_text = f"<b>{self.controller.get_stage_display()}</b>"
        fig.add_annotation(
            x=center_x, y=center_y - 60,
            text=stage_text,
            showarrow=False,
            font=dict(size=16, color='white', family='Arial Black'),
            bgcolor='rgba(0, 0, 0, 0.8)',
            bordercolor='white',
            borderwidth=2
        )
    
    def _draw_card_placeholders(self, fig: go.Figure, center_x: int, center_y: int):
        """Draw card placeholders for preflop"""
        card_spacing = 70
        start_x = center_x - (3 * card_spacing) // 2
        
        for i in range(5):  # 5 community cards total
            card_x = start_x + (i * card_spacing)
            
            # Different styling for flop vs turn/river
            if i < 3:
                color = 'rgba(255, 255, 255, 0.1)'
                border = 'rgba(255, 255, 255, 0.3)'
                text = '?'
            else:
                color = 'rgba(200, 200, 200, 0.05)'
                border = 'rgba(200, 200, 200, 0.2)'
                text = ''
            
            fig.add_shape(
                type="rect",
                x0=card_x - 25, y0=center_y - 35,
                x1=card_x + 25, y1=center_y + 35,
                fillcolor=color,
                line=dict(color=border, width=2)
            )
            
            if text:
                fig.add_annotation(
                    x=card_x, y=center_y,
                    text=text,
                    showarrow=False,
                    font=dict(size=20, color='rgba(255, 255, 255, 0.3)')
                )
    
    def _draw_single_card(self, fig: go.Figure, card: Card, x: int, y: int):
        """Draw a single playing card"""
        # Card background
        fig.add_shape(
            type="rect",
            x0=x - 25, y0=y - 35,
            x1=x + 25, y1=y + 35,
            fillcolor='white',
            line=dict(color='black', width=2)
        )
        
        # Card text with suit emoji
        card_text = card.to_display()
        
        # Color based on suit
        text_color = 'red' if card.suit in ['H', 'D'] else 'black'
        
        fig.add_annotation(
            x=x, y=y,
            text=f"<b>{card_text}</b>",
            showarrow=False,
            font=dict(size=14, color=text_color, family='Arial Black')
        )
    
    def _draw_pot_info(self, fig: go.Figure):
        """Draw pot information"""
        center_x = self.table_width // 2
        pot_y = (self.table_height // 2) + 80
        
        pot_text = f"<b>POT: {self.model.pot_size:.1f}</b>"
        fig.add_annotation(
            x=center_x, y=pot_y,
            text=pot_text,
            showarrow=False,
            font=dict(size=18, color='#FFD700', family='Arial Black'),
            bgcolor='rgba(0, 0, 0, 0.8)',
            bordercolor='#FFD700',
            borderwidth=2
        )
    
    def _configure_layout(self, fig: go.Figure, title: str):
        """Configure the plot layout"""
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            xaxis=dict(
                range=[-50, self.table_width + 50],
                showgrid=False,
                showticklabels=False,
                zeroline=False
            ),
            yaxis=dict(
                range=[-50, self.table_height + 50],
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=1
            ),
            plot_bgcolor='rgba(25, 25, 25, 1)',      # Dark background
            paper_bgcolor='rgba(40, 40, 40, 1)',     # Dark paper
            height=600,
            margin=dict(l=20, r=20, t=60, b=20)
        )
    
    # Streamlit-specific render methods
    def render_training_table(self, current_position: str = None) -> go.Figure:
        """Render table for training mode"""
        title = "🎰 Poker Training Table"
        if current_position:
            title += f" - <span style='color: #FF0000;'>YOU ARE {current_position}</span>"
        
        return self.render(show_community_cards=True, show_betting=True, table_title=title)
    
    def render_range_table(self, focus_position: str) -> go.Figure:
        """Render table for range display"""
        title = f"📊 Range Display - Focus: {focus_position}"
        return self.render(show_community_cards=False, show_betting=False, table_title=title)
    
    def render_custom(self, show_cards: bool = True, show_bets: bool = True, 
                     title: str = "Poker Table") -> go.Figure:
        """Render with custom options"""
        return self.render(show_community_cards=show_cards, show_betting=show_bets, table_title=title)
    
    # Interactive Streamlit components
    def render_with_controls(self, key_suffix: str = ""):
        """Render table with interactive controls"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Main table display
            fig = self.render()
            st.plotly_chart(fig, use_container_width=True, key=f"table_{key_suffix}")
        
        with col2:
            # Control panel
            st.markdown("### 🎮 Table Controls")
            
            # Stage controls
            if st.button(f"🃏 New Hand", key=f"new_hand_{key_suffix}"):
                self.controller.start_new_hand()
                st.experimental_rerun()
            
            # Community card controls
            if self.controller.is_preflop():
                if st.button(f"🔥 Deal Flop", key=f"flop_{key_suffix}"):
                    # Example flop
                    from .model import Card
                    self.controller.set_flop(
                        Card("A", "H"), Card("K", "D"), Card("Q", "C")
                    )
                    st.experimental_rerun()
            elif self.model.current_stage.value == "flop":
                if st.button(f"🎯 Deal Turn", key=f"turn_{key_suffix}"):
                    from .model import Card
                    self.controller.set_turn(Card("J", "S"))
                    st.experimental_rerun()
            elif self.model.current_stage.value == "turn":
                if st.button(f"🎲 Deal River", key=f"river_{key_suffix}"):
                    from .model import Card
                    self.controller.set_river(Card("T", "H"))
                    st.experimental_rerun()
            
            # Current stage info
            st.info(f"**Stage**: {self.controller.get_stage_display()}")
            if self.model.pot_size > 0:
                st.info(f"**Pot**: {self.model.pot_size:.1f}")
            
            # Player info
            active_players = self.controller.get_active_players()
            if active_players:
                st.markdown("**Active Players:**")
                for player in active_players:
                    status = "🔴 ACTING" if player.is_current_player else ""
                    bet_info = f" (Bet: {player.current_bet:.1f})" if player.current_bet > 0 else ""
                    st.text(f"• {player.position}: {player.name}{bet_info} {status}")
    
    def render_simple(self) -> go.Figure:
        """Render simple table without extra features"""
        return self.render(show_community_cards=False, show_betting=False, table_title="Poker Table")


# Utility functions for easy integration
def create_training_table(hero_position: str, hero_name: str = "Hero") -> tuple:
    """Create a complete table setup for training"""
    model = PokerTableModel()
    controller = PokerTableController(model)
    view = PokerTableView(controller)
    
    # Setup training scenario
    controller.setup_training_scenario(hero_position, hero_name)
    
    return controller, view

def create_range_display_table(focus_position: str) -> tuple:
    """Create a table setup for range display"""
    model = PokerTableModel()
    controller = PokerTableController(model)
    view = PokerTableView(controller)
    
    # Setup range display scenario
    controller.setup_range_display_scenario(focus_position)
    
    return controller, view

def create_empty_table() -> tuple:
    """Create an empty table for manual setup"""
    model = PokerTableModel()
    controller = PokerTableController(model)
    view = PokerTableView(controller)
    
    return controller, view
