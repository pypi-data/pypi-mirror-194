import inspect
from dataclasses import dataclass
from typing import Optional, List, Callable


@dataclass
class ArgumentProperties:
    """
    A data class representing the properties of a function argument.

    Attributes
    ----------
    name : str
        The name of the argument.
    annotation : Optional[str], optional
        The type annotation of the argument, if specified.
    default : Optional[str], optional
        The default value of the argument, if specified.
    """

    name: str
    annotation: Optional[str]
    default: Optional[str]


@dataclass
class FunctionProperties:
    """
    A data class representing the properties of a function.

    Attributes
    ----------
    name : str
        The name of the function.
    module : str
        The name of the module containing the function.
    result_annotation : str
        The return type annotation of the function.
    args_properties : List[ArgumentProperties]
        A list of ArgumentProperties representing the function's arguments.
    n_not_defaults : int
        The number of non-default arguments in the function.
    n_defaults : int
        The number of arguments with default values in the function.
    """

    name: str
    module: str
    result_annotation: str
    args_properties: List[ArgumentProperties]
    n_not_defaults: int
    n_defaults: int


def get_function_properties(function: Callable) -> FunctionProperties:
    """
    Returns the properties of a function.

    Parameters
    ----------
    function : Callable
        The function to get properties for.

    Returns
    -------
    FunctionProperties
        A FunctionProperties object representing the properties of the function.
    """
    sig = inspect.signature(function)

    args_prop = []

    for name, param in sig.parameters.items():
        args_prop.append(
            ArgumentProperties(
                **{
                    "name": param._name,
                    "annotation": param.annotation
                    if not (param.annotation == inspect._empty)
                    else None,
                    "default": param.default if not (param.default == inspect._empty) else None,
                }
            )
        )

    return FunctionProperties(
        **{
            "name": function.__name__,
            "module": function.__module__,
            "result_annotation": sig.return_annotation,
            "args_properties": args_prop,
            "n_not_defaults": sum(1 for arg in args_prop if arg.default is None),
            "n_defaults": sum(1 for arg in args_prop if arg.default is not None),
        }
    )
