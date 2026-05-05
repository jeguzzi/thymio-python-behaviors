import pyenki
import pyenki.viewer
import thymio_behaviors
from pyenki.adapters import Thymio2AsebaAdapter

behavior = thymio_behaviors.ExplorerBehavior()
robot = pyenki.Thymio2()
world = pyenki.World(radius=50)
world.add_object(robot)
thymio = Thymio2AsebaAdapter(robot)
thymio.set_behavior(behavior)
pyenki.viewer.init()
pyenki.viewer.run_in_viewer(world, duration=10)
pyenki.viewer.cleanup()
