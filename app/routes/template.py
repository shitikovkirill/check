from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

from app.check.dependencies import CheckService

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/check",
    tags=["templates"],
)


@router.get("/{secret}", response_class=PlainTextResponse)
async def get_check_template(
    request: Request,
    secret: str,
    service: CheckService,
):
    check, owner = await service.get_by_secret(secret)
    return templates.TemplateResponse(
        request=request, name="check.txt", context={"check": check, "owner": owner}
    )
