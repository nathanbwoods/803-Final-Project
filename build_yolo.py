import os
import pathlib
import pandas as pd
import pickle
from absl import app
import numpy as np
import cv2
import pybboxes as pbx

from homography import Transformer
import HarvestAgent
from UnitId import sc_to_enumerate


YOLO_DIR = 'labels'
IMG_DIR = 'images'
VAL_OUTPUT_DIR = 'validation_boxes'


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


def imageDir():
    imageDir = pathlib.Path(IMG_DIR)
    return imageDir


def imagePath(fileName):
    fileName = os.path.splitext(fileName)[0] + '.png'
    filePath = imageDir() / fileName
    return filePath


def outputDir():
    return  pathlib.Path(VAL_OUTPUT_DIR)


def outputPath(fileName):
    fileName = os.path.splitext(fileName)[0] + '.png'
    return outputDir() / fileName


def val_boxes(yolo_data, image_path, output_path):
    print(F"Validating boxes using {image_path}, output to {output_path}")
    img = cv2.imread(str(image_path))

    for box in yolo_data.tolist():
        if 0 < box[3] and 0 < box[4]:
            b = pbx.YoloBoundingBox(box[1], box[2], box[3], box[4], img.shape[0:2])
            b = pbx.convert_bbox(b, to_type="voc")
            cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 1)

    cv2.imwrite(str(output_path), img)


def convert_truth(replay_num, transformer, val_output_frequency=1000):

    fileDir = yoloDir(replay_num)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)

    out_dir = outputDir()
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for ind, truth_file in enumerate(os.listdir(truthDir(replay_num))):
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
        truth['w'] = truth['radius'] * transformer.x_scale * 2
        truth['h'] = truth['radius'] * transformer.y_scale * 2

        # scId -> enumerated id
        truth['ind_type'] = truth['sc_type'].map(sc_to_enumerate)

        # cull non-coplanar units
        # truth.drop(truth[truth['pos.z'] < 8].index, inplace=True)
        #
        # truth.drop(truth[truth['pos.z'] > 14].index, inplace=True)


        # Output the data
        yolo_data = truth[['ind_type', 'u', 'v', 'w', 'h']].values
        col_format = '%d', '%1.6f', '%1.6f', '%1.6f', '%1.6f'
        np.savetxt(yolo_file_path, yolo_data, fmt=col_format)

        # Visualize validation boxes
        if val_output_frequency and ind % val_output_frequency == 0:
            print(truth_path)
            img_path = imagePath(truth_filename)
            vis_output_path = outputPath(truth_filename)
            val_boxes(yolo_data, img_path, vis_output_path)


def main(unused):

    with open("./transformer.pickle", 'rb') as f:
        transformer = pickle.load(f)

    for dir in os.listdir(HarvestAgent.TRUTH_DIR):
        print(F"Converting {dir}")
        convert_truth(dir, transformer)


if __name__ == "__main__":
    app.run(main)