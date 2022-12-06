import random

from .IntegerInterval import IntegerInterval

class IntegerIntervalSet:
    """One per replay, per unit type."""

    def __init__( self, intervals = None ):
        self.dirty = True
        self.intervals = intervals
        if self.intervals is None:
            self.intervals = []
        else:
            self.clean()


    def __contains__( self, time : int ):
        self.clean()
        for interval in self.intervals:
            if time in interval:
                return True
        return False

    
    def clean( self ):
        """Sort intervals and merge where possible."""
        if not self.dirty:
            return
        if len( self.intervals ) == 0:
            return
        self.intervals.sort()
        newInts = [ self.intervals[0] ]
        for right in self.intervals[1:]:
            left = newInts.pop()
            if left.canMerge( right ):
                newInts.append( left.merge( right ) )
            else:
                newInts.append( left )
                newInts.append( right )
        self.intervals = newInts
            
        
    def add( self, begin : int, end : int ):
        self.intervals.append( IntegerInterval( begin, end ) )
        self.dirty = True


    def addOne( self, time: int ):
        """Convenience function for self.add()."""
        self.add( time, time )


    def subtract( self, begin : int, end : int ):
        # Probably faster to bunch up all the small intervals.
        self.clean()
        intermediates = []
        removal = IntegerInterval( begin, end )
        for intvl in self.intervals:
            intermediates += intvl.subtract( removal )
        self.intervals = intermediates
        # Do we need to clean again?  Not sure.


    def count( self ):
        counter = 0
        for interval in self.intervals:
            counter += interval.count()
        return counter


    def random( self ):
        target = random.randint( 0, self.count() - 1 )
        for intvl in self.intervals:
            intvlCount = intvl.count()
            if target < intvlCount:
                return intvl.random()
            else:
                target -= intvlCount
        raise RuntimeError( "IntegerIntervalSet.random() failed." )
    
        
    def __repr__( self ):
        self.clean()
        elems = [ "IntegerIntervalSet: (" ]
        elems += [ ",".join( [ str(i) for i in self.intervals ] ) ]
        elems.append( f"\t) # IntegerIntervalSet ({self.count()})" )
        return "\n".join( elems )
