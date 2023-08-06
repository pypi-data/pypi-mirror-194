from threading import Lock


class Signal:
    """
    Thread Safe Signal
    Generate event between multiple threads
    """
    lock = Lock()
    target = None

    def emit(self) -> None:
        """
        Calls callback when signal emits
        :return: None
        """
        self.lock.acquire()
        if self.target:
            self.target()
        self.lock.release()

    def connect(self, target) -> None:
        """
        Add callback function reference
        :param target: callback function reference
        :return: None
        """
        self.lock.acquire()
        self.target = target
        self.lock.release()

    def disconnect(self) -> None:
        """
        Removes callback function reference
        :return: None
        """
        self.lock.acquire()
        self.target = None
        self.lock.release()
