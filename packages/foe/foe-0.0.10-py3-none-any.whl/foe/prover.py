from .logic import (
    Equation,
    Function,
    Variable,
    Substitution,
    mgu,
    Problem,
    Sequent,
    Term,
    get_subterm,
    replace_subterm,
    substitute
)
from .evaluator import Evaluator
import heapq as hq


class TermInstance():
    def __init__(
        self,
        sequent_index,
        sequent_side,
        equation_index,
        equation_side,
        subterm_index,
    ):
        self.sequent_index = sequent_index
        self.sequent_side = sequent_side
        self.equation_index = equation_index
        self.equation_side = equation_side
        self.subterm_index = subterm_index

    def __repr__(self):
        return "TermInstance({}, {}, {}, {}, {})".format(
            self.sequent_index,
            self.sequent_side,
            self.equation_index,
            self.equation_side,
            self.subterm_index,
        )

    def __eq__(self, other):
        return (
            self.sequent_index == other.sequent_index
            and self.sequent_side == other.sequent_side
            and self.equation_index == other.equation_index
            and self.equation_side == other.equation_side
            and self.subterm_index == other.subterm_index
        )

    def __lt__(self, other):
        return (
            self.sequent_index,
            self.sequent_side,
            self.equation_index,
            self.equation_side,
            self.subterm_index
        ) < (
            other.sequent_index,
            other.sequent_side,
            other.equation_index,
            other.equation_side,
            other.subterm_index
        )

    def sequent(self, sequentlist: list[Sequent]) -> Sequent:
        """Converts the term instance to the corresponding sequent.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Sequent
            The sequent corresponding to the term instance.
        """
        return sequentlist[self.sequent_index]

    def equation(self, sequentlist: list[Sequent]) -> Equation:
        """Converts the sequent instance to the corresponding equation.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Equation
            The equation corresponding to the sequent instance.
        """
        if self.sequent_side == "l":
            eqs = sequentlist[self.sequent_index].left
        elif self.sequent_side == "r":
            eqs = sequentlist[self.sequent_index].right
        else:
            raise ValueError(
                "Invalid sequent side: {}. Must be\
                'l' or 'r'.".format(self.sequent_side)
            )
        return eqs[self.equation_index]

    def toplevel(self, sequentlist: list[Sequent]) -> Term:
        """Converts the term instance to the corresponding top level term.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Term
            The term corresponding to the term instance.
        """
        eq = self.equation(sequentlist)
        if self.equation_side == "l":
            return eq.left
        elif self.equation_side == "r":
            return eq.right
        else:
            raise ValueError(
                "Invalid equation side: {}. Must be\
                'l' or 'r'.".format(self.equation_side)
            )

    def term(self, sequentlist: list[Sequent]) -> Term:
        """Converts the term instance to the corresponding subterm.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.

        Returns
        -------
        Term
            The subterm corresponding to the term instance.
        """
        term = self.toplevel(sequentlist)
        return get_subterm(term, self.subterm_index)

    def replace_in_equation(
        self, equation: Equation, t: Term
    ) -> Equation:
        """Replaces the subterm corresponding to the term instance with the
        given term in the corresponding equation.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.
        t : Term
            The term to replace the subterm with.
        """
        if self.equation_side == "l":
            return Equation(
                replace_subterm(equation.left, self.subterm_index, t),
                equation.right
            )
        elif self.equation_side == "r":
            return Equation(
                equation.left,
                replace_subterm(equation.right, self.subterm_index, t)
            )
        else:
            raise ValueError(
                "Invalid equation side: {}. Must be\
                'l' or 'r'.".format(self.equation_side)
            )

    def sequent_without_equation(self, sequentlist: list[Sequent]) -> Sequent:
        """Removes the equation corresponding to the term instance from the
        corresponding sequent.

        Parameters
        ----------
        sequentlist : list[Sequent]
            The list of sequents to draw from.
        """
        seq = self.sequent(sequentlist)
        if self.sequent_side == "l":
            return Sequent(
                seq.left[: self.equation_index] +
                seq.left[self.equation_index + 1:],
                seq.right
            )
        elif self.sequent_side == "r":
            return Sequent(
                seq.left,
                seq.right[: self.equation_index] +
                seq.right[self.equation_index + 1:]
            )
        else:
            raise ValueError(
                "Invalid sequent side: {}. Must be\
                'l' or 'r'.".format(self.sequent_side)
            )


