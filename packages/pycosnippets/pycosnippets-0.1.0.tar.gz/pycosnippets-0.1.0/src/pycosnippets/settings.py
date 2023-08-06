import os


PYCO_TIMEOUT = int(os.environ.get(
    "PYCO_TIMEOUT",
    default=600
))

PYCO_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Jupyter Notebook

PYCO_NOTEBOOK_VERSION = int(os.environ.get(
    "PYCO_NOTEBOOK_VERSION",
    default=4
))

# Testing

PYCO_TEST_SNIPPET = """
pyco.load_gist(
    u="rhdzmota",
    g="9aa444dfb15b5d8a96d1204bf173309a",
    f="hello.py",
)

hello(world="{world}")
"""

# Templates settings

PYCO_NOTEBOOK_TEMPLATE_NAME = os.environ.get(
    "PYCO_NOTEBOOK_TEMPLATE",
    default="default.ipynb"
)

PYCO_NOTEBOOK_TEMPLATE_PATH = os.environ.get(
    "PYCO_NOTEBOOK_TEMPLATE_PATH",
    default=os.path.join(PYCO_BASE_PATH, "templates", PYCO_NOTEBOOK_TEMPLATE_NAME)
)

PYCO_NOTEBOOK_TEMPLATE_OUTPUT_PATH = os.environ.get(
    "PYCO_NOTEBOOK_TEMPLATE_OUTPUT_PATH",
    default=os.path.join(PYCO_BASE_PATH, ".out")
)

# Create template output path if not exists
os.makedirs(PYCO_NOTEBOOK_TEMPLATE_OUTPUT_PATH, exist_ok=True)

# Commandline

PYCO_CMD_OUTPUT_DIRECTORY = os.environ.get(
    "PYCO_CMD_OUTPUT_DIRECTORY",
    default="."
)
