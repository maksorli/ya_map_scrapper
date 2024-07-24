import itertools


class ProxyRotator:
    """Rotates proxies for each request."""

    def __init__(self, proxies: list):
        self.proxies = itertools.cycle(proxies)
        self.current_proxy = None
        self.request_counter = 0

    def change_proxy(self) -> dict:
        """Switch to the next proxy."""
        self.current_proxy = next(self.proxies)
        self.request_counter = 0
        return self.current_proxy

    def get_proxy(self) -> dict:
        """Get the current proxy, changing it if necessary."""
        if self.request_counter % 2 == 0:
            self.change_proxy()
        self.request_counter += 1
        return self.current_proxy
