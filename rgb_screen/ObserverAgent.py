import pdb

from pysc2.lib import features
import matplotlib.pyplot as plt


class ObserverAgent():
    def __init__(self):
        self.action_spec = None

    def step(self, time_step, obs):
        rgb_screen = features.Feature.unpack_rgb_image(obs.render_data.map)
        plt.imshow(rgb_screen)
        plt.title(F"Step:")
        plt.savefig(time_step+".png")
