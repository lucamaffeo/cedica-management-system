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
    luca = auth.create_employee(name="Luca", surname="Perez", dni="12345679", email="luca1@gmail.com", start_date="2021-01-01",  active=True)  


    #PAGOS
    pago1 = board.create_payment(amount=1000, beneficiary_id=1, payment_type="Honorarios", description="Pago de honorarios")

    #JINETES/AMAZONAS
    jinete1 = board.create_jineteAmazona(nombre="Juan", apellido="Perez", dni=51321513, edad=25, fecha_nacimiento="1996-01-01", lugar_nacimiento="CABA", domicilio="Av. Siempre Viva 123", telefono="123456789", contacto_emergencia="Maria", tel_contacto="123456789", becado=False, porcentaje_beca=0, profesionales="Dr. Juan Perez", documentacion={"dni": "url", "certificado_discapacidad": "url"})

    #CABALLOS
    caballo = board.create_horse(nombre="Caballo1", fecha_nacimiento="2010-01-01", sexo="Macho", raza="Criollo", pelaje="Blanco", compra_donacion="Compra", sede_asignada="Sede1", entrenador_id=1, tipo_ja_asignados="Hipoterapia", documentacion={"certificado_veterinario": "url"})

    #RECIBOS
    recibo = board.create_receipt(ja_id=1, monto=1000, medio_pago="Efectivo", empleado_id=1, observaciones="Sin observaciones") 

    print("Seed ejecutado correctamente")
    
