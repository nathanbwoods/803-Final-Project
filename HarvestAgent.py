import os
import os.path
import pathlib
import csv

from pysc2.lib import features, actions
import matplotlib.pyplot as plt

from util import UnitId
import util
from util import ReplayPicTally

# Where the raw ground truth CSVs go.
TRUTH_DIR = 'truth'
# Where the rgb_screen captures go.
SCREEN_DIR = 'screen'


def truthDir( replayNum ):
    fileDir = pathlib.Path( TRUTH_DIR ) / f"r{replayNum:06d}"
    return fileDir


def truthFile ( replayNum, step ):
    fileName = f"truth_r{replayNum:06d}_t{step:06d}.csv"
    return fileName


def truthPath( replayNum, step ):
    filePath = truthDir( replayNum ) / truthFile( replayNum, step )
    return filePath

def screenDir(replayNum):
    fileDir = pathlib.Path(SCREEN_DIR) / f"r{replayNum:06d}"
    return fileDir

def screenFile ( replayNum, step ):
    fileName = f"truth_r{replayNum:06d}_t{step:06d}.png"
    return fileName

def screenPath( replayNum, step ):
    filePath = screenDir( replayNum ) / screenFile( replayNum, step )
    return filePath


class HarvestAgent():
    def __init__(self):
        self.action_spec = actions.ActionSpace.RAW


    def set( self, num : int ):
        """Replay number; used for ground truth."""
        self.num = num


    def step(self, time_step, obs ):
        step = int( time_step.observation["game_loop"] )
        self.ground_truth( obs, step )
        # Take picture.

    def ground_truth( self, obs, step : int ) -> None:
        """Write the raw ground truth file."""
        units = obs.observation.raw_data.units
        cameraPosRaw = obs.observation.raw_data.player.camera

        fileDir = screenDir( self.num )
        if not os.path.exists( fileDir ):
            os.makedirs( fileDir )
        filePath = screenPath( self.num, step )

        rgb_screen = features.Feature.unpack_rgb_image(obs.observation.render_data.map)

        plt.imsave(filePath, rgb_screen)

        fileName = screenFile( self.num, step )
        print( f"Done writing png {fileName}." )
        
        csvRows = [ [ "name",
                      "sc_type",
                      "ml_type",
                      "owner",
                      "pos.x",
                      "pos.y",
                      "pos.z",
                      "radius",
                      "is_on_screen" ] ]
        csvRows.append( [ "Camera", "-1", "-1", "-1",
                          cameraPosRaw.x,
                          cameraPosRaw.y,
                          cameraPosRaw.z,
                          "-1",
                          "False" ] )
            
        for unit in units:
            if unit.is_on_screen:
                newRow = [ UnitId.unitsSc[unit.unit_type],
                           unit.unit_type,
                           UnitId.unitsMl[UnitId.unitsSc[unit.unit_type]],
                           unit.owner,
                           unit.pos.x,
                           unit.pos.y,
                           unit.pos.z,
                           unit.radius,
                           unit.is_on_screen ]
                csvRows.append( newRow )

        fileDir = truthDir( self.num )
        if not os.path.exists( fileDir ):
            os.makedirs( fileDir )
        filePath = truthPath( self.num, step )
        with open( filePath, 'w' ) as f:
            csvWriter = csv.writer( f )
            for row in csvRows:
                csvWriter.writerow( row )
        fileName = truthFile( self.num, step )
        print( f"Done writing csv {fileName}." )
                    
        
#dir(time_step)
#time_step.observation.keys() #NamedDict
#time_step.observation.feature_screen._index_names #NamedNumpyArray
