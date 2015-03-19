r"""
Documentation for the game theory catalog

A catalog of named normal form games.
The docstrings give an interpretation of the situation they model.

AUTHOR:

- James Campbell and Vince Knight (06-2014)
"""
from sage.game_theory.normal_form_game import NormalFormGame
from sage.matrix.constructor import matrix
from sage.functions.generalized import sign


def PrisonersDilemma(R=-2, P=-4, S=-5, T=0):
    r"""
    Return a Prisoners dilemma game.

    Assume two thieves have been caught by the police
    and separated for questioning.
    If both thieves cooperate and do not divulge any information they will
    each get a short sentence.
    If one defects he/she is offered a deal while the other thief will get a
    long sentence.
    If they both defect they both get a medium length sentence.

    This can be modeled as a normal form game using the following two matrices
    [Webb]_:

    .. math::

        A = \begin{pmatrix}
            R&S\\
            T&P\\
            \end{pmatrix}


        B = \begin{pmatrix}
            R&T\\
            S&P\\
            \end{pmatrix}

    Where :math:`T > R > P > S`.

    - :math:`R` denotes the reward received for cooperating.
    - :math:`S` denotes the 'sucker' utility.
    - :math:`P` denotes the utility for punishing the other player.
    - :math:`T` denotes the temptation payoff.

    an often used version [Webb]_ is the following:

    .. math::

        A = \begin{pmatrix}
            -2&-5\\
            0&-4\\
            \end{pmatrix}


        B = \begin{pmatrix}
            -2&0\\
            -5&-4\\
            \end{pmatrix}

    There is a single Nash equilibria for this at which both thieves defect.
    This can be implemented in Sage using the following::

        sage: g = game_theory.PrisonersDilemma()
        sage: g
        Prisoners dilemma: Normal Form Game with the following utilities: {(0, 1): [-5, 0], (1, 0): [0, -5], (0, 0): [-2, -2], (1, 1): [-4, -4]}
        sage: g.obtain_nash()
        [[(0, 1), (0, 1)]]

    Note that we can pass other values of R, P, S, T::

        sage: g = game_theory.PrisonersDilemma(R=-1, P=-2, S=-3, T=0)
        sage: g
        Prisoners dilemma: Normal Form Game with the following utilities: {(0, 1): [-3, 0], (1, 0): [0, -3], (0, 0): [-1, -1], (1, 1): [-2, -2]}
        sage: g.obtain_nash()
        [[(0, 1), (0, 1)]]

    If we pass values that fail the defining requirement: :math:`T > R > P > S` we get an error message::

        sage: g = game_theory.PrisonersDilemma(R=-1, P=-2, S=0, T=5)
        Traceback (most recent call last):
        ...
        TypeError: The input values for a Prisoners Dilemma must be of the form T > R > P > S.

    REFERENCES:

    .. [Webb] James Webb.
       *Game theory: decisions, interaction and Evolution*
       Springer Science & Business Media
    """
    if not (T > R > P > S):
        raise TypeError("The input values for a Prisoners Dilemma must be of the form T > R > P > S.")
    A = matrix([[R, S], [T, P]])
    g = NormalFormGame([A, A.transpose()])
    g.rename('Prisoners dilemma: ' + repr(g))
    return g


