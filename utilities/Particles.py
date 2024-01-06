import pygame
from utilities.image import load_image
import random
import shared


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, name, *groups):
        super().__init__(*groups)
        self.fire = [load_image(name)]
        self.fire.append(pygame.transform.scale(self.fire[0], (shared.WIDTH * 0.007, shared.HEIGHT * 0.02)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, shared.WIDTH, shared.HEIGHT)):
            self.kill()


def create_particles(position, groop, name):
    particle_count = 5
    numbers = [-6, -5, -4, -3, 3, 4, 5, 6]
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), name, groop)
