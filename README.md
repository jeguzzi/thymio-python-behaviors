# thymio-python-behaviors

Python port of the behaviors implemented in the Thymio firmware.

Use `pyaseba` or `pyenki` to apply the behaviors to real and simulated robots.


## Example with real Thymio (pyaseba)

```python
import time

from pyaseba.client.thymio import Thymio

import thymio_behaviors

behavior = thymio_behaviors.ExplorerBehavior()
thymio = Thymio()
if thymio.connect(start_mirroring=True):
    thymio.set_controller(behavior, time_step=0.1)
    time.sleep(10)
thymio.close(reset=True)
```

Have a look at the [complete example](https://github.com/jeguzzi/pyaseba/blob/main/examples/thymio/node/behavior.py) that selects which behavior to run. 

## Example with simulated Thymio (pyenki)

```python
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
```

Have a look at the [complete example](https://github.com/jeguzzi/enki/blob/rolling/examples/python/thymio_behavior.py) that selects which behavior to run. 

