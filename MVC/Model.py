from MVC.EventManager import *

# State machine constants for the StateMachine class below
STATE_CV = 1
STATE_POSE = 2
STATE_HAND = 3
STATE_FACEMESH = 4
STATE_HOLISTIC = 5

class GameEngine(object):
    def __init__(self, evManager):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.state = StateMachine_level_1()

        self.first_state = STATE_CV

        self.load_settings_and_data()
        
    def load_settings_and_data(self):
        import pygame
        icon_path = "Resources/Images/icon.png"
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)

        self.add_button_path = "Resources/Images/Buttons_add.png"
        self.minus_button_path = "Resources/Images/Buttons_minus.png"
        self.bun_sprite_path = "Resources/Images/Bun/"
        self.ball_path = "Resources/Images/Ball_Images/"
        self.ball_time = 0.6
        self.bun_sprite_time = 0.6


    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event, QuitEvent):
            self.running = False

        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)


    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(InitializeEvent())
        self.state.push(self.first_state)

        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)


class StateMachine_level_1(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    
    def __init__ (self):
        self.statestack = []
    
    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None
    
    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.statestack.pop()
            print(self.statestack)
            return len(self.statestack) > 0
        except IndexError:
            # empty stack
            return None
    
    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.statestack.append(state)
        print(self.statestack)
        return state