#!/usr/bin/env python3
import asyncio
import os.path
import platform
import shlex
import sys

from dotenv import load_dotenv
from nicegui import ui

class InputValues:
    def __init__(self):
        self.buy_ticker = ""
        self.buy_quantity = ""
        self.sell_ticker = ""
        self.sell_quantity = ""

# Initialize .env file
load_dotenv()
   
    

async def find_brokers():
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
    result.content = 'Loading...'
    spinner.set_visibility(True)
    print(command)
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
        result.content = f'```\n{output}\n```'""
    spinner.set_visibility(False)
    return output

async def create_broker_table(command: str):
    output = await run_command(command)
    print(output)

# Enhanced label with styling and an icon
with ui.row().style('height: 5vh; align-items: center; justify-content: center;'):
    ui.icon('swap_horiz', color='green', size='lg')
    ui.label('AutoRSA').style('font-size: 24px; font-weight: bold; color: blue;')

brokers =  asyncio.run(find_brokers())

if brokers is not None:
    input_values = InputValues()
    with ui.column():
        toggle1 = ui.toggle(brokers, value=brokers[0])
        with ui.row():
            toggle2 = ui.toggle(['Holdings', "Stock Buy", "Stock Sell"], value="Holdings")
        with ui.row().bind_visibility_from(toggle2, 'value', value="Holdings"):
            ui.button('Run Holdings', on_click=lambda: run_command(f'python3 autoRSA.py {toggle2.value} {toggle1.value} false')).props('no-caps')
        with ui.row().bind_visibility_from(toggle2, 'value', value="Stock Buy"):
            ui.input(label='Ticker', placeholder='Enter Ticker', on_change=lambda e: setattr(input_values, "buy_ticker", e.value))
            ui.input(label='Quantity', placeholder='Enter Quantity', on_change=lambda e: setattr(input_values, "buy_quantity", e.value))
        with ui.row().bind_visibility_from(toggle2, 'value', value="Stock Sell"):
            ui.input(label='Ticker', placeholder='Enter Ticker', on_change=lambda e: setattr(input_values, "sell_ticker", e.value))
            ui.input(label='Quantity', placeholder='Enter Quantity', on_change=lambda e: setattr(input_values, "sell_quantity", e.value))
        
        with ui.row().bind_visibility_from(toggle2, 'value', value="Stock Buy"):
            ui.button("Run Dry Stock Buy", on_click=lambda: run_command(f'python3 autoRSA.py buy {input_values.buy_quantity} {input_values.buy_ticker} {toggle1.value} true')).props('no-caps')
            ui.button("Run Stock Buy", on_click=lambda: run_command(f'python3 autoRSA.py buy {input_values.buy_quantity} {input_values.buy_ticker} {toggle1.value} false')).props('no-caps')
    
        with ui.row().bind_visibility_from(toggle2, 'value', value="Stock Sell"):
            ui.button("Run Dry Stock Sell", on_click=lambda: run_command(f'python3 autoRSA.py sell {input_values.sell_quantity} {input_values.sell_ticker} {toggle1.value} true')).props('no-caps')
            ui.button("Run Stock Sell", on_click=lambda: run_command(f'python3 autoRSA.py sell {input_values.sell_quantity} {input_values.sell_ticker} {toggle1.value} false')).props('no-caps')
    
with ui.card(), ui.row():
    result, spinner = ui.markdown(), ui.spinner(size="lg")
    spinner.set_visibility(False)

# NOTE: On Windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(reload=platform.system() != 'Windows')