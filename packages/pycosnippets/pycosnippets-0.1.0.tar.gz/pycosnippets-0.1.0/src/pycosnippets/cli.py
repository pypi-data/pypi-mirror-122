import importlib
from typing import Dict, List, Optional

from pycosnippets.pyco import PyCo
from pycosnippets.utils import (
    json_pretty_print,
    json_save,
)
from pycosnippets.settings import (
    PYCO_TEST_SNIPPET,
)


class Main:

    def __init__(self):
        self.pyco = PyCo.instance()

    @json_pretty_print.decorator
    def hello_world(self, world: Optional[str] = None, template_path: Optional[str] = None) -> List[Dict]:
        return self.run_snippet(
            code=PYCO_TEST_SNIPPET.format(world=world or "Pythonista"),
            template_path=template_path,
        )

    @json_pretty_print.decorator
    @json_save.metadecorator(overwrite=True)
    def run_gist(
            self,
            user: str,
            gist_id: str,
            file: str,
            commit: Optional[str] = None,
            save: Optional[str] = None,
            template_path: Optional[str] = None
    ) -> List[Dict]:
        return self.pyco.run_gist(
            u=user,
            g=gist_id,
            f=file,
            c=commit,
            template_path=template_path
        )

    @json_pretty_print.decorator
    @json_save.metadecorator(overwrite=True)
    def run_script(self, filepath: str, save: Optional[str] = None, template_path: Optional[str] = None) -> List[Dict]:
        return self.pyco.run_script(
            filepath=filepath,
            template_path=template_path
        )

    @json_pretty_print.decorator
    @json_save.metadecorator(overwrite=True)
    def run_snippet(self, code: str, save: Optional[str] = None, template_path: Optional[str] = None) -> List[Dict]:
        return self.pyco.run_code(
            code_snippet=code,
            template_path=template_path
        )
