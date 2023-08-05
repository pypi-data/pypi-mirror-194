import wetsuit


# Don't want to startup H2O server for tests
def test_instantiate():
    tf = wetsuit.H2oFrameTransformer(features=['x1', 'x2'], response='y')
    assert tf
