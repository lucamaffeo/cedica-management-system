from src.core import board
from src.core import auth
def run():
    issue1 = board.create.issue(
        email ="jose@mail.com",
        tittle ="Mi computadora no funciona",
        descripcion ="Mi departamento me compro una nueva "
    )
    issue2 = board.create.issue(
        email ="maria@mail.com",
        tittle ="No puedo obtener mis emails",
        descripcion ="no puedo acceder a mis emails",
        status = "in progress"
    )
    issue3 = board.create.issue(
        email ="ruben@mail.com",
        tittle ="No puedo imprimir",
        descripcion ="no puedo imprimir en la impresora de la oficina",
        status = "done"
    )

Luca = auth.create_user(email="luca@mail.com", password="123456")
Franco = auth.create_user(email="franco@mail.com", password="123456")
Messi = auth.create_user(email="messi@mail.com", password="123456")


board.assign_user(issue1, Luca)
board.assign_user(issue2, Franco)
board.assign_user(issue3, Messi)