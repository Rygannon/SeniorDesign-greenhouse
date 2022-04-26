#TODO
# update waiting for data from sleep to more dynamic
# SECOND SCHEDULER FOR WATERING/POND CHECK OTHER PI

import RPi.GPIO as GPIO
import time
import serial
import schedule
import csv

# start serial port and make it global
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

# GPIO pins
FAN_PIN = 7
DRIP_BOARD_PIN = 5
WATER_PUMP_PIN = 3
AUX_TANK_PUMP_PIN = 11
FANS_PIN = 13
ROOF_FAN_PIN = 15

def F2C (tempF):
    tempC = (tempF - 32) * (5.0/9.0)
    return tempC

def DataRequest(request):
    # sending request
    request = request.encode("utf-8")
    ser.write(request)
    request = request.decode("utf-8")

    # give a delay to give time for transmission
    # probably not the best way to wait for data
    time.sleep(3)

    # check for confirmation from Arudino
    if(ser.in_waiting > 0):
        confirmation = ser.read()
        confirmation = confirmation.decode("utf-8")
        print("request confirmation: " + str(confirmation))
        if(request == confirmation):
            # return true if data is ready to read
            # sleep just for testing. switch to actually wait a bit for response
            time.sleep(3)
            if(ser.in_waiting > 0):
                return True
            else:
                ser.flushInput()
                return False
    # return false if the Arduino does not respond
    else:
        print("No response from Arduino.")
        return False

        

def TemperatureControl(lowTempThresh, highTempThresh):
    print("Temperature control")
    dataReady = DataRequest('T')
    if (dataReady):
        # read data into a float
        temperature = ser.readline()
        ser.flushInput()
        temp = temperature.decode("utf-8")
        temp = float(temperature)
        print("temperature in degrees C: " + str(temp))

        # relay control
        # check temperature against thresholds (assume temp sent as float in celcius)
        if(temp >= highTempThresh):
            GPIO.output(FAN_PIN, GPIO.LOW)
            GPIO.output(FANS_PIN, GPIO.LOW)
            GPIO.output(ROOF_FAN_PIN, GPIO.LOW)
            print("The fan has been turned on")
        elif(temp < lowTempThresh):
            GPIO.output(FAN_PIN, GPIO.HIGH)
            GPIO.output(FANS_PIN, GPIO.HIGH)
            GPIO.output(FANS_PIN, GPIO.HIGH)
            print("The fan has been turned off") 
    else:
        print("Error reading temperature")

        
def HumidityControl(lowHumidityThresh, highHumidityThresh):
    print("drip board control")
    dataReady = DataRequest('H')
    if (dataReady):
        # read data into a float
        humidity = ser.readline()
        ser.flushInput()
        humidity = humidity.decode("utf-8")
        humidity = float(humidity) # add try / except statement here
        print("Relative humidity (%): " + str(humidity))

      # relay control
        # check humidity against thresholds
        if(humidity >= highHumidityThresh):
            GPIO.output(DRIP_BOARD_PIN, GPIO.LOW)
            GPIO.output(FAN_PIN, GPIO.LOW)
            print("The drip board has been turned on")
        elif(humidity < lowHumidityThresh):
            GPIO.output(DRIP_BOARD_PIN, GPIO.HIGH)
            GPIO.output(FAN_PIN, GPIO.HIGH)
            print("The drip board has been turned off")
        

def WateringControl(soilMoistureThresh, activeSchedule):
    print("watering pump control")
    dataReady = DataRequest('M')
    if (dataReady):
        # read data into a float
        soilMoisture = ser.readline()
        ser.flushInput()
        soilMoisture = soilMoisture.decode("utf-8")
        soilMoisture = int(soilMoisture)
        print("Soil Moisture: " + str(soilMoisture))

      # relay control
        # check moisture against thresholds
        if(soilMoisture >= soilMoistureThresh):# and dripBoardFlag == 0):
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # have it turn off via timer
            activeSchedule.every(3).seconds.do(WateringControl, soilMoistureThresh = soilMoistureThresh, activeSchedule = activeSchedule).tag('watering-in-progress') 
            print("The watering system has been turned on")
        elif(soilMoisture < soilMoistureThresh):# and dripBoardFlag == 1):
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            activeSchedule.clear('watering-in-progress')
            print("The watering system has been turned off") 
        