def subtermindices(term: Term) -> list[tuple[int, ...]]:
    """Returns a list of all subterm indices for the given term.

    Parameters
    ----------
    term : Term
        The term to get the subterm indices for.

    Returns
    -------
    list[Tuple]
        The list of subterm indices.
    """
    if isinstance(term, Variable):
        return [tuple()]
    elif isinstance(term, Function):
        indices = [tuple()]
        for i, arg in enumerate(term.args):
            for subindex in subtermindices(arg):
                indices.append((i,) + subindex)
        return indices
    else:
        raise ValueError(
            "Invalid term type: {}. Must be\
            Variable or Function.".format(type(term))
        )


def positive_toplevel_terminstances(
    sequentlist: list[Sequent]
) -> list[TermInstance]:
    """Converts a list of sequents to a list of top level term instances.

    Parameters
    ----------
    sequentlist : list[Sequent]
        The list of sequents to convert.

    Returns
    -------
    list[TermInstance]
        The list of top level term instances.
    """
    terminstances = []
    for i, seq in enumerate(sequentlist):
        for j, eq in enumerate(seq.right):
            for side in ["l", "r"]:
                terminstances.append(
                    TermInstance(i, "r", j, side, tuple())
                )
    return terminstances


def terminstances(sequentlist: list[Sequent]) -> list[TermInstance]:
    """Converts a list of sequents to a list of term instances.

    Parameters
    ----------
    sequentlist : list[Sequent]
        The list of sequents to convert.

    Returns
    -------
    list[TermInstance]
        The list of term instances.
    """
    terminstances = []
    for i, seq in enumerate(sequentlist):
        for j, eq in enumerate(seq.left):
            for subindex in subtermindices(eq.left):
                terminstances.append(
                    TermInstance(i, "l", j, "l", subindex)
                )
            for subindex in subtermindices(eq.right):
                terminstances.append(
                    TermInstance(i, "l", j, "r", subindex)
                )
        for j, eq in enumerate(seq.right):
            for subindex in subtermindices(eq.left):
                terminstances.append(
                    TermInstance(i, "r", j, "l", subindex)
                )
            for subindex in subtermindices(eq.right):
                terminstances.append(
                    TermInstance(i, "r", j, "r", subindex)
                )
    return terminstances


