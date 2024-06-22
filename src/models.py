from typing import List, Optional

from pydantic import BaseModel


class Validation(BaseModel):
    required: Optional[bool] = None


class Parameter(BaseModel):
    key: str
    title: str
    description: str
    type: str
    validation: Optional[Validation] = None


class Tool(BaseModel):
    id: str
    key: str
    title: str
    description: str
    type: str
    inputParameters: List[Parameter]
    outputParameters: List[Parameter]
    toolId: str
