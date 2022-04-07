#TODO
# update waiting for data from sleep to more dynamic
# clean data request function conditional stuff (flags)
# would be better to make a device class with thresholds, pin numbers, on/off flags
# figure out flag issue
# integrate GUI


import RPi.GPIO as GPIO
import time
import serial
import schedule

# start serial port and make it global
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

# GPIO pins
FAN_PIN = 7
DRIP_BOARD_PIN = 5
WATER_PUMP_PIN = 3
AUX_TANK_PUMP_PIN = 11

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
    # on / off flag this needs to be somewhere else but ok for testing
    fanFlag = 0 # FIX FLAG ISSUES
    
    # threholds
    #highTempThresh = 15.0
    #lowTempThresh = 14.6
    
    print("fan control")
    dataReady = DataRequest('T')
    if (dataReady):
        # read data into a float
        temperature = ser.readline()
        ser.flushInput()
        temp = temperature.decode("utf-8")
        temp = float(temperature) # add try / except statement here
        print("temperature in degrees C: " + str(temp))

        # relay control
        # check temperature against thresholds (assume temp sent as float in celcius)
        if(temp >= highTempThresh):# and fanFlag == 0):
            GPIO.output(FAN_PIN, GPIO.LOW)
            # fanFlag = 1
            print("The fan has been turned on")
        elif(temp < lowTempThresh):# and fanFlag == 1):
            GPIO.output(FAN_PIN, GPIO.HIGH)
            # fanFlag = 0
            print("The fan has been turned off")
        
        
        
    else:
        print("Error reading temperature")
        
def HumidityControl(lowHumidityThresh, highHumidityThresh):
    # on / off flag this needs to be somewhere else but ok for testing
    dripBoardFlag = 0 # FIX FLAG ISSUES
    
    # threholds
    #highHumidityThresh = 20.0
    #lowHumidityThresh = 10.0
    
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
        if(humidity >= highHumidityThresh):# and dripBoardFlag == 0):
            GPIO.output(DRIP_BOARD_PIN, GPIO.LOW)
            # dripBoardFlag = 1
            print("The drip board has been turned on")
        elif(humidity < lowHumidityThresh):# and dripBoardFlag == 1):
            GPIO.output(DRIP_BOARD_PIN, GPIO.HIGH)
            # dripBoardFlag = 0
            print("The drip board has been turned off")
        

def WateringControl(soilMoistureThresh):
    # on / off flag this needs to be somewhere else but ok for testing
    waterPumpFlag = 0 # FIX FLAG ISSUES
    
    # threholds
    # soilMoistureThresh = 200
    
    print("watering pump control")
    dataReady = DataRequest('M')
    if (dataReady):
        # read data into a float
        soilMoisture = ser.readline()
        ser.flushInput()
        soilMoisture = soilMoisture.decode("utf-8")
        soilMoisture = int(soilMoisture) # add try / except statement here
        print("Soil Moisture: " + str(soilMoisture))

      # relay control
        # check moisture against thresholds
        if(soilMoisture >= soilMoistureThresh):# and dripBoardFlag == 0):
            GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # have it turn off via timer
            # dripBoardFlag = 1
            print("The watering system has been turned on")
        elif(soilMoisture < soilMoistureThresh):# and dripBoardFlag == 1):
            GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
            # dripBoardFlag = 0
            print("The watering system has been turned off") 
    
    

def PondLevelControl(lowWaterLevelThresh):
    # on / off flag this needs to be somewhere else but ok for testing
    auxTankPumpFlag = 0 # FIX FLAG ISSUES
    
    # threholds
    #lowWaterLevelThresh = 250
    
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
        if(pondLevel <= lowWaterLevelThresh):# and dripBoardFlag == 0):
            GPIO.output(AUX_TANK_PUMP_PIN, GPIO.LOW) # have it turn off via timer
            # dripBoardFlag = 1
            print("The auxilary water tank pump has been turned on")
        elif(pondLevel > lowWaterLevelThresh):# and dripBoardFlag == 1):
            GPIO.output(AUX_TANK_PUMP_PIN, GPIO.HIGH)
            # dripBoardFlag = 0
            print("The auxilary water tank pump has been turned off") 


def main(args):
    
    #setting up the GPIO board for the correct pins
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(FAN_PIN, GPIO.OUT) #set up pin for fan to output
    GPIO.output(FAN_PIN, GPIO.HIGH) # High = relay off

    GPIO.setup(DRIP_BOARD_PIN, GPIO.OUT)
    GPIO.output(DRIP_BOARD_PIN, GPIO.HIGH)

    GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)

    GPIO.setup(AUX_TANK_PUMP_PIN, GPIO.OUT)
    GPIO.output(AUX_TANK_PUMP_PIN, GPIO.HIGH)
    
    # scheduling periods in minutes
    tempCheckPeriod = 20
    humidityCheckPeriod = 20
    soilMoistureCheckPeriod = 30
    pondLevelCheckPeriod = 10

    # thresholds
    pondThresh = 250
    wateringThresh = 600
    lowerHumidityThresh = 10.0
    upperHumidityThresh = 15.0
    lowerTempThresh = 16.0
    upperTempThresh = 20.0
    
    # setting up serial communication with Arduino
    time.sleep(5)
    ser.flushInput()
    ser.flushOutput()
    

    try:
        # schedule fan control
        schedule.every(tempCheckPeriod).minutes.do(TemperatureControl, lowTempThresh = lowerTempThresh, highTempThresh = upperTempThresh)
        # schedule drip board control
        schedule.every(humidityCheckPeriod).seconds.do(HumidityControl, lowHumidityThresh = lowerHumidityThresh, highHumidityThresh = upperHumidityThresh)
        # scheduling watering pump control
        schedule.every(soilMoistureCheckPeriod).seconds.do(WateringControl, soilMoistureThresh = wateringThresh)
        # scheduling pond level control
        schedule.every(pondLevelCheckPeriod).seconds.do(PondLevelControl, lowWaterLevelThresh = pondThresh)
        
        # check for pending tasks and run them
        while True:
            # print("checking for pending tasks")
            schedule.run_pending()
            time.sleep(5)

    # quit on ctrl+C        
    except KeyboardInterrupt:
        print("Quitting")
        GPIO.cleanup()
        ser.close()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
