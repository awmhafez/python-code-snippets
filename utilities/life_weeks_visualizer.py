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
        self.SCREEN_WIDTH = 900
        self.SCREEN_HEIGHT = 800  # Smaller window, content will scroll
        self.SPHERE_RADIUS = 4
        self.ITEM_MARGIN = 6
        self.ROW_SPACING = 8  # Extra space between rows/years
        self.WEEKS_PER_ROW = 52
        
        # Colors
        self.COLOR_BACKGROUND = (248, 248, 250)
        self.COLOR_TEXT = (60, 60, 60)
        self.COLOR_CURRENT_WEEK = (34, 197, 94)  # Green for current week
        self.COLOR_FUTURE_WEEK = (156, 163, 175)  # Light gray for future
        self.COLOR_PAST_WEEK = (75, 85, 99)  # Darker gray for past
        self.COLOR_YEAR_LINE = (209, 213, 219)  # Subtle gray lines
        self.COLOR_DECADE_LINE = (107, 114, 128)  # Darker for decades
        self.COLOR_HOVER_TEXT = (31, 41, 55)
        self.COLOR_HOVER_BG = (254, 249, 195)
        self.COLOR_AGE_LABEL = (107, 114, 128)
        
        # Calculate weeks
        self.total_weeks, self.current_week = self._calculate_weeks()
        self.start_date = datetime.datetime(self.birth_year, self.birth_month, self.birth_day)
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('A Life In Weeks')
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font('freesansbold.ttf', 14)
        
        # Mouse tracking
        self.mouse_pos = (0, 0)
        self.hovered_week = None
        
        # Scrolling
        self.scroll_y = 0
        self._calculate_max_scroll()
        
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
    
    def _calculate_max_scroll(self):
        """Calculate maximum scroll distance."""
        max_row = (self.total_weeks - 1) // self.WEEKS_PER_ROW
        content_height = (95 + 4 * self.ITEM_MARGIN + 
                         max_row * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS + self.ROW_SPACING) + 
                         4 * self.SPHERE_RADIUS)
        self.max_scroll = max(0, content_height - self.SCREEN_HEIGHT)
    
    def _get_grid_position(self, week_number: int) -> Tuple[int, int]:
        """Calculate x, y position for a given week number."""
        row = week_number // self.WEEKS_PER_ROW
        col = week_number % self.WEEKS_PER_ROW
        
        x = (2 * self.ITEM_MARGIN + 
             col * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS) + 
             2 * self.SPHERE_RADIUS)
        y = (95 + 2 * self.ITEM_MARGIN + 
             row * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS + self.ROW_SPACING) + 
             2 * self.SPHERE_RADIUS - self.scroll_y)
        
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
        """Draw the title and life progress summary with background."""
        # White background for header area
        header_height = 85
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.SCREEN_WIDTH, header_height))
        
        # Optional: Add subtle border at bottom of header
        pygame.draw.line(self.screen, (230, 230, 230), (0, header_height - 1), (self.SCREEN_WIDTH, header_height - 1), 1)
        
        # Main title
        font_title = pygame.font.Font('freesansbold.ttf', 28)
        title_text = font_title.render(self.name, True, self.COLOR_TEXT)
        title_rect = title_text.get_rect()
        title_rect.center = (self.SCREEN_WIDTH // 2, 40)
        self.screen.blit(title_text, title_rect)
        
        # Progress summary
        current_age = (datetime.datetime.now() - self.start_date).days / 365.25
        progress_pct = (self.current_week / self.total_weeks) * 100
        
        font_sub = pygame.font.Font('freesansbold.ttf', 14)
        summary_text = f"Age {current_age:.1f} • Week {self.current_week:,} of {self.total_weeks:,} • {progress_pct:.1f}% complete"
        summary_surface = font_sub.render(summary_text, True, self.COLOR_AGE_LABEL)
        summary_rect = summary_surface.get_rect()
        summary_rect.center = (self.SCREEN_WIDTH // 2, 65)
        self.screen.blit(summary_surface, summary_rect)
    
    def _get_week_date(self, week_number: int) -> datetime.datetime:
        """Get the date for a given week number."""
        start_monday = self.start_date - datetime.timedelta(days=self.start_date.weekday())
        week_date = start_monday + datetime.timedelta(weeks=week_number)
        return week_date
    
    def _get_hovered_week(self, mouse_pos: Tuple[int, int]) -> int:
        """Get the week number under the mouse cursor, or None if no week."""
        for week in range(min(self.total_weeks, self.WEEKS_PER_ROW * 100)):
            x, y = self._get_grid_position(week)
            # Only check weeks that are visible on screen
            if y < -self.SPHERE_RADIUS or y > self.SCREEN_HEIGHT + self.SPHERE_RADIUS:
                continue
            distance = math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2)
            if distance <= self.SPHERE_RADIUS + 2:
                return week
        return None
    
    def _draw_year_lines(self):
        """Draw horizontal lines to separate years and decades."""
        max_row = min((self.total_weeks - 1) // self.WEEKS_PER_ROW, 99)
        
        for year in range(1, self.target_age + 1):
            row = year - 1
            if row > max_row:
                break
                
            y_line = (95 + 2 * self.ITEM_MARGIN + 
                     row * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS + self.ROW_SPACING) + 
                     2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS // 2 + self.ROW_SPACING // 2 - self.scroll_y)
            
            x_start = 2 * self.ITEM_MARGIN
            x_end = (2 * self.ITEM_MARGIN + 
                    (self.WEEKS_PER_ROW - 1) * (2 * self.SPHERE_RADIUS + self.SPHERE_RADIUS) + 
                    2 * self.SPHERE_RADIUS)
            
            # Only draw lines that are visible on screen
            if y_line >= -10 and y_line <= self.SCREEN_HEIGHT + 10:
                # Different styling for decades vs years
                if year % 10 == 0:
                    # Decade lines - thicker and darker
                    pygame.draw.line(self.screen, self.COLOR_DECADE_LINE, (x_start - 5, y_line), (x_end + 30, y_line), 2)
                    # Decade label
                    font = pygame.font.Font('freesansbold.ttf', 14)
                    decade_text = font.render(f"Age {year}", True, self.COLOR_DECADE_LINE)
                    self.screen.blit(decade_text, (x_end + 35, y_line - 7))
                elif year % 5 == 0:
                    # 5-year marks
                    pygame.draw.line(self.screen, self.COLOR_YEAR_LINE, (x_start, y_line), (x_end + 15, y_line), 1)
                    font = pygame.font.Font('freesansbold.ttf', 10)
                    year_text = font.render(f"{year}", True, self.COLOR_AGE_LABEL)
                    self.screen.blit(year_text, (x_end + 20, y_line - 5))
                else:
                    # Regular year lines - very subtle
                    pygame.draw.line(self.screen, self.COLOR_YEAR_LINE, (x_start, y_line), (x_end, y_line), 1)
    
    def _draw_weeks(self):
        """Draw all week circles that are visible on screen."""
        for week in range(min(self.total_weeks, self.WEEKS_PER_ROW * 100)):
            x, y = self._get_grid_position(week)
            
            # Only draw circles that are visible on screen
            if y >= -self.SPHERE_RADIUS and y <= self.SCREEN_HEIGHT + self.SPHERE_RADIUS:
                color, width = self._get_week_color_and_width(week)
                pygame.draw.circle(self.screen, color, (x, y), self.SPHERE_RADIUS, width)
    
    def _draw_hover_info(self):
        """Draw date information for hovered week."""
        if self.hovered_week is not None:
            week_date = self._get_week_date(self.hovered_week)
            age_years = (week_date - self.start_date).days // 365.25
            
            date_str = week_date.strftime("%B %d, %Y")
            age_str = f"Age: {age_years:.1f} years"
            week_str = f"Week {self.hovered_week + 1} of {self.total_weeks}"
            
            texts = [date_str, age_str, week_str]
            text_surfaces = [self.font_small.render(text, True, self.COLOR_HOVER_TEXT) for text in texts]
            
            max_width = max(surface.get_width() for surface in text_surfaces)
            total_height = sum(surface.get_height() for surface in text_surfaces) + 10
            
            info_x = self.mouse_pos[0] + 15
            info_y = self.mouse_pos[1] - total_height - 10
            
            if info_x + max_width + 20 > self.SCREEN_WIDTH:
                info_x = self.mouse_pos[0] - max_width - 35
            if info_y < 0:
                info_y = self.mouse_pos[1] + 15
            
            pygame.draw.rect(self.screen, self.COLOR_HOVER_BG, 
                           (info_x - 10, info_y - 5, max_width + 20, total_height + 10))
            pygame.draw.rect(self.screen, self.COLOR_HOVER_TEXT, 
                           (info_x - 10, info_y - 5, max_width + 20, total_height + 10), 1)
            
            current_y = info_y
            for surface in text_surfaces:
                self.screen.blit(surface, (info_x, current_y))
                current_y += surface.get_height()
    
    def run(self):
        """Run the main application loop."""
        # Set window position (Windows-specific)
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = "2000,100"
        
        # Initial draw will happen in main loop
        
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.hovered_week = self._get_hovered_week(self.mouse_pos)
                elif event.type == pygame.MOUSEWHEEL:
                    # Scroll up/down with mouse wheel
                    scroll_speed = 30
                    self.scroll_y -= event.y * scroll_speed
                    self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
                elif event.type == pygame.KEYDOWN:
                    # Scroll with arrow keys
                    if event.key == pygame.K_UP:
                        self.scroll_y = max(0, self.scroll_y - 50)
                    elif event.key == pygame.K_DOWN:
                        self.scroll_y = min(self.max_scroll, self.scroll_y + 50)
                    elif event.key == pygame.K_HOME:
                        self.scroll_y = 0  # Go to top
                    elif event.key == pygame.K_END:
                        self.scroll_y = self.max_scroll  # Go to bottom
            
            # Redraw everything
            self.screen.fill(self.COLOR_BACKGROUND)
            self._draw_year_lines()
            self._draw_weeks()
            self._draw_hover_info()
            self._draw_title()  # Draw title last so it covers scrollable content
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Main function to run the life weeks visualizer."""
    # Configuration - update these values
    BIRTH_YEAR = 1991
    BIRTH_MONTH = 1
    BIRTH_DAY = 29
    TARGET_AGE = 88
    NAME = "A LIFE IN WEEKS"
    
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