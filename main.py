import sys

import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((720, 720))
        self.display = pygame.Surface((320, 320))

        self.player_img = pygame.image.load(
            "./assets/images/entities/player.png"
        ).convert()

        self.player_img.set_colorkey((0, 0, 0))
        self.player_pos = pygame.Vector2(100, 100)

        self.movement = [False, False]

    def run(self) -> None:
        clock = pygame.time.Clock()

        while True:
            self.player_pos.x += self.movement[1] - self.movement[0]
            self.display.fill((100, 100, 200))
            self.display.blit(self.player_img, self.player_pos)

            self.handleEvents()
            self.updateScreen()

            clock.tick(60)

    def handleEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_a:
                    self.movement[0] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_a:
                    self.movement[0] = False

    def updateScreen(self) -> None:
        self.screen.blit(
            pygame.transform.scale(
                self.display, (self.screen.get_width(), self.screen.get_height())
            ),
            (0, 0),
        )
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
