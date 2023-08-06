import os
import json
import time
import hashlib
import functools
from typing import Callable, Optional
from traitlets.config.configurable import SingletonConfigurable

from pycosnippets.settings import PYCO_CMD_OUTPUT_DIRECTORY


def get_code_id(code: str) -> str:
    now = time.time()
    return f"""{int(now)}-{hashlib.md5(code.encode("utf-8")).hexdigest()}"""


class JsonPrettyPrint(SingletonConfigurable):

    def __call__(self, obj: dict, **kwargs):
        string = json.dumps(obj, indent=4, **kwargs)
        print(string)

    def decorator(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)
            self(obj=output)
        return wrapper

    def metadecorator(self, **json_kwargs) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                output = func(*args, **kwargs)
                self(obj=output, **json_kwargs)
            return wrapper
        return decorator


json_pretty_print = JsonPrettyPrint.instance()


class JsonSave(SingletonConfigurable):

    def __call__(self, obj: dict, filepath: str, overwrite: bool = False, **kwargs) -> dict:
        string = json.dumps(obj, indent=4, **kwargs)
        if os.path.exists(filepath) and not overwrite:
            raise ValueError(f"File already exists and overwrite flag is set to False: {filepath}")
        with open(filepath, "w") as file:
            file.write(string)
        return obj

    def decorator(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            save_path = kwargs.get("save")
            output = func(*args, **kwargs)
            if not save_path:
                return output
            self(obj=output, filepath=save_path)
        return wrapper

    def metadecorator(
            self,
            filepath: Optional[str] = None,
            overwrite: bool = False,
            save_path_argname: Optional[str] = None,
            **kwargs
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                save_path = kwargs.get(save_path_argname or "save", filepath)
                output = func(*args, **kwargs)
                if not save_path:
                    return output
                self(obj=output, filepath=save_path, overwrite=overwrite, **kwargs)
            return wrapper
        return decorator


json_save = JsonSave.instance()
