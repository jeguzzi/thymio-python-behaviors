# thymio-python-behaviors

Python port of the behaviors implemented in the Thymio firmware.

Use `pyaseba` or `pyenki` to apply the behaviors to real and simulated robots.


## Example with real Thymio (pyaseba)

```python
import time

import thymio_behaviors
from pyaseba.client.thymio import Thymio

behavior = thymio_behaviors.ExplorerBehavior()
thymio = Thymio()
if thymio.connect(start_mirroring=True):
    thymio.set_behavior(behavior, time_step=0.1)
    time.sleep(10)
thymio.close(reset=True)
```

Have a look at the [complete example](https://github.com/jeguzzi/pyaseba/blob/main/examples/thymio/node/behavior.py) that selects which behavior to run. 

## Example with simulated Thymio (pyenki)

```python
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
```

Have a look at the [complete example](https://github.com/jeguzzi/enki/blob/rolling/examples/python/thymio_behavior.py) that selects which behavior to run. 

