import util

mySet = util.IntegerIntervalSet()
for thisRange in [ range( 20 ),
                   range( 30, 40 ),
                   range( 100, 150 ) ]:
    for i in thisRange:
        mySet.add( i, i )

print( "Before: ", mySet )
randoms = [ mySet.random() for i in range( 1000 ) ]
for r in randoms:
    if r not in mySet:
        print( f"WARNING: {r} not in set but was returned randomly!" )

subtractions = [ ( 18, 19 ),
                 ( 25, 35 ),
                 ( 38, 38 ),
                 ( 105, 106 ),
                 ( 149, 150 ) ]
for begin, end in subtractions:
    mySet.subtract( begin, end )

print( "After:", mySet )
randoms = [ mySet.random() for i in range( 1000 ) ]
for r in randoms:
    if r not in mySet:
        print( f"WARNING: {r} not in set but was returned randomly!" )

