from datetime import datetime
from typing_extensions import Literal
import importlib.resources
import pygame

from PIL import Image, ImageDraw, ImageFont, ImageOps
from lennakatten_pi.utils import GrayLevel

ICON_SIZE = 32


class MockDisplay:
    def __init__(self, width=320, height=240):
        self.image = Image.new("RGB", (width, height), 0xFFFFFF)
        self.draw = ImageDraw.Draw(self.image)
        self.width = width
        self.height = height
        self.font = ImageFont.load_default()
        self.pygame_initialized = False
        self.pygame_screen = None
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self.pygame_screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("MockDisplay")
        self.pygame_initialized = True
        self._update_pygame()  # Show initial white image

    def _update_pygame(self):
        # Convert PIL image to pygame surface and display
        mode = self.image.mode
        size = self.image.size
        data = self.image.tobytes()
        surface = pygame.image.fromstring(data, size, mode)
        self.pygame_screen.blit(surface, (0, 0))  # type: ignore
        pygame.display.flip()

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

    def show(self):
        if self.pygame_initialized:
            self._update_pygame()
            # Handle window events to keep it responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        else:
            self.image.show()


class DrawableImage:
    def __init__(self, width=320, height=240):
        self.img = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.img)


if __name__ == "__main__":
    disp = MockDisplay()
    disp.draw_menu()
    disp.show()
