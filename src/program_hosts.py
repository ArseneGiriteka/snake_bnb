from colorama import Fore
from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc
from src.data.owners import Owner
from src.infrastructure.state import active_account
from src.services.data_service import find_account_by_email


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('Login to your [a]ccount')
    print('[L]ist your cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')
    # TODO: Get name & email
    name = input('What is your name?')
    email = input('What is your email?').strip().lower()

    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with email {email} already exist")
        return

    # TODO: Create account, set as logged in.
    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    # TODO: Get email
    email = input('What is your email?').strip().lower()

    # TODO: Find account in DB, set as logged in.
    account = find_account_by_email(email)

    if not account:
        error_msg(f"Error: account with {email} does not exist")
        return

    state.active_account = account
    success_msg(f"Success: you are logged as {state.active_account.name}")


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')

    # TODO: Require an account
    if not state.active_account:
        error_msg(f"you must login first to register a cage")
        return

    # TODO: Get info about cage
    meters = input('how many square meters is the cage? ')
    if not meters:
        error_msg("Cancelled")
        return

    meters = float(meters)
    price = float(input('What is your budget ? '))
    carpeted = input('Is it carpeted [Y, n]? ').strip().lower().startswith('y')
    has_toys = input('Have snake toys [y, n]? ').strip().lower().startswith('y')
    allow_dangerous = input('Can you host venomous snakes [Y, n]? ').strip().lower().startswith('y')
    name = input('Give your cage a name: ').strip()
    # TODO: Save cage to DB.

    cage = svc.register_cage(active_account ,name, meters, carpeted, has_toys, allow_dangerous,)
    state.reload_account()
    success_msg(f"Success: You've successfully registered the cage with id: {cage.id}")

    print(" -------- NOT IMPLEMENTED -------- ")


def list_cages(supress_header=False):
    if not state.active_account:
        error_msg(f"you must login first to register a cage")
        return

    if not supress_header:
        print(' ******************     Your cages     **************** ')

    # TODO: Require an account
    # TODO: Get cages, list details

    print(" -------- NOT IMPLEMENTED -------- ")


def update_availability():
    print(' ****************** Add available date **************** ')

    # TODO: Require an account
    # TODO: list cages
    # TODO: Choose cage
    # TODO: Set dates, save to DB.

    print(" -------- NOT IMPLEMENTED -------- ")


def view_bookings():
    print(' ****************** Your bookings **************** ')

    # TODO: Require an account
    # TODO: Get cages, and nested bookings as flat list
    # TODO: Print details for each

    print(" -------- NOT IMPLEMENTED -------- ")


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
