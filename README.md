# py-codegen

A Python library for programmatically generating Python code with proper formatting and structure.

## Features

- Generate Python functions with type hints and docstrings
- Create control flow statements (`if`/`elif`/`else`, `for`, `while`, `try`/`except`)
- Generate Python classes with constructors and methods
- Create variables with automatic type inference
- Automatic code formatting with proper indentation
- Support for complex data structures and nested types

## Example

Here's a quick example of how to use `pycodegen` to generate a Python function with control flow:
```
import gen_types


cf = gen_types.ControlFlow(
    statement="if",
    condition={"a == 1": "return a", "a == 2": "return b", "": "return c"},
)

func = gen_types.PyFunction(
    name="func",
    args={"a": "int", "b": "int"},
    kwargs={"c": 3, "d": [1, 2, 3]},
    docstring="This is a function",
    implementation="\n".join([
        cf.generate(),
        "return a + b + c + e",
    ]),
)

print(func.generate())
```

This code will generate the follow Python code:
```
def func(a: int, b: int, c: int = 3, d: List[int] = [1, 2, 3]):
    """This is a function"""
    if a == 1:
        return a
    elif a == 2:
        return b
    else:
        return c
    return a + b + c + e
```
