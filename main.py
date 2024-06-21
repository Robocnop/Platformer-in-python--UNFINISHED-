import pygame

pygame.init()
myVector = pygame.math.Vector2
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()
displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = myVector((10, 385))
        self.vel = myVector(0, 0)
        self.acc = myVector(0, 0)

        self.jumping = False

    def move(self):
        self.acc = myVector(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits and self.vel.y > 0:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0

            self.jumping = False

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits and not self.jumping:
            self.vel.y = -15
            self.jumping = True

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT-10))


PT1 = Platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
    displaySurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)
    P1.move()
    P1.update()
    pygame.display.update()
    FramePerSec.tick(FPS)