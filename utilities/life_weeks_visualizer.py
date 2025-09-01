"""
A Life in Weeks Visualizer

A pygame-based application that visualizes a human life as a grid of weeks,
showing how many weeks have passed and how many remain until a target age.
Each dot represents one week of life.
"""

import math
import datetime
from typing import Tuple

import pygame


class LifeWeeksVisualizer:
    """Visualizes a life in weeks using pygame."""
    
    def __init__(self, birth_year: int, birth_month: int, birth_day: int, 
                 target_age: int = 82, name: str = "A LIFE IN WEEKS"):
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.target_age = target_age
        self.name = name
        
        # Display constants
        self.SCREEN_WIDTH = 810
        self.SCREEN_HEIGHT = 1345
        self.SPHERE_RADIUS = 5
        self.ITEM_MARGIN = 5
        self.WEEKS_PER_ROW = 52
        
        # Colors
        self.COLOR_BACKGROUND = (255, 255, 255)
        self.COLOR_TEXT = (100, 100, 100)
        self.COLOR_CURRENT_WEEK = (8, 143, 143)
        self.COLOR_FUTURE_WEEK = (100, 100, 100)
        self.COLOR_PAST_WEEK = (100, 100, 100)
        
        # Calculate weeks
        self.total_weeks, self.current_week = self._calculate_weeks()
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('A Life In Weeks')
        self.clock = pygame.time.Clock()
        
    def _calculate_weeks(self) -> Tuple[int, int]:
        """Calculate total weeks and current week number."""
        start_date = datetime.datetime(self.birth_year, self.birth_month, self.birth_day)
        end_date = start_date + datetime.timedelta(weeks=52 * self.target_age)
        today = datetime.datetime.now()
        
        # Get Monday of each week for consistent calculations
        start_monday = start_date - datetime.timedelta(days=start_date.weekday())
        end_monday = end_date - datetime.timedelta(days=end_date.weekday())
        today_monday = today - datetime.timedelta(days=today.weekday())
        
        total_weeks = int((end_monday - start_monday).days / 7)
        current_week = int((today_monday - start_monday).days / 7)
        
        return total_weeks, current_week
    
    def _get_grid_position(self, week_number: int) -> Tuple[int, int]:
        """Calculate x, y position for a given week number."""
        row = week_number // self.WEEKS_PER_ROW
        col = week_number % self.WEEKS_PER_ROW
        
        x = (2 * self.ITEM_MARGIN + 
             col * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS) + 
             2 * self.SPHERE_RADIUS)
        y = (85 + 2 * self.ITEM_MARGIN + 
             row * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS) + 
             2 * self.SPHERE_RADIUS)
        
        return x, y
    
    def _get_week_color_and_width(self, week_number: int) -> Tuple[Tuple[int, int, int], int]:
        """Determine color and line width for a given week."""
        if week_number + 1 == self.current_week:
            return self.COLOR_CURRENT_WEEK, 0
        elif week_number >= self.current_week:
            return self.COLOR_FUTURE_WEEK, 1
        else:
            return self.COLOR_PAST_WEEK, 0
    
    def _draw_title(self):
        """Draw the title text."""
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render(self.name, True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (self.SCREEN_WIDTH // 2, 50)
        self.screen.blit(text, text_rect)
    
    def _draw_weeks(self):
        """Draw all week circles."""
        for week in range(min(self.total_weeks, self.WEEKS_PER_ROW * 100)):
            x, y = self._get_grid_position(week)
            color, width = self._get_week_color_and_width(week)
            
            pygame.draw.circle(self.screen, color, (x, y), self.SPHERE_RADIUS, width)
    
    def run(self):
        """Run the main application loop."""
        # Set window position (Windows-specific)
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = "2000,100"
        
        # Initial draw
        self.screen.fill(self.COLOR_BACKGROUND)
        self._draw_title()
        self._draw_weeks()
        pygame.display.flip()
        
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Main function to run the life weeks visualizer."""
    # Configuration - update these values
    BIRTH_YEAR = 1991
    BIRTH_MONTH = 1
    BIRTH_DAY = 29
    TARGET_AGE = 82
    NAME = "ADAM HAFEZ - A LIFE IN WEEKS"
    
    visualizer = LifeWeeksVisualizer(
        birth_year=BIRTH_YEAR,
        birth_month=BIRTH_MONTH,
        birth_day=BIRTH_DAY,
        target_age=TARGET_AGE,
        name=NAME
    )
    
    print(f"Total weeks in {TARGET_AGE} years: {visualizer.total_weeks}")
    print(f"Current week: {visualizer.current_week}")
    
    visualizer.run()


if __name__ == '__main__':
    main()