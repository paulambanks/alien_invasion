# Main file that creates a number of important objects throughout the game.

import pygame
from pygame.sprite import Group
from settings import Settings  # imports settings into the main program
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

from ship import Ship
import game_functions as gf


def run_game():
    """Initialize pygame, settings and screen object."""
    pygame.init()

    ai_settings = Settings()  # Settings are stored in ai_settings
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # Stores the display surface as a (Tuple)!
    pygame.display.set_caption("Alien Invasion")

    # Make a Play button
    play_button = Button(ai_settings, screen, "Play")

    # Create and instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)  # Creates the ship instance
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:  # Start the main loop for the game!

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
