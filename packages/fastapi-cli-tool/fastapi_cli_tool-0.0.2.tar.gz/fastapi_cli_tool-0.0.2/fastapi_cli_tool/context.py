import subprocess
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator

from fastapi_cli_tool.constants import (
    Database,
    License,
    PackageManager,
    PythonVersion,
    DatabaseORM,
)
from fastapi_cli_tool.helpers import get_package_version


class AppContext(BaseModel):
    name: str
    folder_name: str
    snake_name: str

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        values["snake_name"] = values["folder_name"].replace("-", "_")
        return values


class ProjectContext(BaseModel):
    name: str
    folder_name: str
    packaging: PackageManager

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    python: PythonVersion

    license: Optional[License]
    year: int

    pre_commit: bool = False
    docker: bool = False

    database: Optional[Database] = None
    database_orm: DatabaseORM

    fastapi: str = get_package_version("fastapi")
    pytest: str = get_package_version("pytest")
    tzdata: str = get_package_version("tzdata")
    pytz: str = get_package_version("pytz")
    fastapi_mail: str = get_package_version("fastapi-mail")
    passlib: str = get_package_version("passlib")
    asgiref: str = get_package_version("asgiref")
    uvicorn: str = get_package_version("uvicorn")
    python_jose: str = get_package_version("python-jose")
    pytest_cov: str = get_package_version("pytest-cov")

    orm_version: str = "*"

    use_code_formatter: bool = False

    black: str = get_package_version("black")
    isort: str = get_package_version("isort")

    @root_validator()
    def validate_orm(cls, values: dict):
        orms = {"TortoiseORM": "tortoise-orm", "SQLAlchemy": "SQLAlchemy"}
        values["orm_version"] = get_package_version(orms[values["database_orm"]])
        return values

    @root_validator(pre=True)
    def validate_project(cls, values: dict):
        try:
            values["username"] = subprocess.check_output(
                ["git", "config", "--get", "user.name"]
            )
            values["email"] = subprocess.check_output(
                ["git", "config", "--get", "user.email"]
            )
        except subprocess.CalledProcessError:
            ...
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        values["year"] = datetime.today().year
        return values

    class Config:
        use_enum_values = True
