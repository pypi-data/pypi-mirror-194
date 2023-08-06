from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l1lllll1l1l11ll1Il1l1, llll1ll11l1ll111Il1l1, public, llll1l11ll11l11lIl1l1, ll1ll1l1l1lllll1Il1l1
from reloadium.corium.l111lll111111111Il1l1 import llll1ll111111111Il1l1, l1l11l111l111ll1Il1l1
from reloadium.corium.llll1ll11l1ll111Il1l1 import ll1ll11l111l1111Il1l1, l111ll11ll1lll1lIl1l1
from reloadium.corium.l1l11lll1111111lIl1l1 import l11111ll1llll11lIl1l1
from reloadium.corium.l11l1lllll1111l1Il1l1 import l11l1lllll1111l1Il1l1
from reloadium.corium.l1lll111l1l11ll1Il1l1 import l1111111llll1ll1Il1l1
from reloadium.corium.ll11ll11111ll111Il1l1 import lll1111111ll1l11Il1l1, lll111l1lll11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['l111l1lllll11lllIl1l1', 'l11ll111l11ll1l1Il1l1', 'll1llll1ll1l111lIl1l1']


l1ll1111l11l1ll1Il1l1 = l11l1lllll1111l1Il1l1.lll1l1lll11llll1Il1l1(__name__)


class l111l1lllll11lllIl1l1:
    @classmethod
    def lll111l111l11lllIl1l1(lll111l1l11111l1Il1l1) -> Optional[FrameType]:
        lllll11l1llll111Il1l1: FrameType = sys._getframe(2)
        ll111l11ll111lllIl1l1 = next(ll1ll1l1l1lllll1Il1l1.lllll11l1llll111Il1l1.l111ll1l1111l1llIl1l1(lllll11l1llll111Il1l1))
        return ll111l11ll111lllIl1l1


class l11ll111l11ll1l1Il1l1(l111l1lllll11lllIl1l1):
    @classmethod
    def ll11111l1lll1l1lIl1l1(l1ll1lll1111111lIl1l1, l1lll111l1l1l1llIl1l1: List[Any], l111lll1111l1ll1Il1l1: Dict[str, Any], l1ll11ll1llll11lIl1l1: List[lll1111111ll1l11Il1l1]) -> Any:  # type: ignore
        with l111ll11ll1lll1lIl1l1():
            assert l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1
            lllll11l1llll111Il1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1.lllll1l1l1ll11l1Il1l1.ll1l1l11l1111l11Il1l1()
            lllll11l1llll111Il1l1.ll111lll1ll1ll1lIl1l1()

            ll1ll1111ll1lll1Il1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.l1l11ll11l1l11l1Il1l1.l1l1ll1ll11l1l11Il1l1(lllll11l1llll111Il1l1.l1lll1l1llllllllIl1l1, lllll11l1llll111Il1l1.l1l1l1ll1l1l11llIl1l1.lll1l1l111l1ll11Il1l1())
            assert ll1ll1111ll1lll1Il1l1
            l1l1l1ll11l111llIl1l1 = l1ll1lll1111111lIl1l1.lll111l111l11lllIl1l1()

            for ll1l111ll1l1llllIl1l1 in l1ll11ll1llll11lIl1l1:
                ll1l111ll1l1llllIl1l1.ll1lll1l1ll1l1l1Il1l1()

            for ll1l111ll1l1llllIl1l1 in l1ll11ll1llll11lIl1l1:
                ll1l111ll1l1llllIl1l1.llll111llll11ll1Il1l1()


        ll111l11ll111lllIl1l1 = ll1ll1111ll1lll1Il1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1);        lllll11l1llll111Il1l1.ll1l1lll1llll111Il1l1.additional_info.pydev_step_stop = l1l1l1ll11l111llIl1l1  # type: ignore

        return ll111l11ll111lllIl1l1

    @classmethod
    async def lll1l1ll11llll1lIl1l1(l1ll1lll1111111lIl1l1, l1lll111l1l1l1llIl1l1: List[Any], l111lll1111l1ll1Il1l1: Dict[str, Any], l1ll11ll1llll11lIl1l1: List[lll111l1lll11111Il1l1]) -> Any:  # type: ignore
        with l111ll11ll1lll1lIl1l1():
            assert l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1
            lllll11l1llll111Il1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1.lllll1l1l1ll11l1Il1l1.ll1l1l11l1111l11Il1l1()
            lllll11l1llll111Il1l1.ll111lll1ll1ll1lIl1l1()

            ll1ll1111ll1lll1Il1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.l1l11ll11l1l11l1Il1l1.l1l1ll1ll11l1l11Il1l1(lllll11l1llll111Il1l1.l1lll1l1llllllllIl1l1, lllll11l1llll111Il1l1.l1l1l1ll1l1l11llIl1l1.lll1l1l111l1ll11Il1l1())
            assert ll1ll1111ll1lll1Il1l1
            l1l1l1ll11l111llIl1l1 = l1ll1lll1111111lIl1l1.lll111l111l11lllIl1l1()

            for ll1l111ll1l1llllIl1l1 in l1ll11ll1llll11lIl1l1:
                await ll1l111ll1l1llllIl1l1.ll1lll1l1ll1l1l1Il1l1()

            for ll1l111ll1l1llllIl1l1 in l1ll11ll1llll11lIl1l1:
                await ll1l111ll1l1llllIl1l1.llll111llll11ll1Il1l1()


        ll111l11ll111lllIl1l1 = await ll1ll1111ll1lll1Il1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1);        lllll11l1llll111Il1l1.ll1l1lll1llll111Il1l1.additional_info.pydev_step_stop = l1l1l1ll11l111llIl1l1  # type: ignore

        return ll111l11ll111lllIl1l1


