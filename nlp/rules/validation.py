from . import _validators
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Type,
    Union,
    overload
)
import yaml
from loguru import logger

from nlp.tokens import Token
from nlp.utils.cli import print_color

IN = "in"
NOT_IN = "not_in"
VALIDATOR = "validator"
VALIDATION = "validation"
FOLLOWS = "follows"


class CumulativeCallback:
    """
    A callable object that runs multiple callbacks, returning True if any of them return True.

    Args:
        None

    Attributes:
        _callbacks (List[Callable]): A list of callbacks to be run.

    Examples:
        >>> def callback1():
        ...     return False
        ...
        >>> def callback2():
        ...     return True
        ...
        >>> def callback3():
        ...     return False
        ...
        >>> cp = CumulativeCallback()
        >>> cp.add(callback1)
        >>> cp.add(callback2)
        >>> cp.add(callback3)
        >>> cp(True, False)
        True
        >>> cp(False, False)
        False
    """

    def __init__(self):
        self._callbacks: List[Callable] = []

    def __call__(self, *args) -> bool:
        """
        Call all the registered callbacks with the given args and return True if any of them return True.

        Args:
            *args (Any): Arguments to be passed to the callbacks.

        Returns:
            bool: True if any of the registered callbacks returned True.

        """
        for cb in self._callbacks:
            result = cb(*args)
            if result:
                return True
        return False

    def add(self, callback: Callable) -> None:
        """
        Add a callback to the list of registered callbacks.

        Args:
            callback (Callable): A callable object to be registered.

        Returns:
            None
        """
        self._callbacks.append(callback)

    def __iadd__(self, callback: Callable) -> "CumulativeCallback":
        """
        Add a callback to the list of registered callbacks.

        Args:
            callback (Callable): A callable object to be registered.

        Returns:
            CumulativeCallback: The CumulativeCallback object itself.
        """
        self.add(callback)
        return self

    def __repr__(self):
        return f"CumulativeCallback(callbacks={len(self._callbacks)})"


def compare_metadata(token, metadata: Dict[str, Any]) -> bool:
    valid = []
    for k, v in metadata.items():
        valid.append(
            (token.metadata.get(k) if token.metadata is not None else None) == v)
    return all(valid)


class Validator:
    def __init__(
        self,
        first: Callable[[Token], bool],
        second: Callable[[Token], bool],
        rules: Dict[str, Any],
    ):
        self.first = first
        self.second = second
        self.rules = rules

    def validate(self, first: Token, second: Token, *, verbose: bool = False) -> bool:
        res = self.first(first) and self.second(second)
        if verbose:
            pass
            # ...
        return res


_VALIDATORS: Dict[str, Callable[[Token], bool]] = dict()


def register_validator(name, validator: Callable[[Token, Dict[str, Any]], bool]) -> None:
    if name in _VALIDATORS:
        raise ValueError("validator with name %r already exists!" % name)
    _VALIDATORS[name] = validator


_validators.register()


@logger.catch
def make_callback(rule: Dict[str, Any]) -> Validator:
    first_rule = rule.copy()
    first_rule.pop(FOLLOWS, None)
    validator = first_rule.pop(VALIDATOR)
    first = partial(_VALIDATORS[validator], rule=first_rule)
    second = CumulativeCallback()
    follows = rule.get(FOLLOWS)
    if follows:
        for rule_ in follows:
            validator = rule_.pop(VALIDATOR)
            second += partial(_VALIDATORS[validator], rule=rule_)
    else:
        second += lambda *_, **__: False
    return Validator(first, second, rule)

# def make_callback(rule: Dict[str, Any]) -> Validator:
#    first_rule = rule.copy()
#    first_rule.pop(FOLLOWS, None)
#    validator = first_rule.pop(VALIDATOR)
#    first = partial(_VALIDATORS[validator],  rule=first_rule)
#    second = CumulativeCallback()
#    follows = rule.get(FOLLOWS)
#    if follows:
#        for rule_ in follows:
#            validator = rule_.pop(VALIDATOR)
#            second += partial(_VALIDATORS[validator], rule=rule_)
#    else:
#        second += lambda *_, **__: False
#    validator = Validator(first, second)
#    validator.rules = rule
#    return validator


@overload
def build_rules(rules: List[Dict[str, Any]]) -> Dict[str, List[Validator]]: ...


@overload
def build_rules(path: str) -> Dict[str, List[Validator]]: ...


def build_rules(rules: Union[str, List[Dict[str, Any]]]) -> Dict[str, List[Validator]]:
    if isinstance(rules, str):
        with open(rules, encoding="utf-8") as fd:
            rules = list(yaml.load_all(fd, yaml.FullLoader))
    elif not isinstance(rules, list):
        raise ValueError(
            "rules must be a list of dictionaries or a path to a YAML file")

    rule_callbacks: Dict[str, List[Validator]] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("each rule must be a dictionary")
        if VALIDATOR not in rule:
            raise ValueError(f"missing '{VALIDATOR}' key in rule {rule}")
        validator = rule[VALIDATOR]
        if validator not in rule_callbacks:
            rule_callbacks[validator] = []
        callback = make_callback(rule)
        if callback is not None:
            rule_callbacks[validator].append(callback)
    return rule_callbacks


# def build_rules(rules: Union[str, List[Dict[str, Any]]]) -> Dict[str, List[Validator]]:
#    if isinstance(rules, str):
#        with open(rules, encoding="utf-8") as fd:
#            rules = list(yaml.load_all(fd, yaml.FullLoader))
#    rule_callbacks: Dict[str, List[Validator]] = {}
#    for rule in rules:
#        validator = rule[VALIDATOR]
#        if validator not in rule_callbacks:
#            rule_callbacks[validator] = []
#        callback = make_callback(rule)
#        if callback is not None:
#            rule_callbacks[validator].append(callback)
#    logger.info("VALIDATORS: {}", len(_VALIDATORS))
#    return rule_callbacks
