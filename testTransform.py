
from pysc2.lib import transform


def get_w2s_transform( map_size, rgb_screen_px ):

    # World has origin at bl, world_tl has origin at tl.
    world_to_world_tl = transform.Linear(
        point.Point(1, -1), point.Point(0, map_size.y))

    # Move the point to be relative to the camera. This gets updated per frame.
    world_tl_to_world_camera_rel = transform.Linear(
        offset= -map_size / 4)

    rgb_world_per_pixel = ( rgb_screen_px / 24)
    world_camera_rel_to_rgb_screen = transform.Linear(
        rgb_world_per_pixel, rgb_screen_px / 2)

    world_to_rgb_screen = transform.Chain(
        world_to_world_tl,
        world_tl_to_world_camera_rel,
        world_camera_rel_to_rgb_screen)
    world_to_rgb_screen_px = transform.Chain(
        world_to_rgb_screen,
        transform.PixelToCoord())

    rgb_screen_to_main_screen = transform.Linear(
          screen_size_px / rgb_screen_px)
    world_to_main_screen = transform.Chain(  # surf
                      world_to_rgb_screen,
                      rgb_screen_to_main_screen)

    return world_to_main_screen
