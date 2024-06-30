from config import font, screen_width, screen_height

def draw_menu(screen):
    menu_text = font.render("Menu", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2, screen_height // 2 - menu_text.get_height() // 2 - 40))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 - quit_text.get_height() // 2))
