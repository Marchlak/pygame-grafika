from model_g import *
import glm
import pygame

class Scene:
    def __init__(self, app):
        self.app = app
        self.app.time = 0.0
        self.objects = []
        self.gradient_animation_active = False 

        self.skybox = AdvancedSkyBox(app)

        self.scene_start_time = self.app.time
        self.events = [
            {'stop_gradient': True, 'duration': 0.0},
            {'skybox': 'skybox', 'duration': 0.0},
            {'music': 'stop','duration':0.0},
            {'cat': 'staying_cat', 'duration': 4.0},
            {'music': 'start','duration':0.0},
            {'cat': 'spinning_cat', 'duration': 1.8, 'rotation_speed': 250.0},
            {'cat': 'staying_cat', 'duration': 1.2},
            {'cat': 'spinning_cat', 'duration': 2.2, 'rotation_speed': 100.0},
            {'cat': 'staying_cat', 'duration': 0.9},
            {'start_gradient': True, 'duration': 0.0},
            {'skybox': 'skybox3', 'duration': 0.0},
            {'cat': 'spinning_cat', 'duration': 12.0, 'rotation_speed': 800.0},
            {'cat': 'spinning_cat', 'duration': 8.0, 'rotation_speed': 1200.0},
            {'cat': 'spinning_cat', 'duration': 8.0, 'rotation_speed': 1600.0},
            {'cat': 'staying_cat', 'duration': 0.4},
            {'cat': 'spinning_cat', 'duration': 3.0, 'rotation_speed': 1200.0},
            {'cat': 'staying_cat', 'duration': 0.4},
            {'cat': 'spinning_cat', 'duration': 3.0, 'rotation_speed': 1600.0},
            {'cat': 'staying_cat', 'duration': 0.4},
            {'cat': 'spinning_cat', 'duration': 1.5, 'rotation_speed': 1600.0},
            {'cat': 'staying_cat', 'duration': 0.4},
            {'cat': 'spinning_cat', 'duration': 14.0, 'rotation_speed': 400.0},
            {'cat': 'spinning_cat', 'duration': 2.0, 'rotation_speed': 2600.0},
            {'music': 'stop','duration': 0.0},



        ]
        self.load()
        self.current_event_index = 0
        self.event_start_time = 0.0

    def add_object(self, obj):
        self.objects.append(obj)

    def start_gradient_animation(self):
        self.gradient_animation_active = True
        for obj in self.objects:
            if isinstance(obj, Cube):
                obj.set_texture(0)

    def stop_gradient_animation(self):
        self.gradient_animation_active = False
        for obj in self.objects:
            if isinstance(obj, Cube):
                obj.set_texture(1)


    def load(self):
        app = self.app
        add = self.add_object


        n, s = 20, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))


        self.staying_cat = StayingCat(app, pos=(0, -1, -10), scale=(10, 10, 10))
        self.spinning_cat = SpinningCat(app, pos=(0, -1, -10), scale=(0.2, 0.2, 0.2), rot=(0, 270, 0))


        self.current_cat = None
        self.switch_to_event(self.events[0])

    def switch_to_event(self, event):

        if self.current_cat and self.current_cat in self.objects:
            self.objects.remove(self.current_cat)


        if 'start_gradient' in event and event['start_gradient']:
            self.start_gradient_animation()
        elif 'stop_gradient' in event and event['stop_gradient']:
            self.stop_gradient_animation()


        if 'skybox' in event:
            skybox_tex_id = event['skybox']
            self.skybox.set_texture(skybox_tex_id)

        if "music" in event:
            if event['music'] == 'start':
                pygame.mixer.music.load("resources/project.mp3")
                pygame.mixer.music.play(-1)
            if event['music'] == 'stop':
                pygame.mixer.music.stop()


        if "cat" in event:
            if event['cat'] == 'staying_cat':
                self.current_cat = self.staying_cat
            elif event['cat'] == 'spinning_cat':
                self.current_cat = self.spinning_cat

                rotation_speed = event.get('rotation_speed', 50.0)  # Domyślnie 50.0
                self.spinning_cat.set_rotation_speed(rotation_speed)
            else:
                self.current_cat = None


        if self.current_cat:
            self.add_object(self.current_cat)


        self.event_start_time = self.app.time - self.scene_start_time

    def update(self):
        current_time = self.app.time  
        event = self.events[self.current_event_index]
        elapsed_time = current_time - self.event_start_time


        if elapsed_time >= event['duration']:

            self.current_event_index += 1
            if self.current_event_index >= len(self.events):

                self.current_event_index = 0

            self.switch_to_event(self.events[self.current_event_index])


        for obj in self.objects:
            obj.update()

