#! /usr/bin/env python

# Standard imports
import glob
import pathlib
import tqdm

# PySC2-related imports
import pysc2
import pysc2.lib.units # Not included in pysc2 import
import pysc2.run_configs

from absl import flags, app
FLAGS = flags.FLAGS
flags.DEFINE_string("replay", None, "Path to a replay file.")
flags.DEFINE_string("agent", None, "Path to an agent.")

# Local project imports
import util

SC_DIR = "/home/schulzew/Classes/Project/StarCraftII"
MIN_GOOD_TICKS = 1000

# Using SC2 numbering
CORE_UNITS = []

def main( unused_argv ):
    # Generate a directory of all the replays and map them to integers.
    replays = util.StrIdMap()
    
    replayDir = pathlib.Path( SC_DIR ) / "Replays"
    replayPattern = str( replayDir / "*.SC2Replay" )
    replayFiles = glob.glob( replayPattern )
    # import pdb; pdb.set_trace()
    # Filter for good replays.
    goodFiles = []
    poorReplays = 0
    errorReplays = 0
    
    sc2config = pysc2.run_configs.get()
    sc2controller = sc2config.start().controller
    for iReplay, replayFile in enumerate( replayFiles ):
        print( iReplay )
        try:
            replayData = sc2config.replay_data( replayFile )
            if sc2controller.replay_info( replayData ).game_duration_loops > MIN_GOOD_TICKS:
                goodFiles.append( replayFile )
            else:
                poorReplays += 1
        except pysc2.lib.remote_controller.RequestError as e:
            errorReplays += 1

    print( f"Corrupt: {errorReplays}, Poor: {poorReplays}, Good: {len( goodReplays )}" )
            
    replayNames = [ pathlib.Path( f ).name for f in goodFiles ]
    for iReplay, replayName in enumerate( replayNames ):
        replays[iReplay] = replayName

    # Generate a directory of units.
    unitsSc = util.StrIdMap() # 259 units numbered up to 1961
    unitsMl = util.StrIdMap() # With 0-to-258 numbering
    for unitList in [ pysc2.lib.units.Protoss,
                      pysc2.lib.units.Terran,
                      pysc2.lib.units.Zerg,
                      pysc2.lib.units.Neutral ]:
        for enum in unitList:
            unitsSc[enum.numerator] = enum.name
    for iUnit, scId in enumerate( unitsSc ):
        unitName = unitsSc[scId]
        unitsMl[iUnit] = unitName


    print( unitsSc )
    print( unitsMl )

    for key in sorted( unitsSc.keys() ):
        print( f"{key}, #{unitsSc[key]}" )


if __name__ == "__main__":
    app.run( main )
