import os
import os.path

from . import UnitId


DEFAULT_FILENAME = "tally/global.pkl"


def exists():
    return os.path.exists( DEFAULT_FILENAME )


def load():
    with open( DEFAULT_FILENAME, 'rb' ) as f:
        return pickle.load( f )


class GlobalPicTally:
    def __init__( self ):
        self.pics = { key : 0
                      for key in UnitId.unitsSc }


    def add( self, unit ):
        if unit not in self.pics:
            self.pics[unit] = 1
        else:
            self.pics[unit] += 1

        
    def save( self ):
        if not os.path.exists( "tally" ):
            os.makedirs( "tally" )
        with open( DEFAULT_FILENAME, 'wb' ) as f:
            pickle.dump( self, f )

            
    def loadReplayTally( self, replayTally ):
        for key in replayTally.pics:
            if key not in self.pics:
                self.pics[key] = replayTally.pics[key]
            else:
                self.pics[key] += replayTally.pics[key]


    def leastViewed( self ):
        result = sorted( self.pics.keys(), key = lambda k: self.pics[k] )
        filtered = [ k for k in result if k in UnitId.unitsMain ]
        return filtered
                      

    def __repr__( self ):
        elems = []
        for key in sorted( self.pics.keys(), key = lambda k: self.pics[k] ):
            unitName = UnitId.unitsSc[key]
            elems.append( f"({key}/{unitName}:{self.pics[key]})" )
        return ",".join( elems )