def CoordinationGame(A=10, a=5, B=0, b=0, C=0, c=0, D=5, d=10):
    r"""
    Return a 2 by 2 Coordination Game

    A coordination game is a particular type of game where the pure Nash
    equilibria is for the players to pick the same strategies (or equivalent)
    strategies [Webb]_.

    In general these are represented as a normal form game using the
    following two matrices:

    .. math::

        A = \begin{pmatrix}
            A&C\\
            B&D\\
            \end{pmatrix}

        B = \begin{pmatrix}
            a&c\\
            b&d\\
            \end{pmatrix}

    Where :math:`A > B, D > C` and :math:`a > c, d > b`.

    An often used version is the following:

    .. math::

        A = \begin{pmatrix}
            10&0\\
            0&5\\
            \end{pmatrix}


        B = \begin{pmatrix}
            5&0\\
            0&10\\
            \end{pmatrix}

    This is the default version of the game created by this function::

        sage: g = game_theory.CoordinationGame()
        sage: g
        Coordination game: Normal Form Game with the following utilities: {(0, 1): [0, 0], (1, 0): [0, 0], (0, 0): [10, 5], (1, 1): [5, 10]}

    There are two pure Nash equilibria and one mixed::

        sage: g.obtain_nash()
        [[(0, 1), (0, 1)], [(2/3, 1/3), (1/3, 2/3)], [(1, 0), (1, 0)]]

    We can also pass different values of the input parameters::

        sage: g = game_theory.CoordinationGame(A=9, a=6, B=2, b=1, C=0, c=1, D=4, d=11)
        sage: g
        Coordination game: Normal Form Game with the following utilities: {(0, 1): [0, 1], (1, 0): [2, 1], (0, 0): [9, 6], (1, 1): [4, 11]}
        sage: g.obtain_nash()
        [[(0, 1), (0, 1)], [(2/3, 1/3), (4/11, 7/11)], [(1, 0), (1, 0)]]

    Note that an error is returned if the defining inequality is not obeyed :math:`A > B, D > C` and :math:`a > c, d > b`::

        sage: g = game_theory.CoordinationGame(A=9, a=6, B=0, b=1, C=2, c=10, D=4, d=11)
        Traceback (most recent call last):
        ...
        TypeError: The input values for a Coordination game must be of the form A > B, D > C, a > c and d > b.

    REFERENCES:

    .. [Webb] James Webb.
       *Game theory: decisions, interaction and Evolution*
       Springer Science & Business Media
    """
    if not (A > B  and  D > C and a > c and d > b):
        raise TypeError("The input values for a Coordination game must be of the form A > B, D > C, a > c and d > b.")
    A = matrix([[A, C], [B, D]])
    B = matrix([[a, c], [b, d]])
    g = NormalFormGame([A, B])
    g.rename('Coordination game: ' + repr(g))
    return g


def BattleOfTheSexes():
    r"""
    Return a Battle of the Sexes game

    Consider two payers: Amy and Bob.
    Amy prefers to play video games and Bob prefers to
    watch a movie. They both however want to spend their evening
    together.
    This can be modeled as a normal form game using the following two matrices
    [Webb]_:

    .. math::

        A = \begin{pmatrix}
            3&1\\
            0&2\\
            \end{pmatrix}


        B = \begin{pmatrix}
            2&1\\
            0&3\\
            \end{pmatrix}

    This is a particular type of Coordination Game.
    There are three Nash equilibria:

    1. Amy and Bob both play video games;
    2. Amy and Bob both watch a movie;
    3. Amy plays video games 75% of the time and Bob watches a movie 75% of the time.

    This can be implemented in Sage using the following::

        sage: g = game_theory.BattleOfTheSexes()
        sage: g
        Battle of the sexes - Coordination game: Normal Form Game with the following utilities: {(0, 1): [1, 1], (1, 0): [0, 0], (0, 0): [3, 2], (1, 1): [2, 3]}
        sage: g.obtain_nash()
        [[(0, 1), (0, 1)], [(3/4, 1/4), (1/4, 3/4)], [(1, 0), (1, 0)]]

    REFERENCES:

    .. [Webb] James Webb.
       *Game theory: decisions, interaction and Evolution*
       Springer Science & Business Media
    """
    g = CoordinationGame(A=3, a=2, B=0, b=0, C=1, c=1, D=2, d=3)
    g.rename('Battle of the sexes - ' + repr(g))
    return g


