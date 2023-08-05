# calibcam
A charuco based calibrator for camera setups (intrinsic and extrinsic coordinates).

# Installation

## Windows

1. (If not already done:) [Install Anaconda](https://docs.anaconda.com/anaconda/install/windows/)
2. Clone git@github.com:bbo-lab/calibcam.git 
3. Open Anaconda prompt via Start Menu
4. Using `cd` and `dir`, navigate to the calibcam directory INSIDE the repository (which may also be named calibcam)
5. Create conda environment using `conda env create -f environment.yml`
6. Switch to multitrackpy environment: `conda activate calibcam`
7. Navigate to repository (folder containing setup.py) and install via: `pip install .`


# Usage

## Windows

1. From `[repository]/calibcam/boards`, copy the appropriate board into the calibration video directory and rename to `board.npy`
2. Open Anaconda prompt via Start Menu
3. Switch to calibcam environment: `conda activate calibcam`
4. Run the program with `python -m calibcam`
5. In GUI, click "Perform calibration"
6. Select all calibration videos
7. After calibration, check reprojection in GUI
8. Run `multicalibration_matlab_mcl_gen.m` in the video directory in MATLAB
9. Save resulting mcl file into video directory

Alternatively, run purely commandline based with
```
$ python -m calibcam --help
usage: __main__.py [-h] [--videos [VIDEOS [VIDEOS ...]]] [--board BOARD]

Calibrate set of cameras

optional arguments:
  -h, --help            show this help message and exit
  --videos [VIDEOS [VIDEOS ...]]
  --board BOARD
```
