import time
from lennakatten_pi.mock import MockDisplay
import pygame


def main():
    disp = MockDisplay()
    disp.draw_menu()
    disp.show()
    time.sleep(1)
    disp.draw_menu(selected=1)
    disp.show()
    time.sleep(1)
    disp.draw_menu(selected=2)
    disp.show()
    time.sleep(0.2)
    disp.draw_menu(selected=1)
    disp.show()
    # Keep the pygame window open
    while True:
        for event in disp.pygame_screen and pygame.event.get() or []:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