def StagHunt():
    r"""
    Return a Stag Hunt game.

    Assume two friends go out on a hunt. Each can individually choose to hunt
    a stag or hunt a hare. Each player must choose an action without knowing
    the choice of the other. If an individual hunts a stag, he must have the
    cooperation of his partner in order to succeed. An individual can get a
    hare by himself, but a hare is worth less than a stag.

    This can be modeled as a normal form game using the following two matrices
    [Skyrms]_:

    .. math::

        A = \begin{pmatrix}
            5&0\\
            4&2\\
            \end{pmatrix}


        B = \begin{pmatrix}
            5&4\\
            0&2\\
            \end{pmatrix}

    This is a particular type of Coordination Game.
    There are three Nash equilibria:

        1. Both friends hunting the stag.
        2. Both friends hunting the hare.
        3. Both friends hunting the stag 2/3rds of the time.

    This can be implemented in Sage using the following::

        sage: g = game_theory.StagHunt()
        sage: g
        Stag hunt - Coordination game: Normal Form Game with the following utilities: {(0, 1): [0, 4], (1, 0): [4, 0], (0, 0): [5, 5], (1, 1): [2, 2]}
        sage: g.obtain_nash()
        [[(0, 1), (0, 1)], [(2/3, 1/3), (2/3, 1/3)], [(1, 0), (1, 0)]]

    REFERENCES:

    .. [Skyrms] Brian Skyrms.
       *The stag hunt and the evolution of social structure*
       Cambridge University Press
    """
    g = CoordinationGame(A=5, a=5, B=4, b=0, C=0, c=4, D=2, d=2)
    g.rename('Stag hunt - ' + repr(g))
    return g


def AntiCoordinationGame(A=3, a=3, B=5, b=1, C=1, c=5, D=0, d=0):
    r"""
    Return a 2 by 2 AntiCoordination Game

    An anti coordination game is a particular type of game where the pure Nash
    equilibria is for the players to pick different strategies (or equivalent)
    strategies.

    In general these are represented as a normal form game using the
    following two matrices:

    .. math::

        A = \begin{pmatrix}
            A&C\\
            B&D\\
            \end{pmatrix}

        B = \begin{pmatrix}
            a&c\\
            b&d\\
            \end{pmatrix}

    Where :math:`A < B, D < C` and :math:`a < c, d > b`.

    An often used version is the following:

    .. math::

        A = \begin{pmatrix}
            3&1\\
            5&0\\
            \end{pmatrix}


        B = \begin{pmatrix}
            3&5\\
            1&0\\
            \end{pmatrix}

    This is the default version of the game created by this function::

        sage: g = game_theory.AntiCoordinationGame()
        sage: g
        Anti coordination game: Normal Form Game with the following utilities: {(0, 1): [1, 5], (1, 0): [5, 1], (0, 0): [3, 3], (1, 1): [0, 0]}

    There are two pure Nash equilibria and one mixed::

        sage: g.obtain_nash()
        [[(0, 1), (1, 0)], [(1/3, 2/3), (1/3, 2/3)], [(1, 0), (0, 1)]]

    We can also pass different values of the input parameters::

        sage: g = game_theory.AntiCoordinationGame(A=2, a=3, B=4, b=2, C=2, c=8, D=1, d=0)
        sage: g
        Anti coordination game: Normal Form Game with the following utilities: {(0, 1): [2, 8], (1, 0): [4, 2], (0, 0): [2, 3], (1, 1): [1, 0]}
        sage: g.obtain_nash()
        [[(0, 1), (1, 0)], [(2/7, 5/7), (1/3, 2/3)], [(1, 0), (0, 1)]]

    Note that an error is returned if the defining inequality is not obeyed :math:`A > B, D > C` and :math:`a > c, d > b`::

        sage: g = game_theory.AntiCoordinationGame(A=8, a=3, B=4, b=2, C=2, c=8, D=1, d=0)
        Traceback (most recent call last):
        ...
        TypeError: The input values for an Anti coordination game must be of the form A < B, D < C, a < c and d < b.
    """
    if not (A < B  and  D < C and a < c and d < b):
        raise TypeError("The input values for an Anti coordination game must be of the form A < B, D < C, a < c and d < b.")
    A = matrix([[A, C], [B, D]])
    B = matrix([[a, c], [b, d]])
    g = NormalFormGame([A, B])
    g.rename('Anti coordination game: ' + repr(g))
    return g


