from gunicorn.app.base import BaseApplication
from typing import Dict


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class UserModelApplication(StandaloneApplication):
    """
    Gunicorn application to run a Flask app in Gunicorn loading first the
    user's model.
    """

    def __init__(
        self, app, options: Dict = None
    ):
        super().__init__(app, options)

    def load(self):
        try:
            # logger.debug("Calling user load method")
            # self.user_object.load()
            pass
        except (NotImplementedError, AttributeError):
            pass
            # logger.debug("No load method in user model")
        return self.application