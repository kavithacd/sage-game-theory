"""
Extensive Form Games with N players.

This module implements a class for extensive form games
[NN2007]_. Graphical representations of the games are implemented and solution
algorithms are being developed (with an interface to gambit).

A well known example that can be implemented as an extensive form game is the
battle of the sexes. Consider two players, Celine and Bob. The two are deciding
on how to spend their evening, they can either watch Sports or go and see a
Comedy. Bob would prefer to see a Comedy, Celine would prefer to watch a Sports
movie. Depending on who choses what, there are different payoffs, this can be
demonstrated in tree Form.

.. PLOT::
    :width: 500 px

    player_1 = Player('Bob')
    player_2 = Player('Celine')
    leaf_1 = Leaf({player_1: 2, player_2: 3})
    leaf_2 = Leaf({player_1: 0, player_2: 0})
    leaf_3 = Leaf({player_1: 1, player_2: 1})
    leaf_4 = Leaf({player_1: 3, player_2: 2})
    node_3 = Node({'Sports': leaf_1, 'Comedy': leaf_2}, 'c', player_2)
    node_2 = Node({'Sports': leaf_3, 'Comedy': leaf_4}, 'b', player_2)
    node_1 = Node({'Sports': node_3, 'Comedy': node_2}, 'a', player_1)
    battle_of_the_sexes = ExtensiveFormGame(node_1)
    battle_of_the_sexes.set_info_set([node_2, node_3])
    p = battle_of_the_sexes.plot(view_info_sets=True)
    sphinx_plot(p)

We can see there are three nodes, one for Bob, two for Celine. Connecting those
nodes are actions. These actions represent choices made by one player, and the
actions then lead on to a node of another player.  So Bob either chooses Sports
or Comedy, and Celine chooses Sports or Comedy. The location of the payoffs
correspond to the leaf of the underlying tree and they show the outcome for each
player.  So if Bob chooses Sports, and Celine chooses Sports, we see the payoff
is (2, 3), which represents Bob getting a payoff of 2, and Celine getting a
payoff of 3. Note that the green line between Celine's two nodes indicate that
they are in the same 'information set', in other words, Celine does not know
what Bob has picked. Thus the following game corresponds to a different
situation which is easier for both players to coordinate:

.. PLOT::
    :width: 500 px

    player_1 = Player('Bob')
    player_2 = Player('Celine')
    leaf_1 = Leaf({player_1: 2, player_2: 3})
    leaf_2 = Leaf({player_1: 0, player_2: 0})
    leaf_3 = Leaf({player_1: 1, player_2: 1})
    leaf_4 = Leaf({player_1: 3, player_2: 2})
    node_3 = Node({'Sports': leaf_1, 'Comedy': leaf_2}, 'c', player_2)
    node_2 = Node({'Sports': leaf_3, 'Comedy': leaf_4}, 'b', player_2)
    node_1 = Node({'Sports': node_3, 'Comedy': node_2}, 'a', player_1)
    battle_of_the_sexes = ExtensiveFormGame(node_1)
    p = battle_of_the_sexes.plot(view_info_sets=True)
    sphinx_plot(p)

The first game (with the information set) corresponds to the following normal
form game (which are also implemented in Sage)::

    sage: A = matrix([[3, 1], [0, 2]])
    sage: B = matrix([[2, 1], [0, 3]])
    sage: battle_of_the_sexes = NormalFormGame([A, B])
    sage: battle_of_the_sexes
    Normal Form Game with the following utilities: {(0, 1): [1, 1], (1, 0): [0, 0], (0, 0): [3, 2], (1, 1): [2, 3]}

To generate an extensive form game we need to generate the nodes and assign them
to players as well as describing the actions they have and to which node each
action goes. As such it makes sense to start with the terminal nodes of the
tree, but the initial step is to create players as each node will map players to
utilities::

    sage: player_1, player_2 = Player('Bob'), Player('Celine')
    sage: player_1, player_2
    (Bob, Celine)

Once we have done this, we are ready to create our leafs::

    sage: leaf_1 = Leaf({player_1: 2, player_2: 3})
    sage: leaf_1
    Extensive form game leaf with utilities given by: (2, 3)
    sage: leaf_2 = Leaf({player_1: 0, player_2: 0})
    sage: leaf_2
    Extensive form game leaf with utilities given by: (0, 0)
    sage: leaf_3 = Leaf({player_1: 1, player_2: 1})
    sage: leaf_3
    Extensive form game leaf with utilities given by: (1, 1)
    sage: leaf_4 = Leaf({player_1: 3, player_2: 2})
    sage: leaf_4
    Extensive form game leaf with utilities given by: (3, 2)

We can then create the parents of these leafs, the general :code:`Node` class
takes 3 arguments: a dictionary mapping actions to other nodes, a name for the
node and finally the player who makes the decision at this node::

    sage: node_1 = Node({'Sports': leaf_3, 'Comedy': leaf_4}, 'b', player_2)
    sage: node_1
    Extensive form game node with name: b
    sage: node_1.player
    Celine
    sage: node_1.name
    'b'
    sage: node_2 = Node({'Sports': leaf_1, 'Comedy': leaf_2}, 'c', player_2)
    sage: node_2
    Extensive form game node with name: c
    sage: node_2.player
    Celine
    sage: node_2.name
    'c'

Finally, we create the root of the tree::

    sage: root = Node({'Sports': node_2, 'Comedy': node_1}, 'a', player_1)
    sage: root
    Extensive form game node with name: a
    sage: root.player
    Bob
    sage: root.name
    'a'

The extensive form game can then be created by passing this root (which
recursively has all required information)::

    sage: battle_of_the_sexes = ExtensiveFormGame(root)
    sage: battle_of_the_sexes
    Extensive Form Game with the following underlying tree: {...

By default all nodes are in their own information set. If we plot the tree we
see this::

    sage: battle_of_the_sexes.plot(view_info_sets=True)
    Graphics object consisting of 23 graphics primitives

Here is the output (this is the same tree as above):

.. PLOT::
    :width: 500 px

    player_1 = Player('Bob')
    player_2 = Player('Celine')
    leaf_1 = Leaf({player_1: 2, player_2: 3})
    leaf_2 = Leaf({player_1: 0, player_2: 0})
    leaf_3 = Leaf({player_1: 1, player_2: 1})
    leaf_4 = Leaf({player_1: 3, player_2: 2})
    node_3 = Node({'Sports': leaf_1, 'Comedy': leaf_2}, 'c', player_2)
    node_2 = Node({'Sports': leaf_3, 'Comedy': leaf_4}, 'b', player_2)
    node_1 = Node({'Sports': node_3, 'Comedy': node_2}, 'a', player_1)
    battle_of_the_sexes = ExtensiveFormGame(node_1)
    p = battle_of_the_sexes.plot(view_info_sets=True)
    sphinx_plot(p)

An extensive form game where all nodes are in their own information set is said
to have 'perfect information'. The game we have so far still has perfect
information::

    sage: battle_of_the_sexes.info_sets
    [[Extensive form game node with name: a],
     [Extensive form game node with name: b],
     [Extensive form game node with name: c]]
    sage: battle_of_the_sexes.perfect_info()
    True

To set the information sets as described above we use the :code:`set_info_set`
method::

    sage: battle_of_the_sexes.set_info_set([node_1, node_2])
    sage: battle_of_the_sexes.info_sets
    [[Extensive form game node with name: a],
     [Extensive form game node with name: b,
      Extensive form game node with name: c]]

Now the game does not have perfect information::

    sage: battle_of_the_sexes.perfect_info()
    False

Information sets are demonstrated visually on the graph we plot by setting
``view_info_sets`` to be ``True`` while plotting::

    sage: battle_of_the_sexes.plot(view_info_sets=True)
    Graphics object consisting of 22 graphics primitives

Which will be plotted as follows:

.. PLOT::
    :width: 500 px

    player_1 = Player('Bob')
    player_2 = Player('Celine')
    leaf_1 = Leaf({player_1: 2, player_2: 3})
    leaf_2 = Leaf({player_1: 0, player_2: 0})
    leaf_3 = Leaf({player_1: 1, player_2: 1})
    leaf_4 = Leaf({player_1: 3, player_2: 2})
    node_3 = Node({'Sports': leaf_1, 'Comedy': leaf_2}, 'c', player_1)
    node_2 = Node({'Sports': leaf_3, 'Comedy': leaf_4}, 'b', player_1)
    node_1 = Node({'Sports': node_3, 'Comedy': node_2}, 'a', player_2)
    battle_of_the_sexes = ExtensiveFormGame(node_1)
    battle_of_the_sexes.set_info_set([node_2, node_3])
    p = battle_of_the_sexes.plot(view_info_sets = True)
    sphinx_plot(p)

We can remove information sets which automatically sets all the nodes in that
information set to be in their own information set::

    sage: battle_of_the_sexes.remove_info_set([node_1, node_2])
    sage: battle_of_the_sexes.info_sets
    [[Extensive form game node with name: a],
     [Extensive form game node with name: b],
     [Extensive form game node with name: c]]

Here is an example of a larger game: a 3 player rock paper scissors variant
where all players play at the same time.

Here is a function to compute the utilities of a particular strategy profile::

    sage: def strategy_to_utility(P1, P2, P3):
    ....:     what_beats = {'R': 'P', 'P': 'S', 'S': 'R'}
    ....:     what_loses = {'R': 'S', 'P': 'R', 'S': 'P'}
    ....:     p1_score = [P2, P3].count(what_loses[P1])- [P2, P3].count(what_beats[P1])
    ....:     p2_score = [P1, P3].count(what_loses[P2])- [P1, P3].count(what_beats[P2])
    ....:     p3_score = [P2, P1].count(what_loses[P3])- [P2, P1].count(what_beats[P3])
    ....:     return p1_score, p2_score, p3_score

Here we get all possible strategy profiles at each level of the tree::

    sage: import itertools
    sage: all_possible_profiles = list(itertools.product(['R','P','S'], repeat=3))
    sage: all_second_level_profiles = list(itertools.product(['R','P','S'], repeat=2))
    sage: all_first_level_profiles = [('R',), ('P',), ('S',)]

Creating our players::

    sage: p1 = Player('P1')
    sage: p2 = Player('P2')
    sage: p3 = Player('P3')

Putting nodes in a dictionary by level so as to recursively build up the tree::

    sage: third_level_dictionary = {profile:Leaf({p1:strategy_to_utility(*profile)[0], p2:strategy_to_utility(*profile)[1], p3:strategy_to_utility(*profile)[2]}) for profile in all_possible_profiles}
    sage: second_level_dictionary = {profile:Node({'R':third_level_dictionary[profile+('R',)], 'P':third_level_dictionary[profile+('P',)], 'S':third_level_dictionary[profile+('S',)]},player=p3) for profile in all_second_level_profiles}
    sage: first_level_dictionary = {profile:Node({'R':second_level_dictionary[profile+('R',)], 'P':second_level_dictionary[profile+('P',)], 'S':second_level_dictionary[profile+('S',)]},player=p2) for profile in all_first_level_profiles}

Building the node of the tree::

    sage: root = Node({'P':first_level_dictionary[('P',)], 'R':first_level_dictionary[('R',)], 'S':first_level_dictionary[('S',)]}, player=p1)

Building the tree::

    sage: g = ExtensiveFormGame(root)

Setting the information sets::

    sage: info_set_for_p3 = second_level_dictionary.values()
    sage: info_set_for_p2 = first_level_dictionary.values()
    sage: g.set_info_set(info_set_for_p2)
    sage: g.set_info_set(info_set_for_p3)

    sage: p = g.plot()
    sage: p
    Graphics object consisting of 122 graphics primitives

If you would like to see this tree run the follow but beware it's a large
plot!::

    sage: p.show(figsize=[20, 50])  # modifies the size of the plot

"""
from sage.graphs.all import Graph
from sage.plot.line import line2d
from sage.graphs.generic_graph import GenericGraph
from operator import attrgetter
from copy import copy
from parser import Parser


