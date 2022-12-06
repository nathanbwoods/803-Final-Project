#! /usr/bin/env python

# Standard imports
import glob
import pathlib
import tqdm

# PySC2-related imports
from pysc2.env.environment import TimeStep, StepType
import pysc2
import pysc2.lib.units # Not included in pysc2 import
import pysc2.run_configs
from s2clientprotocol import sc2api_pb2 as sc_pb

from absl import flags, app
flags.DEFINE_string("replay", None, "Path to a replay file.")
flags.DEFINE_string("agent", "ObserverAgent.ObserverAgent", "Path to an agent.")
FLAGS = flags.FLAGS

# Local project imports
import util

SC_DIR = "/home/schulzew/Classes/Project/StarCraftII"
MIN_GOOD_TICKS = 1000

# Using SC2 numbering
CORE_UNITS = []

def main( unused_argv ):
    # Generate a directory of all the replays and map them to integers.
    replays = util.StrIdMap()
    FLAGS.sc2_timeout = 10
    
    replayDir = pathlib.Path( SC_DIR ) / "Replays"
    replayPattern = str( replayDir / "*.SC2Replay" )
    replayFiles = glob.glob( replayPattern )

    # Filter for good replays.
    goodFiles = []
    poorReplays = 0
    errorReplays = 0

    sc2config = pysc2.run_configs.get()
    sc2controller = sc2config.start().controller
    import pdb; pdb.set_trace()
    for iReplay, replayFile in enumerate( replayFiles ):
        print( iReplay )
        replayData = sc2config.replay_data( replayFile )
        ticks = sc2controller.replay_info( replayData ).game_duration_loops
        print( f"Ticks: {ticks}" )

            # print( replayFile, ticks )
            # if ticks > MIN_GOOD_TICKS:
            #     goodFiles.append( replayFile )
            # else:
            #     poorReplays += 1
        #except pysc2.lib.remote_controller.RequestError as e:
        # except Exception as e:
        #     errorReplays += 1

    print( f"Corrupt: {errorReplays}, Poor: {poorReplays}, Good: {len( goodReplays )}" )
            
    replayNames = [ pathlib.Path( f ).name for f in goodFiles ]
    for iReplay, replayName in enumerate( replayNames ):
        replays[iReplay] = replayName


if __name__ == "__main__":
    app.run( main )


