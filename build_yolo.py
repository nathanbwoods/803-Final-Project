import os
import pathlib
import pandas as pd
import pickle
from absl import app
import numpy as np

import HarvestAgent
from UnitId import sc_to_enumerate


YOLO_DIR = 'labels'


def truthDir(replayNum):
    fileDir = pathlib.Path( HarvestAgent.TRUTH_DIR ) / replayNum
    return fileDir


def truthPath( replayNum, file_name ):
    filePath = truthDir( replayNum ) / file_name
    return filePath


def yoloDir(replayNum):
    fileDir = pathlib.Path(YOLO_DIR)
    return fileDir


def yoloPath(replayNum, fileName):
    fileName = os.path.splitext(fileName)[0] + '.txt'
    filePath = yoloDir(replayNum) / fileName
    return filePath


def convert_truth(replay_num, transformer):

    fileDir = yoloDir(replay_num)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)

    for truth_file in os.listdir(truthDir(replay_num)):
        truth_filename = os.fsdecode(truth_file)
        truth_path = truthPath(replay_num, truth_filename)
        yolo_file_path = yoloPath(replay_num, truth_filename)

        truth = pd.read_csv(truth_path)

        # Center observation to camera
        camera = truth.loc[truth['name'] == 'Camera']
        c_x, c_y = float(camera['pos.x']), float(camera['pos.y'])
        truth['pos.x'] -= c_x
        truth['pos.y'] -= c_y

        # Transform to camera plane
        uv = transformer.homography_transform(truth[['pos.x', 'pos.y', 'pos.z']].values)
        truth['u'] = uv[:, 0]
        truth['v'] = uv[:, 1]

        # Drop camera row
        truth.drop(truth[truth['name'] == 'Camera'].index, inplace=True)

        # Scale width and height
        truth['w'] = truth['radius'] * transformer.x_scale
        truth['h'] = truth['radius'] * transformer.y_scale

        # scId -> enumerated id
        truth['ind_type'] = truth['sc_type'].map(sc_to_enumerate)

        # drop units with locations not between 0 and 1
        truth.drop(truth[truth['u'] < 0].index, inplace=True)
        truth.drop(truth[truth['v'] < 0].index, inplace=True)
        truth.drop(truth[truth['u'] > 1].index, inplace=True)
        truth.drop(truth[truth['v'] > 1].index, inplace=True)

        # Output the data
        yolo_data = truth[['ind_type', 'u', 'v', 'w', 'h']].values
        col_format = '%d', '%1.6f', '%1.6f', '%1.6f', '%1.6f'
        np.savetxt(yolo_file_path, yolo_data, fmt=col_format)


def main(unused):

    with open("./transformer.pickle", 'rb') as f:
        transformer = pickle.load(f)

    for dir in os.listdir(HarvestAgent.TRUTH_DIR):
        print(F"Converting {dir}")
        convert_truth(dir, transformer)


if __name__ == "__main__":
    app.run(main)