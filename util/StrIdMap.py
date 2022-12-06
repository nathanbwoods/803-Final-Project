#! /usr/bin/env python
# William Schulze, 2022

import pprint

class StrIdMap:
    """Map bidirectionally between strings and integer IDs."""
    def __init__( self, **kwargs ):
        self.num2str = {}
        self.str2num = {}
        for key, value in kwargs.items():
            self[key] = value

            
    def _enforceType( self, val ):
        if not isinstance( val, int ):
            if not isinstance( val, str ):
                msg = ( f"Error using a StrIdMap with key {val}."
                        " The input value is neither a string nor an int."
                        f"It's a {type(val)}, and StrIdMap doesn't "
                         "handle that." )
                raise TypeError( msg )

            
    def __getitem__( self, key ):
        # Make sure it's an int or string.
        self._enforceType( key )
        
        if isinstance( key, int ):
            if key in self.num2str:
                return self.num2str[key]
            else:
                return "UNKNOWN"
        elif isinstance( key, str ):
            return self.str2num[key]
            
            
    def __setitem__( self, key, value ):
        # Make sure we have ints and strings.
        self._enforceType( key )
        self._enforceType( value )

        allVals = [ key, value ]
        numVals = [ k for k in allVals if isinstance( k, int ) ]
        strVals = [ k for k in allVals if isinstance( k, str ) ]

        if not ( len( numVals ) == 1 and len( strVals ) == 1 ):
            msg = ( f"Error trying to use StrIdMap with values {allVals}."
                    "StrIdMap requires one int and one string." )
            raise TypeError( msg )

        self.num2str[numVals[0]] = strVals[0]
        self.str2num[strVals[0]] = numVals[0]

    def __len__( self ):
        return self.num2str.__len__()

    def __iter__( self ):
        return self.num2str.__iter__()

    def __reversed__( self ):
        return self.num2str.__reversed__()

    def __repr__( self ):
        return pprint.pformat( self.num2str )

        


            
            
            
