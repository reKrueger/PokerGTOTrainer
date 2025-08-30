#!/usr/bin/env python3
"""
Console Table Visualizer for Poker Positions
ASCII art representation of poker table
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import Position


class PokerTableVisualizer:
    """Creates ASCII representation of poker table with positions"""
    
    def create_compact_table(self, current_position=None):
        """Create a compact table representation with all 6-max positions"""
        # Enhanced table layout showing all 6 positions clearly
        lines = [
            "                                         ",
            "         BB                    UTG       ",
            "          \\                    /        ",
            "           \\                  /         ",
            "            \\________________/          ",
            "            |                |          ",
            "            |   POKER TABLE  |          ",
            "            |     6-MAX      |          ",
            "            |________________|          ",
            "           /                  \\         ",
            "          /                    \\        ",
            "        SB                     CO        ",
            "                                         ",
            "         BTN                   MP        ",
            "                                         "
        ]
        
        # Highlight current position with brackets
        if current_position:
            highlighted_lines = []
            for line in lines:
                new_line = line
                if current_position.short_name in line:
                    # Replace position with highlighted version
                    new_line = line.replace(current_position.short_name, f"[{current_position.short_name}]")
                highlighted_lines.append(new_line)
            return highlighted_lines
        
        return lines
    
    def display_compact_table(self, current_position=None):
        """Display compact table version"""
        table_lines = self.create_compact_table(current_position)
        
        print()
        for line in table_lines:
            print(line)
        
        if current_position:
            print(f">>> Du sitzt auf {current_position.short_name} ({current_position.full_name}) <<<")
        print()
    
    def create_detailed_table(self, current_position=None, show_all_info=True):
        """Create detailed table with position info"""
        lines = [
            "",
            "    POKER TISCH - ALLE 6 POSITIONEN (6-MAX)",
            "    " + "=" * 42,
            "",
            "         BB                    UTG",
            "       (Big Blind)        (Under Gun)", 
            "          \\                    /",
            "           \\                  /",
            "            \\________________/",
            "            |                |",
            "            |   POKER TABLE  |",
            "            |     6-MAX      |", 
            "            |                |",
            "            |________________|",
            "           /                  \\",
            "          /                    \\",
            "        SB                     CO",
            "    (Small Blind)        (Cut Off)",
            "",
            "         BTN                   MP",
            "       (Button/Dealer)  (Middle Pos)",
            "",
            "    Spielrichtung: UTG -> MP -> CO -> BTN -> SB -> BB",
            ""
        ]
        
        # Highlight current position
        if current_position:
            pos_name = current_position.short_name
            highlighted_lines = []
            for line in lines:
                if pos_name in line and not "(" in line and not "Spielrichtung" in line:  # Only highlight the short name line
                    new_line = line.replace(pos_name, f">>> {pos_name} <<<")
                    highlighted_lines.append(new_line)
                else:
                    highlighted_lines.append(line)
            return highlighted_lines
        
        return lines
    
    def display_detailed_table(self, current_position=None):
        """Display detailed table with descriptions"""
        table_lines = self.create_detailed_table(current_position)
        
        for line in table_lines:
            print(line)
        
        if current_position:
            print(f"    *** DEINE POSITION: {current_position.short_name} ({current_position.full_name}) ***")
            print()
    
    def show_all_positions_info(self):
        """Show detailed info about all 6 positions"""
        print("\n*** ALLE 6 POSITIONEN IM DETAIL ***")
        print("=" * 50)
        
        positions_info = [
            (Position.UTG, "Under The Gun", "Erste Position - Sehr enge Range"),
            (Position.MP, "Middle Position", "Mittlere Position - Medium Range"), 
            (Position.CO, "Cut Off", "Spaete Position - Erweiterte Range"),
            (Position.BTN, "Button/Dealer", "Beste Position - Weiteste Range"),
            (Position.SB, "Small Blind", "Bereits investiert - Defensive Range"),
            (Position.BB, "Big Blind", "Letzte Aktion preflop - Defense Range")
        ]
        
        for i, (pos, full_name, description) in enumerate(positions_info, 1):
            print(f"{i}. {pos.short_name} - {full_name}")
            print(f"   {description}")
            if i < len(positions_info):
                print()
        
        print("=" * 50)
        print("Aktionsreihenfolge: UTG -> MP -> CO -> BTN -> SB -> BB")
        print("Position wird staerker = Range wird weiter!")
        print()


def demo_table_visualization():
    """Demo the table visualization"""
    visualizer = PokerTableVisualizer()
    
    print("*** POKER TISCH VISUALISIERUNG - ALLE 6 POSITIONEN ***")
    print("*" * 55)
    
    # Show complete table overview
    print("\n1. Kompletter Tisch mit allen Positionen:")
    visualizer.display_detailed_table()
    
    # Show all position info
    visualizer.show_all_positions_info()
    
    # Show table with each position highlighted
    positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
    
    print("2. Einzelne Positionen hervorgehoben:")
    for i, pos in enumerate(positions, 1):
        print(f"\n--- {i}/6: {pos.short_name} ({pos.full_name}) ---")
        visualizer.display_compact_table(pos)


if __name__ == "__main__":
    demo_table_visualization()
