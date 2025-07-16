from lennakatten_pi.mock import MockDisplay
import pygame

BUTTON_HEIGHT = 40

class App:
    def __init__(self):
        self.disp = MockDisplay(
            button_callbacks=[
                self.button_1,
                self.button_2,
                self.button_3,
                self.button_4,
            ]
        )

    def button_1(self):
        print("Button 1 pressed")

    def button_2(self):
        print("Button 2 pressed")

    def button_3(self):
        print("Button 3 pressed")

    def button_4(self):
        print("Button 4 pressed")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    idx = self.disp.get_button_index(event.pos)
                    if idx is not None:
                        self.disp.button_callbacks[idx]()
                        self.disp.update()