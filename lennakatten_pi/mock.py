from datetime import datetime
from typing_extensions import Literal
from typing import Callable, List, Optional
import importlib.resources

from PIL import Image, ImageDraw, ImageFont, ImageOps
from lennakatten_pi.utils import GrayLevel
import pygame

ICON_SIZE = 32
BUTTON_HEIGHT = 40
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)


class MockDisplay:
    def __init__(
        self,
        width: int = 320,
        height: int = 240,
        button_callbacks: Optional[List[Callable[[], None]]] = None,
    ):
        self.image = Image.new("RGB", (width, height), 0xFFFFFF)
        self.draw = ImageDraw.Draw(self.image)
        self.width = width
        self.height = height
        self.font = ImageFont.load_default()
        self.pygame_initialized = False
        self.pygame_screen = None
        self.button_rects: List[pygame.Rect] = []
        if button_callbacks is None:
            button_callbacks = [lambda: None] * 4
        self.button_callbacks = button_callbacks
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self.pygame_screen = pygame.display.set_mode(
            (self.width, self.height + BUTTON_HEIGHT)
        )
        pygame.display.set_caption("MockDisplay")
        self.pygame_initialized = True
        self.update()  # Show initial white image

    def _draw_buttons(self):
        self.button_rects = []
        button_width = self.width // 4
        font = pygame.font.SysFont(None, 24)
        for i in range(4):
            x = i * button_width
            y = self.height
            rect = pygame.Rect(x, y, button_width, BUTTON_HEIGHT)
            self.button_rects.append(rect)
            pygame.draw.rect(self.pygame_screen, BUTTON_COLOR, rect)
            text = font.render(f"Button {i+1}", True, BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            self.pygame_screen.blit(text, text_rect)

    def update(self):
        # Convert PIL image to pygame surface and display
        mode = self.image.mode
        size = self.image.size
        data = self.image.tobytes()
        surface = pygame.image.fromstring(data, size, mode)
        self.pygame_screen.blit(surface, (0, 0))
        self._draw_buttons()
        pygame.display.flip()

    def get_button_index(self, pos):
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                return i
        return None

    def draw_menu(
        self,
        menu_name: Literal["main", "timetable_select"] = "main",
        selected: Literal[0, 1, 2, 3] = 0,
        menu_height=40,
    ):
        """Draw the bottom menu to the screen."""
        # Clear bottom part of screen
        self.draw.rectangle(
            (0, self.height - menu_height, self.width, self.height), fill="white"
        )

        # Vertical lines
        for x in range(0, self.width, self.width // 4):
            if x == 0:
                continue
            self.draw.line(
                (x, self.height - menu_height, x, self.height), fill=0x000000
            )

        # Horizontal line
        self.draw.line(
            (0, self.height - menu_height, self.width, self.height - menu_height),
            fill=0x000000,
        )

        midpoints = [2 * n * self.width // 8 + self.width // 8 for n in range(0, 4)]

        for i, midpoint in enumerate(midpoints):
            img_path = str(
                importlib.resources.files("lennakatten_pi").joinpath(
                    f"img/{menu_name}{i + 1}.png"
                )
            )
            if i == selected:
                self.draw.rectangle(
                    (
                        i * self.width // 4,
                        self.height - menu_height,
                        (i + 1) * self.width // 4,
                        self.height,
                    ),
                    fill="black",
                )
                icon = Image.open(img_path)
                icon = ImageOps.invert(icon)
            else:
                icon = Image.open(img_path)

            self.image.paste(
                icon, (midpoint - ICON_SIZE // 2, self.height - menu_height + 4)
            )

    def clear(self):
        """Clears the display to white."""
        self.image.paste(0xFFFFFF, (0, 0, self.width, self.height))


class DrawableImage:
    def __init__(self, width=320, height=240):
        self.img = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.img)


if __name__ == "__main__":
    def dummy_cb(): print("Button pressed")
    disp = MockDisplay(button_callbacks=[dummy_cb]*4)
    disp.draw_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                idx = disp.get_button_index(event.pos)
                if idx is not None:
                    disp.button_callbacks[idx]()
                    disp.update()
        self.img = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.img)


if __name__ == "__main__":
    disp = MockDisplay()
    disp.draw_menu()
    disp.show()