def HawkDove():
    r"""
    Return a Hawk Dove game

    Suppose two birds of prey must share a limited resource.
    The birds can act like a hawk or a dove.
    Hawks always fight over the resource to the point of exterminating a
    fellow hawk and/or take a majority of the resource from a dove.
    Two doves can share the resource.
    This can be modeled as a normal form game using the following two matrices
    [Cressman]_:

    .. math::

        A = \begin{pmatrix}
            0&3\\
            1&2\\
            \end{pmatrix}


        B = \begin{pmatrix}
            0&1\\
            3&2\\
            \end{pmatrix}

    This is a particular example of an anti coordination game.
    There are three Nash equilibria:

        1. One bird acts like a Hawk and the other like a Dove.
        2. Both birds are equally likely to act like a Hawk of a Dove.

    This can be implemented in Sage using the following::

        sage: g = game_theory.HawkDove()
        sage: g
        Hawk-Dove - Anti coordination game: Normal Form Game with the following utilities: {(0, 1): [3, 1], (1, 0): [1, 3], (0, 0): [0, 0], (1, 1): [2, 2]}
        sage: g.obtain_nash()
        [[(0, 1), (1, 0)], [(1/2, 1/2), (1/2, 1/2)], [(1, 0), (0, 1)]]

    REFERENCES:

    .. [Cressman] Cressman, Ross.
       *Evolutionary dynamics and extensive form games*
       MIT Press
    """
    g = AntiCoordinationGame(A=0, a=0, B=1, b=3, C=3, c=1, D=2, d=2)
    g.rename('Hawk-Dove - ' + repr(g))
    return g


def Pigs():
    r"""
    Return a Pigs game

    Consider two pigs.
    One dominant pig and one subservient pig.
    These pigs share a pen.
    There is a lever in the pen that delivers food but if either pig pushes
    the lever it will take them a little while to get to the food.
    If the dominant pig pushes the lever, the subservient pig has some time
    to eat most of the food before being pushed out of the way.
    If the subservient pig push the lever,
    the dominant pig will eat all the food.
    Finally if both pigs go to push the lever the subservient pig will be
    able to eat a third of the food.

    This can be modeled as a normal form game using the following two matrices:

    .. math::

        A = \begin{pmatrix}
            4&2\\
            6&0\\
            \end{pmatrix}


        B = \begin{pmatrix}
            2&3\\
            -1&0\\
            \end{pmatrix}

    There is a single Nash equilibrium at which the dominant pig pushes the
    lever and the subservient pig does not.

    This can be implemented in Sage using the following::

        sage: g = game_theory.Pigs()
        sage: g
        Pigs: Normal Form Game with the following utilities: {(0, 1): [2, 3], (1, 0): [6, -1], (0, 0): [4, 2], (1, 1): [0, 0]}
        sage: g.obtain_nash()
        [[(1, 0), (0, 1)]]
    """
    A = matrix([[4, 2], [6, 0]])
    B = matrix([[2, 3], [-1, 0]])
    g = NormalFormGame([A, B])
    g.rename('Pigs: ' + repr(g))
    return g


def MatchingPennies():
    r"""
    Return a Matching pennies game

    Consider two players who can choose to display a coin either Heads
    facing up or Tails facing up.
    If both players show the same face then player 1 wins,
    if not then player 2 wins.

    This can be modeled as a zero sum normal form game with the following
    matrix:

    .. math::

        A = \begin{pmatrix}
            1&-1\\
            -1&1\\
            \end{pmatrix}

    There is a single Nash equilibria at which both players randomly
    (with equal probability) pick heads or tails.

    This can be implemented in Sage using the following::

        sage: g = game_theory.MatchingPennies()
        sage: g
        Matching pennies: Normal Form Game with the following utilities: {(0, 1): [-1, 1], (1, 0): [-1, 1], (0, 0): [1, -1], (1, 1): [1, -1]}
        sage: g.obtain_nash()
        [[(1/2, 1/2), (1/2, 1/2)]]
    """
    A = matrix([[1, -1], [-1, 1]])
    g = NormalFormGame([A])
    g.rename('Matching pennies: ' + repr(g))
    return g