def PondLevelControl(lowWaterLevelThresh, activeSchedule):
    print("Pond Water Level Control")
    dataReady = DataRequest('L')
    if (dataReady):
        # read data into a float
        pondLevel = ser.readline()
        ser.flushInput()
        pondLevel = pondLevel.decode("utf-8")
        pondLevel = int(pondLevel) # add try / except statement here
        print("Pond water level: " + str(pondLevel))

      # relay control
        # check moisture against thresholds
        if(pondLevel <= lowWaterLevelThresh):
            GPIO.output(AUX_TANK_PUMP_PIN, GPIO.LOW) # have it turn off via timer
            # add flags so it doesnt keep adding schedule 
            activeSchedule.every(3).seconds.do(PondLevelControl, lowWaterLevelThresh = lowWaterLevelThresh, activeSchedule = activeSchedule).tag('pond-filling') # edit timing for real thing
            print("The auxilary water tank pump has been turned on")
        elif(pondLevel > lowWaterLevelThresh):# and dripBoardFlag == 1):
            GPIO.output(AUX_TANK_PUMP_PIN, GPIO.HIGH)
            activeSchedule.clear('pond-filling')
            print("The auxilary water tank pump has been turned off") 


def main(args):
    
    #setting up the GPIO board for the correct pin
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(FAN_PIN, GPIO.OUT) #set up pin for fan to output
    GPIO.output(FAN_PIN, GPIO.HIGH) # High = relay off

    GPIO.setup(DRIP_BOARD_PIN, GPIO.OUT)
    GPIO.output(DRIP_BOARD_PIN, GPIO.HIGH)

    GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)

    GPIO.setup(AUX_TANK_PUMP_PIN, GPIO.OUT)
    GPIO.output(AUX_TANK_PUMP_PIN, GPIO.HIGH)
    
    GPIO.setup(FANS_PIN, GPIO.OUT)
    GPIO.output(FANS_PIN, GPIO.HIGH)

    GPIO.setup(ROOF_FAN_PIN, GPIO.OUT)
    GPIO.output(ROOF_FAN_PIN, GPIO.HIGH)
    
    
    # scheduling periods in minutes UPDATE
    tempCheckPeriod = 30
    humidityCheckPeriod = 10
    soilMoistureCheckPeriod = 10
    pondLevelCheckPeriod = 50


    # thresholds READ FROM CSV
    # default values
    pondThresh = 700
    wateringThresh = 600
    lowerHumidityThresh = 10.0
    upperHumidityThresh = 15.0
    lowerTempThresh = 10.0
    upperTempThresh = 15.0
    # update thresholds from csv file
  
    try:
        with open('parameters.csv', mode='r') as file:
            csvReader = csv.DictReader(file)
            for row in csvReader:
                lowerTempThresh = F2C(float(row['min_temp']))   
                upperTempThresh = F2C(float(row['max_temp']))
                lowerHumidityThresh = float(row['min_hum'])
                upperHumidityThresh = float(row['max_hum'])
                wateringThresh = int(row['min_moist'])
     
    except:
        print("Error reading parameters CSV file.")

    
    # setting up serial communication with Arduino
    time.sleep(5)
    ser.flushInput()
    ser.flushOutput()

    mainSchedule = schedule.Scheduler()
    activeSchedule = schedule.Scheduler()



    try:
        # schedule fan control
        mainSchedule.every(tempCheckPeriod).seconds.do(TemperatureControl, lowTempThresh = lowerTempThresh, highTempThresh = upperTempThresh)
        # schedule drip board control
        mainSchedule.every(humidityCheckPeriod).seconds.do(HumidityControl, lowHumidityThresh = lowerHumidityThresh, highHumidityThresh = upperHumidityThresh)
        # scheduling watering pump control
        mainSchedule.every(soilMoistureCheckPeriod).seconds.do(WateringControl, soilMoistureThresh = wateringThresh, activeSchedule=activeSchedule)
        # scheduling pond level control
        mainSchedule.every(pondLevelCheckPeriod).seconds.do(PondLevelControl, lowWaterLevelThresh = pondThresh, activeSchedule=activeSchedule)
        
        # check for pending tasks and run them
        while True:
            # print("checking for pending tasks")
            mainSchedule.run_pending()
            activeSchedule.run_pending()
            time.sleep(1)

    # quit on ctrl+C        
    except KeyboardInterrupt:
        print("Quitting")
        GPIO.cleanup()
        ser.close()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
