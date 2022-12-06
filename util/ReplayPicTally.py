import pickle
import os
import os.path

from . import UnitId

def exists( replayId ):
    return os.path.exists( id2file( replayId ) )


def load( replayId ):
    with open( id2file( replayId ), 'rb' ) as f:
        return pickle.load( f )


def id2file( replayId ):
    return f"tally/replay_{replayId:06d}.pkl"


class ReplayPicTally:
    def __init__( self ):
        self.pics = {}


    def save( self, replayNum ):
        if not os.path.exists( "tally" ):
            os.makedirs( "tally" )
        with open( id2file( replayNum ), 'wb' ) as f:
            pickle.dump( self, f )
            
        
    def add( self, key ):
        if key not in self.pics:
            self.pics[key] = 1
        else:
            self.pics[key] += 1


    def __repr__( self ):
        elems = []
        for key in sorted( self.pics.keys(), key = lambda k: self.pics[k] ):
            unitName = UnitId.unitsSc[key]
            elems.append( f"({key}/{unitName}:{self.pics[key]})" )
        return ",".join( elems )
