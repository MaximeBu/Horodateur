# Importations
import serial
import time

ser = serial.Serial('COM6', 9600)

# Laisser le temps à la connexion de s'établir
time.sleep(2)

# write output data to the serial interface
# these data are read by Arduino's serial:
inputPin = "A0"

menu = 1

# first flush possibly existing data in the input buffer:
ser.flushInput()

# loop until manually stopped
while True:
    try:
        # read a single line from the serial interface represented by the ser object
        lineBytes = ser.readline()
        print(lineBytes)
        
        # convert Bytes returned by the ser.readline() function toString
        yValue = lineBytes.decode('utf-8')
        print(yValue)
        
        # split the string that should have the following form:INPUTPIN: VALUE
        # into an array
        # yVAlue = line.split(':')

        yValue = int(yValue)

        if (yValue < 40 and menu > 1) :
            menu -= 1
            ser.write(menu)
        elif (yValue > 140 and menu < 4) :
            menu += 1
            ser.write(menu)
        
        # if the array has two elements, the line was correctly formated as INPUTPIN: VALUE
        print(f"Pin: {inputPin} has value: {yValue}", menu)
    
    except KeyboardInterrupt:
        break  # stop the while loop

ser.close()