from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ApiEndpoint(BaseModel):
    path: str
    method: str = "GET"
    handler: str = ""
    source_file: str = ""


class EntityItem(BaseModel):
    name: str
    stem: str
    attributes: List[Dict[str, str]] = Field(default_factory=list)
    source_file: str = ""
    relationships: List[str] = Field(default_factory=list)


class ServiceItem(BaseModel):
    name: str
    stem: str
    source_file: str = ""


class RepositoryItem(BaseModel):
    name: str
    stem: str
    source_file: str = ""


class ControllerItem(BaseModel):
    name: str
    stem: str
    apis: List[ApiEndpoint] = Field(default_factory=list)
    source_file: str = ""


class ProjectMetadata(BaseModel):
    language: str = "UNKNOWN"
    build_tool: str = "STANDARD"
    apis: List[ApiEndpoint] = Field(default_factory=list)
    entities: List[EntityItem] = Field(default_factory=list)
    services: List[ServiceItem] = Field(default_factory=list)
    repositories: List[RepositoryItem] = Field(default_factory=list)
    controllers: List[ControllerItem] = Field(default_factory=list)
    all_source_files: List[str] = Field(default_factory=list)
