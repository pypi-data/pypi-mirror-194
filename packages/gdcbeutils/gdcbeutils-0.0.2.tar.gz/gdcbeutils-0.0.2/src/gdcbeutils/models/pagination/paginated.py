"""
    Support for pagination using Pydantic
"""
import json
from typing import Any, Dict, Generic, List, TypeVar

from pydantic import BaseModel, validator


class Pagination(BaseModel):
    """Defines a pagination model"""

    page: int
    per_page: int = 20

    @classmethod
    def from_params(cls, obj: Dict[str, Any]):
        """Defines a pagination from default parameters"""
        return cls(
            page=obj.get("page", 1),
            per_page=obj.get("per_page", 100),
        )

    @validator("page")
    def must_be_at_least_1(self, value: int):
        """Page must start at 1"""
        if value <= 0:
            return 1
        return value


T = TypeVar("T")


class PaginatedResult(Pagination, Generic[T]):
    """Defines a Paginated result model"""

    page_count: int
    first_page: bool
    previous_page: bool
    next_page: bool
    result: List[T]

    @classmethod
    def from_db(
        cls,
        result: List[T],
        page_settings: Pagination | None = None,
    ):
        """Returns a paginated result from a database result set"""
        if not page_settings:
            page_settings = Pagination.from_params("{}")

        return cls(
            page=page_settings.page,
            per_page=page_settings.per_page,
            page_count=len(result),
            first_page=(page_settings.page > 1),
            previous_page=(page_settings.page > 1),
            next_page=len(result) >= page_settings.per_page,
            result=result,
        )

    def to_api(self):
        """Return results as s json to be returned by api calls"""
        return json.loads(self.json())
