import os
import time
import sys
import threading
import json
from tkinter import Tk, Label, Button

class IncrementalGame:
    def __init__(self, save_file='save.data.json', suffix_file='suffixes.json'):
        self.save_file = save_file
        self.suffix_file = suffix_file
        self.resources = 0  # Total resources
        self.resources_per_click = 5  # Strong click power to start
        self.auto_resources_per_second = 0  # Resources gained automatically per second
        self.upgrade_cost_click = 10  # Cost to increase resources per click
        self.upgrade_cost_auto = 20  # Cost to increase auto resources per second
        self.milestone_multiplier = 2  # Factor to increase per milestone
        self.last_milestone_resources = 1  # Tracks resources at last milestone
        
        # Load suffixes for formatting large numbers
        self.suffixes = self.load_suffixes()

        # Try to load saved game data
        self.load_game()

        # Initialize Tkinter GUI
        self.root = Tk()
        self.root.title("Incremental Game")
        
        # Create UI components
        self.resource_label = Label(self.root, text="", font=("Arial", 14))
        self.resource_label.pack(pady=10)
        
        self.click_button = Button(self.root, text="Click for Resources", command=self.click)
        self.click_button.pack(pady=5)
        
        self.upgrade_click_button = Button(self.root, text="Upgrade Click Power", command=self.upgrade_click)
        self.upgrade_click_button.pack(pady=5)
        
        self.upgrade_auto_button = Button(self.root, text="Upgrade Auto Collection", command=self.upgrade_auto)
        self.upgrade_auto_button.pack(pady=5)
        
        self.save_button = Button(self.root, text="Save Game", command=self.save_game)
        self.save_button.pack(pady=5)
        
        # Setup the auto-collect mechanism
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.auto_collect()

    def load_suffixes(self):
        """Load suffixes from a JSON file."""
        if os.path.exists(self.suffix_file):
            with open(self.suffix_file, 'r') as f:
                data = json.load(f)
                return data.get("suffixes", [])
        else:
            print("Suffix file not found.")
            return []

    def format_number(self, num):
        """Format numbers for readability based on loaded suffixes."""
        for suffix in reversed(self.suffixes):
            if num >= suffix['value']:
                return f"{num / suffix['value']:.2f} {suffix['name']}"
        return str(num)

    def click(self):
        """Simulate a click to earn resources."""
        self.resources += self.resources_per_click
        self.check_milestone()
        self.update_display()

    def upgrade_click(self):
        """Upgrade resources per click exponentially if enough resources are available."""
        if self.resources >= self.upgrade_cost_click:
            self.resources -= self.upgrade_cost_click
            self.resources_per_click = round(self.resources_per_click * 2)
            self.upgrade_cost_click = round(self.upgrade_cost_click * 2)  # Exponential cost increase
        else:
            print("Not enough resources for click upgrade.")
        self.update_display()

    def upgrade_auto(self):
        """Upgrade auto-resource generation exponentially if enough resources are available."""
        if self.resources >= self.upgrade_cost_auto:
            self.resources -= self.upgrade_cost_auto
            self.auto_resources_per_second = max(1, round(self.auto_resources_per_second * 2))
            self.upgrade_cost_auto = round(self.upgrade_cost_auto * 2)  # Exponential cost increase
        else:
            print("Not enough resources for auto upgrade.")
        self.update_display()

    def auto_collect(self):
        """Collect resources automatically based on auto_resources_per_second."""
        self.resources += self.auto_resources_per_second
        self.check_milestone()
        self.update_display()
        self.root.after(1000, self.auto_collect)

    def check_milestone(self):
        """Check if a milestone is reached and apply rewards."""
        if self.resources >= self.last_milestone_resources * self.milestone_multiplier:
            self.resources_per_click = round(self.resources_per_click * 1.2)  # Slight boost to clicking
            self.auto_resources_per_second = round(self.auto_resources_per_second * 2)  # Strong boost to auto-collection
            self.last_milestone_resources = self.resources  # Update for next milestone
            print("\nMilestone reached! Auto resources doubled, click resources increased.")

    def update_display(self):
        """Update the displayed game status on the UI."""
        resources_formatted = self.format_number(self.resources)
        click_power_formatted = self.format_number(self.resources_per_click)
        auto_per_sec_formatted = self.format_number(self.auto_resources_per_second)
        click_upgrade_cost_formatted = self.format_number(self.upgrade_cost_click)
        auto_upgrade_cost_formatted = self.format_number(self.upgrade_cost_auto)

        self.resource_label.config(
            text=f"Resources: {resources_formatted}\n"
                 f"Click Power: {click_power_formatted}\n"
                 f"Auto/sec: {auto_per_sec_formatted}\n"
                 f"Click Upgrade Cost: {click_upgrade_cost_formatted}\n"
                 f"Auto Upgrade Cost: {auto_upgrade_cost_formatted}"
        )

    def save_game(self):
        """Save the game state to a file."""
        game_data = {
            'resources': self.resources,
            'resources_per_click': self.resources_per_click,
            'auto_resources_per_second': self.auto_resources_per_second,
            'upgrade_cost_click': self.upgrade_cost_click,
            'upgrade_cost_auto': self.upgrade_cost_auto,
            'last_milestone_resources': self.last_milestone_resources,
            'milestone_multiplier': self.milestone_multiplier
        }
        with open(self.save_file, 'w') as f:
            json.dump(game_data, f)
        print("Game saved.")

    def load_game(self):
        """Load the game state from a file."""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                game_data = json.load(f)
                self.resources = game_data.get('resources', 0)
                self.resources_per_click = game_data.get('resources_per_click', 5)
                self.auto_resources_per_second = game_data.get('auto_resources_per_second', 0)
                self.upgrade_cost_click = game_data.get('upgrade_cost_click', 10)
                self.upgrade_cost_auto = game_data.get('upgrade_cost_auto', 20)
                self.last_milestone_resources = game_data.get('last_milestone_resources', 1)
                self.milestone_multiplier = game_data.get('milestone_multiplier', 2)
            print("Game loaded.")
        else:
            print("No save file found. Starting a new game.")

    def on_closing(self):
        """Save the game and close the window."""
        self.save_game()
        self.root.destroy()

# Run the game
if __name__ == "__main__":
    game = IncrementalGame()
    game.root.mainloop()
