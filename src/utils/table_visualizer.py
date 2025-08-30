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
    
    def create_compact_table(self, current_position=None, show_players=True):
        """Create a compact table representation with all 6-max positions"""
        if show_players:
            # 6 Spieler um den rechteckigen Tisch verteilt
            lines = [
                "                                           ",
                "                   Spieler1               ",
                "                    (UTG)                 ",
                "                      |                   ",
                "  Spieler6 __________|__________ Spieler2 ",
                "   (BB)   |                     | (MP)    ",
                "          |      POKER TABLE    |         ",
                "          |        6-MAX        |         ",
                "   (SB)   |_____________________|  (CO)   ",
                "  Spieler5           |           Spieler3 ",
                "                     |                    ",
                "                  Spieler4               ",
                "                   (BTN)                 ",
                "                                         "
            ]
        else:
            # Position-only layout - rechteckig
            lines = [
                "                                           ",
                "                     UTG                  ",
                "                      |                   ",
                "    BB    ____________|____________   MP  ",
                "          |                       |       ",
                "          |      POKER TABLE      |       ",
                "          |        6-MAX          |       ",
                "    SB    |_______________________|   CO  ",
                "                      |                   ",
                "                     BTN                  ",
                "                                         "
            ]
        
        # Highlight current position with brackets
        if current_position and show_players:
            highlighted_lines = []
            position_to_player = {
                Position.UTG: "Spieler1",
                Position.MP: "Spieler2", 
                Position.CO: "Spieler3",
                Position.BTN: "Spieler4",
                Position.SB: "Spieler5",
                Position.BB: "Spieler6"
            }
            
            player_name = position_to_player.get(current_position, "")
            for line in lines:
                new_line = line
                if player_name in line:
                    # Replace player with highlighted version
                    new_line = line.replace(player_name, f"[{player_name}]")
                highlighted_lines.append(new_line)
            return highlighted_lines
        elif current_position and not show_players:
            highlighted_lines = []
            for line in lines:
                new_line = line
                if current_position.short_name in line:
                    # Replace position with highlighted version
                    new_line = line.replace(current_position.short_name, f"[{current_position.short_name}]")
                highlighted_lines.append(new_line)
            return highlighted_lines
        
        return lines
    
    def display_compact_table(self, current_position=None, show_players=True):
        """Display compact table version with players or positions"""
        table_lines = self.create_compact_table(current_position, show_players)
        
        print()
        for line in table_lines:
            print(line)
        
        if current_position and show_players:
            position_to_player = {
                Position.UTG: "Spieler1",
                Position.MP: "Spieler2", 
                Position.CO: "Spieler3",
                Position.BTN: "Spieler4",
                Position.SB: "Spieler5",
                Position.BB: "Spieler6"
            }
            player_name = position_to_player.get(current_position, "Unbekannt")
            print(f">>> Du bist {player_name} auf {current_position.short_name} ({current_position.full_name}) <<<")
        elif current_position:
            print(f">>> Du sitzt auf {current_position.short_name} ({current_position.full_name}) <<<")
        print()
    
    def create_detailed_table(self, current_position=None, show_players=True):
        """Create detailed table with position info"""
        if show_players:
            lines = [
                "",
                "    POKER TISCH - 6 SPIELER (6-MAX)",
                "    " + "=" * 35,
                "",
                "                   Spieler1               ",
                "                    (UTG)                 ",
                "                      |                   ",
                "  Spieler6 __________|__________ Spieler2 ",
                "   (BB)   |                     | (MP)    ",
                "          |      POKER TABLE    |         ",
                "          |        6-MAX        |         ",
                "   (SB)   |_____________________|  (CO)   ",
                "  Spieler5           |           Spieler3 ",
                "                     |                    ",
                "                  Spieler4               ",
                "                   (BTN)                 ",
                "",
                "    Spielrichtung: Spieler1->2->3->4->5->6",
                ""
            ]
        else:
            lines = [
                "",
                "    POKER TISCH - ALLE 6 POSITIONEN (6-MAX)",
                "    " + "=" * 42,
                "",
                "                     UTG                  ",
                "                (Under The Gun)           ",
                "                      |                   ",
                "    BB    ____________|____________   MP  ",
                "(Big Blind)|                       |(Middle Pos)",
                "          |      POKER TABLE      |       ",
                "          |        6-MAX          |       ",
                "(Small Blind)|_______________________|  (Cut Off)",
                "    SB                |                CO ",
                "                     |                    ",
                "                    BTN                   ",
                "                (Button/Dealer)           ",
                "",
                "    Spielrichtung: UTG -> MP -> CO -> BTN -> SB -> BB",
                ""
            ]
        
        # Highlight current position
        if current_position and show_players:
            position_to_player = {
                Position.UTG: "Spieler1",
                Position.MP: "Spieler2", 
                Position.CO: "Spieler3",
                Position.BTN: "Spieler4",
                Position.SB: "Spieler5",
                Position.BB: "Spieler6"
            }
            player_name = position_to_player.get(current_position, "")
            highlighted_lines = []
            for line in lines:
                if player_name in line and not "(" in line and not "Spielrichtung" in line:
                    new_line = line.replace(player_name, f">>> {player_name} <<<")
                    highlighted_lines.append(new_line)
                else:
                    highlighted_lines.append(line)
            return highlighted_lines
        elif current_position and not show_players:
            pos_name = current_position.short_name
            highlighted_lines = []
            for line in lines:
                if pos_name in line and not "(" in line and not "Spielrichtung" in line:
                    new_line = line.replace(pos_name, f">>> {pos_name} <<<")
                    highlighted_lines.append(new_line)
                else:
                    highlighted_lines.append(line)
            return highlighted_lines
        
        return lines
    
    def display_detailed_table(self, current_position=None, show_players=True):
        """Display detailed table with descriptions"""
        table_lines = self.create_detailed_table(current_position, show_players)
        
        for line in table_lines:
            print(line)
        
        if current_position and show_players:
            position_to_player = {
                Position.UTG: "Spieler1",
                Position.MP: "Spieler2", 
                Position.CO: "Spieler3",
                Position.BTN: "Spieler4",
                Position.SB: "Spieler5",
                Position.BB: "Spieler6"
            }
            player_name = position_to_player.get(current_position, "Unbekannt")
            print(f"    *** DU BIST: {player_name} auf {current_position.short_name} ({current_position.full_name}) ***")
        elif current_position:
            print(f"    *** DEINE POSITION: {current_position.short_name} ({current_position.full_name}) ***")
        print()
    
    def show_all_players_info(self):
        """Show detailed info about all 6 players and their positions"""
        print("\n*** ALLE 6 SPIELER AM TISCH ***")
        print("=" * 40)
        
        players_info = [
            ("Spieler1", Position.UTG, "Under The Gun", "Erste Position - Sehr enge Range"),
            ("Spieler2", Position.MP, "Middle Position", "Mittlere Position - Medium Range"), 
            ("Spieler3", Position.CO, "Cut Off", "Spaete Position - Erweiterte Range"),
            ("Spieler4", Position.BTN, "Button/Dealer", "Beste Position - Weiteste Range"),
            ("Spieler5", Position.SB, "Small Blind", "Bereits investiert - Defensive Range"),
            ("Spieler6", Position.BB, "Big Blind", "Letzte Aktion preflop - Defense Range")
        ]
        
        for player, pos, full_name, description in players_info:
            print(f"{player} - {pos.short_name} ({full_name})")
            print(f"   {description}")
            print()
        
        print("=" * 40)
        print("Aktionsreihenfolge: Spieler1 -> Spieler2 -> Spieler3 -> Spieler4 -> Spieler5 -> Spieler6")
        print("Position wird staerker = Range wird weiter!")
        print()


def demo_table_visualization():
    """Demo the table visualization"""
    visualizer = PokerTableVisualizer()
    
    print("*** POKER TISCH VISUALISIERUNG - 6 SPIELER ***")
    print("*" * 45)
    
    # Show complete table with players
    print("\n1. Kompletter Tisch mit allen 6 Spielern:")
    visualizer.display_detailed_table(show_players=True)
    
    # Show all player info
    visualizer.show_all_players_info()
    
    # Show table with each position highlighted (as players)
    positions = [Position.UTG, Position.MP, Position.CO, Position.BTN, Position.SB, Position.BB]
    
    print("2. Einzelne Spieler hervorgehoben:")
    for i, pos in enumerate(positions, 1):
        position_to_player = {
            Position.UTG: "Spieler1",
            Position.MP: "Spieler2", 
            Position.CO: "Spieler3",
            Position.BTN: "Spieler4",
            Position.SB: "Spieler5",
            Position.BB: "Spieler6"
        }
        player_name = position_to_player.get(pos, "Unbekannt")
        print(f"\n--- {i}/6: {player_name} auf {pos.short_name} ({pos.full_name}) ---")
        visualizer.display_compact_table(pos, show_players=True)


if __name__ == "__main__":
    demo_table_visualization()
