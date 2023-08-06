# Thread Safe Signal
```text
Signal to generate and receive event between different threads
```

## Installation:
```bash
pip install pyrvsignal
```

## Example code:

```python
import time
from threading import Thread
from pyrvsignal import Signal


class MyThread(Thread):
    started = Signal()
    finished = Signal()

    def __init__(self, target, args):
        self.target = target
        self.args = args
        Thread.__init__(self)

    def run(self) -> None:
        self.started.emit()
        self.target(*self.args)
        self.finished.emit()


def do_my_work(details):
    print(f"Doing work: {details}")
    time.sleep(10)

def started_work():
    print("Started work")
    
def finished_work():
    print("Work finished")

thread = MyThread(target=do_my_work, args=("testing",))
thread.started.connect(started_work)
thread.finished.connect(finished_work)
thread.start()
```

## Contact
&emsp; If any suggestions mail to [ravikiranb36@gmail.com](mailto:admin@w3schools.io)