# -*- coding: utf-8 -*-

import typing as T
import dataclasses


@dataclasses.dataclass
class Base:
    _fields_cache = None  # type: T.Dict[str, dataclasses.Field]

    @classmethod
    def _get_fields(cls) -> T.Dict[str, dataclasses.Field]:
        if cls._fields_cache is None:
            cls._fields_cache = {field.name: field for field in dataclasses.fields(cls)}
        return cls._fields_cache

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: T.Optional[dict]) -> T.Optional["Base"]:
        if data is None:
            return data
        fields = cls._get_fields()
        kwargs = dict()
        for field_name in fields:
            if field_name in data:
                kwargs[field_name] = data[field_name]
        return cls(**kwargs)
