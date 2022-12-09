#! /usr/bin/env python

import numpy as np
import pandas as pd

np.set_printoptions( linewidth = 200, precision = 5 )

NUM_ITERS = 1
ITER_MULT = 0.1
#FIELD_OF_VIEW_DEG = 25.7302679
FIELD_OF_VIEW_DEG = 25.3
# 0 is looking straight down, 90 is level with ground
#PITCH_UP_DEG = 32.6364857
PITCH_UP_DEG = 32.72
CAM_DIST = 36.3
#CAM_DIST = 33.1
CAM_Z = 11.62
TEST_POINTS = [ np.array( ( [0],[0],[0] ) ),
                np.array( ( [1],[0],[0] ) ),
                np.array( ( [0],[1],[0] ) ),
                np.array( ( [0],[0],[1] ) ),
                ]


SCV_POINTS = pd.read_csv( "/home/schulzew/Classes/Project/nbw/data/Aw4.csv" )

#camX = 121.4609375
#camY = 27.08984375
#camZ = 11.989
#camZ = 11.6
#camZ = 9.98922824859619
#scv_points.X -= camX
#scv_points.Y -= camY


#scv_points['U'] /= 1024
#scv_points['V'] /= 1024
#scv_points['V'] = scv_points['V']


def deg2rad( degs ):
    return degs * np.pi / 180

def makeCamera( fov, pitch, dist, verbose = False ):
    affine = np.eye( 3 )
    affine[:,0] = np.array( ( 1,
                              0,
                              0 ) )
    affine[:,1] = np.array( ( 0,
                              -1,
                              0 ) )
    affine[:,2] = np.array( [.5, .5, 1] ) 

    projection = np.zeros( (3,4) )
    focal_length = 1 / np.tan( deg2rad( fov ) )
    projection[0,0] = focal_length
    projection[1,1] = focal_length
    projection[2,2] = 1

    extrinsic = np.zeros( (4,4) )
    extrinsic[:,0] = np.array( [1, 0, 0, 0] )  # Same as world.
    extrinsic[:,1] = np.array( [0,
                                np.cos( deg2rad( pitch ) ),
                                np.sin( deg2rad( pitch ) ),
                                0] )
    extrinsic[:,2] = np.array( [0,
                                np.sin( deg2rad( pitch ) ),
                                -np.cos( deg2rad( pitch ) ),
                                0] )
    extrinsic[:,3] = np.array( [0,
                                # Want -Cy, but Cy is negative in world frame
                                # -CAM_DIST * np.sin( deg2rad( PITCH_UP_DEG ) ),
                                0,
                                # Want -Cz, but Cz is positive in world frame
                                # -CAM_DIST * np.cos( deg2rad( PITCH_UP_DEG ) ),
                                dist,
                                1] )

    camera = affine.dot( projection ).dot( extrinsic )
    
    if verbose:
        print( f"Affine:\n {affine}" )
        print( f"Projection:\n {projection}" )
        print( f"Extrinsic:\n {extrinsic}" )
        print( f"Camera:\n{camera}" )
    return camera

camera = makeCamera( FIELD_OF_VIEW_DEG,
                     PITCH_UP_DEG,
                     CAM_DIST,
                     verbose = True )

def transformPoint( point, matrix = camera ):
    point = point.reshape((-1,1))
    ones = np.ones( 1 ).reshape((1,1))
    hpoint = np.vstack( ( point, ones ) )
    trans = matrix.dot( hpoint )
    return trans

def n( homoPoint ):
    norm = homoPoint / homoPoint[2]
    return np.array( norm[:-1] )

def transform( points, matrix = camera ):
    hPoints = np.hstack( ( points,
                           np.ones( ( points.shape[0] ) ).reshape( (-1,1)) ) )
    trans = hPoints.dot( matrix.T )
    norm = trans / trans[:,2].reshape((-1,1))
    trunc = norm[:,:-1]
    return trunc

for point in TEST_POINTS:
    print( f"Point { point.T}:{(transformPoint(point)).T} -> {n(transformPoint(point)).T}" )


