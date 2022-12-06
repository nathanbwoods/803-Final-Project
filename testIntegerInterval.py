import util

goodSet = [ ( 1, 1 ),
            ( 1, 2 ),
            ( 1, 3 ) ]
testSet = [ ( 0, 0 ),
            ( 0, 1 ),
            ( 1, 1 ),
            ( 1, 2 ),
            ( 2, 2 ),
            ( 2, 3 ),
            ( 3, 3 ),
            ( 3, 4 ),
            ( 1, 3 ),
            ( 0, 4 ) ]

for intvl in goodSet:
    left = util.IntegerInterval( *intvl )
    for testIntvl in testSet:
        right = util.IntegerInterval( *testIntvl )
        print( f"{left} minus {right}:{left.subtract(right)}" )
