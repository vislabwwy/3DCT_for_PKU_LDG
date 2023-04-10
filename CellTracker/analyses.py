"""
A module for analyses after tracking
Author: Chentao Wen

"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib as mpl

mpl.rcParams["axes.spines.right"] = False
mpl.rcParams["axes.spines.top"] = False

def get_signals(path_raw, path_tracked, volume_num, layer_num): # vislabwwy: used for pku-ldg-lab
    """
    Get transcription signals of all cells

    Parameters
    ----------
    path_raw : str
        The path of the images for extracting signals
    path_tracked : str
        The path of the tracked labels
    volume_num : int
        The number of the volumes
    layer_num : int
        the number of layers in the raw images and the tracked labels

    Returns
    -------
    signals : numpy.ndarray
        The extracted signals with shape (volume, label)
    """
    images_label, images_raw = _read_image(1, layer_num, path_raw, path_tracked)
    cell_num = np.max(images_label)
    signals = np.zeros((volume_num, cell_num))
    max_loc = np.zeros((volume_num, cell_num,4))
    for frame in range(1, volume_num + 1):

        print("t=%i"%frame, end="\r")

        # read raw images and labels
        if frame>=2:
            images_label, images_raw = _read_image(frame, layer_num, path_raw, path_tracked)

        # calculate transcription signals of each cell
        for label in range(1, cell_num + 1):
            # make a mask of each label
            label_i = np.copy(images_label)
            label_i[np.where(label_i!=label)]=0

            # extract raw intensities of the label
            signals_i = images_raw*label_i/label
            # calculate wanted singals (modify the fomula here if needed)
            # find the position of the maximum vale (depth,height,width)
            max_pos = np.where(signals_i==np.max(signals_i))
            # center of multiple points
            depth = int(np.floor(np.mean(max_pos[0])))
            height = int(np.floor(np.mean(max_pos[1])))
            width = int(np.floor(np.mean(max_pos[2])))
            mean = (depth+height+width)/3

            # signal area summation 1*5*5
            detected_signals = np.sum(signals_i[depth,height-2:height+3,width-2:width+3])                  
            # background summation 1*15*15
            background_signals = np.sum(signals_i[depth,height-7:height+8,width-7:width+8])
            # signal correction
            signal_area = 25 # 1*5*5
            background_area = 225 # 1*15*15
            mean_bg = (background_signals - detected_signals)/(background_area - signal_area)
            corrected_signals = detected_signals - (mean_bg * signal_area) 

            # store value in signals array
            signals[frame-1, label-1] = corrected_signals
            max_loc[frame-1, label-1] = (depth,height,width,mean)

            # save the label image for cell location
            label_i[np.where(label_i==label)]=255
            label_i[:,height,width]=0
            max_projection_i = np.max(label_i,axis = 0)
            cv2.imwrite("./cell_trace/cell_%i_%i.png" %(label,frame),max_projection_i)
    # save separate csv file for each cell
    np.savetxt("./cell_trace/signal.txt",signals,delimiter=',')
    for label in range(1, cell_num + 1):
        np.savetxt("./cell_trace/cell_%i.txt"%label,signals[:,label-1],delimiter=',')
        np.savetxt("./cell_trace/max_loc_%i.txt"%label,max_loc[:,label-1],delimiter=',')
    return signals

def get_activities(path_raw, path_tracked, volume_num, layer_num):
    """
    Get activities of all cells

    Parameters
    ----------
    path_raw : str
        The path of the images for extracting activities
    path_tracked : str
        The path of the tracked labels
    volume_num : int
        The number of the volumes
    layer_num : int
        the number of layers in the raw images and the tracked labels

    Returns
    -------
    activities : numpy.ndarray
        The extracted activities with shape (volume, label)
    """
    images_label, images_raw = _read_image(1, layer_num, path_raw, path_tracked)
    cell_num = np.max(images_label)
    activities = np.zeros((volume_num, cell_num))
    discard_ratio = 0.1
    for frame in range(1, volume_num + 1):

        print("t=%i"%frame, end="\r")

        # read raw images and labels
        if frame>=2:
            images_label, images_raw = _read_image(frame, layer_num, path_raw, path_tracked)

        # calculate mean intensities of each cell of top 90% area
        for label in range(1, cell_num + 1):
            intensity_label_i = images_raw[images_label==label]
            threshold = np.floor(np.size(intensity_label_i) * discard_ratio).astype(int)
            sorted_intensity_idx = np.argsort(intensity_label_i)
            activities[frame-1, label-1] = np.mean(intensity_label_i[sorted_intensity_idx[threshold:]])
    return activities


def _read_image(frame, layer_num, path_raw, path_tracked):
    """Read 3D images of raw activities and tracked labels"""
    images_raw = []
    images_label = []
    for z in range(1, layer_num + 1):
        images_raw.append(cv2.imread(path_raw % (frame, z), -1))
        images_label.append(cv2.imread(path_tracked % (frame, z), -1))
    images_raw = np.array(images_raw)
    images_label = np.array(images_label)
    return images_label, images_raw


def optimize_row_column(duration, n_signals, figsize):
    """
    Return the proper number of row, column for visualization

    Parameters
    ----------
    duration : int
        Number of time points for each signal.
    n_signals : int
        Number of signals.
    figsize : tuple
        size of the figure to show activities

    Returns
    -------
    row_n : int
        Number of row
    column_n : int
        Number of column

    Notes
    -----
    The row_n and colume_n are designed to make sure the xy_ratio of each subplot propotional with duration.

    Examples
    --------
    >>> optimize_row_column(duration=200, n_signals=100, figsize=(40, 20))
    (14, 8)
    """
    width_hight_ratio = figsize[0]/figsize[1]
    total_length = duration * n_signals
    row_n = int((total_length / (50 * width_hight_ratio)) ** 0.5)
    column_n = int(np.ceil(n_signals / row_n))
    return row_n, column_n


def draw_signals(signals, ylim_upper=None, ylim_lower=None, figsize=(40, 20)):
    """
    Draw signals in multiple subplots

    Parameters
    ----------
    signals : numpy.ndarray
        N Signals with T time points with shape (T, N)
    ylim_upper : float
        ylim upper bound. If None, set it to the highest value.
    ylim_lower : float
        ylim lower bound. If None, set it to the lowest value.
    figsize : tuple
        Size of the figure

    Returns
    -------
    fig : matplotlib.figure
    axes : array of matplotlib.axes.Axes
    """
    row_n, column_n = optimize_row_column(signals.shape[0], signals.shape[1], figsize)
    fig, axes = plt.subplots(row_n, column_n, figsize=figsize)
    for row in range(row_n):
        for column in range(column_n):
            n = row * column_n + column
            if n >= signals.shape[1]:
                break
            axes[row, column].plot(signals[:, n], lw=2)
            upper_sig_n, lower_sig_n = np.nanmax(signals[:, n]), np.nanmin(signals[:, n])
            if ylim_upper is not None:
                upper_sig_n = ylim_upper
            if ylim_lower is not None:
                lower_sig_n = ylim_lower
            axes[row, column].set_ylim(lower_sig_n, upper_sig_n)
            axes[row, column].set_title("N%d" % (n + 1), va="top")
            if row<row_n-1:
                axes[row, column].get_xaxis().set_visible(False)
    plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98, wspace=0.2, hspace=0.2)
    return fig, axes
