
class StartWindowView:
    """
        Creates a Welcome page for game
    """
    def __init__(self, screen):
        self.screen = screen

    def text_objects(self,text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        pygame.font.init()
        myfont = pygame.font.Font('freesansbold.ttf', 30)
        mylargefont = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = self.text_objects('Welcome to Pro Pong', mylargefont)
        TextSurf1, TextRect1 = self.text_objects('Player1: (bottom) arrow keys', myfont)
        TextSurf2, TextRect2 = self.text_objects('Player2: (top) A move left, D move right', myfont)
        TextSurf3, TextRect3 = self.text_objects('Press Space Bar to Start', mylargefont)
        TextRect.center = ((640/2),(480/4))
        TextRect1.center = ((640/2),(480/2 - 30))
        TextRect2.center = ((640/2),(480/2 + 30))
        TextRect3.center = ((640/2),(480/4 * 3))
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf1, TextRect1)
        screen.blit(TextSurf2, TextRect2)
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()
