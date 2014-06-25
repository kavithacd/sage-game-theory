r"""
Commutative rings
"""
#*****************************************************************************
#  Copyright (C) 2005      David Kohel <kohel@maths.usyd.edu>
#                          William Stein <wstein@math.ucsd.edu>
#                2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2013 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.category_with_axiom import CategoryWithAxiom

class CommutativeRings(CategoryWithAxiom):
    """
    The category of commutative rings

    commutative rings with unity, i.e. rings with commutative * and
    a multiplicative identity

    EXAMPLES::

         sage: C = CommutativeRings(); C
         Category of commutative rings
         sage: C.super_categories()
         [Category of rings, Category of commutative magmas]

    TESTS::

        sage: TestSuite(C).run()

        sage: QQ['x,y,z'] in CommutativeRings()
        True
        sage: GroupAlgebra(DihedralGroup(3), QQ) in CommutativeRings()
        False
        sage: MatrixSpace(QQ,2,2) in CommutativeRings()
        False

    GroupAlgebra should be fixed::

        sage: GroupAlgebra(CyclicPermutationGroup(3), QQ) in CommutativeRings() # todo: not implemented
        True

    """
    class ElementMethods:
        pass

    class Finite(CategoryWithAxiom):
        class ParentMethods:
            def cyclotomic_cosets(self, q, cosets=None):
                r"""
                Return the (multiplicative) orbits of ``q`` in the ring.

                Let `R` be a finite commutative ring. The group of invertible
                elements `R^*` in `R` gives rise to a group action on `R` by
                multiplication.  An orbit of the subgroup generated by an
                invertible element `q` is called a `q`-*cyclotomic coset* (since
                in a finite ring, each invertible element is a root of unity).

                These cosets arise in the theory of minimal polynomials of
                finite fields, duadic codes and combinatorial designs. Fix a
                primitive element `z` of `GF(q^k)`. The minimal polynomial of
                `z^s` over `GF(q)` is given by

                .. math::

                         M_s(x) = \prod_{i \in C_s} (x - z^i),


                where `C_s` is the `q`-cyclotomic coset mod `n` containing `s`,
                `n = q^k - 1`.

                .. NOTE::

                    When `R = \ZZ / n \ZZ` the smallest element of each coset is
                    sometimes callled a *coset leader*. This function returns
                    sorted lists so that the coset leader will always be the
                    first element of the coset.

                INPUT:

                - ``q`` -- an invertible element of the ring

                - ``cosets`` -- an optional lists of elements of ``self``. If
                  provided, the function only return the list of cosets that
                  contain some element from ``cosets``.

                OUTPUT:

                A list of lists.

                EXAMPLES::

                    sage: Zmod(11).cyclotomic_cosets(2)
                    [[0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
                    sage: Zmod(15).cyclotomic_cosets(2)
                    [[0], [1, 2, 4, 8], [3, 6, 9, 12], [5, 10], [7, 11, 13, 14]]

                Since the group of invertible elements of a finite field is
                cyclic, the set of squares is a particular case of cyclotomic
                coset::

                    sage: K = GF(25,'z')
                    sage: a = K.multiplicative_generator()
                    sage: K.cyclotomic_cosets(a**2,cosets=[1])
                    [[1, 2, 3, 4, z + 1, z + 3,
                      2*z + 1, 2*z + 2, 3*z + 3,
                      3*z + 4, 4*z + 2, 4*z + 4]]
                    sage: sorted(b for b in K if not b.is_zero() and b.is_square())
                    [1, 2, 3, 4, z + 1, z + 3,
                     2*z + 1, 2*z + 2, 3*z + 3,
                     3*z + 4, 4*z + 2, 4*z + 4]

                We compute some examples of minimal polynomials::

                    sage: K = GF(27,'z')
                    sage: a = K.multiplicative_generator()
                    sage: R.<X> = PolynomialRing(K, 'X')
                    sage: a.minimal_polynomial(X)
                    X^3 + 2*X + 1
                    sage: cyc3 = Zmod(26).cyclotomic_cosets(3,cosets=[1]); cyc3
                    [[1, 3, 9]]
                    sage: prod(X - a**i for i in cyc3[0])
                    X^3 + 2*X + 1

                    sage: (a**7).minimal_polynomial(X)
                    X^3 + X^2 + 2*X + 1
                    sage: cyc7 = Zmod(26).cyclotomic_cosets(3,cosets=[7]); cyc7
                    [[7, 11, 21]]
                    sage: prod(X - a**i for i in cyc7[0])
                    X^3 + X^2 + 2*X + 1

                Cyclotomic cosets of fields are useful in combinatorial design
                theory to provide so called difference families (see
                :wikipedia:`Difference_set`). This is illustrated on the
                following examples::

                    sage: K = GF(5)
                    sage: a = K.multiplicative_generator()
                    sage: H = K.cyclotomic_cosets(a**2, cosets=[1,2]); H
                    [[1, 4], [2, 3]]
                    sage: sorted(x-y for D in H for x in D for y in D if x != y)
                    [1, 2, 3, 4]

                    sage: K = GF(37)
                    sage: a = K.multiplicative_generator()
                    sage: H = K.cyclotomic_cosets(a**4, cosets=[1]); H
                    [[1, 7, 9, 10, 12, 16, 26, 33, 34]]
                    sage: sorted(x-y for D in H for x in D for y in D if x != y)
                    [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, ..., 33, 34, 34, 35, 35, 36, 36]
                """
                q = self(q)

                try:
                    ~q
                except ZeroDivisionError:
                    raise ValueError("%s is not invertible in %s"%(q,self))

                if cosets is None:
                    rest = set(self)
                else:
                    rest = set(self(x) for x in cosets)

                orbits = []
                while rest:
                    x0 = rest.pop()
                    o = [x0]
                    x = q*x0
                    while x != x0:
                        o.append(x)
                        rest.discard(x)
                        x *= q
                    o.sort()
                    orbits.append(o)

                orbits.sort()
                return orbits