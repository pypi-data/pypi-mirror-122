from pydantic import BaseModel


class KoilState(object):

    def __init__(self, threaded=False) -> None:
        self.threaded = threaded
        super().__init__()