import os
import re
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sys


print("Opening heart rate file")

## Pass in FitBit file, then motion

heart_rate = []
countHeartbeatMeasurements = 0

## Lance Running
# start_time = datetime.datetime.strptime("2017-04-30 15:56:00", "%Y-%m-%d %H:%M:%S")
# actual_start_time = datetime.datetime.strptime("2017-04-30 15:56:00", "%Y-%m-%d %H:%M:%S")
# end_time = datetime.datetime.strptime("2017-04-30 16:30:00", "%Y-%m-%d %H:%M:%S")

## Lance Sitting
# start_time = datetime.datetime.strptime("2017-04-30 19:28:00", "%Y-%m-%d %H:%M:%S")
# actual_start_time = datetime.datetime.strptime("2017-04-30 19:28:00", "%Y-%m-%d %H:%M:%S")
# end_time = datetime.datetime.strptime("2017-04-30 20:15:00", "%Y-%m-%d %H:%M:%S")

## Anudeep Running
start_time = datetime.datetime.strptime("2017-05-01 16:01:00", "%Y-%m-%d %H:%M:%S")
actual_start_time = datetime.datetime.strptime("2017-05-01 16:01:00", "%Y-%m-%d %H:%M:%S")
end_time = datetime.datetime.strptime("2017-05-01 16:33:00", "%Y-%m-%d %H:%M:%S")


## Anudeep Sitting
# start_time = datetime.datetime.strptime("2017-05-01 15:23:00", "%Y-%m-%d %H:%M:%S")
# actual_start_time = datetime.datetime.strptime("2017-05-01 15:23:00", "%Y-%m-%d %H:%M:%S")
# end_time = datetime.datetime.strptime("2017-05-01 15:56:00", "%Y-%m-%d %H:%M:%S")


# First, we'll handle FitBit data
with open(sys.argv[1]) as file1:
    for line in file1:
        temp = re.split(",", line)
        lineTime = datetime.datetime.strptime(temp[0], "%Y-%m-%d %H:%M:%S")

        # get times within start and end time specified
        # actual start time will be set to the time of the first data point we use
        if (start_time < lineTime < end_time):
            if countHeartbeatMeasurements == 0:
                actual_start_time = lineTime 
            else:
                delta = lineTime - actual_start_time
                temp[0] = delta.seconds
                temp[1] = float(temp[1][:-1])
                    
                heart_rate.append(temp)

        countHeartbeatMeasurements = countHeartbeatMeasurements + 1
        if (lineTime > end_time):
            break; # we don't need to process any more lines

for x in heart_rate:
    print(x)
# exit()


print("Opening motion file")
acc_data = [] #1
gyro_data = [] #4
count = 0
start_time = 0

# Handling SmartWatch data
with open(sys.argv[2]) as file1:
    for line in file1:
        temp = re.split(' |,', line)
        temp = [float(e) for e in temp]

        if count == 0:
            start_time = temp[0]
            temp[0] = 0
        else:
            temp[0] = temp[0] - start_time


        if temp[1] == 4 and temp[0] >= 0:
            temp[0] = temp[0] * 0.000000001
            gyro_data.append(temp)
        elif temp[1] == 1 and temp[0] >= 0:
            temp[0] = temp[0] * 0.000000001
            acc_data.append(temp)
            
        count = count + 1

# for x in gyro_data:
#     print(x)
# exit()



## Trying to determine operating range of gyroscope
# minX = 500
# maxX = -500
# minY = 500
# maxY = -500
# minZ = 500
# maxZ = -500

# for reading in gyro_data:
#     print(reading)

#     if (reading[3] < minX and reading[2] == 3.0):
#         minX = reading[3]
#     if (reading[3] > maxX and reading[2] == 3.0):
#         maxX = reading[3]

#     if (reading[4] < minY and reading[2] == 3.0):
#         minY = reading[4]
#     if (reading[4] > maxY and reading[2] == 3.0):
#         maxY = reading[4]

#     if (reading[5] < minZ and reading[2] == 3.0):
#         minZ = reading[5]
#     if (reading[5] > maxZ and reading[2] == 3.0):
#         maxZ = reading[5]

# print(minX)
# print(maxX)
# print(minY)
# print(maxY)
# print(minZ)
# print(maxZ)
# exit()


# Handling gyro data to get difference in rotation between timestamps

count = 0

previous_x = 0
previous_y = 0
previous_z = 0

gyro_diff_data = []
# timestamp, gyro_signal(4), quality_reading, x, y, z
for reading in gyro_data:

    this_x = reading[3]
    this_y = reading[4]
    this_z = reading[5]

    if count == 0:
        diff_x = 0.0
        diff_y = 0.0
        diff_z = 0.0
    else:
        diff_x = this_x - previous_x
        diff_y = this_y - previous_y
        diff_z = this_z - previous_z



    temp = [reading[0], reading[1], reading[2], diff_x, diff_y, diff_z]
    gyro_diff_data.append(temp)



    # print("\nthis")    
    # print(this_x)
    # print(this_y)
    # print(this_z)

    # print("\nprevious")    
    # print(previous_x)
    # print(previous_y)
    # print(previous_z)

    # print("\ndiff")
    # print(diff_x)
    # print(diff_y)
    # print(diff_z)

    # print(temp)
    # print(reading)
    # print("----------")

    previous_x = this_x
    previous_y = this_y
    previous_z = this_z

    count = count + 1
# exit()