class ll1llll1ll1l111lIl1l1(l111l1lllll11lllIl1l1):
    @classmethod
    def ll11111l1lll1l1lIl1l1(l1ll1lll1111111lIl1l1) -> Optional[ModuleType]:  # type: ignore
        with l111ll11ll1lll1lIl1l1():
            assert l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1
            lllll11l1llll111Il1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.lll1111ll11ll11lIl1l1.lllll1l1l1ll11l1Il1l1.ll1l1l11l1111l11Il1l1()

            l111lll11l11111lIl1l1 = Path(lllll11l1llll111Il1l1.l111lll1ll1l1111Il1l1.f_globals['__spec__'].origin).absolute()
            ll111ll1l1ll1l11Il1l1 = lllll11l1llll111Il1l1.l111lll1ll1l1111Il1l1.f_globals['__name__']
            lllll11l1llll111Il1l1.ll111lll1ll1ll1lIl1l1()
            l11111l11ll1l11lIl1l1 = l11111ll1llll11lIl1l1.ll1l1111l11lllllIl1l1.l1l1ll11ll1ll1llIl1l1.l1l11l11111l11l1Il1l1(l111lll11l11111lIl1l1)

            if ( not l11111l11ll1l11lIl1l1):
                l1ll1111l11l1ll1Il1l1.l1ll1llll1ll1lllIl1l1('Could not retrieve src.', lllllllll1111lllIl1l1={'file': l1111111llll1ll1Il1l1.llll1lll1llll111Il1l1(l111lll11l11111lIl1l1), 
'fullname': l1111111llll1ll1Il1l1.ll111ll1l1ll1l11Il1l1(ll111ll1l1ll1l11Il1l1)})

            assert l11111l11ll1l11lIl1l1

        try:
            l11111l11ll1l11lIl1l1.l11111l1l111lll1Il1l1()
            l11111l11ll1l11lIl1l1.llll1111lll1llllIl1l1(ll111ll111l1ll11Il1l1=False)
            l11111l11ll1l11lIl1l1.llll11l11ll11111Il1l1(ll111ll111l1ll11Il1l1=False)
        except ll1ll11l111l1111Il1l1 as lll111l1l1l1ll11Il1l1:
            lllll11l1llll111Il1l1.l111ll1lll11llllIl1l1(lll111l1l1l1ll11Il1l1)
            return None

        import importlib.util

        ll11l11l11l1ll1lIl1l1 = lllll11l1llll111Il1l1.l111lll1ll1l1111Il1l1.f_locals['__spec__']
        l11l1lll11111111Il1l1 = importlib.util.module_from_spec(ll11l11l11l1ll1lIl1l1)

        l11111l11ll1l11lIl1l1.ll1ll1l1111l1l1lIl1l1(l11l1lll11111111Il1l1)
        return l11l1lll11111111Il1l1


l1l11l111l111ll1Il1l1.lll1lll11l1ll11lIl1l1(llll1ll111111111Il1l1.llllllll1llllll1Il1l1, l11ll111l11ll1l1Il1l1.ll11111l1lll1l1lIl1l1)
l1l11l111l111ll1Il1l1.lll1lll11l1ll11lIl1l1(llll1ll111111111Il1l1.l11111l1ll111111Il1l1, l11ll111l11ll1l1Il1l1.lll1l1ll11llll1lIl1l1)
l1l11l111l111ll1Il1l1.lll1lll11l1ll11lIl1l1(llll1ll111111111Il1l1.l111l11111l11l11Il1l1, ll1llll1ll1l111lIl1l1.ll11111l1lll1l1lIl1l1)
