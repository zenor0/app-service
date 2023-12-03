from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 200
    message: str = 'success'
    data: dict = {}


class RouteMeta():
    title: str
    # icon: str | None = None
    # expended: bool | None = None
    # orderNo: int | None = None
    # hidden: bool | None = None
    # hiddenBreadcrumb: bool | None = None
    # single: bool | None = None
    # keepAlive: bool | None = None
    # frameSrc: str | None = None
    # frameBlank: bool | None = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class RouteItem():
    path: str
    name: str
    # component: str | None = None
    # components: str | None = None
    # redirect: str | None = None
    # meta: RouteMeta
    # children: list | None = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DashboardPanel:
    title: str
    number: str
    leftType: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
