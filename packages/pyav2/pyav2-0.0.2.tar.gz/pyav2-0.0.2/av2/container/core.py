from av.container.core import Container as AvContainer


class Container():
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.close()
        pass
