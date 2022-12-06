import os
import os.path
import pathlib

from pysc2.lib import features
import matplotlib.pyplot as plt

from util import UnitId
import util
from util import ReplayPicTally

TICKS_PER_SCREENSHOT = 100
DOCKET_DIR = 'docket'

def docketName( replayNum ):
    return f"docket_{replayNum:06d}.txt"

def docketPath( replayNum ):
    filePath = pathlib.Path( DOCKET_DIR ) / docketName( replayNum )
    return filePath

class ScoutAgent():
    def __init__(self):
        self.iStep = -1
        self.duration = 1000 # By default, take 10 screenshots.
        self.action_spec = None
        self.intervals = util.ReplayIntervalSet( 0, "Unknown" )

        
    def set( self, num, name, duration ):
        self.intervals.num = num
        self.intervals.name = name
        self.duration = duration


    def step(self, time_step, actions, obs, ctrl ):
        self.iStep += 1
        if self.iStep % 1000 == 0:
            print( f"Step {self.iStep}", end = ',', flush = True)

        units = obs.observation.raw_data.units
        # Camera-visible units only:
        typesFound = {}
        for unit in [ u for u in units if u.is_on_screen ]:
            typesFound[unit.unit_type] = True
        for unit_type in typesFound:
            self.intervals.add( unit_type, self.iStep )


    def finalReport( self ):
        print( self.intervals )


    def pickScreenshots( self, globalTally, picsToTake = None ):
        # By default, 1 pic per 100 ticks.
        if picsToTake is None:
            picsToTake = int( self.duration / TICKS_PER_SCREENSHOT )
        print( f"Taking {picsToTake} pics." )

        # The desired product.
        screenshotTimes = []

        # Just a cache so we don't reprocess.
        replayTally = ReplayPicTally.ReplayPicTally()

        for iPic in range( picsToTake ):
            print( f"Pic {iPic}" )
            leastViewed = globalTally.leastViewed()
            for unit in leastViewed:
                if unit not in self.intervals:
                    continue
                picTime, picVis = self.intervals.random( unit )
                print( f"PicTime {picTime}" )
                screenshotTimes.append( picTime )
                for visible in picVis:
                    replayTally.add( visible )
                    globalTally.add( visible )
                break
        replayTally.save( self.intervals.num )

        self.writeScreenshots( screenshotTimes )
        print( f"Local Tally: {replayTally}" )
        print( f"Global Tally: {globalTally}" )
        


    def writeScreenshots( self, screenshotTimes ):
        if not os.path.exists( DOCKET_DIR ):
            os.makedirs( DOCKET_DIR )
        fileName = pathlib.Path( DOCKET_DIR ) / f"docket_{self.intervals.num:06d}.txt"
        with open( fileName, 'w' ) as f:
            f.writelines( [ f"# {self.intervals.num}, {self.intervals.name}\n" ] )
            for screenshotTime in sorted( screenshotTimes ):
                f.writelines( [ f"{screenshotTime}\n" ] )
        
        
#dir(time_step)
#time_step.observation.keys() #NamedDict
#time_step.observation.feature_screen._index_names #NamedNumpyArray
