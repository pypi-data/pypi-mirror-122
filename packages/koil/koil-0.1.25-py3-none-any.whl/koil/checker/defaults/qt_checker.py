from typing import Union
from koil.checker.base import BaseChecker
from koil.checker.registry import register_checker
from koil.state import KoilState


class QtKoilState(KoilState):
    
    def __init__(self, qt_app=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.qt_app = qt_app


@register_checker()
class QtChecker(BaseChecker):

    def force_state(self) -> Union[None, KoilState]:
        """Checks if a running Qt Instance is there, if so we would like
        to run in a seperate thread

        Returns:
            Union[None, KoilState]: [description]
        """

        try:
            from qtpy import QtWidgets

            instance = QtWidgets.QApplication.instance() 

            if instance is None:
                return None

            else:
                return QtKoilState(qt_app=instance,threaded=True)
        except:
            return None

