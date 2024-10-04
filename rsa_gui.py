#!/usr/bin/env python3
import asyncio
import os.path
import platform
import shlex
import sys

from dotenv import load_dotenv
from nicegui import ui



async def find_brokers():
    load_dotenv()
    brokers = []
    brokers.append("BBAE") if os.getenv("BBAE") else None
    brokers.append("Chase") if os.getenv("CHASE") else None
    brokers.append("DSPAC") if os.getenv("DSPAC") else None
    brokers.append("Fennel") if os.getenv("FENNEL") else None
    brokers.append("Fidelity") if os.getenv("FIDELITY") else None
    brokers.append("Firstrade") if os.getenv("FIRSTRADE") else None
    brokers.append("Public") if os.getenv("PUBLIC_BROKER") else None
    brokers.append("Robinhood") if os.getenv("ROBINHOOD") else None
    brokers.append("Schwab") if os.getenv("SCHWAB") else None
    brokers.append("Sofi") if os.getenv("SOFI") else None
    brokers.append("Tradier") if os.getenv("TRADIER") else None
    brokers.append("Tastytrade") if os.getenv("TASTYTRADE") else None
    brokers.append("Tornado") if os.getenv("TORNADO") else None
    brokers.append("Vanguard") if os.getenv("VANGUARD") else None
    brokers.append("Webull") if os.getenv("WEBULL") else None
    brokers.append("Wellsfargo") if os.getenv("WELLSFARGO") else None
    return brokers

async def run_command(command: str) -> None:
    """Run a command in the background and display the output in the pre-created dialog."""
    dialog.open()
    result.content = ''
    command = command.replace('python3', sys.executable)  # NOTE replace with machine-independent Python path (#1240)
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command, posix='win' not in sys.platform.lower()),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    # NOTE we need to read the output in chunks, otherwise the process will block
    output = ''
    while True:
        new = await process.stdout.read(4096)
        if not new:
            break
        output += new.decode()
        # NOTE the content of the markdown element is replaced every time we have new output
        result.content = f'```\n{output}\n```'

with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

ui.label('AutoRSA')

with ui.expansion('Brokers found:'):
    brokers = asyncio.run(find_brokers())
    for broker in brokers:
        if broker is not None:
            ui.label(broker)
ui.button('python3 autoRSA.py holdings schwab false', on_click=lambda: run_command('python3 autoRSA.py holdings schwab false')).props('no-caps')
ui.button('python3 autoRSA.py', on_click=lambda: run_command('python3 autoRSA.py')).props('no-caps')
with ui.row().classes('items-center'):
    ui.button('python3 autoRSA.py "<message>"', on_click=lambda: run_command(f'python3 autoRSA.py "{message.value}"')) \
        .props('no-caps')
    message = ui.input('message', value='NiceGUI')

# NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(reload=platform.system() != 'Windows')