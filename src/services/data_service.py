from typing import List

from src.data.cages import Cage
from src.data.owners import Owner
from src.infrastructure import state
from src.infrastructure.state import active_account


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects().filter(email=email).first()
    return owner


def register_cage(account: Owner, name: str, meters: float, carpeted: bool, has_toys: bool, allow_dangerous: bool, price: float) -> Cage:
    cage = Cage()

    cage.name = name
    cage.price = price
    cage.square_meters = meters
    cage.has_toys = has_toys
    cage.is_carpeted = carpeted
    cage.allow_dangerous_snakes = allow_dangerous

    cage.save()

    account = find_account_by_email(account.email)
    account.cage_ids.append(cage.id)
    account.save()

    return cage

def get_cages_for_user(account) -> List[Cage]:
    query = Cage.objects(id__in=account.cage_ids) # query the Cage objects that have an id in cages id
    return list(query)