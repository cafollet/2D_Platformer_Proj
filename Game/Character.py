import os
import pygame


def string_sort(string_to_sort):
    return int(string_to_sort[-8:-4])


class Character:
    """
    Character object for pygame
    """
    def __init__(self, x, y, vx=0, vy=0, ax=0, ay=0, img_path=""):
        """
        Construct a character
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.img_path = img_path
        self.images = []
        self.sprite = pygame.sprite.Sprite()
        self.frame = 0


    def step(self, dt):
        """
        update all values
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def create(self):
        self.images = []
        # If file path is a folder (Aka Animated)
        if os.path.isdir(self.img_path):
            img_list = sorted([x for x in os.listdir(self.img_path) if x[0] != "."], key=string_sort)
            for x in img_list:
                image = pygame.image.load(self.img_path + '/' + x)
                self.images.append(image)
        else:
            image = pygame.image.load(self.img_path)
            self.images.append(image)

    def draw(self, screen):
        if self.img_path == "":
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 1)
        else:
            f_index = self.frame // 8
            if f_index > len(self.images) - 1:
                self.frame = 0
                f_index = 0
            frame_image = self.images[f_index]
            flipped_image = pygame.transform.flip(frame_image, True, False)
            if self.vx < 0:
                self.sprite.image = flipped_image
            elif self.vx > 0:
                self.sprite.image = frame_image
            else:
                # MUST BE FIXED TO BE WHATEVER IMAGE WAS LAST USED
                self.sprite.image = frame_image
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.center = [self.x, -self.y]
            group = pygame.sprite.Group(self.sprite)
            group.draw(screen)
            self.frame += 1

if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 400
    screen = pygame.display.set_mode([screen_width, screen_height])
    clock = pygame.time.Clock()

    floor_y = -screen_height / 2

    character = Character(screen_width / 2, -screen_height / 2, 0, 0, 0, 0, "Cowboy.png")
    rate = 5
    l_key, r_key = (False, False)
    while True:
        jump = False
        print(character.y)
        if character.y > floor_y:
            character.ay = -981
        elif character.y <= floor_y:
            character.ay = 0
            character.vy = 0
            character.y = floor_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    l_key = False
                if event.key == pygame.K_RIGHT:
                    r_key = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    l_key = True
                if event.key == pygame.K_RIGHT:
                    r_key = True
                if event.key == pygame.K_SPACE:
                    jump = True

        if jump:
            character.vy = 200

        if character.vy == 0:
            if (l_key and r_key) or (not l_key and not r_key):
                character.vx = 0
                character.img_path = "Idle"
            elif l_key:
                character.vx = -100
                character.img_path = "Walking"
            elif r_key:
                character.vx = 100
                character.img_path = "Walking"
        elif character.vy < 0:
            # Falling
            character.img_path = "Jump/"
            if character.vy > -5:  # Small range
                character.img_path += "Fall 1"
            elif character.vy > -10: # Medium range
                character.img_path += "Fall 2"
            else: # Anything Higher
                character.img_path += "Fall Max"

        elif character.vy > 0:
            # Jumping
            character.img_path = "Jump/"
            if character.vy < 5:  # Small range
                character.img_path += "Jump 1"
            elif character.vy < 10: # Medium range
                character.img_path += "Jump 2"
            else: # Anything Higher
                character.img_path += "Jump Max"


        screen.fill((100, 100, 100))
        dt = clock.tick(60) / 1000
        character.step(dt)
        character.create()
        character.draw(screen)
        pygame.display.flip()