"""
Poker Table UI Module
====================

MVC Architecture for Poker Table Display:
- Model: PokerTableModel (data structure)
- View: PokerTableView (UI component)
- Controller: PokerTableController (logic & state management)

Usage:
    from poker_table_ui import PokerTableController, PokerTableModel, PokerTableView
    
    # Create model
    table_model = PokerTableModel()
    
    # Create controller
    controller = PokerTableController(table_model)
    
    # Create view
    view = PokerTableView(controller)
    
    # Use in Streamlit
    view.render()
"""

from .model import PokerTableModel
from .view import PokerTableView
from .controller import PokerTableController

__all__ = ['PokerTableModel', 'PokerTableView', 'PokerTableController']