## Replace rotation values with magnitududes of change
# for index in range(0, len(gyro_data)-1):
#     gyro_data[index][3] = gyro_diff_data[index][3]
#     gyro_data[index][4] = gyro_diff_data[index][4]
#     gyro_data[index][5] = gyro_diff_data[index][5]






past_count = 0
count = 0
coordinated_acc = []

for i in range(0, len(heart_rate)):
    curr_time_stamp = heart_rate[i][0]
    x = 0
    y = 0
    z = 0
    temp_var = []

    while count < len(acc_data) and acc_data[count][0] < curr_time_stamp :
        x += abs(acc_data[count][3])
        y += abs(acc_data[count][4])
        z += abs(acc_data[count][5])
        count += 1
    temp_var.append(x/(count-past_count-1)) 
    temp_var.append(y/(count-past_count-1))
    temp_var.append(z/(count-past_count-1)) 
    temp_var.append(count-past_count-1) 
    temp_var.append(curr_time_stamp)
    coordinated_acc.append(temp_var) 
    past_count = count


#acc_count = count
count = 0
past_count = 0
coordinated_gyro = []       
for i in range(0, len(heart_rate)):
    curr_time_stamp = heart_rate[i][0]
    x = 0
    y = 0
    z = 0
    temp_var = []

    while count < len(gyro_data) and gyro_data[count][0] < curr_time_stamp :
        x += abs(gyro_data[count][3])
        y += abs(gyro_data[count][4])
        z += abs(gyro_data[count][5])
        count += 1

    if (count-past_count-1) > 0:
        temp_var.append(x/(count-past_count-1)) 
        temp_var.append(y/(count-past_count-1))
        temp_var.append(z/(count-past_count-1))
        temp_var.append(count-past_count-1) 
    else:
        temp_var.append(0.0) 
        temp_var.append(0.0)
        temp_var.append(0.0)
        temp_var.append(count-past_count-1) 
    temp_var.append(curr_time_stamp)
    coordinated_gyro.append(temp_var) 
    past_count = count      

final_data = []




for i in range(0, len(heart_rate)):
    temp = []
    temp.append(heart_rate[i][0])
    if heart_rate[i][0] != coordinated_gyro[i][4] or heart_rate[i][0] != coordinated_acc[i][4] or coordinated_gyro[i][4] != coordinated_acc[i][4]:
        print("Something's Messed UP !!")
    temp.append(coordinated_acc[i][0])
    temp.append(coordinated_acc[i][1])
    temp.append(coordinated_acc[i][2])
    temp.append(coordinated_gyro[i][0])
    temp.append(coordinated_gyro[i][1])
    temp.append(coordinated_gyro[i][2])
    temp.append(heart_rate[i][1])
    final_data.append(temp)  
    # 0th col is time elapsed,
    # 1-3 are x,y,z of accelerometer,
    # 4-6 are x,y,z of gyroscope,
    # 7th is heart rate

#print(count, len(gyro_data), acc_count, len(acc_data))

# for reading in final_data:
#     print(reading)
#     time.sleep(0.05)




graph_x_values = []
graph_y_values = []

print("Processing final_data")
for reading in final_data:

    averageAccelorometerMagnitude = (abs(reading[1]) + abs(reading[2]) + abs(reading[3])) / 3.0
    averageGyroscopeMagnitude = (abs(reading[4]) + abs(reading[5]) + abs(reading[6])) / 3.0

    # print readings(x,y,z), average magnitude, largest magnitude
    # print("   ", reading[1], reading[2], reading[3])
    # print(averageAccelorometerMagnitude)
    # print(max(abs(reading[1]), abs(reading[2]), abs(reading[3])))
    # time.sleep(0.20)

    graph_x_values.append(reading[7])
    graph_y_values.append(abs(reading[5]))
    # graph_y_values.append(averageAccelorometerMagnitude)
    # graph_y_values.append(averageGyroscopeMagnitude)
    print(reading[7])
    print(averageAccelorometerMagnitude)
    print()


# plt.plot(np.array(graph_x_values), np.array(graph_y_values))
plt.scatter(graph_x_values, graph_y_values)
plt.autoscale(enable=True, axis=u'both', tight=False)

# line of best fit
plt.plot(graph_x_values, np.poly1d(np.polyfit(graph_x_values, graph_y_values, 1))(graph_x_values))

plt.xlabel('Heart Rate')
plt.ylabel('Magnitude (accelerometer)')
plt.title('Chart Title')
plt.grid(True)
plt.draw() # non-blocking


degree = 1
results = {}

coeffs = np.polyfit(graph_x_values, graph_y_values, degree)
 # Polynomial Coefficients
results['polynomial'] = coeffs.tolist()

correlation = np.corrcoef(graph_x_values, graph_y_values)[0,1]

 # r
results['correlation'] = correlation
 # r-squared
results['determination'] = correlation**2

print(results)

plt.show()

 
# # starting with arg1, plot arg2 items with step arg3
# t = arange(0.0, 20.0, 1)


# s = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# s2 = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
 

# plt.subplot(2, 1, 1)
# plt.plot(t, s)          #plot with x and y axes
# plt.ylabel('Value')
# plt.title('First chart')
# plt.grid(True)
 
# plt.subplot(2, 1, 2)
# plt.plot(t, s2)
# plt.xlabel('Item (s)')
# plt.ylabel('Value')
# plt.title('Second chart')
# plt.grid(True)
# plt.show()