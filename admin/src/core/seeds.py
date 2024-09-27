from src.core import auth
from src.core import board
def run():

    #ROLES
    system_admin = auth.create_role(name="system_admin")
    administracion = auth.create_role(name="administracion")
    voluntario = auth.create_role(name="voluntario")
    tecnica = auth.create_role(name="tecnica")
    ecuestre = auth.create_role(name="ecuestre")

    #Administración: index, show, update, create, destroy. (PERMISIONS)
    index = auth.create_permission(name="index")
    show = auth.create_permission(name="show")
    update = auth.create_permission(name="update")
    create = auth.create_permission(name="create")
    destroy = auth.create_permission(name="destroy")

    #ROLE_PERMISSIONS


    #USUARIOS
    admin = auth.create_user(email="admin@admin.com", password="admin", role_id=1, alias="admin")
    luca = auth.create_user(email="luca@mail.com", password="123456", role_id=1, alias="Luca")
    
    #EMPLEADOS
    luca = auth.create_employee(nombre="Luca", apellido="Perez", dni="12345679", email="luca1@gmail.com", fecha_inicio="2021-01-01",  activo=True)  

    #PAGOS
    pago1 = board.create_payment(monto=1000, beneficiario_id=1, tipo_pago="Honorarios", descripcion="Pago de honorarios")

    print("Seed ejecutado correctamente")
    
