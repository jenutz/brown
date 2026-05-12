import libcst as cst
from functools import partial


class SpacesTransformer(cst.CSTTransformer):
    SPACE_MAP = {
        cst.TypeAlias: {
            "after_type_parameters": True,
            "after_type": True,
            "after_name": False,
            "after_equals": True,
        },
        cst.SimpleStatementSuite: {"leading_whitespace": True},
        cst.Annotation: {"after": True, "before": False},
        cst.AssignTarget: {"before": True, "after": True},
        cst.AssignEqual: {"before": True, "after": True},
        cst.AsName: {"before": True, "after": True},
        cst.ImportFrom: {"before": True, "after": True},
        cst.Import: {"after": True},
        cst.Param: {"after_star": False, "after_param": False},
        cst.Decorator: {"after_at": False},
        cst.Call: {"after_func": False, "before_args": False},
        cst.TypeParam: {"after_star": False},
        cst.ParamSpec: {"after_star": False},
        cst.Colon: {"after": True, "before": False},
        cst.Comma: {"after": True, "before": False},
        cst.Dot: {"after": False, "before": False},
        cst.LeftSquareBracket: {"after": False},
        cst.RightSquareBracket: {"before": False},
        cst.Subscript: {"after_value": False},
        cst.LeftParen: {"after": False},
        cst.RightParen: {"before": False},
        cst.LeftCurlyBrace: {"after": False},
        cst.RightCurlyBrace: {"before": False},
        cst.FormattedStringExpression: {"after": False, "before": False},
        cst.If: {"after": False, "before": True},
        cst.Else: {"before": False},
        cst.IfExp: {"after": True, "before": True},
        cst.CompIf: {"before_test": True, "before": True},
        cst.Try: {"before": False},
        cst.Raise: {"after": True},
        cst.ExceptHandler: {"after": True, "before": False},
        cst.Finally: {"before": False},
        cst.Match: {"after_match": True, "before_colon": False},
        cst.MatchStar: {"before": False},
        cst.MatchMappingElement: {"after": True, "before": False},
        cst.MatchClass: {"after_cls": False, "before_patterns": False},
        cst.BitAnd: {"before": True, "after": True},
        cst.BitAndAssign: {"before": True, "after": True},
        cst.BitInvert: {"before": True, "after": True},
        cst.BitOr: {"before": True, "after": True},
        cst.BitOrAssign: {"before": True, "after": True},
        cst.BitXor: {"before": True, "after": True},
        cst.BitXorAssign: {"before": True, "after": True},
        cst.NamedExpr: {"before": True, "after": True},
        cst.DictComp: {"after": True, "before": False},
        cst.CompFor: {"before": True, "after": True},
        cst.Nonlocal: {"after": True},
        cst.Return: {"after": True},
        cst.Yield: {"after": True},
        cst.Await: {"after": True},
        cst.Del: {"after": True},
        cst.With: {"after": True, "before": False},
        cst.Assert: {"after": True},
        cst.For: {"after_for": True, "before_in": True, "after_in": True, "before_colon": False},
        cst.Lambda: {"after": True},
        cst.ClassDef: {
            "after_class": True,
            "after_name": False,
            "before_colon": False,
            "after_type_parameters": False,
        },
    }

    def on_leave(self, old_node, new_node):
        node_type = type(new_node)

        if node_type in self.SPACE_MAP:
            return self._generic_replace(old_node, new_node, self.SPACE_MAP[node_type])

        method_name = f"leave_{node_type.__name__}"
        handler = getattr(self, method_name, None)

        return handler(old_node, new_node)

    def _generic_replace(self, old_node, new_node, rules=None):
        if not rules:
            print(new_node)
            assert False
        changes = {}
        for attr_name in dir(new_node):
            if "whitespace" not in attr_name:
                continue

            current_value = getattr(new_node, attr_name, None)
            if not isinstance(current_value, cst.SimpleWhitespace):
                continue

            target_value = " "
            for rule_key, should_space in rules.items():
                if rule_key in attr_name:
                    target_value = " " if should_space else ""
                    changes[attr_name] = cst.SimpleWhitespace(value=target_value)
                    break

        return new_node.with_changes(**changes)

    def leave_TrailingWhitespace(self, old_node, new_node):
        return new_node.with_changes(whitespace=cst.SimpleWhitespace(value=""))

    def leave_ComparisonTarget(self, old_node, new_node):
        new_operator = self._generic_replace(
            new_node.operator, new_node.operator, {"after": True, "before": True}
        )
        return new_node.with_changes(operator=new_operator)

    def leave_NotIn(self, old_node, new_node):
        return new_node.with_changes(whitespace_between=cst.SimpleWhitespace(value=" "))

    def leave_BooleanOperation(self, old_node, new_node):
        new_operator = self._generic_replace(
            new_node.operator, new_node.operator, {"after": True, "before": True}
        )
        return new_node.with_changes(operator=new_operator)

    def leave_BinaryOperation(self, old_node, new_node):
        new_operator = self._generic_replace(
            new_node.operator, new_node.operator, {"after": True, "before": True}
        )
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

    def leave_FunctionDef(self, old_node, new_node):
        changes = {
            "whitespace_after_def": True,
            "whitespace_after_name": False,
            "whitespace_before_params": False,
            "whitespace_before_colon": False,
        }
        new_node = self._generic_replace(old_node, new_node, rules=changes)
        if new_node.asynchronous:
            new_async = self._generic_replace(
                new_node.asynchronous, new_node.asynchronous, {"after": True, "before": True}
            )
            new_node = new_node.with_changes(asynchronous=new_async)
        if new_node.returns:
            new_annotation = self._generic_replace(
                new_node.returns, new_node.returns, {"after": True, "before": True}
            )
            new_node = new_node.with_changes(returns=new_annotation)
        if new_node.type_parameters:
            new_node = new_node.with_changes(
                whitespace_after_type_parameters=cst.SimpleWhitespace("")
            )
        return new_node

    def leave_AugAssign(self, old_node, new_node):
        new_operator = self._generic_replace(
            new_node.operator, new_node.operator, {"after": True, "before": True}
        )
        return new_node.with_changes(operator=new_operator)

    def leave_Arg(self, old_node, new_node):
        new_node = self._generic_replace(old_node, new_node, rules={"after": False})
        if new_node.equal is not cst.MaybeSentinel.DEFAULT:
            new_equal = self._generic_replace(
                new_node.equal, new_node.equal, rules={"after": False, "before": False}
            )
            new_node = new_node.with_changes(equal=new_equal)
        return new_node

    def leave_MatchCase(self, old_node, new_node):
        changes = {"after_case": True, "before_colon": False}
        new_node = self._generic_replace(old_node, new_node, rules=changes)
        if new_node.guard:
            changes = {"after_if": True, "before_if": True}
            new_node = self._generic_replace(old_node, new_node, rules=changes)
        return new_node
