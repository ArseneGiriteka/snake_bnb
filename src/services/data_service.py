from src.data.cages import Cage
from src.data.owners import Owner


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects().filter(email=email).first()
    return owner


def register_cage(active_account: Owner, name: str, meters: float, carpeted: bool, has_toys: bool, allow_dangerous: bool, price: float) -> Cage:
    cage = Cage()

    cage.name = name
    cage.price = price
    cage.square_meters = meters
    cage.has_toys = has_toys
    cage.is_carpeted = carpeted
    cage.allow_dangerous_snakes = allow_dangerous

    cage.save()

    account = find_account_by_email(active_account.email)
    print(f"SUCCESS: You've registered successfully the cage id: {cage.id} !")
    account.cage_ids.append(cage.id)
    return cage