def RPS():
    r"""
    Return a Rock-Paper-Scissors game

    Rock-Paper-Scissors is a zero sum game usually played between two
    players where each player simultaneously forms one of three
    shapes with an outstretched hand.The game has only three possible outcomes
    other than a tie: a player who decides to play rock will beat another
    player who has chosen scissors ("rock crushes scissors") but will lose to
    one who has played paper ("paper covers rock"); a play of paper will lose
    to a play of scissors ("scissors cut paper"). If both players throw the
    same shape, the game is tied and is usually immediately replayed to break
    the tie.

    There is a single Nash equilibrium to this game, corresponding to players
    randomly choosing (with equal probability) between Rock, Paper and
    Scissors.

    This can be modeled as a zero sum normal form game with the following
    matrix:

    .. math::

        A = \begin{pmatrix}
            0 & -1 & 1\\
            1 & 0 & -1\\
            -1 & 1 & 0\\
            \end{pmatrix}

    This can be implemented in Sage using the following::

        sage: g = game_theory.RPS()
        sage: g
        Rock-Paper-Scissors: Normal Form Game with the following utilities: {(0, 1): [-1, 1], (1, 2): [-1, 1], (0, 0): [0, 0], (2, 1): [1, -1], (1, 1): [0, 0], (2, 0): [-1, 1], (2, 2): [0, 0], (1, 0): [1, -1], (0, 2): [1, -1]}
        sage: g.obtain_nash()
        [[(1/3, 1/3, 1/3), (1/3, 1/3, 1/3)]]
    """
    A = matrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    g = NormalFormGame([A])
    g.rename('Rock-Paper-Scissors: ' + repr(g))
    return g


def RPSLS():
    r"""
    Return a Rock-Paper-Scissors-Lizard-Spock game

    Rock-Paper-Scissors-Lizard-Spock an extension of Rock-Paper-Scissors.
    It is a zero sum game usually played between two
    players where each player simultaneously forms one of three
    shapes with an outstretched hand. This game became popular
    after appearing on the television show 'Big Bang Theory'.
    The rules for the game can be summarised as follows:

    - Scissors cuts Paper
    - Paper covers Rock
    - Rock crushes Lizard
    - Lizard poisons Spock
    - Spock smashes Scissors
    - Scissors decapitates Lizard
    - Lizard eats Paper
    - Paper disproves Spock
    - Spock vaporizes Rock
    - (and as it always has) Rock crushes scissors

    There is a single Nash equilibrium to this game, corresponding to players
    randomly choosing (with equal probability) between Rock, Paper, Scissors
    Lizard and Spock.

    This can be modeled as a zero sum normal form game with the following
    matrix:

    .. math::

        A = \begin{pmatrix}
            0 & -1 & 1 & 1 & -1\\
            1 & 0 & -1 & -1 & 1\\
            -1 & 1 & 0 & 1 & -1\\
            -1 & 1 & -1 & 0 & 1\\
            1 & -1 & 1 & -1 & 0\\
            \end{pmatrix}

    This can be implemented in Sage using the following::

        sage: g = game_theory.RPSLS()
        sage: g
        Rock-Paper-Scissors-Lizard-Spock: Normal Form Game with the following utilities: {(1, 3): [-1, 1], (3, 0): [-1, 1], (2, 1): [1, -1], (0, 3): [1, -1], (4, 0): [1, -1], (1, 2): [-1, 1], (3, 3): [0, 0], (4, 4): [0, 0], (2, 2): [0, 0], (4, 1): [-1, 1], (1, 1): [0, 0], (3, 2): [-1, 1], (0, 0): [0, 0], (0, 4): [-1, 1], (1, 4): [1, -1], (2, 3): [1, -1], (4, 2): [1, -1], (1, 0): [1, -1], (0, 1): [-1, 1], (3, 1): [1, -1], (2, 4): [-1, 1], (2, 0): [-1, 1], (4, 3): [-1, 1], (3, 4): [1, -1], (0, 2): [1, -1]}
        sage: g.obtain_nash()
        [[(1/5, 1/5, 1/5, 1/5, 1/5), (1/5, 1/5, 1/5, 1/5, 1/5)]]
    """
    A = matrix([[0, -1, 1, 1, -1],
                [1, 0, -1, -1, 1],
                [-1, 1, 0, 1 , -1],
                [-1, 1, -1, 0, 1],
                [1, -1, 1, -1, 0]])
    g = NormalFormGame([A])
    g.rename('Rock-Paper-Scissors-Lizard-Spock: ' + repr(g))
    return g


