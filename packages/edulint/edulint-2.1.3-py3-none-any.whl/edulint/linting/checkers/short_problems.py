from astroid import nodes  # type: ignore
from typing import TYPE_CHECKING, Optional, List, Tuple, Union, Any, Callable

from pylint.checkers import BaseChecker  # type: ignore
from pylint.checkers.utils import only_required_for_messages

if TYPE_CHECKING:
    from pylint.lint import PyLinter  # type: ignore

from edulint.linting.checkers.utils import get_range_params, get_const_value


class Short(BaseChecker):
    name = "short-problems"
    msgs = {
        "R6601": (
            "Use %s.append(%s) instead of %s.",
            "use-append",
            "Emitted when code extends list by a single argument instead of appending it."
        ),
        "R6602": (
            "Use integral division //.",
            "use-integral-division",
            "Emitted when the code uses float division and converts the result to int."
        ),
        "R6603": (
            "Use isdecimal to test if string contains a number.",
            "use-isdecimal",
            "Emitted when the code uses isdigit or isnumeric."
        ),
        "R6604": (
            "Do not use %s loop with else.",
            "no-loop-else",
            "Emitted when the code contains loop with else block."
        ),
        "R6605": (
            "Use elif.",
            "use-elif",
            "Emitted when the code contains else: if construction instead of elif."
        ),
        "R6606": (
            "Remove the for loop, as it makes %s.",
            "remove-for",
            "Emitted when a for loop would always perform at most one iteration."
        ),
        "R6607": (
            "Use %s instead of repeated %s in %s.",
            "no-repeated-op",
            "Emitted when the code contains repeated adition/multiplication instead of multiplication/exponentiation."
        ),
        "R6608": (
            "Redundant arithmetic: %s",
            "redundant-arithmetic",
            "Emitted when there is redundant arithmetic (e.g. +0, *1) in an expression."
        ),
        "R6609": (
            "Use augmenting assignment: '%s %s= %s'",
            "use-augmenting-assignment",
            "Emitted when an assignment can be simplified by using its augmented version.",
        ),
        "R6610": (
            "Do not multiply list with mutable content.",
            "do-not-multiply-mutable",
            "Emitted when a list with mutable contents is being multiplied."
        ),
        "R6611": (
            "Use else instead of elif.",
            "redundant-elif",
            "Emitted when the condition in elif is negation of the condition in the if."
        ),
        "R6612": (
            "Unreachable else.",
            "unreachable-else",
            "Emitted when the else branch is unreachable due to totally exhaustive conditions before."
        )
    }

    def _check_extend(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute) and node.func.attrname == "extend" \
                and len(node.args) == 1 \
                and isinstance(node.args[0], nodes.List) and len(node.args[0].elts) == 1:
            self.add_message("use-append", node=node, args=(
                node.func.expr.as_string(),
                node.args[0].elts[0].as_string(),
                node.as_string()
            ))

    def _check_augassign_extend(self, node: nodes.AugAssign) -> None:
        if node.op == "+=" and isinstance(node.value, nodes.List) and len(node.value.elts) == 1:
            self.add_message("use-append", node=node, args=(
                node.target.as_string(),
                node.value.elts[0].as_string(),
                node.as_string())
            )

    def _check_isdecimal(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute) and node.func.attrname in ("isdigit", "isnumeric"):
            self.add_message("use-isdecimal", node=node)

    def _check_div(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Name) and node.func.name == "int" \
                and len(node.args) == 1 \
                and isinstance(node.args[0], nodes.BinOp) and node.args[0].op == "/":
            self.add_message("use-integral-division", node=node)

    def _check_loop_else(self, nodes: List[nodes.NodeNG], parent_name: str) -> None:
        if nodes:
            self.add_message("no-loop-else", node=nodes[0].parent, args=(parent_name))

    def _check_else_if(self, node: nodes.If) -> None:
        if node.has_elif_block():
            first_body = node.body[0]
            first_orelse = node.orelse[0]
            assert first_body.col_offset >= first_orelse.col_offset
            if first_body.col_offset == first_orelse.col_offset:
                self.add_message("use-elif", node=node.orelse[0])

    def _check_iteration_count(self, node: nodes.For) -> None:

        def get_const(node: nodes.NodeNG) -> Any:
            return node.value if isinstance(node, nodes.Const) else None

        range_params = get_range_params(node.iter)
        if range_params is None:
            return

        start, stop, step = range_params
        start, stop, step = get_const(start), get_const(stop), get_const(step)

        if start is not None and stop is not None and step is not None:
            if start >= stop:
                self.add_message("remove-for", node=node, args=("no iterations",))
            elif start + step >= stop:
                self.add_message("remove-for", node=node, args=("only one iteration",))

    def _check_repeated_operation_rec(self, node: nodes.NodeNG, op: str, name: Optional[str] = None) \
            -> Optional[Tuple[int, str]]:
        if isinstance(node, nodes.BinOp):
            if node.op != op:
                return None

            lt = self._check_repeated_operation_rec(node.left, op, name)
            if lt is None:
                return None

            count_lt, name_lt = lt
            assert name is None or name == name_lt
            rt = self._check_repeated_operation_rec(node.right, op, name_lt)
            if rt is None:
                return None

            count_rt, _ = rt
            return count_lt + count_rt, name

        if (name is None and type(node) in (nodes.Name, nodes.Attribute, nodes.Subscript)) or name == node.as_string():
            return 1, node.as_string()
        return None

    def _check_repeated_operation(self, node: nodes.BinOp) -> None:
        if node.op in ("+", "*"):
            result = self._check_repeated_operation_rec(node, node.op)
            if result is None:
                return

            # DANGER: on some structures, + may be available but not *
            self.add_message("no-repeated-op", node=node, args=(
                "multiplication" if node.op == "+" else "exponentiation",
                "addition" if node.op == "+" else "muliplication",
                node.as_string()
            ))

    def _check_redundant_arithmetic(self, node: Union[nodes.BinOp, nodes.AugAssign]) -> None:
        if isinstance(node, nodes.BinOp):
            op = node.op
            left = get_const_value(node.left)
            right = get_const_value(node.right)
        elif isinstance(node, nodes.AugAssign):
            op = node.op[:-1]
            left = None
            right = get_const_value(node.value)
        else:
            assert False, "unreachable"

        if (op == "+" and (left in (0, "") or right in (0, ""))) \
                or (op == "-" and (left == 0 or right == 0)) \
                or (op == "*" and (left in (0, 1) or right in (0, 1))) \
                or (op == "/" and right == 1) \
                or (op in ("/", "//", "%")
                    and (isinstance(node, nodes.BinOp) and node.left.as_string() == node.right.as_string()
                         or isinstance(node, nodes.AugAssign) and node.target.as_string() == node.value.as_string())) \
                or (op == "**" and right in (0, 1)):
            self.add_message("redundant-arithmetic", node=node, args=(node.as_string(),))

    def _check_augmentable(self, node: Union[nodes.Assign, nodes.AnnAssign]) -> None:
        def add_message(target: str, param: nodes.BinOp) -> None:
            self.add_message("use-augmenting-assignment", node=node, args=(target, node.value.op, param.as_string()))

        if not isinstance(node.value, nodes.BinOp):
            return
        bin_op = node.value

        if isinstance(node, nodes.Assign):
            if len(node.targets) != 1:
                return
            target = node.targets[0].as_string()
        elif isinstance(node, nodes.AnnAssign):
            target = node.target.as_string()
        else:
            assert False, "unreachable"

        if target == bin_op.left.as_string():
            add_message(target, bin_op.right)
        if bin_op.op in "+*|&" and target == bin_op.right.as_string():
            add_message(target, bin_op.left)

    def _check_multiplied_list(self, node: nodes.BinOp) -> None:
        def is_mutable(elem: nodes.NodeNG) -> bool:
            return type(elem) in (nodes.List, nodes.Set, nodes.Dict) \
                or (
                    isinstance(elem, nodes.Call)
                    and isinstance(elem.func, nodes.Name)
                    and elem.func.name in ("list", "set", "dict")
                )

        if node.op != "*" or (not isinstance(node.left, nodes.List) and not isinstance(node.right, nodes.List)):
            return

        assert not isinstance(node.left, nodes.List) or not isinstance(node.right, nodes.List)
        lst = node.left if isinstance(node.left, nodes.List) else node.right

        if any(is_mutable(elem) for elem in lst.elts):
            self.add_message("do-not-multiply-mutable", node=node)

    NEGATED_OP = {
        ">=": "<", "<=": ">", ">": "<=", "<": ">=", "==": "!=", "!=": "==", "is": "is not", "is not": "is",
        "in": "not in", "not in": "in", "and": "or", "or": "and"
    }

    def _check_redundant_elif(self, node: nodes.If) -> None:
        def ops_match(lt: nodes.NodeNG, rt: nodes.NodeNG, lt_transform: Callable[[str], str]) -> bool:
            return all(lt_transform(lt_op) == rt_op for (lt_op, _), (rt_op, _) in zip(lt.ops, rt.ops))

        def to_values(node: nodes.NodeNG) -> List[nodes.NodeNG]:
            return [node.left] + [val for _, val in node.ops]

        def all_are_negations(lt_values: List[nodes.NodeNG], rt_values: List[nodes.NodeNG], new_rt_negated: bool) \
                -> bool:
            return all(is_negation(ll, rr, new_rt_negated) for ll, rr in zip(lt_values, rt_values))

        def strip_nots(node: nodes.NodeNG, negated_rt: bool) -> Tuple[nodes.NodeNG, bool]:
            while isinstance(node, nodes.UnaryOp) and node.op == "not":
                negated_rt = not negated_rt
                node = node.operand
            return node, negated_rt

        def is_negation(lt: nodes.NodeNG, rt: nodes.NodeNG, negated_rt: bool) -> bool:
            lt, negated_rt = strip_nots(lt, negated_rt)
            rt, negated_rt = strip_nots(rt, negated_rt)

            if not isinstance(lt, type(rt)):
                return False

            if isinstance(lt, nodes.BoolOp) and isinstance(rt, nodes.BoolOp):
                if len(lt.values) == len(rt.values) \
                        and ((negated_rt and lt.op == rt.op) or (not negated_rt and Short.NEGATED_OP[lt.op] == rt.op)):
                    return all_are_negations(lt.values, rt.values, negated_rt)
                return False

            if isinstance(lt, nodes.Compare) and isinstance(rt, nodes.Compare):
                if len(lt.ops) != len(rt.ops):
                    return False

                if negated_rt and ops_match(lt, rt, lambda op: op):
                    return all_are_negations(to_values(lt), to_values(rt), negated_rt)

                if not negated_rt and ops_match(lt, rt, lambda op: Short.NEGATED_OP[op]):
                    return all_are_negations(to_values(lt), to_values(rt), not negated_rt)

                return False

            return negated_rt and lt.as_string() == rt.as_string()

        if not node.has_elif_block():
            return

        if_test = node.test
        elif_test = node.orelse[0].test

        if is_negation(if_test, elif_test, negated_rt=False):
            self.add_message("redundant-elif", node=node.orelse[0])
            if len(node.orelse[0].orelse) > 0:
                self.add_message("unreachable-else", node=node.orelse[0].orelse[0])

    @only_required_for_messages("use-append", "use-isdecimal", "use-integral-division")
    def visit_call(self, node: nodes.Call) -> None:
        self._check_extend(node)
        self._check_isdecimal(node)
        self._check_div(node)

    @only_required_for_messages("use-append", "redundant-arithmetic")
    def visit_augassign(self, node: nodes.AugAssign) -> None:
        self._check_augassign_extend(node)
        self._check_redundant_arithmetic(node)

    @only_required_for_messages("no-loop-else")
    def visit_while(self, node: nodes.While) -> None:
        self._check_loop_else(node.orelse, "while")

    @only_required_for_messages("no-loop-else", "remove-for")
    def visit_for(self, node: nodes.For) -> None:
        self._check_loop_else(node.orelse, "for")
        self._check_iteration_count(node)

    @only_required_for_messages("use-elif", "redundant-elif")
    def visit_if(self, node: nodes.If) -> None:
        self._check_else_if(node)
        self._check_redundant_elif(node)

    @only_required_for_messages("no-repeated-op", "redundant-arithmetic", "do-not-multiply-mutable")
    def visit_binop(self, node: nodes.BinOp) -> None:
        self._check_repeated_operation(node)
        self._check_redundant_arithmetic(node)
        self._check_multiplied_list(node)

    @only_required_for_messages("use-augmenting-assignment")
    def visit_assign(self, node: nodes.Assign) -> None:
        self._check_augmentable(node)

    @only_required_for_messages("use-augmenting-assignment")
    def visit_annassign(self, node: nodes.AnnAssign) -> None:
        self._check_augmentable(node)


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(Short(linter))
