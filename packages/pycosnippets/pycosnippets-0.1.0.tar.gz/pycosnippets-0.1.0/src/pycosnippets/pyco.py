import os
import sys
import time
from uuid import uuid4
from typing import Dict, List, Optional, Tuple
from multiprocessing import Process, Manager
from traitlets.config.configurable import SingletonConfigurable

import IPython

from pycosnippets.gists import Gist
from pycosnippets.templates import Template
from pycosnippets.utils import get_code_id
from pycosnippets.settings import PYCO_NOTEBOOK_TEMPLATE_OUTPUT_PATH


def run_code(snippet: str, template_path: Optional[str] = None) -> Tuple[str, List[Dict]]:
    template = Template(path=template_path)
    notebook = template.add_snippet(code=snippet, new_filepath=PYCO_NOTEBOOK_TEMPLATE_OUTPUT_PATH)
    notebook.execute()
    last_code_id = notebook.metadata["snippets"][-1]["code_id"]
    last_outputs = notebook.get_last_outputs()
    return last_code_id, last_outputs


def run_worker(execution_id: str, executions: Dict, snippet: str, template_path: Optional[str] = None):
    code_id, output = run_code(snippet=snippet, template_path=template_path)
    executions[execution_id] = {
        "code_id": code_id,
        "output": output
    }


class PyCo(SingletonConfigurable):

    def __init__(self):
        # TODO: delete all the multiprocessing implementation
        # TODO: Save both the executions & cache in a external datastore (i.e. Redis)
        # self.manager = Manager()
        self.executions = {}  # self.manager.dict()
        self.cache = {}  # TODO: load previous state

    def info(self) -> Dict:
        return {
            "pyco_id": id(self),
            "timestamp": time.time(),
            "records": {
                "executions": len(self.executions),
                "cache": len(self.cache)
            },
            "mem": {
                "executions": sys.getsizeof(self.executions),
                "cache": sys.getsizeof(self.cache)
            }
        }

    @property
    def ipython(self):
        return IPython.get_ipython()

    def magic(self, line: str):
        return self.ipython.magic(line)

    @staticmethod
    def get_gist(u: str, g: str, f: str, c: Optional[str] = None) -> str:
        gist = Gist(username=u, gist_id=g, filename=f, commit=c)
        return gist.get_code()

    def load_code(self, code_snippet: str):
        user_ns = getattr(self.ipython, 'user_ns', globals())
        exec(compile(code_snippet, f"{int(time.time())}", "exec"), user_ns, user_ns)

    def load_gist(self, u: str, g: str, f: str, c: Optional[str] = None):
        gist = Gist(username=u, gist_id=g, filename=f, commit=c)
        code_snippet = gist.get_code()
        self.load_code(code_snippet=code_snippet)

    @staticmethod
    def get_script(filepath: str) -> str:
        if not os.path.exists(filepath):
            raise ValueError(f"Script not found: {filepath}")
        with open(filepath, "r") as file:
            return file.read()

    def load_script(self, filepath: str):
        code_snippet = self.get_script(filepath)
        self.load_code(code_snippet=code_snippet)

    def run_code(
            self,
            code_snippet: str,
            template_path: Optional[str] = None,
            use_cache: bool = False,
            external_metadata: Optional[Dict] = None,
    ) -> Dict:
        if not use_cache:
            return self.run_code_without_cache(
                code_snippet=code_snippet,
                template_path=template_path,
                external_metadata=external_metadata
            )
        _, *code_id = get_code_id(code=code_snippet).split("-")
        output = self.cache.get("".join(code_id))
        return output if output else self.run_code(
            use_cache=False,
            code_snippet=code_snippet,
            template_path=template_path,
            external_metadata=external_metadata
        )

    def run_code_without_cache(
            self,
            code_snippet: str,
            template_path: Optional[str] = None,
            external_metadata: Optional[Dict] = None
    ) -> Dict:
        start = time.time()
        # Create an unique execution id to facilitate output retrieval
        execution_id = str(uuid4())
        run_worker(execution_id, self.executions, code_snippet, template_path)
        # Get the execution output and save to cache
        res = self.executions[execution_id]
        _, *code_id = res["code_id"].split("-")
        output = {
            "timestamp_start": start,
            "timestamp_final": time.time(),
            "output": res["output"],
            "metadata": external_metadata
        }
        self.cache["".join(code_id)] = output
        return output

    def run_gist(
            self,
            u: str,
            g: str,
            f: str,
            c: Optional[str] = None,
            template_path: Optional[str] = None,
            use_cache: bool = False,
    ) -> Dict:
        gist = Gist(username=u, gist_id=g, filename=f, commit=c)
        code_snippet = gist.get_code()
        return self.run_code(
            code_snippet=code_snippet,
            template_path=template_path,
            use_cache=use_cache,
        )

    def run_script(
            self,
            filepath: str,
            template_path: Optional[str] = None,
            use_cache: bool = False,
    ) -> Dict:
        code_snippet = self.get_script(filepath)
        return self.run_code(
            code_snippet=code_snippet,
            template_path=template_path,
            use_cache=use_cache,
        )
