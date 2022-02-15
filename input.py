import pygame


class InputStr(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, *groups):
        super(InputStr, self).__init__(*groups)
        self.rect = pygame.Rect(x, y, w, h)
        self.image = None
        self.text = ""
        self.text_out = self.text
        self.font = pygame.font.Font(None, 50)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.text_out = self.text
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        self.image = self.font.render(self.text, True, 'white')
        self.rect = self.image.get_rect()
