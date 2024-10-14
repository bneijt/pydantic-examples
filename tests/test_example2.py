from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from pydantic_examples.yaml import yaml_with_comments

Uniq = AfterValidator(lambda v: list(sorted(set(v))))


class SecondLevel(BaseModel, extra="forbid"):
    """Nested documentation is also documentation"""

    value: Annotated[int, Field(description="actual value")] = 0


class FirstLevel(BaseModel, extra="forbid"):
    """Nested documentation is also documentation"""

    fst: SecondLevel = SecondLevel()


class RootModel(BaseModel):
    """Root docstring"""

    fst: FirstLevel = FirstLevel()
    fst_list: list[FirstLevel] = [FirstLevel()]
    fst_dict: dict[str, FirstLevel] = {"a": FirstLevel()}


EXPECTED = """# Root docstring
fst:
    fst:
# Nested documentation is also documentation
        value: 0 # actual value
"""


def test_example2() -> None:
    rm = RootModel()
    assert yaml_with_comments(rm) == EXPECTED, "Should produce expected value"
