import pygame
import sys

from time import sleep

from bullet import Bullet
from alien import Alien


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Starts the game"""

    # Reset the game settings
    ai_settings.initialize_dynamic_settings()

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Resent the game statistics
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images
    sb.prep_images()

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create new fleet and center new ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Response to keypress"""

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_p and not stats.game_active:
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.key == pygame.K_q:
            sys.exit()


def check_keyup_events(event, ship):
    """Response to key releases"""

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Response to keypress and mouse events"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Returns a tuple of mouse cursor coordinates
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of alien that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)

    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create the alien and place it in a row"""
    safe = ai_settings.safe_rect()
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + safe.top
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create the full fleet of Aliens"""
    # Create and alien and place it in the row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create a fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and remove old bullets"""
    # Update bullet position.
    bullets.update()

    # Delete the bullets that reached the top of the screen
    for bullet in bullets.copy():
        if 0 >= bullet.rect.bottom:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collision"""
    # Remove bullets and aliens that have collided

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()

    start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    # Decrement ships_left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of alien and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center new ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Starts new level when all aliens have been destroyed"""

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any alien ship have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat it the same as if the ship got hit
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    Check if the fleet is at edge,
    and then update the positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for Alien-ship collisions
    if pygame.sprite.spritecollide(ship, aliens, True):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # Look for Aliens hitting the bottom of the screen
    check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()  # Draw the ship on the screen
    aliens.draw(screen)  # Draw the alien on the screen

    # Draw the score information
    sb.show_score()

    # Draw the button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make most recently draw screen visible.
    pygame.display.flip()