try:
    from gambit import Game
except ImportError:
    Game = None

class ExtensiveFormGame():
    r"""
    An object representing an Extensive Form Game. Primarily used to compute the
    Nash Equilibria.

    INPUT:

    - ``generator`` - Can be an instance of the Node class which serves as the
      root of the tree.
    """
    def __init__(self, generator, name=False):
        r"""
        Initializes an Extensive Form game and checks the inputs.

        EXAMPLES:

        A game with 2 players and 8 nodes::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1})
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a7 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a8 = Leaf({player_a1 : 2, player_a2: 1})
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, player = player_a1)
            sage: node_a3 = Node({'A': leaf_a5, 'B': leaf_a6}, player = player_a1)
            sage: node_a4 = Node({'A': leaf_a7, 'B': leaf_a8}, player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, player = player_a2)
            sage: node_a6 = Node({'C': node_a3, 'D': node_a4}, player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: egame_a1.tree
            Graph on 15 vertices

        The generated tree has a variety of attributes::

            sage: egame_a1.players
            [Player 1, Player 2]
            sage: egame_a1.nodes
            [Extensive form game node with name: Node 1,
             Extensive form game node with name: Node 2,
             Extensive form game node with name: Node 3,
             Extensive form game node with name: Node 4,
             Extensive form game node with name: Node 5,
             Extensive form game node with name: Node 6,
             Extensive form game node with name: Tree Root]
            sage: egame_a1.info_sets
            [[Extensive form game node with name: Node 1],
             [Extensive form game node with name: Node 2],
             [Extensive form game node with name: Node 3],
             [Extensive form game node with name: Node 4],
             [Extensive form game node with name: Node 5],
             [Extensive form game node with name: Node 6],
             [Extensive form game node with name: Tree Root]]

        It is possible to have games with more than two players::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: player_3 = Player('Player 3')
            sage: leaf_1 = Leaf({player_1 : 0, player_2: 1, player_3: -5}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1 : 1, player_2: 0, player_3: -4}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1 : 2, player_2: 4, player_3: -3}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1 : 2, player_2: 1, player_3: -2}, 'Leaf 4')
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_3)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.players
            [Player 1, Player 2, Player 3]
            sage: egame_1.nodes
            [Extensive form game node with name: Node 1,
             Extensive form game node with name: Node 2,
             Extensive form game node with name: Root 1]
            sage: egame_1.leafs
            [Extensive form game leaf with utilities given by: (0, 1, -5),
             Extensive form game leaf with utilities given by: (1, 0, -4),
             Extensive form game leaf with utilities given by: (2, 4, -3),
             Extensive form game leaf with utilities given by: (2, 1, -2)]
            sage: egame_1.tree
            Graph on 7 vertices

        If we do not name our nodes, unique names are
        automatically set during the initialisation::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_a = Leaf({player_1 : 0, player_2: 1})
            sage: leaf_b = Leaf({player_1 : 1, player_2: 0})
            sage: leaf_c = Leaf({player_1 : 2, player_2: 4})
            sage: leaf_d = Leaf({player_1 : 2, player_2: 1})
            sage: node_a = Node({'A': leaf_a, 'B': leaf_b}, player = player_2)
            sage: node_b = Node({'A': leaf_c, 'B': leaf_d}, player = player_2)
            sage: root_a = Node({'C': node_a, 'D': node_b}, player = player_1)
            sage: node_a.name is node_b.name is root_a.name
            True
            sage: egame_a = ExtensiveFormGame(root_a)
            sage: node_a.name is node_b.name is root_a.name
            False
            sage: sorted([node_a.name, node_b.name])
            ['Node 1', 'Node 2']
            sage: root_a.name
            'Tree Root'

        If the input is a root, it needs children, actions and players::

            sage: false_root = Node({'C': node_1, 'D': node_2}, 'False Root')
            sage: egame_2 = ExtensiveFormGame(false_root)
            Traceback (most recent call last):
            ...
            AttributeError: Root node has no player.

            sage: false_root = Node(['Action1', 'Action2'])
            sage: false_root.player = player_1
            sage: egame_2 = ExtensiveFormGame(false_root)
            Traceback (most recent call last):
            ...
            AttributeError: Root node has no children.

            sage: false_root = Node([])
            sage: egame_2 = ExtensiveFormGame(false_root)
            Traceback (most recent call last):
            ...
            AttributeError: Root node has no actions.


        If we try to put an object that isn't a graph or a node in the game,
        we'll also return an error::

            sage: egame_2 = ExtensiveFormGame(player_1)
            Traceback (most recent call last):
            ...
            TypeError: Extensive form game must be passed an input in the form of a Node or a Graph object.

            sage: egame_2 = ExtensiveFormGame([node_1, node_2])
            Traceback (most recent call last):
            ...
            TypeError: Extensive form game must be passed an input in the form of a Node or a Graph object.

            sage: egame_2 = ExtensiveFormGame(leaf_1)
            Traceback (most recent call last):
            ...
            TypeError: Extensive form game must be passed an input in the form of a Node or a Graph object.


        Similarly, we cannot create a tree with a Node with a player attribute
        which isn't an instance of the ``Player`` class::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1 : 0, player_2: 1}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1 : 1, player_2: 0}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1 : 2, player_2: 4}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1 : 2, player_2: 1}, 'Leaf 4')
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', leaf_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            Traceback (most recent call last):
            ...
            TypeError: Cannot assign a non Player as a player to a Node.

        """
        self.nodes = []

        if isinstance(generator, Node):
            if generator.actions is False:
                raise AttributeError("Root node has no actions.")
            elif generator.children is False:
                raise AttributeError("Root node has no children.")
            elif generator.player is False:
                raise AttributeError("Root node has no player.")
            else:
                self.tree_root = generator
                self.tree, self.tree_dictionary, self.nodes = self._grow_tree()
                self.players = []
                self.info_sets = [[node] for node in self.nodes]
                self.leafs = []

                self._check_node_names_and_find_players(generator)

                self.players.sort(key=attrgetter('name'))
                self.nodes.sort(key=attrgetter('name', 'parent'))
                self.leafs.sort(key=attrgetter('name', 'payoffs'))
                self.info_sets.sort(key=lambda x: x[0].name)
                self._gambit_branches_store = {}
                self._gambit_iset_store = {}
                self._generation_nodes = []
                self._generation_nodes_2 = []

        else:
            raise TypeError("Extensive form game must be passed an input in the form of a Node or a Graph object.")

        
    def set_info_set(self, node_list):
        r"""
        Combines a list of nodes in to an information set.

        EXAMPLES::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1],
             [Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]
            sage: egame_1.set_info_set([node_1, node_2])
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1,
              Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]

        Once we've set an information set, we can see it visually on the graph::

            sage: egame_1.plot()
            Graphics object consisting of 22 graphics primitives

        On some occasions we might want to plot the tree without showing the
        information sets::

            sage: egame_1.plot(view_info_sets = False)
            Graphics object consisting of 20 graphics primitives

        If by setting an information set we leave a node without an information
        set it is automatically put in a set by itself::

            sage: egame_1.set_info_set([node_1])
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1],
             [Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]

        If two nodes don't have the same actions, an error is returned::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, player = player_2)
            sage: node_2 = Node({'DifferentA': leaf_3, 'B': leaf_4}, player = player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, player = player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.set_info_set([node_1, node_2])
            Traceback (most recent call last):
            ...
            AttributeError: All nodes in the same information set must have the same actions.

        If two nodes have different players, an error is returned::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, player = player_1)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, player = player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, player = player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.set_info_set([node_1, node_2])
            Traceback (most recent call last):
            ...
            AttributeError: All nodes in the same information set must have the same players.
        """
        if len(set([node.player for node in node_list])) != 1:
            raise AttributeError("All nodes in the same information set must have the same players.")
        if len(set([tuple(sorted(node.actions)) for node in node_list])) != 1:
            raise AttributeError("All nodes in the same information set must have the same actions.")

        for node_to_be_set in node_list:
            for info_set in [info_set for info_set in self.info_sets
                             if node_to_be_set in info_set]:
                self.info_sets.remove(info_set)
        self.info_sets.append(sorted(node_list, key=lambda x: x.name))

        for node in self.nodes:
            if not any(node in info_set for info_set in self.info_sets):
                self.info_sets.append([node])

        self.info_sets.sort(key=lambda x: x[0].name)

    def remove_info_set(self, node_list):
        r"""
        Removes an information set and sets all nodes in that information set to
        be in their own information set.

        EXAMPLES::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1 : 0, player_2: 1}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1 : 1, player_2: 0}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1 : 2, player_2: 4}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1 : 2, player_2: 1}, 'Leaf 4')
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.set_info_set([node_1, node_2])
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1,
              Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]
            sage: egame_1.perfect_info()
            False
            sage: egame_1.remove_info_set([node_1, node_2])
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1],
             [Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]
            sage: egame_1.perfect_info()
            True
        """
        self.info_sets.remove(node_list)
        for node_to_be_readded in node_list:
            self.info_sets.append([node_to_be_readded])
        self.info_sets.sort(key=lambda x: x[0].name)

    def perfect_info(self):
        r"""
        Returns True or False, depending on whether or not a game has perfect
        information. A game has perfect information if all nodes are contained
        in information sets with no other nodes.

        All games start of with perfect information, adding information sets
        changes this::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1 : 0, player_2: 1}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1 : 1, player_2: 0}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1 : 2, player_2: 4}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1 : 2, player_2: 1}, 'Leaf 4')
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.perfect_info()
            True
            sage: egame_1.set_info_set([node_1, node_2])
            sage: egame_1.perfect_info()
            False
            sage: egame_1.remove_info_set([node_1, node_2])
            sage: egame_1.perfect_info()
            True
        """
        perfect_info_set = sorted([[node] for node in self.nodes],
                                  key=lambda x: x[0].name)
        return self.info_sets == perfect_info_set

    def plot(self, view_info_sets=True):
        """
        Returns a visual representation of the game::
            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: egame_1.plot()
            Graphics object consisting of 23 graphics primitives

        The plot has the option for whether or not info-sets are visible::

            sage: egame_1.plot(view_info_sets = False)
            Graphics object consisting of 20 graphics primitives
        """

        t = copy(self.tree)
        for node in self.nodes:
            actions = node.node_input.keys()
            for action in actions:
                t.set_edge_label(node, node.node_input[action], str(node.player) + ': ' + action)

        leaf_labels = {leaf: leaf.name + ' - ' + str(leaf.utilities) for leaf in self.leafs}
        # Adding padding so that leaf labels are to the right of the nodes
        leaf_labels = {leaf: (2 * len(leaf_labels[leaf])) * ' ' + leaf_labels[leaf] for leaf in self.leafs}
        t.relabel(leaf_labels)

        node_labels = {node: node.name for node in self.nodes}
        t.relabel(node_labels)

        coloring = [[node.name for node in self.nodes if node.player == player]
                    for player in self.players]
        coloring += [[leaf for leaf in leaf_labels.values()]]


        tree_plot = t.plot(layout='tree', tree_orientation='right',
                           edge_labels=True, tree_root=self.tree_root.name,
                           save_pos=True, axes=False, partition=coloring)

        positions = t.get_pos()
        if view_info_sets is True:
            for info_set in self.info_sets:
                points = sorted([positions[node.name] for node in info_set])
                tree_plot += (line2d(points, linestyle="dashed",
                              color='green'))
        return tree_plot

    def plot_infosets(self):
        """
        """
        t = self._grow_infoset_graph
        infoset_plot = t.plot(axes=False)
        return infoset_plot

    def _grow_tree(self):
        r"""
        A private method to grow a tree from a given root, returns the tree
        object and a sorted list of all nodes.

        TESTS::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: g, d, nodes = egame_1._grow_tree()
            sage: g
            Graph on 7 vertices
            sage: d == {node_2: [leaf_3, leaf_4], node_1: [leaf_1, leaf_2],
            ....:       root_1: [node_1, node_2]}
            True
            sage: nodes
            [Extensive form game node with name: Node 1,
             Extensive form game node with name: Node 2,
             Extensive form game node with name: Root 1]

        If the relationship between the nodes does not correspond to a tree, an
        error is returned. As this method is called in the initialisation
        method, the following test is a functional test and not a true unit
        test::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': node_1}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            Traceback (most recent call last):
            ...
            TypeError: Relationship between nodes does not correspond to a tree.
        """
        d, nodes = self._grow_tree_dictionary()
        t = Graph(d)
        if t.is_tree():
            return t, d, nodes
        else:
            raise TypeError("Relationship between nodes does not correspond to a tree.")

    def _grow_tree_dictionary(self):
        r"""
        Returns a dictionary defining the underlying tree as well as a sorted
        list of nodes.

        TESTS::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: d, nodes = egame_1._grow_tree_dictionary()
            sage: nodes
            [Extensive form game node with name: Node 1,
             Extensive form game node with name: Node 2,
             Extensive form game node with name: Root 1]
            sage: t = Graph(d)
            sage: t
            Graph on 7 vertices

        If a node if not complete then an error is returned::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2')
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            Traceback (most recent call last):
            ...
            AttributeError: One or more of the Nodes in the tree are not
            complete.
        """
        to_check = [self.tree_root]
        checked = []
        while to_check:
            checking = to_check.pop()
            for child in checking.children:
                if not isinstance(child, Leaf):
                    if child._is_complete():
                        child._player_check()
                        to_check.append(child)
                    else:
                        raise AttributeError("One or more of the Nodes in the tree are not complete.")
                checked.append(child)

        d = {node:node.children for node in checked if not isinstance(node, Leaf)}
        d[self.tree_root] = self.tree_root.children
        return d, sorted(d.keys(), key=attrgetter('name'))

    def _grow_infoset_graph_dictionary(self):
        """
        A function that creates a dictionary needed to plot a tree made from the game's information sets.

        TESTS::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1})
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a7 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a8 = Leaf({player_a1 : 2, player_a2: 1})
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, 'Node 1', player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, 'Node 2', player = player_a1)
            sage: node_a3 = Node({'A': leaf_a5, 'B': leaf_a6}, 'Node 3', player = player_a1)
            sage: node_a4 = Node({'A': leaf_a7, 'B': leaf_a8}, 'Node 4', player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, 'Node 5', player = player_a2)
            sage: node_a6 = Node({'C': node_a3, 'D': node_a4}, 'Node 6', player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, 'Tree Root', player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: d = egame_a1._grow_infoset_graph_dictionary()
            sage: expected_outcome = {tuple([root_a]): [tuple([node_a5]), tuple([node_a6])],
            ....: tuple([node_a5]): [tuple([node_a1]), tuple([node_a2])],
            ....: tuple([node_a6]): [tuple([node_a3]), tuple([node_a4])]}
            sage: d == expected_outcome
            True 

        If we change any information sets, the dictionary changes accordingly::

            sage: egame_a1.set_info_set([node_a5, node_a6])
            sage: d = egame_a1._grow_infoset_graph_dictionary()
            sage: expected_outcome = {tuple([node_a5, node_a6]): [tuple([node_a1]), tuple([node_a2]),
            ....: tuple([node_a3]), tuple([node_a4])],
            ....: tuple([root_a]): [tuple([node_a5, node_a6])]}
            sage: d == expected_outcome
            True

            sage: egame_a1.set_info_set([node_a3, node_a4])
            sage: egame_a1.set_info_set([node_a1, node_a2])   
            sage: d = egame_a1._grow_infoset_graph_dictionary()
            sage: expected_outcome = {tuple([root_a]): [tuple([node_a5, node_a6])],
            ....: tuple([node_a5, node_a6]): [tuple([node_a1, node_a2]), tuple([node_a3, node_a4])]}
            sage: d == expected_outcome
            True

            sage: egame_a1.set_info_set([node_a3, node_a4, node_a1, node_a2])
            sage: d = egame_a1._grow_infoset_graph_dictionary()
            sage: expected_outcome =  {tuple([root_a]): [tuple([node_a5, node_a6])],
            ....: tuple([node_a5, node_a6]): [tuple([node_a1, node_a2, node_a3, node_a4])]}
            sage: d == expected_outcome
            True

            sage: egame_a1.remove_info_set([node_a5, node_a6])
            sage: d = egame_a1._grow_infoset_graph_dictionary()
            sage: expected_outcome =  {tuple([root_a]): [tuple([node_a5]), tuple([node_a6])],
            ....: tuple([node_a5]): [tuple([node_a1, node_a2, node_a3, node_a4])],
            ....: tuple([node_a6]): [tuple([node_a1, node_a2, node_a3, node_a4])]}
            sage: d == expected_outcome
            True

        """
        d = {} 
        for info_set_1 in self.info_sets: 
            info_sets = [] 
            for info_set_2 in self.info_sets: 
                if info_set_2 != info_set_1: 
                    if any(kid in info_set_2 for nd in info_set_1 for kid in nd.children): 
                        info_sets.append(tuple(info_set_2)) 
                        d[tuple(info_set_1)] = info_sets 
        return d

    def _grow_infoset_graph(self):
        """
        TESTS::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1})
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1})
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0})
            sage: leaf_a7 = Leaf({player_a1 : 2, player_a2: 4})
            sage: leaf_a8 = Leaf({player_a1 : 2, player_a2: 1})
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, 'Node 1', player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, 'Node 2', player = player_a1)
            sage: node_a3 = Node({'A': leaf_a5, 'B': leaf_a6}, 'Node 3', player = player_a1)
            sage: node_a4 = Node({'A': leaf_a7, 'B': leaf_a8}, 'Node 4', player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, 'Node 5', player = player_a2)
            sage: node_a6 = Node({'C': node_a3, 'D': node_a4}, 'Node 6', player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, 'Tree Root', player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: egame_a1._grow_infoset_graph()
            Graph on 7 vertices

        If we change any information sets, the tree changes accordingly::

            sage: egame_a1.set_info_set([node_a5, node_a6])
            sage: egame_a1._grow_infoset_graph()
            Graph on 6 vertices

            sage: egame_a1.set_info_set([node_a3, node_a4])
            sage: egame_a1.set_info_set([node_a1, node_a2])   
            sage: egame_a1._grow_infoset_graph()
            Graph on 4 vertices

            sage: egame_a1.set_info_set([node_a3, node_a4, node_a1, node_a2])
            sage: egame_a1._grow_infoset_graph()
            Graph on 3 vertices 

            sage: egame_a1.remove_info_set([node_a5, node_a6])
            sage: egame_a1._grow_infoset_graph()
            Graph on 4 vertices
        """
        d = self._grow_infoset_graph_dictionary()
        t = Graph(d)
        return t
    


    def _check_node_names_and_find_players(self, generator):
        r"""
        A method to check the names of the nodes and gives names for the ones
        that do not have names. This also finds all the players.

        This method is embedded in the init method but has been written here to
        improve the readability of the code. The tests for this are functional
        tests.

        TESTS::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_a = Leaf({player_1 : 0, player_2: 1})
            sage: leaf_b = Leaf({player_1 : 1, player_2: 0})
            sage: leaf_c = Leaf({player_1 : 2, player_2: 4})
            sage: leaf_d = Leaf({player_1 : 2, player_2: 1})
            sage: node_a = Node({'A': leaf_a, 'B': leaf_b}, player = player_2)
            sage: node_b = Node({'A': leaf_c, 'B': leaf_d}, player = player_2)
            sage: root_a = Node({'C': node_a, 'D': node_b}, player = player_1)
            sage: node_a.name is node_b.name is root_a.name
            True
            sage: egame_a = ExtensiveFormGame(root_a)
            sage: node_a.name is node_b.name is root_a.name
            False
            sage: sorted([node_a.name, node_b.name])
            ['Node 1', 'Node 2']
            sage: root_a.name
            'Tree Root'
            sage: sorted(egame_a.players, key=lambda x: x.name)
            [Player 1, Player 2]

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_a = Leaf({player_1 : 0, player_2: 1})
            sage: leaf_b = Leaf({player_1 : 1, player_2: 0})
            sage: leaf_c = Leaf({player_1 : 2, player_2: 4})
            sage: leaf_d = Leaf({player_1 : 2, player_2: 1})
            sage: node_a = Node({'A': leaf_a, 'B': leaf_b}, player = player_2)
            sage: node_b = Node({'A': leaf_c, 'B': leaf_d}, 'Node B', player = player_2)
            sage: root_a = Node({'C': node_a, 'D': node_b}, player = player_1)
            sage: node_a.name is root_a.name
            True
            sage: node_b.name
            'Node B'
            sage: egame_a = ExtensiveFormGame(root_a)
            sage: node_a.name is node_b.name is root_a.name
            False
            sage: sorted([node_a.name, node_b.name])
            ['Node 1', 'Node B']
            sage: root_a.name
            'Tree Root'
        """
        node_index = 1
        leaf_index = 1
        self.nodes.sort(key=attrgetter('parent', 'actions'))
        for node in self.nodes:
            if node.player not in self.players:
                self.players.append(node.player)
            if node is generator and node.name is False:
                node.name = "Tree Root"
            if node.name is False:
                node.name = "Node %i" % node_index
                node_index += 1
            for child in node.children:
                if isinstance(child, Leaf) and child.name is False:
                    child.name = "Leaf %i" % leaf_index
                    leaf_index += 1
                    self.leafs.append(child)
                elif isinstance(child, Leaf):
                    self.leafs.append(child)

    def __repr__(self):
        return "Extensive Form Game with the following underlying tree: " + str(self.tree_dictionary)

    def gambit_convert(self):
        r"""
        In order to convert a sage ``ExtensiveFormGame`` into a Gambit ``Game``, we have to set up the sage game as normal, 
        setting up information sets we want, before using ``gambit_convert``::

            sage: from gambit import Game  # optional - gambit
            sage: player_1 = Player('Player 1') 
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_2 = Leaf({player_1: 1, player_2: 0})
            sage: leaf_3 = Leaf({player_1: 2, player_2: 4})
            sage: leaf_4 = Leaf({player_1: 2, player_2: 1})
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_2)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2) 
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)  
            sage: egame_1 = ExtensiveFormGame(root_1) 
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1],
             [Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]
            sage: egame_1.set_info_set([node_1, node_2])
            sage: egame_1.info_sets
            [[Extensive form game node with name: Node 1,
              Extensive form game node with name: Node 2],
             [Extensive form game node with name: Root 1]]
            sage: gambit_egame_1 = egame_1.gambit_convert()  # optional - gambit

        Information can be called from the gambit game using the gambit functions::

            sage: gambit_egame_1.players  # optional - gambit
            [<Player [0] 'Player 1' in game ''>, <Player [1] 'Player 2' in game ''>]
            sage: gambit_egame_1.infosets  # optional - gambit
            [<Infoset [0] '(Extensive form game node with name: Root 1)' for player 'Player 1' in game ''>, 
            <Infoset [0] '(Extensive form game node with name: Node 1, 
            Extensive form game node with name: Node 2)' for player 'Player 2' in game ''>] 
            sage: gambit_egame_1.root  # optional - gambit
            <Node [1] 'Root 1' in game ''>
            sage: gambit_egame_1.outcomes  # optional - gambit
            [<Outcome [0] 'Leaf 1' in game ''>, <Outcome [1] 'Leaf 2' in game ''>, 
            <Outcome [2] 'Leaf 3' in game ''>, <Outcome [3] 'Leaf 4' in game ''>]

        We can also call Gambit's .efg format of the game by simply calling the game::

            sage: gambit_egame_1  # optional - gambit
            EFG 2 R "" { "Player 1" "Player 2" }
            ""
            <BLANKLINE>
            p "Root 1" 1 1 "(Extensive form game node with name: Root 1)" { "C" "D" } 0
            p "Node 1" 2 1 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2)" { "A" "B" } 0
            t "" 1 "Leaf 1" { 0, 1 }
            t "" 2 "Leaf 2" { 1, 0 }
            p "Node 2" 2 1 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2)" { "A" "B" } 0
            t "" 3 "Leaf 3" { 2, 4 }
            t "" 4 "Leaf 4" { 2, 1 }
            <BLANKLINE>


        The following is a test to show that this works for larger trees too::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 1')
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 2')
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4}, 'Leaf 3')
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1}, 'Leaf 4')
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 5')
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 6')
            sage: leaf_a7 = Leaf({player_a1 : 2, player_a2: 4}, 'Leaf 7')
            sage: leaf_a8 = Leaf({player_a1 : 2, player_a2: 1}, 'Leaf 8')
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, "Node 1", player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, "Node 2", player = player_a1)
            sage: node_a3 = Node({'A': leaf_a5, 'B': leaf_a6}, "Node 3", player = player_a1)
            sage: node_a4 = Node({'A': leaf_a7, 'B': leaf_a8}, "Node 4", player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, "Node 5", player = player_a2)
            sage: node_a6 = Node({'C': node_a3, 'D': node_a4}, "Node 6", player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: egame_a1.set_info_set([node_a5, node_a6])
            sage: egame_a1.set_info_set([node_a1, node_a2, node_a3, node_a4])
            sage: gambit_egame_a1 = egame_a1.gambit_convert()  # optional - gambit
            sage: gambit_egame_a1.players  # optional - gambit
            [<Player [0] 'Player 1' in game ''>, <Player [1] 'Player 2' in game ''>]
            sage: gambit_egame_a1.infosets  # optional - gambit
            [<Infoset [0] '(Extensive form game node with name: Tree Root)' for player 'Player 1' in game ''>, 
            <Infoset [1] '(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2, 
            Extensive form game node with name: Node 3, Extensive form game node with name: Node 4)' for player 'Player 1' in game ''>, 
            <Infoset [0] '(Extensive form game node with name: Node 5, Extensive form game node with name: Node 6)' 
            for player 'Player 2' in game ''>]
            sage: gambit_egame_a1.root  # optional - gambit
            <Node [1] 'Tree Root' in game ''>
            sage: gambit_egame_a1.outcomes  # optional - gambit
            [<Outcome [0] 'Leaf 1' in game ''>, <Outcome [1] 'Leaf 2' in game ''>, <Outcome [2] 'Leaf 3' in game ''>, 
            <Outcome [3] 'Leaf 4' in game ''>, <Outcome [4] 'Leaf 5' in game ''>, <Outcome [5] 'Leaf 6' in game ''>, 
            <Outcome [6] 'Leaf 7' in game ''>, <Outcome [7] 'Leaf 8' in game ''>]
            sage: gambit_egame_a1  # optional - gambit
            EFG 2 R "" { "Player 1" "Player 2" }
            ""
            <BLANKLINE>
            p "Tree Root" 1 1 "(Extensive form game node with name: Tree Root)" { "A" "B" } 0
            p "Node 5" 2 1 "(Extensive form game node with name: Node 5, Extensive form game node with name: Node 6)" { "C" "D" } 0
            p "Node 1" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2, 
            Extensive form game node with name: Node 3, Extensive form game node with name: Node 4)" { "A" "B" } 0
            t "" 1 "Leaf 1" { 0, 1 }
            t "" 2 "Leaf 2" { 1, 0 }
            p "Node 2" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2, 
            Extensive form game node with name: Node 3, Extensive form game node with name: Node 4)" { "A" "B" } 0
            t "" 3 "Leaf 3" { 2, 4 }
            t "" 4 "Leaf 4" { 2, 1 }
            p "Node 6" 2 1 "(Extensive form game node with name: Node 5, Extensive form game node with name: Node 6)" { "C" "D" } 0
            p "Node 3" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2, 
            Extensive form game node with name: Node 3, Extensive form game node with name: Node 4)" { "A" "B" } 0
            t "" 5 "Leaf 5" { 0, 1 }
            t "" 6 "Leaf 6" { 1, 0 }
            p "Node 4" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2, 
            Extensive form game node with name: Node 3, Extensive form game node with name: Node 4)" { "A" "B" } 0
            t "" 7 "Leaf 7" { 2, 4 }
            t "" 8 "Leaf 8" { 2, 1 }
            <BLANKLINE>
            
        This is a test with a tree that isn't symmetrical::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 1')
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 2')
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4}, 'Leaf 3')
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1}, 'Leaf 4')
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 5')
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 6')
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, "Node 1",  player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, "Node 2", player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, "Node 3", player = player_a2)
            sage: node_a6 = Node({'C': leaf_a5, 'D': leaf_a6}, "Node 4", player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, "Root", player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: egame_a1.set_info_set([node_a1, node_a2])
            sage: gambit_egame_a1 = egame_a1.gambit_convert()  # optional - gambit
            sage: gambit_egame_a1.players  # optional - gambit
            [<Player [0] 'Player 1' in game ''>, <Player [1] 'Player 2' in game ''>]
            sage: gambit_egame_a1.outcomes  # optional - gambit
            [<Outcome [0] 'Leaf 5' in game ''>, <Outcome [1] 'Leaf 6' in game ''>, <Outcome [2] 'Leaf 1' in game ''>, <Outcome [3]
            'Leaf 2' in game ''>, <Outcome [4] 'Leaf 3' in game ''>, <Outcome [5] 'Leaf 4' in game ''>]
            sage: gambit_egame_a1.root  # optional - gambit
            <Node [1] 'Root' in game ''>
            sage: gambit_egame_a1  # optional - gambit
            EFG 2 R "" { "Player 1" "Player 2" }
            ""
            <BLANKLINE>
            p "Root" 1 1 "(Extensive form game node with name: Root)" { "A" "B" } 0
            p "Node 3" 2 1 "(Extensive form game node with name: Node 3,)" { "C" "D" } 0
            p "Node 1" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2)" { "A" "B" } 0
            t "" 3 "Leaf 1" { 0, 1 }
            t "" 4 "Leaf 2" { 1, 0 }
            p "Node 2" 1 2 "(Extensive form game node with name: Node 1, Extensive form game node with name: Node 2)" { "A" "B" } 0
            t "" 5 "Leaf 3" { 2, 4 }
            t "" 6 "Leaf 4" { 2, 1 }
            p "Node 4" 2 2 "(Extensive form game node with name: Node 4,)" { "C" "D" } 0
            t "" 1 "Leaf 5" { 0, 1 }
            t "" 2 "Leaf 6" { 1, 0 }
            <BLANKLINE>

        This is a test for a game with more than 2 players::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: player_3 = Player('Player 3')
            sage: leaf_1 = Leaf({player_1 : 0, player_2: 1, player_3: -5}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1 : 1, player_2: 0, player_3: -4}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1 : 2, player_2: 4, player_3: -3}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1 : 2, player_2: 1, player_3: -2}, 'Leaf 4')
            sage: node_1 = Node({'A': leaf_1, 'B': leaf_2}, 'Node 1', player_3)
            sage: node_2 = Node({'A': leaf_3, 'B': leaf_4}, 'Node 2', player_2)
            sage: root_1 = Node({'C': node_1, 'D': node_2}, 'Root 1', player_1)
            sage: egame_1 = ExtensiveFormGame(root_1)
            sage: gambit_egame_1 = egame_1.gambit_convert()  # optional - gambit
            sage: gambit_egame_1.players  # optional - gambit
            [<Player [0] 'Player 1' in game ''>, <Player [1] 'Player 2' in game ''>, <Player [2] 'Player 3' in game ''>]
            sage: gambit_egame_1.root  # optional - gambit
            <Node [1] 'Root 1' in game ''>
            sage: gambit_egame_1.infosets  # optional - gambit
            [<Infoset [0] '(Extensive form game node with name: Root 1)' for player 'Player 1' in game ''>, 
            <Infoset [0] '(Extensive form game node with name: Node 2,)' for player 'Player 2' in game ''>, 
            <Infoset [0] '(Extensive form game node with name: Node 1,)' for player 'Player 3' in game ''>]
            sage: gambit_egame_1  # optional - gambit
            EFG 2 R "" { "Player 1" "Player 2" "Player 3" }
            ""
            <BLANKLINE>
            p "Root 1" 1 1 "(Extensive form game node with name: Root 1)" { "C" "D" } 0
            p "Node 1" 3 1 "(Extensive form game node with name: Node 1,)" { "A" "B" } 0
            t "" 1 "Leaf 1" { 0, 1, -5 }
            t "" 2 "Leaf 2" { 1, 0, -4 }
            p "Node 2" 2 1 "(Extensive form game node with name: Node 2,)" { "A" "B" } 0
            t "" 3 "Leaf 3" { 2, 4, -3 }
            t "" 4 "Leaf 4" { 2, 1, -2 }
            <BLANKLINE>

        """
        g = Game.new_tree()
        for player in self.players:
            g.players.add(player.name)
        d = self._grow_infoset_graph_dictionary()
        gambit_root = g.root
        gambit_root.label = self.tree_root.name
        move = gambit_root.append_move(g.players[self.tree_root.player.name], len(self.tree_root.children))
        move.label = "(%s)" %self.tree_root
        for index in range(len(self.tree_root.actions)):
            move.actions[index].label = self.tree_root.actions[index]
        tuple_root = tuple([self.tree_root])
        current_info_sets = d[tuple_root]
        parent_dict = {}
        parent_dict[self.tree_root] = g.root

        while len(current_info_sets)!= 0:
            for info_set in current_info_sets:
                for node in info_set:
                    for i,action in enumerate(node.parent.actions):
                        if node.parent.node_input[action] is node:                        
                          action_getting_index = i
                    gambit_node = parent_dict[node.parent].children[action_getting_index]
                    gambit_node.label = node.name
                    if node is info_set[0]:
                        move = gambit_node.append_move(g.players[node.player.name], len(node.children))
                        move.label = str(tuple(info_set))
                        for action_setting_index in range(len(node.actions)):
                            move.actions[action_setting_index].label = node.actions[action_setting_index]
                    else:
                        gambit_node.append_move(move)
                    for child in node.children:
                        if isinstance(child, Leaf):
                            Outcome = g.outcomes.add(child.name)
                            for player_index in range(len(self.players)):
                                player = self.players[player_index]
                                Outcome[player_index] = int(child[player])
                            leaf_action_index = 0 
                            for i,action in enumerate(node.actions):
                                if node.node_input[action] is child:                        
                                    leaf_action_index = i                                
                            gambit_node.children[leaf_action_index].outcome = Outcome
                        
                    parent_dict[node] = gambit_node
            next_info_sets = []
            for info_set in current_info_sets:
                for key in d.keys():
                    if info_set == key:
                        for listed_info_set in d[key]:
                            next_info_sets.append(listed_info_set)
            current_info_sets = set(next_info_sets)
        return g

    def obtain_nash(self):
        r"""
        To obtain the Nash Equilibria of an ``ExtensiveFormGame``, we firstly set up the game as normal::

            sage: from gambit import Game
            sage: player_1 = Player('1')
            sage: player_2 = Player('2')
            sage: leaf_1 = Leaf({player_1: 2, player_2: 0}, 'Leaf 1')
            sage: leaf_2 = Leaf({player_1: 3, player_2: 1}, 'Leaf 2')
            sage: leaf_3 = Leaf({player_1: 4, player_2: 2}, 'Leaf 3')
            sage: leaf_4 = Leaf({player_1: 3, player_2: 5}, 'Leaf 4')
            sage: leaf_5 = Leaf({player_1: 4, player_2: 1}, 'Leaf 5')
            sage: node_d = Node({'Z': leaf_2, 'Y': leaf_3}, 'd', player_1)
            sage: node_b = Node({'D': leaf_1, 'C': node_d}, 'b', player_2)
            sage: node_c = Node({'B': leaf_4, 'A': leaf_5}, 'c', player_2)
            sage: node_a = Node({'X': node_b, 'W': node_c}, 'a', player_1)
            sage: example = ExtensiveFormGame(node_a)

        Then we simply use the obtain_nash function::

            sage: expected_outcome = [[{'a': {'W': 1.0, 'X': 0.0}, 'd': {'Y': 0.5, 'Z': 0.5}}],
            ....: [{'b': {'C': 0.0, 'D': 1.0}, 'c': {'A': 0.0, 'B': 1.0}}],
            ....: [{'a': {'W': 1.0, 'X': 0.0}, 'd': {'Y': 0.5, 'Z': 0.5}}],
            ....: [{'b': {'C': 0.5, 'D': 0.5}, 'c': {'A': 0.0, 'B': 1.0}}],
            ....: [{'a': {'W': 0.0, 'X': 1.0}, 'd': {'Y': 1.0, 'Z': 0.0}}],
            ....: [{'b': {'C': 1.0, 'D': 0.0}, 'c': {'A': 0.0, 'B': 1.0}}]]
            sage: expected_outcome == example.obtain_nash()
            True

        Here is an example with a different tree::

            sage: leaf_1 = Leaf({player_1: 1, player_2: 5})
            sage: leaf_2 = Leaf({player_1: 5, player_2: 2})
            sage: leaf_3 = Leaf({player_1: 9, player_2: 1})
            sage: leaf_4 = Leaf({player_1: 3, player_2: 0})
            sage: leaf_5 = Leaf({player_1: 2, player_2: 7})
            sage: leaf_6 = Leaf({player_1: 1, player_2: 5})
            sage: node_3 = Node({'f': leaf_2, 'g': leaf_3}, player = player_1)
            sage: node_2 = Node({'d': leaf_1, 'e': node_3}, player = player_2)
            sage: node_4 = Node({'h': leaf_5, 'i': leaf_6}, player = player_2)
            sage: node_1 = Node({'a': node_2, 'b': leaf_4, 'c': node_4}, player = player_1)
            sage: example_2 = ExtensiveFormGame(node_1)
            sage: expected_outcome = [[{'Node 1': {'f': 0.5, 'g': 0.5},
            ....: 'Tree Root': {'a': 0.0, 'b': 1.0, 'c': 0.0}}],
            ....: [{'Node 2': {'d': 1.0, 'e': 0.0}, 'Node 3': {'h': 1.0, 'i': 0.0}}]]
            sage: example_2.obtain_nash() == expected_outcome
            True
            
        The following is a test to show that this works for larger trees too::

            sage: player_a1 = Player('Player 1')
            sage: player_a2 = Player('Player 2')
            sage: leaf_a1 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 1')
            sage: leaf_a2 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 2')
            sage: leaf_a3 = Leaf({player_a1 : 2, player_a2: 4}, 'Leaf 3')
            sage: leaf_a4 = Leaf({player_a1 : 2, player_a2: 1}, 'Leaf 4')
            sage: leaf_a5 = Leaf({player_a1 : 0, player_a2: 1}, 'Leaf 5')
            sage: leaf_a6 = Leaf({player_a1 : 1, player_a2: 0}, 'Leaf 6')
            sage: leaf_a7 = Leaf({player_a1 : 2, player_a2: 4}, 'Leaf 7')
            sage: leaf_a8 = Leaf({player_a1 : 2, player_a2: 1}, 'Leaf 8')
            sage: node_a1 = Node({'A': leaf_a1, 'B': leaf_a2}, "Node 1", player = player_a1)
            sage: node_a2 = Node({'A': leaf_a3, 'B': leaf_a4}, "Node 2", player = player_a1)
            sage: node_a3 = Node({'A': leaf_a5, 'B': leaf_a6}, "Node 3", player = player_a1)
            sage: node_a4 = Node({'A': leaf_a7, 'B': leaf_a8}, "Node 4", player = player_a1)
            sage: node_a5 = Node({'C': node_a1, 'D': node_a2}, "Node 5", player = player_a2)
            sage: node_a6 = Node({'C': node_a3, 'D': node_a4}, "Node 6", player = player_a2)
            sage: root_a = Node({'A': node_a5, 'B': node_a6}, player = player_a1)
            sage: egame_a1 = ExtensiveFormGame(root_a)
            sage: egame_a1.set_info_set([node_a5, node_a6])
            sage: egame_a1.set_info_set([node_a1, node_a2])
            sage: egame_a1.set_info_set([node_a3, node_a4])
            sage: expected_outcome = [[{'Node 1': {'A': 0.5, 'B': 0.5},
            ....: 'Node 2': {'A': 0.5, 'B': 0.5},
            ....: 'Node 3': {'A': 0.0, 'B': 1.0},
            ....: 'Node 4': {'A': 0.0, 'B': 1.0},
            ....: 'Tree Root': {'A': 0.0, 'B': 1.0}}],
            ....: [{'Node 5': {'C': 0.0, 'D': 1.0}, 'Node 6': {'C': 0.0, 'D': 1.0}}]]
            sage: expected_outcome == egame_a1.obtain_nash()  # optional - gambit
            True
            sage: egame_a1.obtain_nash()
            

        """
        from gambit.nash import ExternalLCPSolver
        if Game is None:
            raise NotImplementedError("gambit is not installed")
        gambit_efg = self.gambit_convert()
        solver = ExternalLCPSolver()
        lcp_output = solver.solve(gambit_efg)
        nasheq = Parser(lcp_output).format_gambit_efg_tree(gambit_efg)
        return nasheq


