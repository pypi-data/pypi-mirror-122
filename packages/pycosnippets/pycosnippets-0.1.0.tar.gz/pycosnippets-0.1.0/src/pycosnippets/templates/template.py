import os
import time
import hashlib
import json
from typing import Dict, List, Optional

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

from pycosnippets.settings import (
    PYCO_NOTEBOOK_TEMPLATE_PATH,
    PYCO_NOTEBOOK_VERSION,
)


def validate(path: str) -> bool:
    return os.path.exists(path)


def get_id(code: str) -> str:
    now = time.time()
    return f"""{int(now)}-{hashlib.md5(code.encode("utf-8")).hexdigest()}"""


class Template:

    def __init__(
            self,
            path: Optional[str] = None,
            version: Optional[int] = None,
            allow_multiple_snippets: bool = False,
            snippet_lock: bool = False,
            metadata: Optional[Dict] = None
    ):
        self.path = path or PYCO_NOTEBOOK_TEMPLATE_PATH
        self.version = version or PYCO_NOTEBOOK_VERSION
        self.allow_multiple_snippets = allow_multiple_snippets
        self.snippet_lock = snippet_lock
        self.metadata = metadata or {}

    def read(self) -> Dict:
        with open(self.path, "r") as file:
            content = file.read()
        return json.loads(content)

    def write(
            self,
            data: Dict,
            new_filename: Optional[str] = None,
            new_filepath: Optional[str] = None,
    ) -> str:
        content = json.dumps(data, indent=2)
        filename = new_filename or os.path.basename(self.path)
        filepath = new_filepath or os.path.dirname(self.path)
        notebook_path = os.path.join(filepath, filename)
        with open(notebook_path, "w") as file:
            file.write(content)
        return notebook_path

    def get_last_outputs(self) -> List[Dict]:
        data = self.read()
        return data.get("cells", [{}])[-1].get("outputs", [])

    def add_snippet(
            self,
            code: str,
            new_filename: Optional[str] = None,
            new_filepath: Optional[str] = None,
            allow_multiple_snippets: bool = False,
    ) -> 'Template':
        if self.snippet_lock and not self.allow_multiple_snippets:
            raise ValueError("Existing snippet detected.")
        code_id = get_id(code)
        data = self.read()
        for cell in data.get("cells", []):
            if cell["cell_type"] != "code":
                continue
            source = cell.get("source", [])
            if not len(source):
                continue
            first_line, *_ = source
            if not first_line.startswith("# Code Snippet"):
                continue
            cell["source"] = code
            break
        path = self.write(
            data=data,
            new_filename=new_filename or f"{code_id}.ipynb",
            new_filepath=new_filepath
        )
        metadata_snippets = [*self.metadata.get("snippets", []), {"code_id": code_id, "code": code}]
        return Template(
            path=path,
            version=self.version,
            allow_multiple_snippets=allow_multiple_snippets,
            snippet_lock=True,
            metadata={
                **self.metadata,
                "snippets": metadata_snippets,
            }
        )

    def get_notebook_node(self) -> nbformat.notebooknode.NotebookNode:
        with open(self.path) as file:
            return nbformat.read(file, as_version=4)

    def execute(self):
        ep = ExecutePreprocessor(timeout=600)
        nb = self.get_notebook_node()
        try:
            dirpath = os.path.dirname(self.path)
            ep.preprocess(nb, {"metadata": {"path": dirpath}})
        except CellExecutionError:
            print(self.path)
            raise
        finally:
            with open(self.path, mode="w", encoding="utf-8") as file:
                nbformat.write(nb, file, version=4)