class Prover():
    def __init__(self, problem: Problem, evaluator: Evaluator):
        self.evaluator = evaluator(problem)
        self.initial_sequents = [s.normalize() for s in problem.sequents]
        self.derived_sequents = [s for s in self.initial_sequents]
        self.derived_sequents_set = set(self.derived_sequents)
        self.previous = {i: [] for i in range(len(self.derived_sequents))}
        self.evaluations = [
            (self.evaluator(s), self.derived_sequents.index(s))
            for s in self.derived_sequents
        ]
        hq.heapify(self.evaluations)
        self.superposition_instances: dict[
            Sequent,
            list[(
                TermInstance,
                TermInstance,
                dict[Substitution, Substitution]
            )]
        ] = {s: [] for s in self.derived_sequents}
        for toplevel in positive_toplevel_terminstances(self.initial_sequents):
            for index in terminstances(self.derived_sequents):
                m = mgu(
                    toplevel.toplevel(self.initial_sequents),
                    index.term(self.derived_sequents)
                )
                if m:
                    self.superposition_instances[
                        index.sequent(self.derived_sequents)
                    ].append(
                        (toplevel, index, m)
                    )
        self.proven = 0

    def _saturate(self, index):
        result = {index}
        for s in self.previous[index]:
            result.update(self._saturate(s))
        return result

    def __repr__(self) -> str:
        if self.proven:
            return "\n".join(
                f"{i}: {self.derived_sequents[i]}\t{self.previous[i]}"
                for i in self._saturate(self.proven)
            )
        else:
            return "\n".join(
                f"{i}: {s}\t{self.previous[i]}"
                for i, s in enumerate(self.derived_sequents)
            )

    def expand(self, i: int):
        """Expands the sequent at the given index.

        Parameters
        ----------
        index : int
            The index of the sequent to expand.
        """
        newsequents = set()
        for toplevel, index, m in self.superposition_instances[
            self.derived_sequents[i]
        ]:
            newsequents.add(self.superposition(toplevel, index, m))
        for sequent in newsequents:
            if sequent not in self.derived_sequents_set and (
                not sequent.is_trivial()
            ):
                self.derived_sequents.append(sequent)
                self.derived_sequents_set.add(sequent)
                self.previous[len(self.derived_sequents) - 1] = [
                    toplevel.sequent_index,
                    i
                ]
                self.superposition_instances[sequent] = []
                hq.heappush(
                    self.evaluations,
                    (self.evaluator(sequent), len(self.derived_sequents) - 1)
                )
                for toplevel in positive_toplevel_terminstances(
                    self.initial_sequents
                ):
                    for index in terminstances([sequent]):
                        index.sequent_index = len(self.derived_sequents) - 1
                        m = mgu(
                            toplevel.toplevel(self.initial_sequents),
                            index.term(self.derived_sequents)
                        )
                        if m:
                            self.superposition_instances[sequent].append(
                                (toplevel, index, m)
                            )

    def superposition(
        self,
        toplevel: TermInstance,
        index: TermInstance,
        m: tuple[Substitution, Substitution]
    ):
        """Performs superposition on the given sequents.

        Parameters
        ----------
        toplevel : TermInstance
            The top level term instance.
        index : TermInstance
            The term instance to perform superposition with.
        m : tuple[Substitution, Substitution]
            The most general unifier.

        Returns
        -------
        Sequent
            The sequent resulting from superposition.
        """
        newtoplevel = substitute(
            m[0], toplevel.sequent_without_equation(self.initial_sequents)
        )
        newindex = substitute(
            m[1], index.sequent_without_equation(self.derived_sequents)
        )
        if toplevel.sequent_side == "r":
            if index.sequent_side == "l":
                if toplevel.equation_side == "l":
                    return Sequent(
                        newtoplevel.left +
                        newindex.left + (
                            index.replace_in_equation(
                                substitute(
                                    m[1], index.equation(self.derived_sequents)
                                ),
                                substitute(
                                    m[0], toplevel.equation(
                                        self.initial_sequents
                                    ).right
                                )
                            ),
                        ),
                        newtoplevel.right +
                        newindex.right
                    ).normalize()
                elif toplevel.equation_side == "r":
                    return Sequent(
                        newtoplevel.left +
                        newindex.left + (
                            index.replace_in_equation(
                                substitute(
                                    m[1], index.equation(self.derived_sequents)
                                ),
                                substitute(
                                    m[0], toplevel.equation(
                                        self.initial_sequents
                                    ).left
                                )
                            ),
                        ),
                        newtoplevel.right +
                        newindex.right
                    ).normalize()
            elif index.sequent_side == "r":
                if toplevel.equation_side == "l":
                    return Sequent(
                        newtoplevel.left +
                        newindex.left,
                        newtoplevel.right +
                        newindex.right + (
                            index.replace_in_equation(
                                substitute(
                                    m[1], index.equation(self.derived_sequents)
                                ),
                                substitute(
                                    m[0], toplevel.equation(
                                        self.initial_sequents
                                    ).right
                                )
                            ),
                        )
                    ).normalize()
                elif toplevel.equation_side == "r":
                    return Sequent(
                        newtoplevel.left +
                        newindex.left,
                        newtoplevel.right +
                        newindex.right + (
                            index.replace_in_equation(
                                substitute(
                                    m[1], index.equation(self.derived_sequents)
                                ),
                                substitute(
                                    m[0], toplevel.equation(
                                        self.initial_sequents
                                    ).left
                                )
                            ),
                        )
                    ).normalize()
        elif toplevel.sequent_side == "l":
            raise ValueError("Superposition only supports right sequents.")

    def prove(self, maxsteps: int):
        """Attemps a saturation proof of the given problem.

        Parameters
        ----------
        maxsteps : int
            The maximum number of steps to take.

        Returns
        -------
        self.proven : int
            The index of the empty if the proof succeeds, 0 otherwise.
        """
        while maxsteps > 0:
            if self.evaluations:
                evaluation, index = hq.heappop(self.evaluations)
                if self.derived_sequents[index].is_empty():
                    self.proven = index
                    return self.proven
                self.expand(index)
            else:
                return self.proven
            maxsteps -= 1
        return self.proven
