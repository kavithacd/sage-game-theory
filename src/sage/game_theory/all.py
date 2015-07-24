from sage.misc.lazy_import import lazy_import

lazy_import('sage.game_theory', 'catalog', 'game_theory')
lazy_import('sage.game_theory.cooperative_game', 'CooperativeGame')
lazy_import('sage.game_theory.normal_form_game', 'NormalFormGame')
lazy_import('sage.game_theory.matching_game', 'MatchingGame')
lazy_import('sage.game_theory.extensive_form_game', ['ExtensiveFormGame', 'EFG_Node', 'EFG_Player', 'EFG_Leaf'])
