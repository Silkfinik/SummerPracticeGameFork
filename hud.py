import config
from config import font, current_health

def draw_hud(screen, heart_image):
    """
    Отрисовка HUD (индикаторы на экране).

    :param screen: Объект экрана Pygame.
    :param heart_image: Изображение сердца для отображения здоровья.
    """
    # Отображение счёта
    score_text = font.render(f"Score: {config.score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Отображение здоровья
    if current_health is not None:
        for i in range(current_health):
            screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 50))
