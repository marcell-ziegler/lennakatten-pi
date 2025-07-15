from lennakatten_pi.mock import MockDisplay


def main():
    disp = MockDisplay()
    disp.draw_menu()
    disp.show()
    disp.draw_menu(selected=1)
    disp.show()
