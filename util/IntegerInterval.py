#! /usr/bin/env python

import random

class IntegerInterval:
    """With integer timesteps, when something is true.  Inclusive of endpoints,
    so the beginning is the first time step when it is true, and the end
    is the last time step when it is true."""
    
    def __init__( self, begin : int, end : int ):

        assert( isinstance( begin, int ) )
        assert( isinstance( end, int ) )
        assert( end >= begin )
        
        self.begin = begin
        self.end = end

        
    def __contains__( self, time : int ):
        if time < self.begin:
            return False
        if time > self.end:
            return False
        return True

    
    def isAdjacent( self, other : "IntegerInterval" ):
        if other.begin == self.end + 1:
            return True
        elif other.end == self.begin - 1:
            return True

        
    def add( self, time : int ):
        if time == self.begin - 1:
            self.begin -= 1
        if time == self.end + 1:
            self.end += 1


    def subtract( self, other: "IntegerInterval" ):
        # Case 1: no overlap.
        if not self.overlaps( other ):
            return [ self ]
        # Case 2: other contains me.
        elif ( other.begin <= self.begin
               and other.end >= self.end ):
            return []
        # Case 3: other contains begin.
        elif ( other.begin <= self.begin
               and other.end >= self.begin
               and other.end <= self.end ):
            newBegin = other.end + 1
            return [ IntegerInterval( newBegin, self.end ) ]
        # Case 4: other contains end.
        elif ( other.begin >= self.begin
               and other.begin <= self.end
               and other.end >= self.end ):
            newEnd = other.begin - 1
            return [ IntegerInterval( self.begin, newEnd ) ]
        # Case 5: I contain other.
        else:
            return [ IntegerInterval( self.begin, other.begin - 1 ),
                     IntegerInterval( other.end + 1, self.end ) ]


    def overlaps( self, other : "IntegerInterval" ):
        if other.end < self.begin:
            return False
        if other.begin > self.end:
            return False
        return True


    def canMerge( self, other: "IntegerInterval" ):
        if self.overlaps( other ):
            return True
        elif self.isAdjacent( other ):
            return True
        return False
    
    
    def merge( self, other : "IntegerInterval" ):
        """Assumes they've already been tested and overlap."""
        newBegin = min( self.begin, other.begin )
        newEnd = max( self.end, other.end )
        return IntegerInterval( newBegin, newEnd )


    def count( self ):
        return self.end - self.begin + 1


    def random( self ):
        return random.randint( self.begin, self.end )
    

    def __lt__( self, other ):
        return self.begin < other.begin

    
    def __repr__( self ):
        return f"({self.begin},{self.end})"

                                      
