import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.llll1ll11l1ll111Il1l1 import l111ll11ll1lll1lIl1l1
from reloadium.lib.ll1111111ll11lllIl1l1.l1ll1ll1lll1l111Il1l1 import llllllll1111l11lIl1l1, l11l1111lllllll1Il1l1
from reloadium.corium.ll11ll11111ll111Il1l1 import lll1111111ll1l11Il1l1
from reloadium.corium.ll1ll1l1l1lllll1Il1l1 import l1l1l1l11lllllllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(repr=False)
class lll1l1l1111ll1l1Il1l1(l11l1111lllllll1Il1l1):
    l1ll1ll1lll1l111Il1l1: "l1111l1l11ll1l11Il1l1"
    ll1l11ll1llll1llIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l111111l11ll111lIl1l1(lll111l1l11111l1Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l111111l11ll111lIl1l1()

        l111ll1lll111l1lIl1l1 = list(_sessions.values())

        for l11l1l1111l1l1llIl1l1 in l111ll1lll111l1lIl1l1:
            if ( not l11l1l1111l1l1llIl1l1.is_active):
                continue

            l11l1lllll111ll1Il1l1 = l11l1l1111l1l1llIl1l1.begin_nested()
            lll111l1l11111l1Il1l1.ll1l11ll1llll1llIl1l1.append(l11l1lllll111ll1Il1l1)

    def __repr__(lll111l1l11111l1Il1l1) -> str:
        return 'DbMemento'

    def ll1lll1l1ll1l1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        super().ll1lll1l1ll1l1l1Il1l1()

        while lll111l1l11111l1Il1l1.ll1l11ll1llll1llIl1l1:
            l11l1lllll111ll1Il1l1 = lll111l1l11111l1Il1l1.ll1l11ll1llll1llIl1l1.pop()
            if (l11l1lllll111ll1Il1l1.is_active):
                try:
                    l11l1lllll111ll1Il1l1.rollback()
                except :
                    pass

    def llll111llll11ll1Il1l1(lll111l1l11111l1Il1l1) -> None:
        super().llll111llll11ll1Il1l1()

        while lll111l1l11111l1Il1l1.ll1l11ll1llll1llIl1l1:
            l11l1lllll111ll1Il1l1 = lll111l1l11111l1Il1l1.ll1l11ll1llll1llIl1l1.pop()
            if (l11l1lllll111ll1Il1l1.is_active):
                try:
                    l11l1lllll111ll1Il1l1.commit()
                except :
                    pass


@dataclass
class l1111l1l11ll1l11Il1l1(llllllll1111l11lIl1l1):
    ll11lllll1llll1lIl1l1 = 'Sqlalchemy'

    ll111l1l1lll1111Il1l1: List["Engine"] = field(init=False, default_factory=list)
    l111ll1lll111l1lIl1l1: Set["Session"] = field(init=False, default_factory=set)
    ll1ll1l11l111l1lIl1l1: Tuple[int, ...] = field(init=False)

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l11l1lll11111111Il1l1, 'sqlalchemy')):
            lll111l1l11111l1Il1l1.ll11l1ll1llllll1Il1l1(l11l1lll11111111Il1l1)

        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l11l1lll11111111Il1l1, 'sqlalchemy.engine.base')):
            lll111l1l11111l1Il1l1.l11llll1llll1l1lIl1l1(l11l1lll11111111Il1l1)

    def ll11l1ll1llllll1Il1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: Any) -> None:
        ll111111ll1llll1Il1l1 = Path(l11l1lll11111111Il1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', ll111111ll1llll1Il1l1)[0]

        l111l11ll111l1l1Il1l1 = [int(ll11l1lll111l1l1Il1l1) for ll11l1lll111l1l1Il1l1 in __version__.split('.')]
        lll111l1l11111l1Il1l1.ll1ll1l11l111l1lIl1l1 = tuple(l111l11ll111l1l1Il1l1)

    def ll11l1l1lll1ll11Il1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional["lll1111111ll1l11Il1l1"]:
        ll111l11ll111lllIl1l1 = lll1l1l1111ll1l1Il1l1(ll11lllll1llll1lIl1l1=ll11lllll1llll1lIl1l1, l1ll1ll1lll1l111Il1l1=lll111l1l11111l1Il1l1)
        ll111l11ll111lllIl1l1.l111111l11ll111lIl1l1()
        return ll111l11ll111lllIl1l1

    def l11llll1llll1l1lIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: Any) -> None:
        l1l1111ll1l1l1l1Il1l1 = locals().copy()

        l1l1111ll1l1l1l1Il1l1.update({'original': l11l1lll11111111Il1l1.Engine.__init__, 'reloader_code': l111ll11ll1lll1lIl1l1, 'engines': lll111l1l11111l1Il1l1.ll111l1l1lll1111Il1l1})





        l111ll11ll11l11lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        lll1lll11l1l1l1lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (lll111l1l11111l1Il1l1.ll1ll1l11l111l1lIl1l1 <= (1, 3, 24, )):
            exec(l111ll11ll11l11lIl1l1, {**globals(), **l1l1111ll1l1l1l1Il1l1}, l1l1111ll1l1l1l1Il1l1)
        else:
            exec(lll1lll11l1l1l1lIl1l1, {**globals(), **l1l1111ll1l1l1l1Il1l1}, l1l1111ll1l1l1l1Il1l1)

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(l11l1lll11111111Il1l1.Engine, '__init__', l1l1111ll1l1l1l1Il1l1['patched'])
