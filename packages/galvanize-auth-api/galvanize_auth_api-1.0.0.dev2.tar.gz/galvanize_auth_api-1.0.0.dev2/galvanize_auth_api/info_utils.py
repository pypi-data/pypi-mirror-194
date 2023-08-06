from datetime import timedelta, datetime, timezone
from typing import get_type_hints, get_origin, get_args
from dataclasses import is_dataclass
from copy import deepcopy


class FromDictMixin:
    @classmethod
    def from_dict(cls, data, /, has_attributes=True):
        if "data" in data:
            data = data["data"]
        if has_attributes and "attributes" not in data:
            raise ValueError(f"{cls.__name__} expected attributes")
        types = get_type_hints(cls)
        data = deepcopy(data)
        if has_attributes:
            data.update(data["attributes"])
            del data["attributes"]
        for key in list(data.keys()):
            if key not in cls.__match_args__:
                print(
                    f"{cls.__name__} does not support "
                    f"{key} with value {data[key]}"
                )
                del data[key]
            elif (
                key in types
                and get_origin(types[key]) == list
                and len(get_args(types[key])) == 1
                and is_dataclass(get_args(types[key])[0])
            ):
                (t,) = get_args(types[key])
                if hasattr(t, "from_dict"):
                    data[key] = [
                        t.from_dict(
                            d,
                            "attributes" in d,
                        )
                        for d in data[key]
                    ]
                else:
                    data[key] = [t(**d) for d in data[key]]
            elif key in types and is_dataclass(types[key]):
                if hasattr(types[key], "from_dict"):
                    data[key] = types[key].from_dict(
                        data[key],
                        "attributes" in data[key],
                    )
                else:
                    data[key] = types[key](**data[key])
            elif key in types and types[key] == datetime:
                if isinstance(data[key], str):
                    _date = data[key].replace("Z", "+00:00")
                    _date = _date.replace(" ", "0")
                    if _date.endswith("+0000"):
                        _date = _date.replace("+0000", "+00:00")
                    data[key] = datetime.fromisoformat(_date)
                    if (
                        data[key].tzinfo is None
                        or data[key].tzinfo.utcoffset(data[key]) is None
                    ):
                        _date += "+00:00"
                        data[key] = datetime.fromisoformat(_date)
                elif isinstance(data[key], int):
                    data[key] = datetime.fromtimestamp(
                        data[key],
                        tz=timezone.utc,
                    )
            elif key in types and types[key] == timedelta:
                if isinstance(data[key], int):
                    data[key] = timedelta(seconds=data[key])
        return cls(**data)