class Node():
    def __init__(self, node_input, name=False, player=False):
        """
        Node input will be in a dictionary format, consisting of the actions and
        the children of that node::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: child_1 = Leaf({player_1: 0, player_2: 1}, 'Child 1')
            sage: child_2 = Leaf({player_1: 1, player_2: 0}, 'Child 2')
            sage: mother_node = Node({'Action1': child_1, 'Action2': child_2}, 'Mother')
            sage: mother_node.actions
            ['Action1', 'Action2']
            sage: mother_node.children
            [Extensive form game leaf with utilities given by: (0, 1),
             Extensive form game leaf with utilities given by: (1, 0)]

        If we then create a second node, who has :code:`mother_node` as one of
        its children, then the parent of :code:`mother_node` will be set to that
        node::

            sage: sisternode = Node(['inputhere'])
            sage: mother_node.parent
            False
            sage: grandmother_node = Node({'ActionA':mother_node, 'ActionB':sisternode}, 'Node A')
            sage: mother_node.parent
            Extensive form game node with name: Node A

        Nodes can also be created without specifying children or parents by just
        passing the list of actions.  This so that nodes can be passed via a
        tree Sage Graph object to the extensive form game class::

            sage: grandmother_node = Node(['ActionA', 'ActionB'])
            sage: grandmother_node.children
            False
            sage: grandmother_node.parent
            False

        Nodes automatically have player set to false, we can then assign a
        player to that node::

            sage: grandmother_node.player
            False
            sage: grandmother_node.player = player_1
            sage: grandmother_node.player
            Player 1

        If we try to pass an node_input that isn't a dictionary or a list, an
        error is returned::

            sage: grandmother_node = Node(5)
            Traceback (most recent call last):
            ...
            TypeError: Node must be passed an node_input in the form of a dictionary or a list.

            sage: grandmother_node = Node('This is a string')
            Traceback (most recent call last):
            ...
            TypeError: Node must be passed an node_input in the form of a dictionary or a list.

            sage: grandmother_node = Node(matrix([[1, 1], [1, 1]]))
            Traceback (most recent call last):
            ...
            TypeError: Node must be passed an node_input in the form of a dictionary or a list.

            sage: sisternode = Node(['inputhere'])
            sage: grandmother_node = Node(sisternode)
            Traceback (most recent call last):
            ...
            TypeError: Node must be passed an node_input in the form of a dictionary or a list.
        """
        self.node_input = node_input
        self.player = player
        self.name = name
        self.actions = []
        self.children = False
        self.parent = False
        self.is_root = False

        if type(node_input) is dict:
            self.actions = node_input.keys()
            self.children = node_input.values()
            for child in self.children:
                child.parent = self

        elif type(node_input) is list:
            if node_input == []:
                self.actions = False
            else:
                self.actions = node_input

        else:
            raise TypeError("Node must be passed an node_input in the form of a dictionary or a list.")



    def __repr__(self):
        """
        Representation method for the Node::

            sage: repr_node = Node(['inputhere'])
            sage: repr_node
            Extensive form game node without a name
            sage: repr_node.name = "A named Node"
            sage: repr_node
            Extensive form game node with name: A named Node
            sage: repr_node = Node(['inputhere'], "A different name")
            sage: repr_node
            Extensive form game node with name: A different name
        """
        if self.name is False:
            return 'Extensive form game node without a name'
        else:
            return 'Extensive form game node with name: ' + self.name

    def _is_complete(self):
        """
        If we create a node where their children aren't specified and no parent
        is set, the node is considered incomplete::

            sage: b = Node(['Action1', 'Action2'])
            sage: b._is_complete == True
            False

        However, when we do specify all those attributes, the node is then
        considered complete::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: child_1 = Leaf({player_1: 0, player_2: 1}, 'Child 1')
            sage: child_2 = Leaf({player_1: 1, player_2: 0}, 'Child 2')
            sage: mother_node = Node({'Action1': child_1, 'Action2': child_2}, 'Node B', player_1)
            sage: sisternode = Node(['inputhere'])
            sage: grandmother_node = Node({'ActionA':mother_node, 'ActionB':sisternode},
            ....:                         'Node A')
            sage: mother_node._is_complete()
            True

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: child_1 = Leaf({player_1: 0, player_2: 1}, 'Child 1')
            sage: child_2 = Leaf({player_1: 1, player_2: 0}, 'Child 2')
            sage: mother_node = Node({'Action1': child_1, 'Action2': child_2}, 'Node B')
            sage: sisternode = Node(['inputhere'])
            sage: grandmother_node = Node({'ActionA':mother_node, 'ActionB':sisternode},
            ....:                         'Node A')
            sage: mother_node._is_complete()
            False

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: child_1 = Leaf({player_1: 0, player_2: 1}, 'Child 1')
            sage: child_2 = Leaf({player_1: 1, player_2: 0}, 'Child 2')
            sage: mother_node = Node({'Action1': child_1, 'Action2': child_2},
            ....:                    'Node B', player_1)
            sage: sisternode = Node(['inputhere'])
            sage: mother_node._is_complete()
            False

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: child_1 = Leaf({player_1: 0, player_2: 1}, 'Child 1')
            sage: child_2 = Leaf({player_1: 1, player_2: 0}, 'Child 2')
            sage: mother_node = Node({'Action1': child_1, 'Action2': child_2},
            ....:                    'Node B', player_1)
            sage: mother_node.children = False
            sage: sisternode = Node(['inputhere'])
            sage: grandmother_node = Node({'ActionA':mother_node, 'ActionB':sisternode},
            ....:                         'Node A')
            sage: mother_node._is_complete()
            False
        """
        return all([self.parent , self.actions, self.children, self.player])

    def _player_check(self):
        """
        A check primarily used later for creating of Extensive Form Games::
            sage: grandmother_node = Node([])
            sage: mother_node = Node([])
            sage: grandmother_node.player
            False
            sage: grandmother_node.player = mother_node
            sage: grandmother_node._player_check()
            Traceback (most recent call last):
            ...
            TypeError: Cannot assign a non Player as a player to a Node.
        """
        if self.player is not False:
                    if not isinstance(self.player, Player):
                        raise TypeError("Cannot assign a non Player as a player to a Node.")


