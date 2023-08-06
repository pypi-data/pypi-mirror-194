import sys

from reloadium.corium.ll1ll1l1l1lllll1Il1l1.ll11ll1ll1l11l1lIl1l1 import l111ll1lllll1ll1Il1l1

__RELOADIUM__ = True

l111ll1lllll1ll1Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class lll11ll1ll111111Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = lll11ll1ll111111Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
