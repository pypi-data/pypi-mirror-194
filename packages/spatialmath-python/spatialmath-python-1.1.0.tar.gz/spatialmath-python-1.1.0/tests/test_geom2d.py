#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 14:37:24 2020

@author: corkep
"""

from spatialmath.geom2d import *
from spatialmath.pose2d import SE2

import unittest
import numpy.testing as nt
import spatialmath.base as base


class Polygon2Test(unittest.TestCase):

    # Primitives
    def test_constructor1(self):

        p = Polygon2([(1, 2), (3, 2), (2, 4)])
        self.assertIsInstance(p, Polygon2)
        self.assertEqual(len(p), 3)
        self.assertEqual(str(p), "Polygon2 with 4 vertices")
        nt.assert_array_equal(p.vertices(), np.array([[1, 3, 2], [2, 2, 4]]))
        nt.assert_array_equal(
            p.vertices(unique=False), np.array([[1, 3, 2, 1], [2, 2, 4, 2]])
        )

    def test_methods(self):

        p = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))

        self.assertEqual(p.area(), 4)
        self.assertEqual(p.moment(0, 0), 4)
        self.assertEqual(p.moment(1, 0), 0)
        self.assertEqual(p.moment(0, 1), 0)
        nt.assert_array_equal(p.centroid(), np.r_[0, 0])

        self.assertEqual(p.radius(), np.sqrt(2))
        nt.assert_array_equal(p.bbox(), np.r_[-1, -1, 1, 1])

    def test_contains(self):

        p = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))
        self.assertTrue(p.contains([0, 0], radius=1e-6))
        self.assertTrue(p.contains([1, 0], radius=1e-6))
        self.assertTrue(p.contains([-1, 0], radius=1e-6))
        self.assertTrue(p.contains([0, 1], radius=1e-6))
        self.assertTrue(p.contains([0, -1], radius=1e-6))

        self.assertFalse(p.contains([0, 1.1], radius=1e-6))
        self.assertFalse(p.contains([0, -1.1], radius=1e-6))
        self.assertFalse(p.contains([1.1, 0], radius=1e-6))
        self.assertFalse(p.contains([-1.1, 0], radius=1e-6))

        self.assertTrue(p.contains(np.r_[0, -1], radius=1e-6))
        self.assertFalse(p.contains(np.r_[0, 1.1], radius=1e-6))

    def test_transform(self):

        p = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))

        p = p.transformed(SE2(2, 3))

        self.assertEqual(p.area(), 4)
        self.assertEqual(p.moment(0, 0), 4)
        self.assertEqual(p.moment(1, 0), 8)
        self.assertEqual(p.moment(0, 1), 12)
        nt.assert_array_equal(p.centroid(), np.r_[2, 3])

    def test_intersect(self):

        p1 = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))

        p2 = p1.transformed(SE2(2, 3))
        self.assertFalse(p1.intersects(p2))

        p2 = p1.transformed(SE2(1, 1))
        self.assertTrue(p1.intersects(p2))

        self.assertTrue(p1.intersects(p1))

    def test_intersect_line(self):

        p = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))

        l = Line2.Join((-10, 0), (10, 0))
        self.assertTrue(p.intersects(l))

        l = Line2.Join((-10, 1.1), (10, 1.1))
        self.assertFalse(p.intersects(l))

    def test_plot(self):
        p = Polygon2(np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]))
        p.plot()

        p.animate(SE2(1, 2))

    def test_edges(self):

        p = Polygon2([(1, 2), (3, 2), (2, 4)])
        e = p.edges()

        e = list(e)
        nt.assert_equal(e[0], ((1, 2), (3, 2)))
        nt.assert_equal(e[1], ((3, 2), (2, 4)))
        nt.assert_equal(e[2], ((2, 4), (1, 2)))

    # p.move(SE2(0, 0, 0.7))


class Line2Test(unittest.TestCase):
    def test_constructor(self):

        l = Line2([1, 2, 3])
        self.assertEqual(str(l), "Line2: [1. 2. 3.]")

        l = Line2.Join((0, 0), (1, 2))
        nt.assert_equal(l.line, [-2, 1, 0])

        l = Line2.General(2, 1)
        nt.assert_equal(l.line, [2, -1, 1])

    def test_contains(self):
        l = Line2.Join((0, 0), (1, 2))

        self.assertTrue(l.contains((0, 0)))
        self.assertTrue(l.contains((1, 2)))
        self.assertTrue(l.contains((2, 4)))

    def test_intersect(self):

        l1 = Line2.Join((0, 0), (2, 0))  # y = 0
        l2 = Line2.Join((0, 1), (2, 1))  # y = 1
        self.assertFalse(l1.intersect(l2))

        l2 = Line2.Join((2, 1), (2, -1))  # x = 2
        self.assertTrue(l1.intersect(l2))

    def test_intersect_segment(self):

        l1 = Line2.Join((0, 0), (2, 0))  # y = 0
        self.assertFalse(l1.intersect_segment((2, 1), (2, 3)))
        self.assertTrue(l1.intersect_segment((2, 1), (2, -1)))


if __name__ == "__main__":

    unittest.main()
