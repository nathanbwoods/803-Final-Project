#! /usr/bin/env python

from matplotlib import pyplot as plt

# Local imports
import util
from util import GlobalPicTally, ReplayPicTally
from util import ReplayId
from util import UnitId

globalPicTally = GlobalPicTally.GlobalPicTally()
if GlobalPicTally.exists():
    globalPicTally = GlobalPicTally.load()
    
for iReplay in ReplayId.replays:
    if ReplayPicTally.exists( iReplay ):
        print( f"Loading Tally from: {ReplayId.replays[iReplay]}" )
        replayTally = ReplayPicTally.load( iReplay )
        globalPicTally.loadReplayTally( replayTally )

results = list( globalPicTally.pics.items() )
results.sort( key = lambda r: r[1] )
for result in results:
    print( result[0], UnitId.unitsSc[result[0]], result[1] )


y = [ result[1] for result in reversed( results ) ]    
x = [ i / len( y ) for i in range( len( y ) ) ]
fig, ax = plt.subplots()
ax.semilogy( x, y )
ax.grid()
ax.set_title( "Class Sample Count Distribution" )
ax.set_ylabel( "Number of Samples" )
ax.set_xlabel( "Unit Class" )
fig.savefig( "tally.png" )
