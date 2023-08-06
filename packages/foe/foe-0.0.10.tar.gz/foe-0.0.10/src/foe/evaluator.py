from .logic import Equation, Function, Problem, Sequent, Term, Variable
from abc import ABC
import torch


class Evaluator(ABC):
    """An abstract class for evaluating sequents."""
    def __init__(self, problem: Problem):
        self.problem = problem

    def __call__(self, sequent: Sequent):
        """Evaluates the given sequent.

        Parameters
        ----------
        sequent : Sequent
            The sequent to evaluate.

        Returns
        -------
        Any
            The evaluation of the sequent, must implement __lt__.
        """
        raise NotImplementedError


class KBO(Evaluator):
    """An evaluator based on the Knuth-Bendix Ordering."""
    def __init__(self, problem: Problem, weights: dict[str, int] = None):
        super().__init__(problem)
        if weights:
            self.weights = weights
        else:
            self.weights = {x: 1 for i, x in enumerate(problem.functions)}

    def __call__(self, x: Term | Equation | Sequent) -> float:
        """Evaluates the given term, equation or sequent.

        Parameters
        ----------
        sequent : Term | Equation | Sequent
            The term, equation or sequent to evaluate.

        Returns
        -------
        float
            The evaluation of the sequent.
        """
        if isinstance(x, Function):
            return (
                self.weights.get(x.name, 0) + sum(self(y)[0] for y in x.args),
                x.name,
                *tuple(self(y) for y in x.args)
            )
        elif isinstance(x, Variable):
            return (1, "")
        elif isinstance(x, Equation):
            return (
                self(x.left)[0] + self(x.right)[0],
                "=",
                self(x.left),
                self(x.right)
            )
        elif isinstance(x, Sequent):
            return (
                sum(self(y)[0] for y in x.left) +
                sum(self(y)[0] for y in x.right),
                "⊢",
                *tuple(self(y) for y in x.left),
                *tuple(self(y) for y in x.right)
            )
        else:
            raise TypeError(f"Cannot evaluate {x}.")


class Embedding(torch.nn.Module, Evaluator):
    """An evaluator based on a deep logic embedding."""
    def __init__(self, env: Problem, hidden_layers: dict = None):
        super(Embedding, self).__init__()
        self.env = env
        self.dimensions = {}
        self.distribtuion = {}
        for sort in env.sorts:
            self.dimensions[sort] = 1
            self.distribtuion[sort] = torch.distributions.MultivariateNormal(
                    torch.zeros(self.dimensions[sort]),
                    torch.eye(self.dimensions[sort])
                )
        for name in env.functions:
            if hidden_layers:
                self.__setattr__(
                    name,
                    Function_Embedding(
                        self.dimensions,
                        hidden_layers,
                        name,
                        env.function_sorts[name][0],
                        env.function_sorts[name][1],
                    )
                )
            else:
                self.__setattr__(
                    name,
                    Function_Embedding(
                        self.dimensions,
                        {name: [1]},
                        name,
                        env.function_sorts[name][0],
                        env.function_sorts[name][1],
                    )
                )

    def __call__(self, sequent: Sequent):
        """Evaluates the given sequent."""
        return 1 - self.eval_sequent(sequent, *[
            self.distribtuion[self.env.variablessorts[Variable(i)]].sample()
            for i in range(self.env.variablecounter)
        ])

    def eval_term(self, term: Term, *args):
        if type(term) == Variable:
            return args[term.id]
        else:
            return self.__getattr__(term.name)(
                *[self.eval_term(arg, *args) for arg in term.args]
            )

    def eval_equation(self, equation: Equation, *args):
        return torch.min(torch.stack((torch.tensor(1), torch.norm(
            self.eval_term(equation.left, *args) -
            self.eval_term(equation.right, *args)
        ))))

    def eval_sequent(self, sequent: Sequent, *args):
        if sequent.left and sequent.right:
            return torch.min(torch.stack(
                (
                    1 - torch.max(torch.stack(tuple(
                        self.eval_equation(equation, *args)
                        for equation in sequent.left
                    ))),
                    torch.min(torch.stack(tuple(
                        self.eval_equation(equation, *args)
                        for equation in sequent.right
                    )))
                )
            ))
        if sequent.left:
            return 1 - torch.max(torch.stack(tuple(
                self.eval_equation(equation, *args)
                for equation in sequent.left
            )))
        if sequent.right:
            return torch.min(torch.stack(tuple(
                self.eval_equation(equation, *args)
                for equation in sequent.right
            )))
        return torch.tensor(1)

    def forward(self):
        return torch.sum(torch.stack(tuple(
            self.eval_sequent(sequent, *[
                self.distribtuion[
                    self.env.variablessorts[Variable(i)]
                ].sample()
                for i in range(self.env.variablecounter)
            ]) for sequent in self.env.sequents
        )))

    def train(self, epochs=1000, learning_rate=0.001, parameter_coefficient=1):
        optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate)
        for i in range(epochs):
            optimizer.zero_grad()
            loss = self.forward() + parameter_coefficient * torch.max(
                torch.cat(tuple(
                    torch.abs(p.flatten())for p in self.parameters()
                ))
            )
            loss.backward()
            optimizer.step()
            if i % 100 == 0:
                print(loss)


class Function_Embedding(torch.nn.Module):
    def __init__(
        self,
        dimensions: dict,
        hidden_layers: dict,
        name: str,
        input_sorts: list,
        sort: str
    ):
        super(Function_Embedding, self).__init__()
        input_dimension = sum(dimensions[s] for s in input_sorts)
        output_dimension = dimensions[sort]
        for i, n in enumerate(hidden_layers[name] + [output_dimension]):
            self.add_module("linear_{}".format(
                i), torch.nn.Linear(input_dimension, n))
            input_dimension = n
        self.layers = len(hidden_layers[name] + [output_dimension])

    def forward(self, *args):
        if args:
            x = torch.stack(args)
        else:
            x = torch.tensor([])
        for i in range(self.layers - 1):
            x = torch.nn.functional.relu(
                self.__getattr__("linear_{}".format(i))(x))
        return self.__getattr__("linear_{}".format(self.layers - 1))(x)
