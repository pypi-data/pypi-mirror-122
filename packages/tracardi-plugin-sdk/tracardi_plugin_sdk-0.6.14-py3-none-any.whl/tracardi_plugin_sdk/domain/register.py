from typing import List, Optional
from pydantic import BaseModel


class FieldValidation(BaseModel):
    regex: str
    message: str


class Component(BaseModel):
    type: str = 'text'
    props: Optional[dict] = {}


class FormFields(BaseModel):
    id: str
    name: str
    description: Optional[str]
    component: Component
    validation: Optional[FieldValidation]


class FormGroups(BaseModel):
    name: Optional[str]
    description: Optional[str]
    fields: List[FormFields]


class Form(BaseModel):
    title: str
    groups: List[FormGroups]


class Spec(BaseModel):
    className: str
    module: str
    inputs: Optional[List[str]] = []
    outputs: Optional[List[str]] = []
    init: Optional[dict] = None
    form: Optional[Form]
    manual: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = "MIT"
    version: Optional[str] = '0.0.1'


class MetaData(BaseModel):
    name: str
    desc: Optional[str] = ""
    keywords: Optional[List[str]] = []
    type: str
    width: int
    height: int
    icon: str
    editor: str = 'json'
    group: Optional[List[str]] = ["General"]


class Plugin(BaseModel):
    start: bool = False
    debug: bool = False
    spec: Spec
    metadata: MetaData
