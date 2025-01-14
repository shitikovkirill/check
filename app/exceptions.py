class AppException(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        doc = self.__doc__ and self.__doc__.strip()
        super().__init__(msg or doc, *args, **kwargs)
