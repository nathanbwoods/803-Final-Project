import pdb

from pysc2.lib import features, point, actions
from absl import app, flags
from pysc2.env.environment import TimeStep, StepType
from pysc2 import run_configs
from s2clientprotocol import sc2api_pb2 as sc_pb
import importlib

FLAGS = flags.FLAGS
flags.DEFINE_string("replay", None, "Path to a replay file.")
flags.DEFINE_string("agent", None, "Path to an agent.")
flags.mark_flag_as_required("replay")
flags.mark_flag_as_required("agent")

class ReplayEnv:
    def __init__(self,
                 replay_file_path,
                 agent,
                 player_id=1,
                 screen_size_px=(64, 64),
                 minimap_size_px=(64, 64),
                 discount=1.,
                 step_mul=1):

        self.agent = agent
        self.discount = discount
        self.step_mul = step_mul

        self.run_config = run_configs.get('4.10.0')
        self.sc2_proc = self.run_config.start(want_rgb=True)
        self.controller = self.sc2_proc.controller

        replay_data = self.run_config.replay_data(replay_file_path)
        ping = self.controller.ping()
        info = self.controller.replay_info(replay_data)
        if not self._valid_replay(info, ping):
            raise Exception("{} is not a valid replay file!".format(replay_file_path))

        interface = sc_pb.InterfaceOptions()
        interface.raw = True
        interface.score = True
        interface.feature_layer.width = 24
        interface.feature_layer.resolution.x = 84
        interface.feature_layer.resolution.y = 84
        interface.feature_layer.minimap_resolution.x = 64
        interface.feature_layer.minimap_resolution.y = 64
        interface.feature_layer.crop_to_playable_area = True
        interface.feature_layer.allow_cheating_layers = True

        interface.render.resolution.x = 1024
        interface.render.resolution.y = 1024
        interface.render.width = 24
        interface.render.minimap_resolution.x = 128
        interface.render.minimap_resolution.y = 128

        map_data = self.run_config.map_data(info.map_name.replace(" ", "") + ".SC2Map")

        self._episode_length = info.game_duration_loops
        self._episode_steps = 0

        req = sc_pb.RequestStartReplay(
            replay_data=replay_data,
            options=interface,
            map_data=map_data,
            realtime=False,
            disable_fog=False,
            observed_player_id=player_id)

        self.controller.start_replay(req)

        self._state = StepType.FIRST

    @staticmethod
    def _valid_replay(info, ping):
        """Make sure the replay isn't corrupt, and is worth looking at."""
        if (info.HasField("error") or
                    info.base_build != ping.base_build or  # different game version
                    info.game_duration_loops < 1000 or
                    len(info.player_info) != 2):
            # Probably corrupt, or just not interesting.
            return False
#   for p in info.player_info:
#       if p.player_apm < 10 or p.player_mmr < 1000:
#           # Low APM = player just standing around.
#           # Low MMR = corrupt replay or player who is weak.
#           return False
        return True

    def start(self):
        #_features = features.features_from_game_info(self.controller.game_info(), action_space=actions.ActionSpace.RAW)

        while True:
            self.controller.step(self.step_mul)
            obs = self.controller.observe()
            # try:
            #     agent_obs = _features.transform_obs(obs)
            # except:
            #     pass

            if obs.player_result: # Episide over.
                self._state = StepType.LAST
                discount = 0
            else:
                discount = self.discount

            self._episode_steps += self.step_mul

            step = TimeStep(step_type=self._state, reward=0,
                            discount=discount, observation=obs)

            self.agent.step(step, obs.observation, self.controller)

            if obs.player_result:
                break

            self._state = StepType.MID


def main(unused):
    agent_module, agent_name = FLAGS.agent.rsplit(".", 1)
    agent_cls = getattr(importlib.import_module(agent_module), agent_name)

    G_O_O_D_B_O_Y_E = ReplayEnv(FLAGS.replay, agent_cls())
    G_O_O_D_B_O_Y_E.start()

if __name__ == "__main__":
    app.run(main)