import curses
from crew import Crew   
from travel_system import TravelSystem


class Ship:
    def __init__(self):
        self.layout = [
            "##############################",
            "#.                           #",
            "#    ####  ############      #",
            "#    #        #       #      #",
            "#    #        #       #      #",
            "#    ############  ####      #",
            "#.                           #",
            "##############################"
        ]
        self.distance_traveled = 0  
        self.speed = 0  
        self.max_speed = 10  
        self.evasion = 0  # Evasive maneuvers effect
        self.auto_repair = False  # Engineer auto-repair
        self.early_hazard_warning = False  # Radar Operator effect
        self.threat_assessment = False  # Radar Operator level 2 effect
        self.fuel = 50  # Initial fuel amount
        self.hull_integrity = 100  # Initial hull health
        self.current_location = "Starting Point"
        self.travel_system = TravelSystem(self)


        self.crew = Crew(self)  # Initialize crew


    def update(self):
        """Updates the ship's travel progress and engine heat."""
        self.distance_traveled += self.speed  # Increase distance based on speed

        # Apply role benefits
        self.apply_role_bonuses()
        self.crew.update()  # Update crew actions





    def display_status(self, stdscr, pos):
        """Displays ship status (fuel, hull, location)."""
        stdscr.addstr(pos,   2, "📊 Ship Status", curses.A_BOLD)
        stdscr.addstr(pos+1, 2, f"🔋 Fuel: {self.fuel}/100     🛠 Hull: {self.hull_integrity}/100")
        stdscr.addstr(pos+2, 2, f"📍 Location: {self.current_location}")

    def apply_role_bonuses(self):
        """Applies bonuses based on crew roles."""
        role_counts = self.crew.count_roles()

        # Pilot Effects
        if role_counts["Pilot"] >= 1:
            self.speed *= 1.15  # +15% speed
        if role_counts["Pilot"] >= 2:
            self.evasion = 10  # Enable evasive maneuvers

        # Engineer Effects
        if role_counts["Engineer"] >= 1:
            self.engine_heat = max(0, self.engine_heat - 5)  # Reduce heat
        if role_counts["Engineer"] >= 2:
            self.auto_repair = True  # Enable minor ship auto-repairs

        # Medic Effects
        if role_counts["Medic"] >= 1:
            self.crew_health_recovery = 2  # Faster healing
        if role_counts["Medic"] >= 2:
            self.crew_injury_reduction = 50  # Reduce injury severity

        # Radar Operator Effects
        if role_counts["Radar Operator"] >= 1:
            self.early_hazard_warning = True  # Detects hazards 1 turn earlier
        if role_counts["Radar Operator"] >= 2:
            self.threat_assessment = True  # Shows danger level

        # Researcher Effects
        if role_counts["Researcher"] >= 1:
            self.research_points += 1  # Generate research points
        if role_counts["Researcher"] >= 2:
            self.research_speed *= 1.5  # Faster research



    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()
        self.ship_y = height // 2 - len(self.layout) // 2
        self.ship_x = width // 2 - len(self.layout[0]) // 2

        for i, row in enumerate(self.layout):
            stdscr.addstr(self.ship_y + i, self.ship_x, row)



    def is_walkable(self, y, x):
        """Check if the position is walkable (empty space)"""
        return self.layout[y][x] == ' '  