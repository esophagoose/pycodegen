import dataclasses
from typing import Any, Dict, List, NamedTuple, Optional, Union
import textwrap

TAB = "    "
def type_from_value(value: Any) -> str:
    containers = {list, tuple, set, dict}
    if type(value) in containers:
        name = type(value).__name__.title()
        if len(value) > 0:
            if isinstance(value, dict):
                # TODO: Handle multiple types in dict
                key_type = type_from_value(next(iter(value.keys())))
                value_type = type_from_value(next(iter(value.values())))
                name += f"[{key_type}, {value_type}]"
            else:
                name += f"[{type_from_value(next(iter(value)))}]"
        return name
    return type(value).__name__

@dataclasses.dataclass
class PyFunction:
    name: str
    args: Dict[str, str] = dataclasses.field(default_factory=dict)
    kwargs: Dict[str, str] = dataclasses.field(default_factory=dict)
    docstring: str = ""
    implementation: str = ""

    def generate(self) -> str:
        args = []
        for arg, _type in self.args.items():
            arg_string = f"{arg}: {_type}"
            if not _type:
                arg_string = arg
            args.append(arg_string)
        kwargs = [f"{a}: {type_from_value(v)} = {v}" for a, v in self.kwargs.items()]
        header = f"def {self.name}({', '.join(args + kwargs)}):"
        body = "\n".join([f'"""{self.docstring}"""', self.implementation])
        return f"{header}\n{textwrap.indent(body, TAB)}"


class Var(NamedTuple):
    name: str
    value: Any
    comment: Optional[str] = None

    @staticmethod
    def clean(name: str) -> str:
        """
        Clean name to create a valid variable name.
        """
        return "".join(c if c.isalnum() or c in "_." else "_" for c in name)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> List["Variable"]:
        return [cls(name=key, value=value) for key, value in data.items()]

    def generate(self) -> str:
        if self.comment:
            return f"{self.clean(self.name)} = {self.value}  # {self.comment}"
        return f"{self.clean(self.name)} = {self.value}"

CONTROL_FLOW_STATEMENTS = ["if", "for", "while", "try", "with"]
class ControlFlow(NamedTuple):
    statement: str
    condition: Dict[str, str]

    def _next_statement(self, index: int, conditional: str) -> str:
        if index == 0:
            return self.statement
        if self.statement == "if" and conditional:
            return "elif"
        elif self.statement in ["for", "while", "if"]:
            return "else"
        elif self.statement == "try" and index <= 2:
            return ["except", "finally"][index]
        raise ValueError(f"Invalid control flow statement: {self.statement}, index: {index}")

    def generate(self) -> str:
        code = ""
        if self.statement not in CONTROL_FLOW_STATEMENTS:
            raise ValueError(f"Invalid control flow statement: {self.statement}")
        for i, (conditional, body) in enumerate(self.condition.items()):
            if i > 0:
                code += "\n"
            conditional_statement = f"{self._next_statement(i, conditional)} {conditional}"
            code += "\n".join([
                f"{conditional_statement.strip()}:",
                textwrap.indent(body, TAB),
            ])

        return code

@dataclasses.dataclass
class PyClass:
    name: str
    base_class: str = ""
    docstring: str = ""
    class_vars: List[Var] = dataclasses.field(default_factory=list)
    instance_vars: List[Var] = dataclasses.field(default_factory=list)
    constructor: Dict[str, str] = dataclasses.field(default_factory=dict)
    constructor_body: List[str] = dataclasses.field(default_factory=list)
    functions: List[PyFunction] = dataclasses.field(default_factory=list)
    has_init: bool = True
