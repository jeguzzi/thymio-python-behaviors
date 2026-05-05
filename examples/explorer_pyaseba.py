import time

import thymio_behaviors
from pyaseba.client.thymio import Thymio

behavior = thymio_behaviors.ExplorerBehavior()
thymio = Thymio()
if thymio.connect(start_mirroring=True):
    thymio.set_behavior(behavior, time_step=0.1)
    time.sleep(10)
thymio.close(reset=True)
