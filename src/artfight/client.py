from artfight.http import HTTPClient

__all__ = ("ArtfightClient",)


class ArtfightClient:
    def __init__(self) -> None:
        self.http: HTTPClient = HTTPClient()
