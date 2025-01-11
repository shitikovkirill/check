from typing import Annotated

from fastapi import Depends

from app.check.service import CheckService as CheckServiceClass

CheckService = Annotated[CheckServiceClass, Depends()]