def Chicken():
    r"""
    Return a Chicken game.

    Consider two drivers locked in a fierce battle for pride. They drive
    towards a cliff and the winner is declared as the last one to swerve.
    If neither player swerves they will both fall off the cliff.

    This can be modeled as a normal form game using the following two matrices:

    .. math::

        A = \begin{pmatrix}
            0&-1\\
            1&-10\\
            \end{pmatrix}


        B = \begin{pmatrix}
            0&1\\
            -1&-10\\
            \end{pmatrix}

    This is a particular example of an anti coordination game.
    There are three Nash equilibria:

        1. The second player swerving
        2. The first player swerving
        3. Both players swerving with 1 out of 10 times

    This can be implemented in Sage using the following::

        sage: g = game_theory.Chicken()
        sage: g
        Chicken: Anti coordination game: Normal Form Game with the following utilities: {(0, 1): [-1, 1], (1, 0): [1, -1], (0, 0): [0, 0], (1, 1): [-10, -10]}
        sage: g.obtain_nash()
        [[(0, 1), (1, 0)], [(9/10, 1/10), (9/10, 1/10)], [(1, 0), (0, 1)]]
    """
    g = AntiCoordinationGame(A=0, a=0, B=1, b=-1, C=-1, c=1, D=-10, d=-10)
    g.rename('Chicken: ' + repr(g))
    return g

