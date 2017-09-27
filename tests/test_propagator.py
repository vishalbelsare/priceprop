import unittest
import numpy as np
import pandas as pd
import propagator.propagator as prop

class TestIntegrate(unittest.TestCase):
    def test(self):
        np.testing.assert_almost_equal(prop.integrate([1,2,3]), [0,1,3])
        
class TestSmoothTailRBF(unittest.TestCase):
    def test(self):
        x = np.arange(1,100, dtype=float)**-1
        s = prop.smooth_tail_rbf(x)
        np.testing.assert_allclose(s, x, rtol=.01, atol=.01)

class TestPropagate(unittest.TestCase):
    def test_pulse(self):
        np.testing.assert_almost_equal(
            prop.propagate([1,0,0], [1,.5,0]),
            [1,.5,0]
        )
        
class TestResponse(unittest.TestCase):
    
    def test_lsr(self):
        # test simple response
        args = ([-1,0,1,0], [0,1,0,0])
        l,s,r = prop.response(*args)
        np.testing.assert_almost_equal(
            l, range(-2,3)
        )
        np.testing.assert_almost_equal(
            s, [0, -.25, 0, .25, 0]
        )
        np.testing.assert_almost_equal(
            r, [.25,.25,0,0,.25]
        )
        # test ret argument
        np.testing.assert_almost_equal(
            l, prop.response(*args, ret='l')
        )
        np.testing.assert_almost_equal(
            s, prop.response(*args, ret='s')
        )
        np.testing.assert_almost_equal(
            r, prop.response(*args, ret='r')
        )
        
    def test_grouped(seld):
        df = pd.DataFrame({
            'r':    [-2, 0, 1, 0,-4, 0, 1, 0],
            's':    [ 0, 1, 0, 0, 0, 1, 0, 0], 
            'date': [ 0, 0, 0, 0, 1, 1, 1, 1]
        })
        l, s, r = prop.response_grouped_df(df, ['r','s'])
        np.testing.assert_almost_equal(
            l, range(-2,3)
        )
        np.testing.assert_almost_equal(
            s, [ 0., -0.75, 0., 0.25, 0.]
        )
        np.testing.assert_almost_equal(
            r, [.75,.75,0,0,.25]
        )
        
# testing the analytical powerlaws would require to reimplement them and
# they are only helpers for manual testing anyway

class TestTIM1(unittest.TestCase):
    
    def test_tim1(self):
        np.testing.assert_almost_equal(
            prop.tim1([1,0,0,0], [1,.5,0,0]), 
            [1,.5,0,0]
        )

    def test_estimate_tim1(self):
        np.testing.assert_almost_equal(
            prop.estimate_tim1([.25,0,0,0], [0,0,0,.25,.125,0,0], maxlag=4),
            [1,.5,0,0]
        )
    def test_tim2(self):
        np.testing.assert_almost_equal(
            prop.tim2([1,-1], np.array([1,0,], dtype=bool),[1,0,],[.1,0,]),
            [.1,-1]
        )
    def test_estimate_tim2(self):
        gn, gc = prop.estimate_tim2(
            [1,0],[1,0],[0,0],[0,0],[0,.1,0],[0,1,0], maxlag=2
        )
        np.testing.assert_almost_equal(gn, [.1,0])
        np.testing.assert_almost_equal(gc, [1,0])
        )
    def test_hdim2(self):
        np.testing.assert_almost_equal(
            prop.hdim2([1,-1], np.array([1,0,], dtype=bool),[1,0,],[.1,0,]),
            [.1,0]
        )
    def test_estimate_hdim2(self):
        # I can't come up with a non-singular example... save a manual test
        pass