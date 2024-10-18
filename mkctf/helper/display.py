"""Display helper
"""

from re import compile as re_compile

from rich.box import ROUNDED
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text

from ..api import ChallengeAPI
from .subprocess import CalledProcessResult, CalledProcessState

_CONSOLE = Console()
_ANSI_ESC_SEQ_PATTERN = re_compile(rb'\x1b[^m]+m')
_RETURNSTATE_COLOR_MAP = {
    CalledProcessState.SUCCESS: 'green',
    CalledProcessState.NOT_APPLICABLE: 'green',
    CalledProcessState.MANUAL: 'yellow',
    CalledProcessState.NOT_IMPLEMENTED: 'magenta',
    CalledProcessState.FAILURE: 'red',
    CalledProcessState.TIMEOUT: 'red',
    CalledProcessState.EXCEPTION: 'magenta',
}


def _strip_ansi_escape_sequences(data: bytes):
    return _ANSI_ESC_SEQ_PATTERN.sub(b'', data)


def display(item):
    _CONSOLE.print(item)


def display_cpr(slug: str, cpr: CalledProcessResult):
    """Display CalledProcessResult instance"""
    returnstate = cpr.returnstate
    color = _RETURNSTATE_COLOR_MAP[returnstate]
    table = Table(
        'Field',
        'Data',
        box=ROUNDED,
        title=f"{slug} [{returnstate.name}]",
        style=Style(color=color),
        title_style=Style(color=color, bold=True),
        expand=True,
        show_lines=True,
        show_header=False,
    )
    if returnstate == CalledProcessState.EXCEPTION:
        table.add_row(Text('EXCEPTION', style='magenta'), cpr.exception)
    if returnstate != CalledProcessState.SUCCESS:
        stdout = _strip_ansi_escape_sequences(cpr.stdout)
        stderr = _strip_ansi_escape_sequences(cpr.stderr)
        table.add_row(Text('STDOUT', style='blue'), stdout.decode().strip())
        table.add_row(Text('STDERR', style='red'), stderr.decode().strip())
    display(table)


def display_challenge_api(
    challenge_api: ChallengeAPI, summarize: bool = False
):
    """Display ChallengeAPI instance"""
    color = 'green' if challenge_api.config.enabled else 'red'
    if summarize:
        slug = challenge_api.config.slug
        category = challenge_api.config.category
        display(Text(f'[{category:12s}] {slug}', style=color))
        return
    table = Table(
        'Field',
        'Data',
        box=ROUNDED,
        title=challenge_api.config.slug,
        style=Style(color=color),
        title_style=Style(color=color, bold=True),
        expand=True,
        show_lines=True,
        show_header=False,
    )
    config = challenge_api.config.to_dict()
    config.pop('slug')
    config.pop('enabled')
    for field, data in config.items():
        table.add_row(field, str(data))
    table.add_row('description', challenge_api.description)
    display(table)
