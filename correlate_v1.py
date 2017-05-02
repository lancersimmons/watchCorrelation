import os, re, datetime

heart_rate = []
count = 0
start_time = datetime.datetime.strptime("2017-04-30 15:56:00", "%Y-%m-%d %H:%M:%S")
actual_start_time = datetime.datetime.strptime("2017-04-30 15:56:00", "%Y-%m-%d %H:%M:%S")
end_time = datetime.datetime.strptime("2017-04-30 16:38:00", "%Y-%m-%d %H:%M:%S")
with open("Lance's_Data.csv") as file1:
	for line in file1:
		temp = re.split(",", line)
		t = datetime.datetime.strptime(temp[0], "%Y-%m-%d %H:%M:%S")
		if start_time < t < end_time:
			if count == 0:
				actual_start_time = t
			else:
				delta = t - actual_start_time
				temp[0] = delta.seconds
				temp[1] = float(temp[1][:-1])
					
				heart_rate.append(temp)				
		count += 1

#for items in heart_rate:
#	print(items)
acc_data = []#1
gyro_data = []#4
count = 0
start_time = 0
with open("sony_watch.txt") as file1:
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
			
		count += 1
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
		x += acc_data[count][3]
		y += acc_data[count][4]
		z += acc_data[count][5]
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
		x += gyro_data[count][3]
		y += gyro_data[count][4]
		z += gyro_data[count][5]
		count += 1
	temp_var.append(x/(count-past_count-1)) 
	temp_var.append(y/(count-past_count-1))
	temp_var.append(z/(count-past_count-1)) 
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
	final_data.append(temp)  # 1st col is time elapsed, 2-4 are x,y,z of accelerometer, 5-7 are x,y,z of gyroscope, 8 is heart rate 
#print(count, len(gyro_data), acc_count, len(acc_data))
