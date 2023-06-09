import pygame

from misc.settings import *
from misc.support import import_folder

from entities.creature import Creature

class Enemy(Creature):
    def __init__(self, enemy_name, pos, groups, obstacles, damage_player, trigger_death_particles, add_experience_points):
        super().__init__(groups)

        self.obstacles = obstacles
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_experience_points = add_experience_points

        self.monster_name = enemy_name

        self.sprite_type = 'enemy'

        self.import_graphics(enemy_name)
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(0, -10)

        monster_info = monster_data[self.monster_name]

        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']

        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']

        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 500

        self.can_take_damage = True
        self.hit_time = None
        self.cannot_take_damage_duration = 350

        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])

        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}

        main_path = f'../graphics/monsters/{name}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_distance_direction_player(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_distance_direction_player(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0

            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.can_take_damage:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def actions(self, player):
        if self.status == 'attack':
            self.attack_sound.play()
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_distance_direction_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.can_take_damage:
            if current_time - self.hit_time >= self.cannot_take_damage_duration:
                self.can_take_damage = True

    def get_damage(self, player, attack_type):
        if self.can_take_damage:
            self.hit_sound.play()
            self.direction = self.get_distance_direction_player(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_weapon_damage()
            else:
                self.health -= player.get_magic_damage()

            self.hit_time = pygame.time.get_ticks()
            self.can_take_damage = False

    def hit_impact(self):
        if not self.can_take_damage:
            self.direction *= -self.resistance

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_experience_points(self.exp)
            self.death_sound.play()
            self.kill()

    def update(self):
        self.hit_impact()
        self.check_death()

        self.movement(self.speed)
        self.animate()
        self.cooldown()