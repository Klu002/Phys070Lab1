import csv
import pandas as pd
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt

def get_accelerometer_info(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        # only collects data from when acceleration is less than -9, this is when the object is free falling
        start_read = False
        tot_accel = 0
        num_rows = 0
        min_g = float('inf')
        max_g = float('-inf')
        z_list = []
        x_list = []
        max_x_accel = float('-inf')
        max_z_accel = float('-inf')
        g_list = []
        t_list = []
        next(csv_reader)
        for row in csv_reader:
            if start_read and float(row[2]) < -9.5:
                tot_accel += float(row[2])
                num_rows += 1
                z_list.append(float(row[3]))
                x_list.append(float(row[1]))
                g_list.append(float(row[2]))
                t_list.append(float(row[0]))
                # Check max and min
                if min_g > float(row[2]):
                    min_g = float(row[2])
                if max_g < float(row[2]):
                    max_g = float(row[2])
                if max_x_accel < float(row[1]):
                    max_x_accel = float(row[1])
                if max_z_accel < float(row[3]):
                    max_z_accel = float(row[3])
            elif float(row[2]) < -9.5:
                start_read = True
                start_time = float(row[0])
            elif float(row[2]) > -9.5 and start_read:
                end_time = float(row[0])
                break

        delta_time = end_time - start_time
        avgg = tot_accel/num_rows
        stddev = np.std(g_list)
    return {'delta_time': delta_time, 'tot_g': tot_accel, 'num_rows': num_rows, 'x_list': x_list, 'z_list': z_list,
            'min_g': min_g, 'max_g': max_g, 'max_x': max_x_accel, 'max_z': max_z_accel, 'avgg': avgg,
            'avgx': sum(x_list)/num_rows, 'avgz': sum(z_list)/num_rows, 'stdev': stddev, 'g_list': g_list,
            't_list': t_list}


def perfect_g(height, time):
    g = -2*height / (time*time)
    return g


def print_exp_g(height, times):
    trials = []
    for t in times:
        trials.append(perfect_g(height, t))
    avgg = sum(trials) / len(trials)
    print("Calculated g per trial")
    print(trials)
    print("Average g")
    print(avgg)
    print(np.std(trials))
    return trials


def plot_accel_data(file_list, accel_direction, trial=None):
    trial_num = 0
    if trial is None:
        for file in file_list:
            trial_num += 1
            accel_data = get_accelerometer_info(file)
            y_axis = accel_data[accel_direction]
            x_axis = accel_data['t_list']
            t_init = x_axis[0]
            x_axis = [t - t_init for t in x_axis]
            plt.plot(x_axis, y_axis, label='Trial '+str(trial_num))
        plt.ylabel("Vertical Acceleration (m/s^2)")
        plt.xlabel('Time Elapsed In Free Fall (s)')
    else:
        accel_data = get_accelerometer_info(file_list[trial - 1])
        y_axis_g = accel_data['g_list']
        y_axis_x = accel_data['x_list']
        y_axis_z = accel_data['z_list']
        x_axis = accel_data['t_list']
        t_init = x_axis[0]
        x_axis = [t - t_init for t in x_axis]
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Time Elapsed In Free Fall (s)')
        ax1.set_ylabel("Vertical Acceleration (m/s^2)", color=color)
        ax1.plot(x_axis, y_axis_g, color=color,label='Y Acceleration')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Non Vertical Acceleration(m/s^2)', color=color)
        ax2.plot(x_axis, y_axis_z, color=color, label="Z Acceleration")
        ax2.plot(x_axis, y_axis_x, color='green', label="X Acceleration")
        ax2.tick_params(axis='y', labelcolor=color)
        plt.title("Trial " + str(trial))

    plt.legend()
    plt.show()

def display_accelerometer_info(file_list):
    dtime_list = []
    avgg_list = []
    tot_z = 0
    tot_x = 0
    tot_accel = 0
    tot_rows = 0
    data = []
    for file in filelist:
        accel_info = get_accelerometer_info(file)
        accel_info.pop('g_list', None)
        accel_info.pop('x_list', None)
        accel_info.pop('z_list', None)
        accel_info.pop('t_list', None)
        data.append(accel_info)
        avgg_list.append(accel_info['tot_g'] / accel_info['num_rows'])
        dtime_list.append(accel_info['delta_time'])
        tot_accel += accel_info['tot_g']
        tot_rows += accel_info['num_rows']
    df = pd.DataFrame(data)
    print("***Accelerometer***")
    print("overall average g")
    print(tot_accel / tot_rows)
    print(tabulate(df, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    filelist = ['RawData.csv', 'RawData1.csv', 'RawData2.csv', 'RawData3.csv', 'RawData4.csv']
    tape_measure_short = [0.399, 0.396, 0.393, 0.400, 0.391]
    tape_measure_long = [0.504, 0.511, 0.531, 0.51, 0.512]
    tape_short_height = .75
    tape_long_height = 1.197
    print_exp_g(tape_short_height, tape_measure_short)
    print_exp_g(tape_long_height, tape_measure_long)
    plot_accel_data(filelist, 'g_list')
    plot_accel_data(filelist, 'g_list', trial=1)
    display_accelerometer_info(filelist)

