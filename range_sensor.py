import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#triggers the sensor from PI
TRIG = 23
#reads return signal from sensor
ECHO = 24
#buzzer sound
BUZZER = 25

print ("Distance Measurement in Progress")

#Set GPIO ports as inputs/outputs
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

def compute_distance():
    #Trigger pin is set to low and giving sensor time to settle
    GPIO.output(TRIG, False)
    print("Waiting for Sensor to Settle")
    time.sleep(1)

    #set Trigger to HIGH
    GPIO.output(TRIG, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # pulse_start = time.time()
    # pulse_end = time.time()

    #save start time
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    # save time of arrival
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = (pulse_duration * 34300) / 2

    #round to 2 decimal places
    distance = round(distance,2)
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = compute_distance()
            print("Distance", dist, "cm")
            if dist < 100.00:
                while True:
                    GPIO.output(BUZZER, GPIO.HIGH)
                    print('Beep')
                    time.sleep(0.5)
                    GPIO.output(BUZZER, GPIO.LOW)
                    print('No Beep')
                    time.sleep(0.5)
                    dist = compute_distance()
                    if dist > 100.00:
                        break
            time.sleep(0.5)

    #Press CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by our user")
        GPIO.cleanup()
