import pandas as pd
import numpy as np
from homography import Transformer

np.set_printoptions( linewidth = 200, precision = 3 )
np.random.seed( 1 )

NUM_X_POINTS = 14

randH = Transformer(img_size=1)
randH.H = np.random.normal( size = (3, 4) ) # Gives bigger range than random()
randH.H /= randH.H[2,3] # Rescale so M_3,4 = 1

X = np.random.normal( size = (NUM_X_POINTS, 3) )

Y = randH.homography_transform( X )
Y /= np.max(Y)

t = Transformer(img_size=1)
t.fit_homography(X, Y)

yhat = t.homography_transform( X ) 
print( f"Y, Yhat, DeltaY:\n", np.hstack( [ Y, yhat, Y - yhat  ] ) )

print( f"randH: {randH.H}")
print( f"T: {t.H}")
print( f"Delta-H: {t.H - randH.H}" )
