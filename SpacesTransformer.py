import libcst as cst
from functools import partial


class SpacesTransformer(cst.CSTTransformer):
    def __init__(self):
        pass

    def _generic_replace(self, old_node, new_node, rules=None):
        if rules is None:
            rules = {"before": True, "after": True}

        changes = {}
        for attr_name in dir(new_node):
            if "whitespace" not in attr_name:
                continue

            current_value = getattr(new_node, attr_name, None)
            if not isinstance(current_value, cst.SimpleWhitespace):
                continue

            target_value = " "
            # print(attr_name)
            for rule_key, should_space in rules.items():
                if rule_key in attr_name:
                    target_value = " " if should_space else ""
                    changes[attr_name] = cst.SimpleWhitespace(value=target_value)
                    break

        return new_node.with_changes(**changes)

    def leave_TrailingWhitespace(self, old_node, new_node):
        return new_node.with_changes(whitespace=cst.SimpleWhitespace(value=""))

    def leave_ComparisonTarget(self, old_node, new_node):
        new_operator = self._generic_replace(new_node.operator, new_node.operator)
        return new_node.with_changes(operator=new_operator)

    def leave_NotIn(self, old_node, new_node):
        return new_node.with_changes(whitespace_between=cst.SimpleWhitespace(value=" "))

    def leave_BooleanOperation(self, old_node, new_node):
        new_operator = self._generic_replace(new_node.operator, new_node.operator)
        return new_node.with_changes(operator=new_operator)

    def leave_BinaryOperation(self, old_node, new_node):
        new_operator = self._generic_replace(new_node.operator, new_node.operator)
        return new_node.with_changes(operator=new_operator)

    def leave_UnaryOperation(self, old_node, new_node):
        match new_node.operator:
            case cst.Not():
                new_operator = new_node.operator.with_changes(
                    whitespace_after=cst.SimpleWhitespace(value=" ")
                )
            case _:
                new_operator = new_node.operator.with_changes(
                    whitespace_after=cst.SimpleWhitespace(value="")
                )
        return new_node.with_changes(operator=new_operator)

    leave_TypeAlias = partial(
        _generic_replace,
        rules={
            "after_type_parameters": True,
            "after_type": True,
            "after_name": False,
            "after_equals": True,
        },
    )

    def leave_FunctionDef(self, old_node, new_node):
        changes = {
            "whitespace_after_def": True,
            "whitespace_after_name": False,
            "whitespace_before_params": False,
            "whitespace_before_colon": False,
        }
        new_node = self._generic_replace(old_node, new_node, rules=changes)
        if new_node.asynchronous:
            new_async = self._generic_replace(new_node.asynchronous, new_node.asynchronous)
            new_node = new_node.with_changes(asynchronous=new_async)
        if new_node.returns:
            new_annotation = self._generic_replace(new_node.returns, new_node.returns)
            new_node = new_node.with_changes(returns=new_annotation)
        if new_node.type_parameters:
            new_node = new_node.with_changes(
                whitespace_after_type_parameters=cst.SimpleWhitespace("")
            )
        return new_node

    def leave_AugAssign(self, old_node, new_node):
        new_operator = self._generic_replace(new_node.operator, new_node.operator)
        return new_node.with_changes(operator=new_operator)

    leave_Annotation = partial(_generic_replace, rules={"after": True, "before": False})

    # for AnnAssign
    leave_AssignTarget = _generic_replace
    leave_AssignEqual = _generic_replace

    leave_AsName = _generic_replace
    leave_ImportFrom = _generic_replace

    leave_Param = partial(_generic_replace, rules={"after_star": False, "after_param": False})
    leave_Decorator = partial(_generic_replace, rules={"after_at": False})
    leave_Call = partial(_generic_replace, rules={"after_func": False, "before_args": False})

    def leave_Arg(self, old_node, new_node):
        new_node = self._generic_replace(old_node, new_node, rules={"after": False})
        if new_node.equal is not cst.MaybeSentinel.DEFAULT:
            new_equal = self._generic_replace(
                new_node.equal, new_node.equal, rules={"after": False, "before": False}
            )
            new_node = new_node.with_changes(equal=new_equal)
        return new_node

    leave_TypeParam = partial(_generic_replace, rules={"after_star": False})
    leave_ParamSpec = partial(_generic_replace, rules={"after_star": False})

    leave_Colon = partial(_generic_replace, rules={"after": True, "before": False})
    leave_Comma = partial(_generic_replace, rules={"after": True, "before": False})
    leave_Dot = partial(_generic_replace, rules={"after": False, "before": False})
    leave_LeftSquareBracket = partial(_generic_replace, rules={"after": False})
    leave_RightSquareBracket = partial(_generic_replace, rules={"before": False})
    leave_Subscript = partial(_generic_replace, rules={"after_value": False})

    leave_LeftParen = partial(_generic_replace, rules={"after": False})
    leave_RightParen = partial(_generic_replace, rules={"before": False})
    leave_LeftCurlyBrace = partial(_generic_replace, rules={"after": False})
    leave_RightCurlyBrace = partial(_generic_replace, rules={"before": False})

    leave_FormattedStringExpression = partial(
        _generic_replace, rules={"after": False, "before": False}
    )

    leave_If = partial(_generic_replace, rules={"after": False, "before": True})
    leave_Else = partial(_generic_replace, rules={"before": False})
    leave_IfExp = partial(_generic_replace, rules={"after": True, "before": True})
    leave_CompIf= partial(_generic_replace, rules={"before_test": True, "before": True})

    leave_Try = partial(_generic_replace, rules={"before": False})
    leave_Raise = partial(_generic_replace, rules={"after": True})
    leave_ExceptHandler = partial(_generic_replace, rules={"after": True, "before" : False})
    leave_Finally = partial(_generic_replace, rules={"before" : False})

    leave_Match = partial(_generic_replace, rules={"after_match": True, "before_colon": False})

    def leave_MatchCase(self, old_node, new_node):
        changes = {"after_case": True, "before_colon": False}
        new_node = self._generic_replace(old_node, new_node, rules=changes)
        if new_node.guard:
            changes = {"after_if": True, "before_if": True}
            new_node = self._generic_replace(old_node, new_node, rules=changes)
        return new_node

    leave_MatchStar = partial(_generic_replace, rules={"before": False})
    leave_MatchMappingElement = partial(_generic_replace, rules={"after": True, "before": False})
    leave_MatchClass = partial(
        _generic_replace, rules={"after_cls": False, "before_patterns": False}
    )
    leave_BitAnd = leave_BitAndAssign = leave_BitInvert = _generic_replace
    leave_BitOr = leave_BitOrAssign = leave_BitXor = _generic_replace
    leave_BitXorAssign = _generic_replace

    leave_NamedExpr = _generic_replace
    leave_DictComp = partial(_generic_replace, rules={"after": True, "before": False})
    leave_CompFor = _generic_replace

    leave_Nonlocal = partial(_generic_replace, rules={"after": True})
    leave_Return = partial(_generic_replace, rules={"after": True})
    leave_Yield = partial(_generic_replace, rules={"after": True})
    leave_Await = partial(_generic_replace, rules={"after": True})
    leave_Del = partial(_generic_replace, rules={"after": True})
    leave_With = partial(_generic_replace, rules={"after": True, "before": False})
    leave_Assert = partial(_generic_replace, rules={"after": True})

    leave_For = partial(_generic_replace, rules={"after_for": True, "before_in": True, "after_in":True, "before_colon":False})

    leave_Lambda  = partial(_generic_replace, rules={"after": True})

    leave_ClassDef = partial(
        _generic_replace, rules={"after_class": True, "after_name": False, "before_colon": False}
    )