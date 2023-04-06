import matplotlib.pyplot as plt
from CellTracker import analyses

path_raw = ".\\worm1\\raw_data\\Raw_t%04i_z%04i.tif"
path_tracked = ".\\worm1\\track_results_SingleMode\\track_results_t%04i_z%04i.tif"
volume_num = int(input('enter volume numbers(T value): ')) 
layer_num = int(input('enter layer numbers(Z value): '))

signals = analyses.get_signals(path_raw, path_tracked, volume_num, layer_num)

fig,axes = analyses.draw_signals(signals)

plt.savefig(".\\cell_trace\\signal_extraction.png")
plt.show()