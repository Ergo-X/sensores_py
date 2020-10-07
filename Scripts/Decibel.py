import RPi.GPIO as gpio
import time
#import wiringpi

from datetime import datetime, timedelta
from sys import stdout
from time import sleep

class Decibel:
    def medir_decibeis(self):
        gpio.setmode(gpio.BCM) 
        gpio.setup(17, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        pino_sensor = 17
        amostraTempo = timedelta(milliseconds=10)
        ultimoTempo = timedelta(milliseconds=0)
        tempoDecorrido = 0
        valorExibido = 0
        tempoAtual = timedelta(milliseconds=0)

        def millis(tempoAtual):
            tempoAtual = tempoAtual + timedelta(milliseconds=0.1)
            sleep(0.001)
            return tempoAtual

        while True:    
          tempoAtual = millis(tempoAtual);
          tempoDecorrido = tempoAtual - ultimoTempo  
          
          if (gpio.input(pino_sensor) == 0):
            valorExibido = valorExibido + 1

          if (tempoDecorrido > amostraTempo):
            #print(valorExibido+30)
            return (valorExibido+30)
            valorExibido = 0
            ultimoTempo = tempoAtual 





