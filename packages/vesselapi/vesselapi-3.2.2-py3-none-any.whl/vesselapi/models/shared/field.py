from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Any, Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class FieldOptions:
    key: Optional[Any] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('key'), 'exclude': lambda f: f is None }})
    name: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('name'), 'exclude': lambda f: f is None }})
    
class FieldTypeEnum(str, Enum):
    STRING = "string"
    NUMBER = "number"
    DATETIME = "datetime"
    DATE = "date"
    BOOLEAN = "boolean"
    REFERENCE = "reference"
    PHONE = "phone"
    URL = "url"
    ID = "id"
    EMAIL = "email"
    PERCENT = "percent"
    SINGLESELECT = "singleselect"
    MULTISELECT = "multiselect"
    ADDRESS = "address"
    DECIMAL = "decimal"
    TIME = "time"
    DATERANGE = "daterange"
    OBJECT = "object"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Field:
    r"""Field
    (Alias: property) A field is a key-value pair on a CRM Object that provides information about that object.
    """
    
    creatable: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('creatable') }})
    custom: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('custom') }})
    key: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('key') }})
    name: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('name') }})
    required: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('required') }})
    type: FieldTypeEnum = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('type') }})
    universal: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('universal') }})
    updatable: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.field_name('updatable') }})
    is_array: Optional[bool] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('isArray'), 'exclude': lambda f: f is None }})
    options: Optional[list[FieldOptions]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.field_name('options'), 'exclude': lambda f: f is None }})
    