def unitPoints( rawPoints, camZ ):
    points = np.array( rawPoints.loc[:,['X','Y','Z'] ] )
    points[:,2] -= camZ
    return points

scvY = np.array( SCV_POINTS.loc[:,['U','V'] ] )

fov = FIELD_OF_VIEW_DEG
pitch = PITCH_UP_DEG
dist = CAM_DIST
camZ = CAM_Z
for i in range( NUM_ITERS ):
    scvX = unitPoints( SCV_POINTS, camZ )
    
    print( f"Iter {i}" )

    cam = makeCamera( fov, pitch, dist )
    error = np.linalg.norm( transform( scvX, cam ) - scvY )
    print( f"Error: {error}" )
    
    # First, change distance.
    camdM1 = makeCamera( fov, pitch, dist - ITER_MULT )
    camdP1 = makeCamera( fov, pitch, dist + ITER_MULT )
    errordM1 = np.linalg.norm( transform( scvX, camdM1 ) - scvY )
    errordP1 = np.linalg.norm( transform( scvX, camdP1 ) - scvY )

        
    # Second, change FOV.
    camfM1 = makeCamera( fov - ITER_MULT, pitch, dist )
    camfP1 = makeCamera( fov + ITER_MULT, pitch, dist )
    errorfM1 = np.linalg.norm( transform( scvX, camfM1 ) - scvY )
    errorfP1 = np.linalg.norm( transform( scvX, camfP1 ) - scvY )

    # Third, change pitch.
    campM1 = makeCamera( fov, pitch - ITER_MULT, dist )
    campP1 = makeCamera( fov, pitch + ITER_MULT, dist )
    errorpM1 = np.linalg.norm( transform( scvX, campM1 ) - scvY )
    errorpP1 = np.linalg.norm( transform( scvX, campP1 ) - scvY )

    # Fourth, change height.
    scvZM1 = unitPoints( SCV_POINTS, camZ - ITER_MULT )
    scvZP1 = unitPoints( SCV_POINTS, camZ + ITER_MULT )
    errorzM1 = np.linalg.norm( transform( scvZM1, cam ) - scvY ) 
    errorzP1 = np.linalg.norm( transform( scvZP1, cam ) - scvY ) 

    minError = min( [ error,
                      errordM1,
                      errordP1,
                      errorfM1,
                      errorfP1,
                      errorpM1,
                      errorpP1,
                      errorzM1,
                      errorzP1 ] )
    
    if ( errordM1  == minError ):
        print( "-Distance" )
        dist -= ITER_MULT
    elif ( errordP1 == minError ):
        print( "+Distance" )
        dist += ITER_MULT
    elif ( errorfM1 == minError ):
        print( "-FOV" )
        fov -= ITER_MULT
    elif ( errorfP1 == minError ):
        print( "+FOV" )
        fov += ITER_MULT
    elif ( errorpM1 == minError ):
        print( "-Pitch" )
        pitch -= ITER_MULT
    elif ( errorpP1 == minError ):
        print( "+Pitch" )
        pitch += ITER_MULT
    elif ( errorzM1 == minError ):
        print( "-Z" )
        camZ -= ITER_MULT
    elif ( errorzP1 == minError ):
        print( "+Z" )
        camZ += ITER_MULT
    else:
        ITER_MULT *= 1 - 1e-2

    camZ = max( 0, camZ )
    dist = max( 0, dist )
    fov = max( 0, fov )
    pitch = max( 0, pitch )
    pitch = min( pitch, 90 )


scvYhat = transform( scvX, cam )
print( np.hstack( ( scvYhat, scvY ) ) )
print( scvYhat - scvY )

print( f"\nCamera:\n{cam}" )

print( f"\nFOV: {fov}" )
print( f"Distance: {dist}" )
print( f"Pitch: {pitch}" )
print( f"CamZ: {camZ}\n" )

print( np.linalg.norm( scvYhat - scvY ) )
print( np.max( scvYhat - scvY ) )
#testScv = scvX[0,:3]
#print( testScv )
#print( n( transformPoint( scvX[0,:3] ) ) )
