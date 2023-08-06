from lark import Lark, Token, Tree
from importlib.resources import files
from ..logic import Equation, Function, Sequent, Term, Variable, substitute


tptp_grammar = files('foe.parser').joinpath('tptp_grammar.lark').read_text()
tptp_parser = Lark(tptp_grammar, start='tptp_file')


def from_tptp_file(file: str, include_dir: str = "") -> list[Sequent]:
    """
    Parse a TPTP file and return a list of sequents.

    Parameters
    ----------
    file : str
        Path to the TPTP file.
    include_dir : str, optional
        Path to the directory containing the included files, by default ""

    Returns
    -------
    list[Sequent]
        List of sequents.
    """
    with open(file, 'r') as f:
        input = f.read()
    return parse_tptp_file(tptp_parser.parse(input))


def parse_tptp_file(input: Tree) -> dict:
    result = {
        "include": [],
        "axiom": [],
        "negated_conjecture": [],
        "functions": set(),
        "variables": {},
    }
    _parse_tptp_file(input, result)
    return result


def _parse_tptp_file(input: Tree, result: dict):
    for i in input.children:
        match i.children[0].data.value:
            case "include":
                result["include"].append(i.children[0])
            case "annotated_formula":
                _parse_annotated_formula(i.children[0], result)


def _parse_annotated_formula(input: Tree, data: dict):
    match input.children[0].data.value:
        case "fof_annotated":
            return _parse_fof_annotated(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_annotated' allowed, \
input contains {input.children[0].data.value}")


def _parse_fof_annotated(input: Tree, data: dict) -> Term:
    match input.children[1].value:
        case "axiom" | "hypothesis" | "definition" | \
          "assumption" | "lemma" | "theorem":
            data["axiom"].append(
                _parse_fof_formula(input.children[2], data)
            )
        case "negated_conjecture":
            data["negated_conjecture"].append(
                _parse_fof_formula(input.children[2], data)
            )
        case "conjecture":
            data["negated_conjecture"].append(
                Function("not", (_parse_fof_formula(input.children[2], data),))
            )


def _parse_fof_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_logic_formula":
            return _parse_fof_logic_formula(input.children[0], data)
        case _:
            raise ValueError(
                f"Only 'fof_logic_formula'allowed, \
input contains {input.children[0].data.value}")


def _parse_fof_logic_formula(input: Tree, data: dict) -> list[Term]:
    match input.children[0].data.value:
        case "fof_binary_formula":
            return _parse_fof_binary_formula(input.children[0], data)
        case "fof_unitary_formula":
            return _parse_fof_unitary_formula(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_binary_formula', \
'fof_unitary_formula' allowed, input contains {input.children[0].data.value}")


def _parse_fof_binary_formula(input: Tree, data: dict) -> list[Term]:
    match input.children[0].data.value:
        case "fof_binary_nonassoc":
            return _parse_fof_binary_nonassoc(input.children[0], data)
        case "fof_binary_assoc":
            return _parse_fof_binary_assoc(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_binary_nonassoc' and \
'fof_binary_assoc' allowed, input contains {input.data.value}")


def _parse_fof_binary_nonassoc(input: Tree, data: dict) -> Term:
    left = _parse_fof_unitary_formula(input.children[0], data)
    op = input.children[1].value
    right = _parse_fof_unitary_formula(input.children[2], data)
    match op:
        case "<=>":
            return Function("iff", [left, right])
        case "=>":
            return Function("implies", [left, right])
        case "<=":
            return Function("implies", [right, left])
        case "<~>":
            return Function("xor", [left, right])
        case "~|":
            return Function("nor", [left, right])
        case "~&":
            return Function("nand", [left, right])


def _parse_fof_binary_assoc(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_or_formula":
            return _parse_fof_or_formula(input.children[0], data)
        case "fof_and_formula":
            return _parse_fof_and_formula(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_or_formula' and \
'fof_and_formula' allowed, input contains {input.data.value}")


def _parse_fof_or_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_unitary_formula":
            left = _parse_fof_unitary_formula(input.children[0], data)
        case "fof_or_formula":
            left = _parse_fof_or_formula(input.children[0], data)
    right = _parse_fof_unitary_formula(input.children[1], data)
    return Function("or", [left, right])


def _parse_fof_and_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_unitary_formula":
            left = _parse_fof_unitary_formula(input.children[0], data)
        case "fof_and_formula":
            left = _parse_fof_and_formula(input.children[0], data)
    right = _parse_fof_unitary_formula(input.children[1], data)
    return Function("and", [left, right])


def _parse_fof_unitary_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_quantified_formula":
            return _parse_fof_quantified_formula(input.children[0], data)
        case "fof_unary_formula":
            return _parse_fof_unary_formula(input.children[0], data)
        case "fof_atomic_formula":
            return _parse_fof_atomic_formula(input.children[0], data)
        case "fof_logic_formula":
            return _parse_fof_logic_formula(input.children[0], data)


def _parse_fof_quantified_formula(input: Tree, data: dict) -> Term:
    quantifier = input.children[0].value
    variables = _parse_fof_variable_list(input.children[1], data)
    formula = _parse_fof_unitary_formula(input.children[2], data)
    match quantifier:
        case "!":
            return Function(f"forall{len(variables)}", variables + (formula,))
        case "?":
            return Function(f"exists{len(variables)}", variables + (formula,))


def _parse_fof_variable_list(input: Tree, data: dict) -> list[Term]:
    return tuple(
        _parse_variable(i, data) for i in input.children
    )


def _parse_variable(input: Tree, data: dict) -> Term:
    if input not in data["variables"]:
        data["variables"][input] = Variable(len(data["variables"]))
    return data["variables"][input]


def _parse_fof_unary_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_unitary_formula":
            return Function(
                "not",
                [_parse_fof_unitary_formula(input.children[0], data)]
            )
        case "fof_infix_unary":
            return _parse_fof_infix_unary(input.children[0], data)


def _parse_fof_infix_unary(input: Tree, data: dict) -> Term:
    left = _parse_fof_term(input.children[0], data)
    right = _parse_fof_term(input.children[2], data)
    return Function("neq", [left, right])


def _parse_fof_term(input: Tree, data: dict) -> Term:
    if type(input.children[0]) == Token:
        return _parse_variable(input.children[0], data)
    match input.children[0].data.value:
        case "fof_function_term":
            return _parse_fof_function_term(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_function_term' and 'VARIABLE' \
                allowed, input contains {input.children[0].data.value}")


def _parse_fof_function_term(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_plain_term":
            return _parse_fof_plain_term(input.children[0], data, False)
        case _:
            raise ValueError(f"Only 'fof_plain_term' \
                allowed, input contains {input.children[0].data.value}")


def _parse_fof_plain_term(
        input: Tree | Token,
        data: dict,
        predicate: bool
) -> Term:
    data["functions"].add(
        (input.children[0].value, len(input.children) - 1, predicate)
    )
    match len(input.children):
        case 1:
            return Function(input.children[0].value, [])
        case _:
            return Function(
                input.children[0].value,
                [
                    _parse_fof_term(i, data)
                    for i in input.children[1].children
                ]
            )


def _parse_fof_plain_atomic_formula(input: Tree, data: dict) -> Term:
    return _parse_fof_plain_term(input.children[0], data, True)


def _parse_fof_atomic_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_plain_atomic_formula":
            return _parse_fof_plain_atomic_formula(input.children[0], data)
        case "fof_defined_atomic_formula":
            return _parse_fof_defined_atomic_formula(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_plain_atomic_formula' \
allowed, input contains {input.children[0].data.value}")


def _parse_fof_defined_atomic_formula(input: Tree, data: dict) -> Term:
    match input.children[0].data.value:
        case "fof_defined_infix_formula":
            return _parse_fof_defined_infix_formula(input.children[0], data)
        case _:
            raise ValueError(f"Only 'fof_defined_infix_formula' \
allowed, input contains {input.children[0].data.value}")


def _parse_fof_defined_infix_formula(input: Tree, data: dict) -> Term:
    left = _parse_fof_term(input.children[0], data)
    right = _parse_fof_term(input.children[2], data)
    return Function("eq", [left, right])


def skolemize(term: Term, skolem_counter: int) -> Term:
    return _skolemize(term, {"counter": skolem_counter}, set(), True)


def _skolemize(
        term: Term,
        skolem_counter: dict,
        free_variables: set[Variable],
        arity: bool
) -> Term:
    if type(term) == Variable:
        return term
    if type(term) == Function:
        if term.name.startswith("forall"):
            match arity:
                case True:
                    return _skolemize(
                        term.args[-1],
                        skolem_counter,
                        free_variables | set(term.args[:-1]),
                        True
                    )
                case False:
                    substition = {
                        term.args[i]: Function(
                            f"Sk{skolem_counter['counter'] + i}",
                            tuple(free_variables)
                        )
                        for i in range(len(term.args) - 1)
                    }
                    skolem_counter["counter"] += len(term.args) - 1
                    return _skolemize(
                        substitute(substition, term.args[-1]),
                        skolem_counter,
                        free_variables,
                        False
                    )
        if term.name.startswith("exists"):
            match arity:
                case True:
                    substition = {
                        term.args[i]: Function(
                            f"Sk{skolem_counter['counter'] + i}",
                            tuple(free_variables)
                        )
                        for i in range(len(term.args) - 1)
                    }
                    skolem_counter["counter"] += len(term.args) - 1
                    return _skolemize(
                        substitute(substition, term.args[-1]),
                        skolem_counter,
                        free_variables,
                        True
                    )
                case False:
                    return _skolemize(
                        term.args[-1],
                        skolem_counter,
                        free_variables | set(term.args[:-1]),
                        False
                    )
        match term.name:
            case "not":
                return Function(
                    "not",
                    (
                        _skolemize(
                            term.args[0],
                            skolem_counter,
                            free_variables,
                            not arity
                        ),
                    )
                )
            case "and":
                return Function(
                    "and",
                    tuple(
                        _skolemize(
                            child,
                            skolem_counter,
                            free_variables,
                            arity
                        )
                        for child in term.args
                    )
                )
            case "or":
                return Function(
                    "or",
                    tuple(
                        _skolemize(
                            child,
                            skolem_counter,
                            free_variables,
                            arity
                        )
                        for child in term.args
                    )
                )
            case "implies":
                return _skolemize(
                    Function(
                        "or",
                        (
                            Function("not", (term.args[0],)),
                            term.args[1],
                        )
                    ),
                    skolem_counter,
                    free_variables,
                    arity
                )
            case "iff":
                return _skolemize(
                    Function(
                        "and",
                        [
                            Function("implies", (term.args[0], term.args[1],)),
                            Function("implies", (term.args[1], term.args[0],)),
                        ]
                    ),
                    skolem_counter,
                    free_variables,
                    arity
                )
            case "xor":
                return _skolemize(
                    Function(
                        "or",
                        [
                            Function(
                                "and",
                                (Function("not", [term.args[0]]), term.args[1])
                            ),
                            Function(
                                "and",
                                (term.args[0], Function("not", [term.args[1]]))
                            ),
                        ]
                    ),
                    skolem_counter,
                    free_variables,
                    arity
                )
            case "nor":
                return _skolemize(
                    Function("not", (Function("or", term.args),)),
                    skolem_counter,
                    free_variables,
                    arity
                )
            case "nand":
                return _skolemize(
                    Function("not", (Function("and", term.args),)),
                    skolem_counter,
                    free_variables,
                    arity
                )
            case _:
                return term


def cnf(term: Term) -> Term:
    sequents = []
    for clause in _cnf(term):
        sequents.append(
            Sequent(
                [x for x, y in clause if not y],
                [x for x, y in clause if y]
            )
        )
    return sequents


def _cnf(term: Term) -> Term:
    """
    returns a term in conjunctive normal form

    >>> cnf(Function("and", (Function("or", (Variable(1), Variable(2))),
        Function("or", (Variable(3), Variable(4))))))
    [[(Variable(1), True), (Variable(2), True)],
    [(Variable(3), True), (Variable(4), True)]]
    """
    match term.name:
        case "not":
            d = _dnf(term.args[0])
            return [[(x, not y) for x, y in clause] for clause in d]
        case "and":
            return _cnf(term.args[0]) + _cnf(term.args[1])
        case "or":
            c1 = _cnf(term.args[0])
            c2 = _cnf(term.args[1])
            return [x + y for x in c1 for y in c2]
        case "eq":
            return [[(Equation(term.args[0], term.args[1]), True)]]
        case "neq":
            return [[(Equation(term.args[0], term.args[1]), False)]]
        case _:
            return [[(Equation(term, Function("true", tuple())), True)]]


def dnf(term: Term) -> Term:
    sequents = []
    for clause in _dnf(term):
        sequents.append(
            Sequent(
                [x for x, y in clause if not y],
                [x for x, y in clause if y]
            )
        )
    return sequents


def _dnf(term: Term) -> Term:
    match term.name:
        case "not":
            c = _cnf(term.args[0])
            return [[(x, not y) for x, y in clause] for clause in c]
        case "or":
            return _dnf(term.args[0]) + _dnf(term.args[1])
        case "and":
            d1 = _dnf(term.args[0])
            d2 = _dnf(term.args[1])
            return [x + y for x in d1 for y in d2]
        case "eq":
            return [[(Equation(term.args[0], term.args[1]), True)]]
        case "neq":
            return [[(Equation(term.args[0], term.args[1]), False)]]
        case _:
            return [[(Equation(term, Function("true", tuple())), True)]]
