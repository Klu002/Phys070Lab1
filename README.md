# Phys070Lab1
Code used to clean and analyze data for Phys070 Lab1
main.py contains the code used, the rest of the files are csv files containing the raw accelerometer data.
get_accelerometer_info() filters out all data points from when the object is not falling, and returns all related acceleration data in that time frame
as a dictionary
display_accelerometer_info() displays the information from get_accelerometer_info() as a dataframe
plot_accel_data() creates plots using the acceleration data from get_accerlerometer_info()
