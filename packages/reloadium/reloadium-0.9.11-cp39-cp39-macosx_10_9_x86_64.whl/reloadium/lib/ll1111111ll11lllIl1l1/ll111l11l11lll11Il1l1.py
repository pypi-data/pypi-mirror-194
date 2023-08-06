from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.llll1ll11l1ll111Il1l1 import l111ll11ll1lll1lIl1l1
from reloadium.lib.ll1111111ll11lllIl1l1.l1ll1ll1lll1l111Il1l1 import l11l1111lllllll1Il1l1, llll111l111ll1llIl1l1
from reloadium.lib.ll1111111ll11lllIl1l1.ll11lll11ll11l1lIl1l1 import ll111ll1l111l1l1Il1l1
from reloadium.corium.ll1lll1l1ll11111Il1l1 import l11l1111llll1lllIl1l1, l1l11l1l111lll11Il1l1, l11l1l11l1111ll1Il1l1, ll111111l11l1l11Il1l1, ll1l1l1lllll11l1Il1l1
from reloadium.corium.ll11ll11111ll111Il1l1 import lll1111111ll1l11Il1l1, lll111l1lll11111Il1l1
from reloadium.corium.l1l1l11ll1ll11llIl1l1 import ll1l1l11ll11l1llIl1l1
from reloadium.corium.ll1ll1l1l1lllll1Il1l1 import l1l1l1l11lllllllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from django.db import transaction
    from django.db.transaction import Atomic
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass(**ll1l1l1lllll11l1Il1l1)
class l1ll11llll1ll1l1Il1l1(ll111111l11l1l11Il1l1):
    l1ll1111l11ll1l1Il1l1 = 'Field'

    @classmethod
    def l1l1ll1l111lll11Il1l1(l1ll1lll1111111lIl1l1, l111l111l111llllIl1l1: ll1l1l11ll11l1llIl1l1.l111l1ll111l1lllIl1l1, l111lll1ll1l1111Il1l1: Any, l11ll1111llll1l1Il1l1: l1l11l1l111lll11Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(l111lll1ll1l1111Il1l1, 'field') and isinstance(l111lll1ll1l1111Il1l1.field, Field))):
            return True

        return False

    def l111l1l11111lll1Il1l1(lll111l1l11111l1Il1l1, ll111l111lll1111Il1l1: l11l1l11l1111ll1Il1l1) -> bool:
        return True

    @classmethod
    def ll1111l1llllll11Il1l1(l1ll1lll1111111lIl1l1) -> int:
        return 200


