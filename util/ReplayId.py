import pathlib
import glob

import pysc2
import pysc2.lib.units # Not included in pysc2 import

import util

replays = util.StrIdMap()
SC_DIR = "C:\Program Files (x86)\StarCraft II"
replayDir = pathlib.Path( SC_DIR ) / "Replays"
replayPattern = str( replayDir / "*.SC2Replay" )
replayFiles = glob.glob( replayPattern )
replayNames = [ pathlib.Path( f ).name for f in replayFiles ]
for iReplay, replayName in enumerate( replayNames ):
    replays[ iReplay ] = replayName

