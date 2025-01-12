from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/check",
    tags=["templates"],
)


@router.get("/{id}", response_class=PlainTextResponse)
async def get_check_template(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="check.txt", context={"id": id}
    )
