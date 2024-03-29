from MVC.EventManager import *
from Scene.UI_1 import *
import pygame
from pygame.locals import *
import pygame.freetype
import cv2
from Components.Button.Button import button
from Components.Sprite_Engine.Sprite import sprite_engine
from Components.Ball.Ball import Ball_Engine

class UI_View(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        self.model = model

    def initialize(self):
        """
        Initialize the UI.
        """
        pygame.init()
        pygame.font.init()
        pygame.freetype.init()

        pygame.display.set_caption('Test_Project')

        # flags = FULLSCREEN | DOUBLEBUF
        flags = DOUBLEBUF

        if (pygame.display.get_num_displays() >= 2):
            screen_no = 1
        else:
            screen_no = 0

        self.model.screen = pygame.display.set_mode((1280, 720), flags, 16, display = screen_no, vsync=1)

        self.clock = pygame.time.Clock()

        # speedup a little bit
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def quit_pygame(self):
        # shut down the pygame graphics
        self.isinitialized = False
        pygame.quit()

    def init_page(self):
        self.model.add_button = button((100, 150), self.model.add_button_path, self.model, 2)
        self.model.minus_button = button((100, 250), self.model.minus_button_path, self.model, 2)
        
        #self.model.bun_sprite = sprite_engine(self.model.bun_sprite_path, (100, 400), 6, self.model)
        self.model.ball = Ball_Engine(self.model.ball_path, (100, 400), 24, self.model, 0.4)

    def render(self):
        # Display FPS
        self.model.FPS_class.display_FPS(self.model.img)
        try:
            # Display Mediapipe Pose landmarks
            if self.model.currentstate == 2:
                # self.model.Mediapipe_pose_class.draw_all_landmark_circle(self.model.img) # ctrl / to comment
                # self.model.Mediapipe_pose_class.draw_all_landmark_line(self.model.img)
                self.model.Mediapipe_pose_class.draw_all_landmark_drawing_utils(self.model.img)

            # Display Mediapipe Hand landmarks
            if self.model.currentstate == 3:
                # self.model.Mediapipe_hand_class.draw_all_landmark_circle(self.model.img)
                self.model.Mediapipe_hand_class.draw_all_landmark_drawing_utils(self.model.img)

            # Display Mediapipe FaceMesh landmarks
            if self.model.currentstate == 4:
                self.model.Mediapipe_FaceMesh_class.draw_all_landmark_drawing_utils(self.model.img)

            # Display Mediapipe Holistic landmarks 
            if self.model.currentstate == 5:
                self.model.Mediapipe_Holistic_class.draw_all_landmark_drawing_utils(self.model.img)
        except Exception as e:
            print(e)
        # Display Segmentation
        # self.model.img = self.model.segmentation_class.calculate_segmentation(self.model.img, Mediapipe_Holistic_class.get_segmentation_mask())

        # self.model.CV2_class.display_camera(self.model.img) # show image

        # if self.model.CV2_class.check_exit():
        #     self.model.CV2_class.release_camera() # release camera
        #     self.evManager.Post(QuitEvent())

        # if self.model.state == 1:
        #     render_Page1()
            
        """
        Draw things on pygame
        """
        empty_color = pygame.Color(0, 0, 0, 0)
        self.model.screen.fill(empty_color)

        # Convert into RGB
        self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)

        # Convert the image into a format pygame can display
        self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

        # blit the image onto the screen
        self.model.screen.blit(self.model.img, (0, 0))
        
        # Draw button
        self.model.add_button.draw(self.model.screen)
        self.model.minus_button.draw(self.model.screen)

        # Draw ball
        self.model.ball.draw(self.model.ball_time)

        # Update the screen
        pygame.display.flip()

        # limit the redraw speed to 30 frames per second
        self.clock.tick(60)