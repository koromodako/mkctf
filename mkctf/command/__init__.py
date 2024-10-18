"""mkctf command line interface commands
"""

from .build import setup_build
from .configure import setup_configure
from .create import setup_create
from .delete import setup_delete
from .deploy import setup_deploy
from .disable import setup_disable
from .enable import setup_enable
from .enum import setup_enum
from .export import setup_export
from .healthcheck import setup_healthcheck
from .init import setup_init
from .push import setup_push
from .renew_flag import setup_renew_flag
from .update_meta import setup_update_meta


def setup_commands(subparsers):
    """Setup mkctf command line interface commands"""
    for setup_func in (
        setup_init,
        setup_enum,
        setup_create,
        setup_enable,
        setup_disable,
        setup_renew_flag,
        setup_update_meta,
        setup_configure,
        setup_build,
        setup_deploy,
        setup_healthcheck,
        setup_delete,
        setup_export,
        setup_push,
    ):
        setup_func(subparsers)
