"""Extension to t-python-markdown for MkDocs (https://www.mkdocs.org/)"""
from enum import Enum
from t_python_markdown import MarkdownElement


class AdmonitionType(Enum):
  """Admonition types - see class Admonition"""
  NOTE = "note"
  ABSTRACT = "abstract"
  SUMMARY = "summary"
  TLDR = "tldr"
  INFO = "info"
  TODO = "todo"
  TIP = "tip"
  HINT = "hint"
  IMPORTANT = "important"
  SUCCESS = "success"
  CHECK = "check"
  DONE = "done"
  QUESTION = "question"
  HELP = "help"
  FAQ = "faq"
  WARNING = "warning"
  CAUTION = "caution"
  ATTENTION = "attention"
  FAILURE = "failure"
  FAIL = "fail"
  MISSING = "missing"
  DANGER = "danger"
  ERROR = "error"
  BUG = "bug"
  EXAMPLE = "example"
  QUOTE = "quote"
  CITE = "cite"


class Admonition(MarkdownElement):
  """
  MKDOCS admonition extension
  (see https://squidfunk.github.io/mkdocs-material/reference/admonitions/?h=admoni#usage)
  """

  def __init__(self, admonition_type: AdmonitionType, title=None, text=None):
    if not isinstance(admonition_type, AdmonitionType):
      raise ValueError()
    if text is None:
      text = []
    self.__type = admonition_type.value
    self.__title = title
    super().__init__(text)

  def _render_item(self, _parent, _child, _item):
    return _item

  def _render_item_complete(self, _parent, _s):
    if self.__title is not None:
      return f'!!! {self.__type} "{self.__title}"\n    ' + "\n\n    ".join(_s) + "\n"
    return f"!!! {self.__type}\n    " + "\n\n    ".join(_s) + "\n"