def TravellersDilemma(max_value=10):
    r"""
    Return a Travellers dilemma game.

    An airline loses two suitcases belonging to two different travelers. Both
    suitcases happen to be identical and contain identical antiques. An
    airline manager tasked to settle the claims of both travelers explains
    that the airline is liable for a maximum of 10 per suitcase, and in order
    to determine an honest appraised value of the antiques the manager
    separates both travelers so they can't confer, and asks them to write down
    the amount of their value at no less than 2 and no larger than 10. He
    also tells them that if both write down the same number, he will treat
    that number as the true dollar value of both suitcases and reimburse both
    travelers that amount.

    However, if one writes down a smaller number than the other, this smaller
    number will be taken as the true dollar value, and both travelers will
    receive that amount along with a bonus/malus: 2 extra will be paid to the
    traveler who wrote down the lower value and a 2 deduction will be taken
    from the person who wrote down the higher amount. The challenge is: what
    strategy should both travelers follow to decide the value they should
    write down?

    This can be modeled as a normal form game using the following two matrices
    [Basu]_:

    .. math::

        A = \begin{pmatrix}
            10 & 7  & 6 & 5 & 4 & 3 & 2 & 1 & 0\\
            11 & 9  & 6 & 5 & 4 & 3 & 2 & 1 & 0\\
            10 & 10 & 8 & 5 & 4 & 3 & 2 & 1 & 0\\
            9  & 9  & 9 & 7 & 4 & 3 & 2 & 1 & 0\\
            8  & 8  & 8 & 8 & 6 & 3 & 2 & 1 & 0\\
            7  & 7  & 7 & 7 & 7 & 5 & 2 & 1 & 0\\
            6  & 6  & 6 & 6 & 6 & 6 & 4 & 1 & 0\\
            5  & 5  & 5 & 5 & 5 & 5 & 5 & 3 & 0\\
            4  & 4  & 4 & 4 & 4 & 4 & 4 & 4 & 2\\
            \end{pmatrix}

        B = \begin{pmatrix}
            10 & 11 & 10 & 9 & 8 & 7 & 6 & 5 & 4\\
            7  & 9  & 10 & 9 & 8 & 7 & 6 & 5 & 4\\
            6  & 6  & 8  & 9 & 8 & 7 & 6 & 5 & 4\\
            5  & 5  & 5  & 7 & 8 & 7 & 6 & 5 & 4\\
            4  & 4  & 4  & 4 & 6 & 7 & 6 & 5 & 4\\
            3  & 3  & 3  & 3 & 3 & 5 & 6 & 5 & 4\\
            2  & 2  & 2  & 2 & 2 & 2 & 4 & 5 & 4\\
            1  & 1  & 1  & 1 & 1 & 1 & 1 & 3 & 4\\
            0  & 0  & 0  & 0 & 0 & 0 & 0 & 0 & 2\\
            \end{pmatrix}


    There is a single Nash equilibrium to this game resulting in
    both players naming the smallest possible value

    This can be implemented in Sage using the following::

        sage: g = game_theory.TravellersDilemma()
        sage: g
        Travellers dilemma: Normal Form Game with the following utilities: {(7, 3): [5, 1], (4, 7): [1, 5], (1, 3): [5, 9], (4, 8): [0, 4], (3, 0): [9, 5], (2, 8): [0, 4], (8, 0): [4, 0], (7, 8): [0, 4], (5, 4): [7, 3], (0, 7): [1, 5], (5, 6): [2, 6], (2, 6): [2, 6], (1, 6): [2, 6], (5, 1): [7, 3], (3, 7): [1, 5], (0, 3): [5, 9], (8, 5): [4, 0], (2, 5): [3, 7], (5, 8): [0, 4], (4, 0): [8, 4], (1, 2): [6, 10], (7, 4): [5, 1], (6, 4): [6, 2], (3, 3): [7, 7], (2, 0): [10, 6], (8, 1): [4, 0], (7, 6): [5, 1], (4, 4): [6, 6], (6, 3): [6, 2], (1, 5): [3, 7], (8, 8): [2, 2], (7, 2): [5, 1], (3, 6): [2, 6], (2, 2): [8, 8], (7, 7): [3, 3], (5, 7): [1, 5], (5, 3): [7, 3], (4, 1): [8, 4], (1, 1): [9, 9], (2, 7): [1, 5], (3, 2): [9, 5], (0, 0): [10, 10], (6, 6): [4, 4], (5, 0): [7, 3], (7, 1): [5, 1], (4, 5): [3, 7], (0, 4): [4, 8], (5, 5): [5, 5], (1, 4): [4, 8], (6, 0): [6, 2], (7, 5): [5, 1], (2, 3): [5, 9], (2, 1): [10, 6], (8, 7): [4, 0], (6, 8): [0, 4], (4, 2): [8, 4], (1, 0): [11, 7], (0, 8): [0, 4], (6, 5): [6, 2], (3, 5): [3, 7], (0, 1): [7, 11], (8, 3): [4, 0], (7, 0): [5, 1], (4, 6): [2, 6], (6, 7): [1, 5], (8, 6): [4, 0], (5, 2): [7, 3], (6, 1): [6, 2], (3, 1): [9, 5], (8, 2): [4, 0], (2, 4): [4, 8], (3, 8): [0, 4], (0, 6): [2, 6], (1, 8): [0, 4], (6, 2): [6, 2], (4, 3): [8, 4], (1, 7): [1, 5], (0, 5): [3, 7], (3, 4): [4, 8], (0, 2): [6, 10], (8, 4): [4, 0]}
        sage: g.obtain_nash() # optional - lrs
        [[(0, 0, 0, 0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 0, 0, 0, 1)]]

        Note that this command can be used to create travellers dilemma for a
         different maximum value of the luggage. Below is an implementation
        with a maximum value of 5::

        sage: g = game_theory.TravellersDilemma(5)
        sage: g
        Travellers dilemma: Normal Form Game with the following utilities: {(0, 1): [2, 6], (1, 2): [1, 5], (3, 2): [4, 0], (0, 0): [5, 5], (3, 3): [2, 2], (3, 0): [4, 0], (3, 1): [4, 0], (2, 1): [5, 1], (0, 2): [1, 5], (2, 0): [5, 1], (1, 3): [0, 4], (2, 3): [0, 4], (2, 2): [3, 3], (1, 0): [6, 2], (0, 3): [0, 4], (1, 1): [4, 4]}
        sage: g.obtain_nash()
        [[(0, 0, 0, 1), (0, 0, 0, 1)]]

    REFERENCES:

    .. [Basu] Kaushik Basu.
       *The Traveler's Dilemma: Paradoxes of Rationality in Game Theory*
       The American Economic Review (1994): 391-395
    """
    A = matrix([[min(i, j) + 2 * sign(j - i) for j in range(max_value, 1, -1)] for i in range(max_value, 1, -1)])
    g = NormalFormGame([A, A.transpose()])
    g.rename('Travellers dilemma: ' + repr(g))
    return g
