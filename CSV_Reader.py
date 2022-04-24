import csv

def F2C (tempF):
    tempC = (tempF - 32) * (5.0/9.0)
    return tempC

# thresholds
pondThresh = 250
wateringThresh = 600
lowerHumidityThresh = 10.0
upperHumidityThresh = 15.0
lowerTempThresh = 16.0
upperTempThresh = 20.0

#create csv as found in gui code
f = open('parameters.csv', 'w')
writer = csv.writer(f)
writer.writerow(['max_temp', 'min_temp', 'max_hum', 'min_hum',
                 'max_moist', 'min_moist'])
# random parameters for testing
writer.writerow([85.0, 60.0, 70.0, 10.0, 50, 800])
f.close()

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

print(pondThresh)
print(wateringThresh)
print(lowerHumidityThresh)
print(upperHumidityThresh) 
print(lowerTempThresh)
print(upperTempThresh)
