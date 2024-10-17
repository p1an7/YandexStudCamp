
import time
import GPIO as GPIO
import Config as cfg

# Настройки GPIO
buzzer = GPIO.BUZZER
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

# Ноты мелодии
melody = [
    440, 440, 440, 349, 523,
    440, 349, 523, 440, 659,
    659, 659, 698, 523, 784,
    698, 523, 440
]

# Длительности нот
noteDurations = [
    500, 500, 500, 350, 150,
    500, 350, 150, 650, 500,
    350, 150, 500, 350, 150,
    650, 500, 350, 150, 650
]

def play_tone(frequency, duration):
    if frequency > 0:
        period = 1.0 / frequency
        delay = period / 2
        cycles = int(duration * frequency)
        for _ in range(cycles):
            GPIO.output(buzzer, True)
            time.sleep(delay)
            GPIO.output(buzzer, False)
            time.sleep(delay)
    else:
        time.sleep(duration)

def play_melody():
    for i in range(len(melody)):
        noteDuration = 1000 / noteDurations[i]
        play_tone(melody[i], noteDuration)
        time.sleep(noteDuration * 1.30)

