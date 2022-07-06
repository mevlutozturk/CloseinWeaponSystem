import cv2
from threading import Thread
import numpy as np
from RPi import RPi as GPIO
import Stepper
import time
import VL53L0X

class detect:
    def __init__(self):
        self.weapon_motor = 16
        self.tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
        self.tof.open()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.weapon_motor, GPIO.OUT)
        self.videoCapture = cv2.VideoCapture(0)
        self.motor_h = Stepper.stepControl(200,40,38,36,32)
        self.motor_v = Stepper.stepControl(200,37,35,33,23)
        self.motor_v.setSpeed(40)
        self.motor_h.setSpeed(40)
        self.axis_thread = Thread(target=self.axisControl,args=())
        self.meanshift_thread = Thread(target=self.meanshift , args=())
        self.show_image = Thread(target=self.show_capture())
        self.fire_weapon = Thread(target=fire,args=())
        self.meanshift_thread.start()
        self.show_image.start()
        self.axis_thread.start()
        self.fire_weapon.start()

    def meanshift(self):
        self.videoCapture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        ret, self.frame = self.videoCapture.read()
        rows, cols = self.frame.shape[:2]
        w = 200
        h = 300
        col = int((cols - w) / 2)
        row = int((rows - h) / 2)
        shiftWindow = (col, row, w, h)
        roi = self.frame[row:row + h, col:col + w]
        roiHsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lowLimit = np.array((0., 60., 32.))
        highLimit = np.array((180., 255., 255.))
        mask = cv2.inRange(roiHsv, lowLimit, highLimit)
        roiHist = cv2.calcHist([roiHsv], [0], mask, [180], [0, 180])
        cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
        terminationCriteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 10, 1)
        while True:
            ret, self.frame = self.videoCapture.read()
            frameHsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            backprojectedFrame = cv2.calcBackProject([frameHsv], [0], roiHist, [0, 180], 1)
            mask = cv2.inRange(frameHsv, lowLimit, highLimit)
            backprojectedFrame &= mask
            ret, shiftWindow = cv2.meanShift(backprojectedFrame, shiftWindow, terminationCriteria)
            col, row = shiftWindow[:2]
            self.frame = cv2.rectangle(self.frame, (col, row), (col + w, row + h), (255, 255, 0), 4)
            self.h_axis_pos = col + w/2
            self.v_axis_pos = row + h/2
            self.show_capture()
            self.axisControl()
            self.fire()
            if cv2.waitKey(60) & 0xff == ord('q'):
                exit(0)
                break
        return

    def show_capture(self):
        cv2.imshow('air defence system',self.frame)
        return

    def axisControl(self):
        h_step_count = 4
        v_step_count = 4
        if self.h_axis_pos > 260:
            h_step_count = 4
        if self.h_axis_pos < 220:
            h_step_count = -4
        if self.v_axis_pos > 340:
            v_step_count = 4
        if self.v_axis_pos < 300:
            v_step_count = -4
        self.motor_v.step(v_step_count)
        self.motor_h.step(h_step_count)
        return
    def fire(self):
        if self.distance < 2000:
            GPIO.OUT(self.weapon_motor.HIGH)
        if self.distance > 2000:
            GPIO.OUT(self.weapon_motor.LOW)
            pass
    def tof_return(self):
        self.tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

        self.timing = self.tof.get_timing()
        if self.timing < 20000:
            timing = 20000

        for count in range(1, 101):
            self.distance = self.tof.get_distance()
            if self.distance > 0:
                print("%d mm, %d cm, %d" % (self.distance, (self.distance / 10), self.count))
            time.sleep(self.timing / 1000000.00)
            self.tof.stop_ranging()

if __name__ == '__main__':
    weapon = detect()
    try :
        weapon.meanshift()
    except TypeError:
        pass
    cv2.destroyAllshiftWindows()
