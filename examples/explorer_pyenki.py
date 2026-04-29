import pyenki
import pyenki.viewer
from pyenki.adapters import make_controller_from_thymio_behavior

import thymio_behaviors

behavior = thymio_behaviors.ExplorerBehavior()
thymio = pyenki.Thymio2()
thymio.control_step_callback = make_controller_from_thymio_behavior(
    thymio, behavior)
world = pyenki.World(radius=50)
world.add_object(thymio)
pyenki.viewer.init()
pyenki.viewer.run_in_viewer(world, duration=10)
pyenki.viewer.cleanup()
