# ADDING SECOND SCHEDULER FOR ACTIVE DEVICES

# relay control
# check moisture against thresholds
if(soilMoisture >= soilMoistureThresh):
    GPIO.output(WATER_PUMP_PIN, GPIO.LOW) # have it turn off via timer
    activeSchedule.every(3).seconds.do(WateringControl, soilMoistureThresh = soilMoistureThresh, activeSchedule = activeSchedule).tag('watering-in-progress') # change timing for real thing
    print("The watering system is on")
elif(soilMoisture < soilMoistureThresh):
    GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
    print("The watering system is off")
    activeSchedule.clear('watering-in-progress')

# relay control
# check moisture against thresholds
if(pondLevel <= lowWaterLevelThresh):
    GPIO.output(AUX_TANK_PUMP_PIN, GPIO.LOW)# have it turn off via timer
    schedule.every(3).seconds.do(WateringControl, lowWaterLevelThresh = lowWaterLevelThresh, activeSchedule = activeSchedule).tag('pond-filling') # edit timing for real thing
    print("The auxilary water tank pump is on")
            
elif(pondLevel > lowWaterLevelThresh):
    GPIO.output(AUX_TANK_PUMP_PIN, GPIO.HIGH)
    print("The auxilary water tank pump is off")
    schedule.clear('pond-filling')


# setting up schedulers
mainSchedule = schedule.Scheduler()
activeSchedule = schedule.Scheduler()

# check for pending tasks and run them
while True:
    # print("checking for pending tasks")
    mainSchedule.run_pending()
    activeSchedule.run_pending()
    time.sleep(1)
