# python_live_plot.py

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

color1 = 'tab:red'
color2 = 'tab:blue'

def animate(i):
    data = pd.read_csv(sys.argv[1], parse_dates=['Timestamp (ISO 8601)'])
    t = data['Timestamp (ISO 8601)'].values
    U = data['Voltage / V'].values
    I = data['Current / A'].values
    CCAP = data['CCAP / mAh'].values
    DCAP = data['DCAP / mAh'].values
    CAP = [c if m=="Charge" else c-d for (m, c, d) in zip(data['Mode'].values,data['CCAP / mAh'].values,data['DCAP / mAh'].values)]
    slot = data['Slot'].values
    
    ax1 = plt.subplot(211)
    ax1.cla()
    ax1.plot(t, U, color=color1)
    ax1.set_ylabel('U / V', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    plt.gcf().canvas.manager.set_window_title(slot[-1]);
    plt.gcf().suptitle("Mode:"+data['Mode'].values[-1]);
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('I / A', color=color2)  # we already handled the x-label with ax1
    ax2.plot(t, I, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    ax3 = plt.subplot(212, sharex=ax1)
    ax3.cla()
    ax3.plot(t, CAP)
    ax3.set_ylabel('Q / mAh')
    ax3.tick_params(axis='y')
    ax3.set_xlabel('Timestamp')

    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    
ani = FuncAnimation(plt.gcf(), animate, 5000)

plt.show()
