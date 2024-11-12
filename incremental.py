import os
import time
import sys
import threading
import json

class IncrementalGame:
    def __init__(self, save_file='save.data.json'):
        self.save_file = save_file
        self.resources = 0  # Total resources
        self.resources_per_click = 5  # Strong click power to start
        self.auto_resources_per_second = 0  # Resources gained automatically per second
        self.upgrade_cost_click = 10  # Cost to increase resources per click
        self.upgrade_cost_auto = 20  # Cost to increase auto resources per second
        self.milestone_multiplier = 2  # Factor to increase per milestone
        self.last_milestone_resources = 1  # Tracks resources at last milestone
        
        # Try to load saved game data
        self.load_game()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def click(self):
        """Simulate a click to earn resources."""
        self.resources += self.resources_per_click
        self.check_milestone()
        self.display_status()

    def upgrade_click(self):
        """Upgrade resources per click exponentially if enough resources are available."""
        if self.resources >= self.upgrade_cost_click:
            self.resources -= self.upgrade_cost_click
            self.resources_per_click = round(self.resources_per_click * 2)
            self.upgrade_cost_click = round(self.upgrade_cost_click * 2)  # Exponential cost increase
        else:
            print("Not enough resources for click upgrade.")

    def upgrade_auto(self):
        """Upgrade auto-resource generation exponentially if enough resources are available."""
        if self.resources >= self.upgrade_cost_auto:
            self.resources -= self.upgrade_cost_auto
            self.auto_resources_per_second = max(1, round(self.auto_resources_per_second * 2))
            self.upgrade_cost_auto = round(self.upgrade_cost_auto * 2)  # Exponential cost increase
        else:
            print("Not enough resources for auto upgrade.")

    def auto_collect(self):
        """Collect resources automatically based on auto_resources_per_second."""
        while True:
            time.sleep(1)
            self.resources += self.auto_resources_per_second
            self.check_milestone()
            self.display_status()

    def display_status(self):
        """Clear screen and display the current game status."""
        self.clear_screen()
        
        # Format large numbers for readability
        resources_formatted = self.format_number(self.resources)
        click_power_formatted = self.format_number(self.resources_per_click)
        auto_per_sec_formatted = self.format_number(self.auto_resources_per_second)
        click_upgrade_cost_formatted = self.format_number(self.upgrade_cost_click)
        auto_upgrade_cost_formatted = self.format_number(self.upgrade_cost_auto)

        sys.stdout.write(f"Resources: {resources_formatted} | Click Power: {click_power_formatted} "
                         f"| Auto/sec: {auto_per_sec_formatted} | Click Upgrade Cost: {click_upgrade_cost_formatted} "
                         f"| Auto Upgrade Cost: {auto_upgrade_cost_formatted}\n")
        sys.stdout.flush()
        
        print("\nChoose an action:")
        print("1: Click for resources")
        print("2: Upgrade click power")
        print("3: Upgrade auto-collection")
        print("q: Quit")

    def check_milestone(self):
        """Check if a milestone is reached and apply resource doubling."""
        if self.resources >= self.last_milestone_resources * self.milestone_multiplier:
            self.resources_per_click = round(self.resources_per_click * 1.2)  # Slight boost to clicking
            self.auto_resources_per_second = round(self.auto_resources_per_second * 2)  # Strong boost to auto-collection
            self.last_milestone_resources = self.resources  # Update for next milestone
            sys.stdout.write("\nMilestone reached! Auto resources doubled, click resources increased.\n")
            sys.stdout.flush()

    def format_number(self, num):
        """Format numbers for readability (e.g., 1.02 thousand, 1.02 million, 10 billion, etc.)."""
        suffixes = [
            (1e3, "thousand"),
            (1e6, "million"),
            (1e9, "billion"),
            (1e12, "trillion"),
            (1e15, "quadrillion"),
            (1e18, "quintillion"),
            (1e21, "sextillion"),
            (1e24, "septillion"),
            (1e27, "octillion"),
            (1e30, "nonillion"),
            (1e33, "decillion"),
            (1e36, "undecillion"),
            (1e39, "duodecillion"),
            (1e42, "tredecillion"),
            (1e45, "quattuordecillion"),
            (1e48, "quindecillion"),
            (1e51, "sexdecillion"),
            (1e54, "septendecillion"),
            (1e57, "octodecillion"),
            (1e60, "novemdecillion"),
            (1e63, "vigintillion"),
            (1e66, "unvigintillion"),
            (1e69, "duovigintillion"),
            (1e72, "trevigintillion"),
            (1e75, "quattuorvigintillion"),
            (1e78, "quinvigintillion"),
            (1e81, "sexvigintillion"),
            (1e84, "septenvigintillion"),
            (1e87, "octovigintillion"),
            (1e90, "novemvigintillion"),
            (1e93, "trigintillion"),
            (1e96, "untrigintillion"),
            (1e99, "duotrigintillion"),
            (1e102, "tretrigintillion"),
            (1e105, "quattuortrigintillion"),
            (1e108, "quintrigintillion"),
            (1e111, "sextrigintillion"),
            (1e114, "septentrigintillion"),
            (1e117, "octotrigintillion"),
            (1e120, "novemtrigintillion"),
            (1e123, "quadragintillion"),
            (1e126, "unquadragintillion"),
            (1e129, "duoquadragintillion"),
            (1e132, "trequadragintillion"),
            (1e135, "quattuorquadragintillion"),
            (1e138, "quinquadragintillion"),
            (1e141, "sexquadragintillion"),
            (1e144, "septenquadragintillion"),
            (1e147, "octoquadragintillion"),
            (1e150, "novemquadragintillion"),
            (1e153, "quinquagintillion"),
            (1e156, "unquinquagintillion"),
            (1e159, "duoquinquagintillion"),
            (1e162, "trequinquagintillion"),
            (1e165, "quattuorquinquagintillion"),
            (1e168, "quinquinquagintillion"),
            (1e171, "sexquinquagintillion"),
            (1e174, "septenquinquagintillion"),
            (1e177, "octoquinquagintillion"),
            (1e180, "novemquinquagintillion"),
            (1e183, "sexdecillion"),
            (1e186, "Beyond")  #Adjust as needed
        ]

        for threshold, suffix in reversed(suffixes):
            if num >= threshold:
                return f"{num / threshold:.2f} {suffix}"

        return str(num)  # For numbers smaller than the lowest threshold (less than 1000)
    
    def save_game(self):
        """Save the game state to a file."""
        game_data = {
            'resources': self.resources,
            'resources_per_click': self.resources_per_click,
            'auto_resources_per_second': self.auto_resources_per_second,
            'upgrade_cost_click': self.upgrade_cost_click,
            'upgrade_cost_auto': self.upgrade_cost_auto,
            'last_milestone_resources': self.last_milestone_resources
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
            print("Game loaded.")
        else:
            print("No save file found. Starting a new game.")

# Initialize game
game = IncrementalGame()

# Start auto collection in a separate thread
auto_thread = threading.Thread(target=game.auto_collect)
auto_thread.daemon = True
auto_thread.start()

# Main game loop
while True:
    game.display_status()
    action = input("Action: ")
    
    if action == '1':
        game.click()
    elif action == '2':
        game.upgrade_click()
    elif action == '3':
        game.upgrade_auto()
    elif action.lower() == 'q':
        game.save_game()
        print("Thanks for playing!")
        break
    else:
        print("Invalid action.")
