from RPi import RPi as GPIO
import time


class stepControl:
    direction = 0
    steps = 0
    steps_number = 0
    number_of_steps = 0
    last_steps_time = float(0)
    first_time = float(0)
    step_delay = float(0)
    a1 = 0
    a2 = 0
    b1 = 0
    b2 = 0

    def __init__(self, steps_per_revolution, a1, a2, b1, b2):
        self.number_of_steps = steps_per_revolution
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(a1, GPIO.OUT)
        GPIO.setup(a2, GPIO.OUT)
        GPIO.setup(b1, GPIO.OUT)
        GPIO.setup(b2, GPIO.OUT)
        GPIO.output(self.b2, GPIO.LOW)
        GPIO.output(self.b1, GPIO.LOW)
        GPIO.output(self.a2, GPIO.LOW)
        GPIO.output(self.a1, GPIO.LOW)

    def setSpeed(self, your_speed):
        self.your_speed = your_speed
        self.step_delay = 60 * 1000000000 / (self.number_of_steps * self.your_speed)

    def run_step(self, run_step_number):
        if run_step_number == 0:
            GPIO.output(self.b2, GPIO.LOW)
            GPIO.output(self.b1, GPIO.HIGH)
            GPIO.output(self.a2, GPIO.LOW)
            GPIO.output(self.a1, GPIO.HIGH)
        if run_step_number == 1:
            GPIO.output(self.b2, GPIO.LOW)
            GPIO.output(self.b1, GPIO.HIGH)
            GPIO.output(self.a2, GPIO.HIGH)
            GPIO.output(self.a1, GPIO.LOW)
        if run_step_number == 2:
            GPIO.output(self.b2, GPIO.HIGH)
            GPIO.output(self.b1, GPIO.LOW)
            GPIO.output(self.a2, GPIO.HIGH)
            GPIO.output(self.a1, GPIO.LOW)
        if run_step_number == 3:
            GPIO.output(self.b2, GPIO.HIGH)
            GPIO.output(self.b1, GPIO.LOW)
            GPIO.output(self.a2, GPIO.LOW)
            GPIO.output(self.a1, GPIO.HIGH)

    def step(self, steps):
        self.steps = abs(steps)
        if steps > 0:
            self.direction = 1
        if steps < 0:
            self.direction = 0
        while self.steps > 0:
            self.first_time = int(time.time_ns())
            if self.first_time - self.last_steps_time >= self.step_delay:
                self.last_steps_time = self.first_time
                if self.direction == 1:
                    self.steps_number += 1
                    if self.steps_number == self.number_of_steps:
                        self.steps_number = 0
                else:
                    if self.steps_number == 0:
                        self.steps_number = self.number_of_steps
                    self.steps_number -= 1
                self.steps -= 1
                self.run_step(self.steps_number % 4)

        GPIO.output(self.b2, GPIO.LOW)
        GPIO.output(self.b1, GPIO.LOW)
        GPIO.output(self.a2, GPIO.LOW)
        GPIO.output(self.a1, GPIO.LOW)