@dataclass(repr=False)
class lll1l1l1111ll1l1Il1l1(l11l1111lllllll1Il1l1):
    lll1111l1111ll1lIl1l1: "Atomic" = field(init=False)

    lllll1l1l1111l1lIl1l1: bool = field(init=False, default=False)

    def l111111l11ll111lIl1l1(lll111l1l11111l1Il1l1) -> None:
        super().l111111l11ll111lIl1l1()
        from django.db import transaction

        lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1 = transaction.atomic()
        lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__enter__()

    def ll1lll1l1ll1l1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        super().ll1lll1l1ll1l1l1Il1l1()
        if (lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1):
            return 

        lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__exit__(None, None, None)

    def llll111llll11ll1Il1l1(lll111l1l11111l1Il1l1) -> None:
        super().llll111llll11ll1Il1l1()

        if (lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1):
            return 

        lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1 = True
        lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__exit__(None, None, None)

    def __repr__(lll111l1l11111l1Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class ll1l11l1ll1l1l1lIl1l1(llll111l111ll1llIl1l1):
    lll1111l1111ll1lIl1l1: "Atomic" = field(init=False)

    lllll1l1l1111l1lIl1l1: bool = field(init=False, default=False)

    async def l111111l11ll111lIl1l1(lll111l1l11111l1Il1l1) -> None:
        await super().l111111l11ll111lIl1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1 = transaction.atomic()
        await sync_to_async(lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__enter__)()

    async def ll1lll1l1ll1l1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll1lll1l1ll1l1l1Il1l1()
        if (lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1):
            return 

        lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1 = True
        from django.db import transaction

        def llllllllllll11l1Il1l1() -> None:
            transaction.set_rollback(True)
            lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__exit__(None, None, None)
        await sync_to_async(llllllllllll11l1Il1l1)()

    async def llll111llll11ll1Il1l1(lll111l1l11111l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().llll111llll11ll1Il1l1()

        if (lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1):
            return 

        lll111l1l11111l1Il1l1.lllll1l1l1111l1lIl1l1 = True
        await sync_to_async(lll111l1l11111l1Il1l1.lll1111l1111ll1lIl1l1.__exit__)(None, None, None)

    def __repr__(lll111l1l11111l1Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class ll11l1l1ll111lllIl1l1(ll111ll1l111l1l1Il1l1):
    ll11lllll1llll1lIl1l1 = 'Django'

    l1ll111l1111ll11Il1l1: Optional[int] = field(init=False)
    l1ll11l1111ll11lIl1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    def __post_init__(lll111l1l11111l1Il1l1) -> None:
        super().__post_init__()
        lll111l1l11111l1Il1l1.l1ll111l1111ll11Il1l1 = None

    def l11ll1l1l111llllIl1l1(lll111l1l11111l1Il1l1) -> List[Type[l11l1l11l1111ll1Il1l1]]:
        return [l1ll11llll1ll1l1Il1l1]

    def llll1l11l1lll1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        super().llll1l11l1lll1l1Il1l1()
        sys.argv.append('--noreload')

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l11l1lll11111111Il1l1, 'django.core.management.commands.runserver')):
            lll111l1l11111l1Il1l1.llll1111l1ll11l1Il1l1()
            lll111l1l11111l1Il1l1.l1ll111l1l1l1ll1Il1l1()

    def ll11l1l1lll1ll11Il1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional["lll1111111ll1l11Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        ll111l11ll111lllIl1l1 = lll1l1l1111ll1l1Il1l1(ll11lllll1llll1lIl1l1=ll11lllll1llll1lIl1l1, l1ll1ll1lll1l111Il1l1=lll111l1l11111l1Il1l1)
        ll111l11ll111lllIl1l1.l111111l11ll111lIl1l1()
        return ll111l11ll111lllIl1l1

    async def l1l1ll11llll1lllIl1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional["lll111l1lll11111Il1l1"]:
        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        ll111l11ll111lllIl1l1 = ll1l11l1ll1l1l1lIl1l1(ll11lllll1llll1lIl1l1=ll11lllll1llll1lIl1l1, l1ll1ll1lll1l111Il1l1=lll111l1l11111l1Il1l1)
        await ll111l11ll111lllIl1l1.l111111l11ll111lIl1l1()
        return ll111l11ll111lllIl1l1

    def llll1111l1ll11l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l11l1l1llll1llllIl1l1 = django.core.management.commands.runserver.Command.handle

        def llll11l11l11ll1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **llllll1lll11l11lIl1l1: Any) -> Any:
            with l111ll11ll1lll1lIl1l1():
                lll111ll1l11l1l1Il1l1 = llllll1lll11l11lIl1l1.get('addrport')
                if ( not lll111ll1l11l1l1Il1l1):
                    lll111ll1l11l1l1Il1l1 = django.core.management.commands.runserver.Command.default_port

                lll111ll1l11l1l1Il1l1 = lll111ll1l11l1l1Il1l1.split(':')[ - 1]
                lll111ll1l11l1l1Il1l1 = int(lll111ll1l11l1l1Il1l1)
                lll111l1l11111l1Il1l1.l1ll111l1111ll11Il1l1 = lll111ll1l11l1l1Il1l1

            return l11l1l1llll1llllIl1l1(*l1lll111l1l1l1llIl1l1, **llllll1lll11l11lIl1l1)

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(django.core.management.commands.runserver.Command, 'handle', llll11l11l11ll1lIl1l1)

    def l1ll111l1l1l1ll1Il1l1(lll111l1l11111l1Il1l1) -> None:
        import django.core.management.commands.runserver

        l11l1l1llll1llllIl1l1 = django.core.management.commands.runserver.Command.get_handler

        def llll11l11l11ll1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **llllll1lll11l11lIl1l1: Any) -> Any:
            with l111ll11ll1lll1lIl1l1():
                assert lll111l1l11111l1Il1l1.l1ll111l1111ll11Il1l1
                lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1 = lll111l1l11111l1Il1l1.lll111lll11l1l11Il1l1(lll111l1l11111l1Il1l1.l1ll111l1111ll11Il1l1)
                if (env.page_reload_on_start):
                    lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.llll11l11l1l1l1lIl1l1(2.0)

            return l11l1l1llll1llllIl1l1(*l1lll111l1l1l1llIl1l1, **llllll1lll11l11lIl1l1)

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(django.core.management.commands.runserver.Command, 'get_handler', llll11l11l11ll1lIl1l1)

    def lll1lll1llllllllIl1l1(lll111l1l11111l1Il1l1) -> None:
        super().lll1lll1llllllllIl1l1()

        import django.core.handlers.base

        l11l1l1llll1llllIl1l1 = django.core.handlers.base.BaseHandler.get_response

        def llll11l11l11ll1lIl1l1(l11ll1l11l111111Il1l1: Any, l1ll11l1ll11l1l1Il1l1: Any) -> Any:
            l111ll1llll11l1lIl1l1 = l11l1l1llll1llllIl1l1(l11ll1l11l111111Il1l1, l1ll11l1ll11l1l1Il1l1)

            if ( not lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1):
                return l111ll1llll11l1lIl1l1

            l111lll11l11ll11Il1l1 = l111ll1llll11l1lIl1l1.get('content-type')

            if (( not l111lll11l11ll11Il1l1 or 'text/html' not in l111lll11l11ll11Il1l1)):
                return l111ll1llll11l1lIl1l1

            ll111111ll1llll1Il1l1 = l111ll1llll11l1lIl1l1.content

            if (isinstance(ll111111ll1llll1Il1l1, bytes)):
                ll111111ll1llll1Il1l1 = ll111111ll1llll1Il1l1.decode('utf-8')

            l1ll1llll11l1l11Il1l1 = lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.ll111l111ll1111lIl1l1(ll111111ll1llll1Il1l1)

            l111ll1llll11l1lIl1l1.content = l1ll1llll11l1l11Il1l1.encode('utf-8')
            l111ll1llll11l1lIl1l1['content-length'] = str(len(l111ll1llll11l1lIl1l1.content)).encode('ascii')
            return l111ll1llll11l1lIl1l1

        django.core.handlers.base.BaseHandler.get_response = llll11l11l11ll1lIl1l1  # type: ignore

    def ll11ll1l111l111lIl1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path) -> None:
        super().ll11ll1l111l111lIl1l1(llll1lll1llll111Il1l1)

        from django.apps.registry import Apps

        lll111l1l11111l1Il1l1.l1ll11l1111ll11lIl1l1 = Apps.register_model

        def l11ll1llll1ll111Il1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            pass

        Apps.register_model = l11ll1llll1ll111Il1l1

    def llll111ll11lll11Il1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path, l11lll111ll1l1l1Il1l1: List[l11l1111llll1lllIl1l1]) -> None:
        super().llll111ll11lll11Il1l1(llll1lll1llll111Il1l1, l11lll111ll1l1l1Il1l1)

        if ( not lll111l1l11111l1Il1l1.l1ll11l1111ll11lIl1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = lll111l1l11111l1Il1l1.l1ll11l1111ll11lIl1l1
