# 3DeeCellTracker
[![PyPI](https://img.shields.io/pypi/v/3DeeCellTracker)](https://pypi.org/project/3DeeCellTracker/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/3DeeCellTracker)](https://pypi.org/project/3DeeCellTracker/) [![GitHub](https://img.shields.io/github/license/WenChentao/3DeeCellTracker)](https://github.com/WenChentao/3DeeCellTracker/blob/master/LICENSE)
[![Youtube](https://img.shields.io/badge/YouTube-Demo-red)](https://www.youtube.com/watch?v=ctt6o3DY2bA&list=PLGY0oNQomrHERP08iEj-MsluFW8xQJujP)

## 3DCT_for_PKU_LDG:

**3DCT_for_PKU_LDG** is modified from **3DeeCellTracker** for Luo_lab fly transcriptional signal extraction.

**Modifications include:**
- CellTracker/unet3d.py line 36: change "inputs = Input((160,160,16,1))" to "inputs = Input((80,80,8,1))". **Luo-lab pic size is 460*157, smaller than 160**
- CellTracker/tracker.py line 1258: change "self.segresult.r_corrdinates_segment, 20" to "self.segresult.r_corrdinates_segment, 5" **Luo-lab cell number per volume is less than 20. Note that the ffn model should also be updated accordingly**
- CellTracker/analyses.py line 15-88: define a get_signals function. **Used for singal extraction**
- CellTracker/tracker.py line 752: add "self.raw_data = _make_folder(os.path.join(folder_path, "raw_data/"))" to create a folder for storing raw data **We didnt pre-align the raw data, so we use raw_data folder to store these images, the reason is to keep the orginal folder structure(using the data folder for aligned data)**
- CellTracker/tracker.py line 753: add "self.cell_trace = _make_folder(os.path.join(folder_path, "cell_trace/"))" to create a folder for storing final cell traces **The folder is used for storing final results**
- Examples/signal_extraction.ipynb: a jupyter notebook file for signal extraction.
- Examples/single_mode_worm1-clear.ipynb: set Tacker() default parameter " image_name="Den_t%03i_z%03i.tif" " **Denoised data for better segmentation and tracking result**
- 3DCT.yml line 18: comment out to create a conda env which can be installed with modified site package (CellTracker).
---

**3DeeCellTracker** is a deep-learning based pipeline for tracking cells in 3D time lapse images of deforming/moving organs ([eLife, 2021](https://elifesciences.org/articles/59187)).


## Updates:

**3DeeCellTracker v0.4.5 was released with following issues fixed (2022.06.03)**
- Solved an activity load bug.

## Installation

* Create a conda environment for a PC with GPU including prerequisite packages using the 3DCT.yml file:

```console
$ conda env create -f 3DCT.yml
```

* (NOT RECOMMEND) Users can create a conda environment for a PC with only CPU, but it will be slow and may fail.
```console
$ conda env create -f 3DCT-CPU.yml
```

* Install the 3DeeCellTracker package solely by pip

```console
$ pip install 3DeeCellTracker
```

* Update the 3DeeCellTracker package to the latest version

```console
$ pip install --upgrade 3DeeCellTracker
```

For detailed instructions, see [here](Doc/Enviroment.md).
## Quick Start
To learn how to track cells use 3DeeCellTracker, see following notebooks for examples:
1. Track cells in deforming organs: 
    - [**Single mode (clear notebook)**](Examples/single_mode_worm1-clear.ipynb);
    - [**single mode (results)**](https://wenchentao.github.io//3DeeCellTracker/Examples/single_mode_worm1.html)


2. Track cells in freely moving animals: 
    - [**Ensemble mode (clear notebook)**](Examples/ensemble_mode_worm4-clear.ipynb)
    - [**Ensemble mode (results)**](https://wenchentao.github.io//3DeeCellTracker/Examples/ensemble_mode_worm4.html)


3. Train a new 3D U-Net for segmenting cells in new optical conditions: 
    - [**Train 3D U-Net (clear notebook)**](Examples/3D_U_Net_training-clear.ipynb).
    - [**Train 3D U-Net (results)**](https://wenchentao.github.io//3DeeCellTracker/Examples/3D_U_Net_training.html).
   
The data and model files for demonstrating above notebooks can be downloaded [**here**](https://osf.io/dt76c/).

**Note**: Codes above were based on the latest version. 
For old programs used in eLife 2021, please check the "[**Deprecated_programs**](Deprecated_programs)" folder.

## A frequently reported issue and its solution
Multiple users have reported that when running the tracker.match() 
function, a ValueError of shape mismatch occurs. And they were 
discovered to be the result of an incorrect setting of _siz_xyz_, 
which should be (height, width, depth) of the 3D image. 
If you encounter the same error, please double-check that it is 
correctly set.

## Video Tutorials
We have made tutorials explaining how to use our software. See links below (videos in Youtube):

[Tutorial 1: Install 3DeeCellTracker and train the 3D U-Net](https://www.youtube.com/watch?v=ctt6o3DY2bA)

[Tutorial 2: Tracking cells by 3DeeCellTracker](https://www.youtube.com/watch?v=KZ03Y8u8UK0)

[Tutorial 3: Annotate cells for training 3D U-Net](https://www.youtube.com/watch?v=ONSOLJQaq28)

[Tutorial 4: Manually correct the cell segmentation](https://www.youtube.com/watch?v=e7xWaccH63o)

## A Text Tutorial 
We have wrote a tutorial explaining how to install and use 3DeeCellTracker. See [Bio-protocol, 2022](https://bio-protocol.org/e4319)

## How it works
We designed this pipeline for segmenting and tracking cells in 3D + T images in deforming organs. The methods have been explained in [Wen et al. bioRxiv 2018]( https://doi.org/10.1101/385567) and in [Wen et al. eLife, 2021](https://elifesciences.org/articles/59187).

**Overall procedures of our method** ([Wen et al. eLife, 2021–Figure 1](https://elifesciences.org/articles/59187/figures#content))

<img src="https://iiif.elifesciences.org/lax:59187%2Felife-59187-fig1-v1.tif/full/1500,/0/default.jpg" width="400">

**Examples of tracking results** ([Wen et al. eLife, 2021–Videos](https://elifesciences.org/articles/59187/figures#content))

| [Neurons in a ‘straightened’ <br />freely moving worm](https://static-movie-usa.glencoesoftware.com/mp4/10.7554/5/4ce9eaa4a84bf7847c99c81a13ccafd797b40218/elife-59187-fig6-video1.mp4)| [Cardiac cells in a zebrafish larva](https://static-movie-usa.glencoesoftware.com/mp4/10.7554/5/4ce9eaa4a84bf7847c99c81a13ccafd797b40218/elife-59187-fig7-video2.mp4) | [Cells in a 3D tumor spheriod](https://static-movie-usa.glencoesoftware.com/mp4/10.7554/5/4ce9eaa4a84bf7847c99c81a13ccafd797b40218/elife-59187-fig8-video2.mp4) |
| ------------- | ------------- | ------------- | 
| <img src="https://user-images.githubusercontent.com/27986173/115169952-63b4e600-a0fa-11eb-9b85-91292bc9d419.gif" width="340">| <img src="https://user-images.githubusercontent.com/27986173/115170418-90b5c880-a0fb-11eb-9382-13690c3375dc.gif" width="400">| <img src="https://user-images.githubusercontent.com/27986173/115170434-9ad7c700-a0fb-11eb-9004-2e4cff86f7ab.gif" width="200">|


## Citation

If you used this package in your research and is interested in citing it here's how you do it:

```
@article{
author = {Wen, Chentao and Miura, Takuya and Voleti, Venkatakaushik and Yamaguchi, Kazushi and Tsutsumi, Motosuke and Yamamoto, Kei and Otomo, Kohei and Fujie, Yukako and Teramoto, Takayuki and Ishihara, Takeshi and Aoki, Kazuhiro and Nemoto, Tomomi and Hillman, Elizabeth MC and Kimura, Koutarou D},
doi = {10.7554/eLife.59187},
journal = {eLife},
month = {mar},
title = {{3DeeCellTracker, a deep learning-based pipeline for segmenting and tracking cells in 3D time lapse images}},
volume = {10},
year = {2021}
}
```

## Acknowledgements
We wish to thank **JetBrains** for supporting this project 
with free open source **Pycharm** license.

[![Pycharm Logo](pictures/jetbrains_small.png)](https://www.jetbrains.com/) 
[![Pycharm Logo](pictures/icon-pycharm_small.png)](https://www.jetbrains.com/pycharm/)
