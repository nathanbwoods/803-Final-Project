import pdb

import numpy as np
from pysc2.lib import features
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


class ObserverAgent():
    def __init__(self):
        self.action_spec = None

    def step(self, time_step, obs, controller):
        rgb_screen = features.Feature.unpack_rgb_image(obs.render_data.map)
        plt.figure()
        plt.imshow(rgb_screen, aspect='equal')
        plt.imsave('tick_0.png', rgb_screen)
        ax = plt.gca()

        # Major ticks
        ax.set_xticks(np.arange(0, 1024, 24))
        ax.set_yticks(np.arange(0, 1024, 24))

        # Gridlines based on minor ticks
        #ax.grid(which='both')


        plt.title(F"rgb_screen, tick: {obs.game_loop}")
        plt.show()
        pdb.set_trace()
        exit()
