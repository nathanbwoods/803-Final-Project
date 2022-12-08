import pandas as pd
import numpy as np
from homography import Transformer
import pickle


A = pd.read_csv("data/A.csv").values
x = np.array(A[:, 0:3].astype(np.float32))
y = np.array(A[:, 3:5].astype(np.float32))

t = Transformer(img_size=1024)
t.fit_homography(x, y)

with open('./transformer.pickle', 'wb') as f:
    pickle.dump(t, f)