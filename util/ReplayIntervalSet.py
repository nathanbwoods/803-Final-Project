import random
import pickle

from .IntegerIntervalSet import IntegerIntervalSet
from .IntegerInterval import IntegerInterval
from . import UnitId


class ReplayIntervalSet:
    """One per replay.  Includes all unit types."""
    def __init__( self, num : int, name: str, iSets = None ):
        self.num = num
        self.name = name
        self.iSets = iSets
        if self.iSets is None:
            self.iSets = {}


    def add( self, key : int, time: int ):
        """Add a single observation for a single unit."""
        if key not in self.iSets:
            self.iSets[key] = IntegerIntervalSet()
        self.iSets[key].addOne( time )


    def __contains__( self, key ):
        """Does this replay have a frame of the desired unit?"""
        if key not in self.iSets:
            return False
        result = self.iSets[key].count()
        return result
        

    def visibles( self, time : int ):
        results = []
        for unitType in sorted( self.iSets.keys() ):
            if time in self.iSets[unitType]:
                results.append( unitType )
        return results
        

    def count( self ) -> int:
        counter = 0
        for intvl in self.iSets.values():
            counter += intvl.count()


    def random( self, key, removeMargin = 20 ) -> ( int, list ):
        """Make sure to test that key is contained before calling
        this."""
        selected = self.iSets[key].random()

        vis = self.visibles( selected )
        
        for key in self.iSets:
            self.iSets[key].subtract( selected - removeMargin,
                                      selected + removeMargin )

        return selected, vis
        
        
    def __repr__( self ) -> str:
        elems = [ f"\n# {str( self.name )}" ]
        elems += [ f"UnitIntervalSet [{self.num:06d}]: (" ]
        elems += [ f"{l}/{UnitId.unitsSc[l]} :\n{self.iSets[l]}"
                   for l in sorted( self.iSets.keys() ) ]
        elems.append( f"\t) # UnitIntervalSet" )
        return "\n".join( elems )

