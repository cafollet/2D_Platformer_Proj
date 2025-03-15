import os
import pygame


def string_sort(string_to_sort):
    """Sorting key for files"""
    return int(string_to_sort[-8:-4])


class Character(pygame.sprite.Sprite):
    """
    Character object for pygame
    """
    def __init__(self, x, y, group, vx=0, vy=0, ax=0, ay=0, img_path="", dt=1):
        """
        Construct a character
        """
        super().__init__(group)
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.img_path = img_path
        self.images = []
        self.frame = 0
        self.flip_bool = False
        self.dt = dt


    def update(self):
        """
        update all character values
        """
        # Motion Update
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt
        self.vx += self.ax * self.dt
        self.vy += self.ay * self.dt


        # Find correct animation
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


        # Animation Update
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
                self.image = flipped_image
                self.flip_bool = True
            elif self.vx > 0:
                self.image = frame_image
                self.flip_bool = False
            else:
                if self.flip_bool:
                    self.image = flipped_image
                else:
                    self.image = frame_image
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, -self.y]
            self.frame += 1


if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 400
    screen = pygame.display.set_mode([screen_width, screen_height])
    clock = pygame.time.Clock()
    test_group = pygame.sprite.Group()

    floor_y = -screen_height / 2

    character = Character(screen_width / 2, -screen_height / 2, test_group, 0, 0, 0, 0, "Cowboy.png")
    rate = 5
    land = False
    l_key, r_key, jump, shift, crouch = (False, False, False, False, False)
    while True:

        # Test Floor
        if character.y > floor_y:
            character.ay = -1
        elif character.y <= floor_y and character.ay == -1:
            character.ay = 0
            character.vy = 0
            character.y = floor_y
            land = True



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    l_key = False
                if event.key == pygame.K_RIGHT:
                    r_key = False
                if event.key == pygame.K_SPACE:
                    jump = False
                if event.key == pygame.K_DOWN:
                    crouch = False
                if event.key == pygame.K_LSHIFT:
                    shift = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    l_key = True
                if event.key == pygame.K_RIGHT:
                    r_key = True
                if event.key == pygame.K_SPACE:
                    jump = True
                if event.key == pygame.K_DOWN:
                    crouch = True
                if event.key == pygame.K_LSHIFT:
                    shift = True

        # Motion
        if (l_key and r_key) or (not l_key and not r_key):
            character.vx = 0
        elif l_key:
            character.vx = -3
        elif r_key:
            character.vx = 3
        if jump and character.y == floor_y:
            character.vy = 10



        # Animation
        if character.vy == 0:
            if land:
                character.img_path = "Jump/Land"
                land = False
            elif (l_key and r_key) or (not l_key and not r_key):
                character.img_path = "Idle"
            elif l_key:
                character.img_path = "Walking"
            elif r_key:
                character.img_path = "Walking"
        elif character.vy < 0:
            # Falling
            character.img_path = "Jump/"
            if character.vy > -1:  # Small range
                character.img_path += "Fall 1"
            elif character.vy > -3: # Medium range
                character.img_path += "Fall 2"
            else: # Anything Higher
                character.img_path += "Fall Max"


        elif character.vy > 0:
            # Jumping
            character.img_path = "Jump/"
            if character.vy < 1:  # Small range
                character.img_path += "Jump 1"
            elif character.vy < 3: # Medium range
                character.img_path += "Jump 2"
            else: # Anything Higher
                character.img_path += "Jump Max"


        screen.fill((100, 100, 100))
        dt = clock.tick(60) / 1000
        test_group.update()
        test_group.draw(screen)
        pygame.display.flip()