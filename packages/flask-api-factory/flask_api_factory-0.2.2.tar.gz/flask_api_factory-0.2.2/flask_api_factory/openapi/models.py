from pydantic import BaseModel


def _translate_field_name(name_map: dict[str, str]):
    def _translate(field_name):
        return name_map.get(field_name, field_name)

    return _translate


class APIServer(BaseModel):
    url: str
    description: str


class APIContact(BaseModel):
    name: str
    url: str
    email: str


class APILicense(BaseModel):
    name: str
    url: str


class APIInfo(BaseModel):
    title: str
    description: str
    version: str
    contact: APIContact
    license: APILicense

    class Config:
        alias_generator = _translate_field_name({"termOfService": "term_of_service"})
        allow_population_by_field_name = True


class APITag(BaseModel):
    name: str
    description: str


class APIComponent(BaseModel):
    ...


class APIDoc(BaseModel):
    openapi: str = "3.0.0"
    servers: list[APIServer] = []
    info: APIInfo
    tags: list[APITag] = []
    components: dict[str, APIComponent] = {}
    paths: dict[str, str] = {}
