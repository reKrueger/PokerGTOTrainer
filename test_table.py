#!/usr/bin/env python3
"""
Test script to demonstrate the table visualization
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core import *
from utils.table_visualizer import PokerTableVisualizer


def test_table_visualization():
    """Test the table visualization"""
    visualizer = PokerTableVisualizer()
    
    print("*** TISCH VISUALISIERUNG TEST ***")
    print()
    
    # Test compact table with different positions
    positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
    
    for pos in positions:
        print(f"=== Position: {pos.short_name} ===")
        visualizer.display_compact_table(pos)
        print("Druecke ENTER fuer naechste Position...")
        input()
    
    print("=== Detailierte Tischinformationen ===")
    visualizer.display_detailed_table()
    
    print("*** Test abgeschlossen! ***")


if __name__ == "__main__":
    test_table_visualization()
