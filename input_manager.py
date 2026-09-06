import pygame


class InputManager:
    DEADZONE = 0.25

    def __init__(self):
        pygame.joystick.init()

        self.gamepad = None

        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            print("Controller:", self.gamepad.get_name())
        else:
            print("No controller detected")

        self.move_left = False
        self.move_right = False

        self.jump_pressed = False
        self.jump_released = False

        self.shoot_pressed = False
        self.restart_pressed = False

    def begin_frame(self):
        # One-frame inputs reset every frame
        self.jump_pressed = False
        self.jump_released = False
        self.shoot_pressed = False
        self.restart_pressed = False

        # Held movement gets rebuilt every frame
        self.move_left = False
        self.move_right = False

    def handle_event(self, event):

        # controller disconnects/reconnects
        if event.type == pygame.JOYDEVICEREMOVED:
            if self.gamepad is not None:
                if event.instance_id == self.gamepad.get_instance_id():
                    print("CONTROLLER DISCONNECTED")
                    self.gamepad = None
        elif event.type == pygame.JOYDEVICEADDED:
            if self.gamepad is None:
                try:
                    self.gamepad = pygame.joystick.Joystick(event.device_index)
                    self.gamepad.init()
                    print("CONTROLLER RECONNECTED:", self.gamepad.get_name())
                except pygame.error:
                    # Controller was detected, but pygame has not made
                    # the device available yet. The once-per-second
                    # connection check will try again shortly.
                    self.gamepad = None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_z):
                self.jump_pressed = True

            if event.key == pygame.K_x:
                self.shoot_pressed = True

            if event.key == pygame.K_r:
                self.restart_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_SPACE, pygame.K_z):
                self.jump_released = True

        elif event.type == pygame.JOYBUTTONDOWN:
            # Cross / A
            if event.button == 0:
                self.jump_pressed = True

            # Square / X
            if event.button == 2:
                self.shoot_pressed = True

            # Triangle / Y
            if event.button == 3:
                self.restart_pressed = True

        elif event.type == pygame.JOYBUTTONUP:
            # Cross / A
            if event.button == 0:
                self.jump_released = True

    def update_held_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_left = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_right = True

        if self.gamepad is None:
            return

        # Left stick
        stick_x = self.gamepad.get_axis(0)

        if stick_x < -self.DEADZONE:
            self.move_left = True

        if stick_x > self.DEADZONE:
            self.move_right = True

        # PS4-style D-pad as buttons
        if self.gamepad.get_numbuttons() > 14:
            if self.gamepad.get_button(13):
                self.move_left = True

            if self.gamepad.get_button(14):
                self.move_right = True

        # Xbox-style D-pad as hat
        if self.gamepad.get_numhats() > 0:
            hat_x, _ = self.gamepad.get_hat(0)

            if hat_x < 0:
                self.move_left = True

            if hat_x > 0:
                self.move_right = True

    def check_controller_connection(self):
        if self.gamepad is not None:
            return
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            print("CONTROLLER FOUND:", self.gamepad.get_name())