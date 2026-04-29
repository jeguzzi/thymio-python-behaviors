import time

from pyaseba.client.thymio import Thymio

import thymio_behaviors

behavior = thymio_behaviors.ExplorerBehavior()
thymio = Thymio()
if thymio.connect(start_mirroring=True):
    thymio.set_controller(behavior, time_step=0.1)
    time.sleep(10)
thymio.close(reset=True)
