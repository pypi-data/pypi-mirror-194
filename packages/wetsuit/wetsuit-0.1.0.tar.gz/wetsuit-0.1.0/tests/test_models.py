from h2o.estimators import H2OEstimator

import wetsuit


# Don't want to startup H2O server for tests
def test_instantiate():
    reg = wetsuit.WetsuitRegressor(H2OEstimator(), features=['x1', 'x2'], response='y')
    cls = wetsuit.WetsuitClassifier(H2OEstimator(), features=['x1', 'x2'], response='y')
    assert reg
    assert cls
