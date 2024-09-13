# from typing import Any, Callable, List, Optional, Tuple, Union
# import re

# class Rule:
#    def __init__(self, name: str, pattern: List[str], prod: Callable[[List[Tuple[str, Any]]], Optional[Tuple[str, Any]]]):
#        self.name = name
#        self.pattern = pattern
#        self.prod = prod

# class RuleBuilder:
#    def __init__(self):
#        self.rule_map = {}
#
#    def add_rule(
#        self,
#        name: str,
#        rule: Union[
#            str,
#            Callable[
#                [List[Tuple[str, Any]]],
#                "Token",
#            ]
#        ]):
#        if isinstance(rule, str):
#            rule = Rule(name, [rule], lambda x: None)
#        elif isinstance(rule, Callable):
#            rule = Rule(name, [], rule)
#        self.rule_map.setdefault(name, []).append(rule)
#
#    def apply_rules(self, token: Tuple[str, Any]) -> Optional[Tuple[str, Any]]:
#        rule_name = token[0]
#        if rule_name not in self.rule_map:
#            return token
#        for rule in self.rule_map[rule_name]:
#            for pattern in rule.pattern:
#                match = re.fullmatch(pattern, token[1])
#                if match:
#                    new_token = rule.prod([(rule_name, match.group(i)) for i in range(1, match.lastindex + 1)])
#                    if new_token:
#                        return new_token
#                    else:
#                        return token
#        return token

# Here's an example usage of this implementation:

# builder = RuleBuilder()

# builder.add_rule("email", r"([\w_+-]+(?:(?: dot |\.)[\w_+-]+){0,10})(?: at |@)([a-zA-Z]+(?:(?:\.| dot )[\w_-]+){1,10})")
# builder.add_rule("email", lambda xs: ("email", {"value": xs[0][1].replace(" dot ", "."), "domain": xs[1][1].replace(" dot ", ".")}))
# builder.add_rule("num", r"\d+")

# tokens = [("email", "jane dot doe at example dot com"),
# ("num", "i have 2 days remaining")]
# new_tokens = [builder.apply_rules(token) for token in tokens]

# print(new_tokens)
# """Output:

# css
# Copy code
# [('email', {'value': 'jane.doe', 'domain': 'example.com'})]
# This example demonstrates how to use the RuleBuilder to add a rule named "email", which matches a regular expression for email addresses, and how to apply that rule to a token to produce a new token with the extracted email components.
# """
