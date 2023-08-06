class ModelMetadataError(Exception):

    def __init__(self, msg=None, *args: object) -> None:
        if msg is None :
            super().__init__('Model name and version should be provided')
        else :
            super().__init__(msg)


class ModelMethodRequired(Exception):

    def __init__(self, msg=None, *args: object) -> None:
        if msg is None :
            super().__init__('Some required method is not defined')
        else :
            super().__init__(msg)