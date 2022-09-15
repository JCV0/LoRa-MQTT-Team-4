#data generator
import numpy as np
import csv
data_header = ['GPSLat','GPSLon','IMURoll','IMUPitch','IMUYaw','wheelSpeed','percentage','processedKg','thresherSpeed','fuelLevel','mileage','oilLevel','wheelPressure']
data = [] 
for i in range (1,501):
    GPSLat = np.random.uniform(-180,180)
    GPSLon= np.random.uniform(-180,180)
    IMURoll = round(np.random.uniform(0,100),2)
    IMUPitch = round(np.random.uniform(0,100),2)
    IMUYaw = round(np.random.uniform(0,100),2)
    wheelSpeed = round(np.random.uniform(0,180),2)
    percentage = round(np.random.randint(0, 100),2)
    processedKG = round(np.random.randint(0, 2000),2)
    thresherSpeed = round(np.random.uniform(0,100),2)
    fuelLevel = round(np.random.randint(0,100),2)
    mileage = round(np.random.uniform(0,10000),2)
    oilLevel = round(np.random.randint(0,100),2)
    wheelPressure = round(np.random.uniform(32,35),2)
    data.append([GPSLat,GPSLon,IMURoll,IMUPitch,IMUYaw,wheelSpeed,percentage,processedKG,thresherSpeed,fuelLevel,mileage,oilLevel,wheelPressure])

filename = "datos_reto.csv"

with open(filename,'w',newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(data_header)
    csvwriter.writerows(data)

    