class Leaf():
    def __init__(self, payoffs, name=False):
        """
        We can check payoffs of any leaf::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1})
            sage: leaf_1.payoffs[player_1]
            0
            sage: leaf_1[player_1]
            0
            sage: leaf_1[player_2]
            1
            sage: leaf_1.players
            [Player 1, Player 2]
            sage: leaf_1.utilities
            (0, 1)

        The payoffs must be in dictionary form such that the keys are players,
        and the values are either float or integers::

            sage: node_1 = Node(['input']); node_2 = Node(['input'])
            sage: leaf_1 = Leaf({node_1: 0, node_2: 1})
            Traceback (most recent call last):
            ...
            TypeError: The payoffs within Leaf must be in dictionary form with players as keys, and numbers as payoffs.

            sage: leaf_1 = Leaf([0, 1])
            Traceback (most recent call last):
            ...
            TypeError: The payoffs within Leaf must be in dictionary form with players as keys, and numbers as payoffs.
        """
        if type(payoffs) is not dict:
            raise TypeError("The payoffs within Leaf must be in dictionary form with players as keys, and numbers as payoffs.")

        self.payoffs =  payoffs
        self.name = name
        self.players = sorted(payoffs.keys(), key=lambda x:x.name)
        self.parent = False
        self.utilities = tuple([self[player] for player in sorted(self.players, key=lambda x:x.name)])

        for player in self.players:
            if not isinstance(player, Player):
                raise TypeError("The payoffs within Leaf must be in dictionary form with players as keys, and numbers as payoffs.")

    def __repr__(self):
        """
        Representation method for the leaf::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 0, player_2: 1}, 'end_leaf')
            sage: leaf_1
            Extensive form game leaf with utilities given by: (0, 1)

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_1 = Leaf({player_1: 5, player_2: 1}, 'end_leaf')
            sage: leaf_1
            Extensive form game leaf with utilities given by: (5, 1)

            sage: player_1 = Player('Vince')
            sage: player_2 = Player('Hannah')
            sage: player_3 = Player('James')
            sage: leaf_1 = Leaf({player_1: 5, player_2: 1, player_3:10}, 'end_leaf')
            sage: leaf_1
            Extensive form game leaf with utilities given by: (1, 10, 5)
        """
        return 'Extensive form game leaf with utilities given by: ' + str(self.utilities)


    def __delitem__(self, key):
        """
        This method is one of a collection that aims to make a leaf
        instance behave like a dictionary.

        Here we set up deleting an element of the payoffs dictionary::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_dict = Leaf({player_1: 0, player_2: 1})
            sage: del(leaf_dict[player_2])
            sage: leaf_dict.payoffs
            {Player 1: 0}
        """
        self.payoffs.pop(key, None)

    def __getitem__(self, key):
        """
        This method is one of a collection that aims to make a leaf
        instance behave like a dictionary.

        Here we allow for querying a key::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_dict = Leaf({player_1: 0, player_2: 1})
            sage: leaf_dict[player_1]
            0
            sage: del(leaf_dict[player_1])
            sage: leaf_dict[player_1]
            Traceback (most recent call last):
            ...
            KeyError: Player 1

        """
        return self.payoffs[key]

    def __iter__(self):
        """
        This method is one of a collection that aims to make a game
        instance behave like a dictionary.

        Here we allow for iteration over the leaf to correspond to
        iteration over keys of the utility dictionary::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_dict = Leaf({player_1: 0, player_2: 1})
            sage: for key in leaf_dict:
            ....:     print "The player: {}, has payoff {}".format(key, leaf_dict[key])
            The player: Player 2, has payoff 1
            The player: Player 1, has payoff 0
        """
        return iter(self.payoffs)

    def __setitem__(self, key, value):
        """
        This method is one of a collection that aims to make a game
        instance behave like a dictionary.

        Here we set up setting the value of a key::

            sage: player_1 = Player('Player 1')
            sage: player_2 = Player('Player 2')
            sage: leaf_dict = Leaf({player_1: 0, player_2: 1})
            sage: leaf_dict[player_1]
            0
            sage: leaf_dict[player_1] = 2
            sage: leaf_dict[player_1]
            2

        """
        self.payoffs[key] = value


class Player():
    def __init__(self, name):
        """
        We can use Player() to assign players to nodes::

            sage: jack_1 = Node([0, 1])
            sage: jack_1.player = Player('Jack')
            sage: jack_1.player
            Jack

        If a node is not specificed a player, then this should return false::

            sage: sam_1 = Node([0, 1])
            sage: sam_1.player
            False
            sage: sam_player = Player('Sam')
            sage: sam_1.player = sam_player
            sage: sam_1.player
            Sam
            sage: sam_2 = Node([0, 1], player = sam_player)
            sage: sam_2.player
            Sam

        A player can be reassigned for Nodes::
            sage: andy_player = Player('Andy')
            sage: sam_2.player = andy_player
            sage: sam_2.player
            Andy

        We can create players and assign them names::

            sage: ben_player = Player('Benjamin')
            sage: ben_player.name
            'Benjamin'
        """
        self.name = name

    def __repr__(self):
        """
        Representation method for the player::

            sage: apple_1 = Player('Apple')
            sage: apple_1
            Apple
        """
        if self.name is False:
            return "False"
        else:
            return self.name

    def __hash__(self):
        """
        Makes the player class hashable::

            sage: apple_1 = Player('Apple')
            sage: banana_1 = Leaf({apple_1 : 0})
            sage: banana_1.payoffs
            {Apple: 0}
        """
        return hash(self.name)
