from src.core.repositories import user, employee, role, permission
from src.core import models
def run():

    # Permissions

    #User: index, show, update, create, destroy
    user_index = permission.create_permission(name="user_index")
    user_show = permission.create_permission(name="user_show")
    user_update = permission.create_permission(name="user_update")
    user_create = permission.create_permission(name="user_create")
    user_destroy = permission.create_permission(name="user_destroy")

    #Payment: index, show, update, create, destroy
    payment_index = permission.create_permission(name="payment_index")
    payment_show = permission.create_permission(name="payment_show")
    payment_update = permission.create_permission(name="payment_update")
    payment_create = permission.create_permission(name="payment_create")
    payment_destroy = permission.create_permission(name="payment_destroy")

    #Employees: index, show, update, create, destroy
    employee_index = permission.create_permission(name="employee_index")
    employee_show = permission.create_permission(name="employee_show")
    employee_update = permission.create_permission(name="employee_update")
    employee_create = permission.create_permission(name="employee_create")
    employee_destroy = permission.create_permission(name="employee_destroy")
    
    #Riders: index, show, update, create, destroy
    rider_index = permission.create_permission(name="rider_index")
    rider_show = permission.create_permission(name="rider_show")
    rider_update = permission.create_permission(name="rider_update")
    rider_create = permission.create_permission(name="rider_create")
    rider_destroy = permission.create_permission(name="rider_destroy")

    # Roles
    _ = role.create_role(name="system_admin", permissions=[user_index, user_show, user_update, user_create, user_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy,employee_create, employee_destroy, employee_index, employee_show, employee_update, rider_show, rider_index, rider_update, rider_destroy, rider_create], id=1)
    _ = role.create_role(name="administracion", permissions=[payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy, employee_index, employee_show, employee_update, rider_show, rider_index, rider_update, rider_destroy, rider_create], id=2)
    _ = role.create_role(name="tecnica", permissions=[rider_index, rider_create, rider_destroy, rider_show, rider_update], id=3)
    _ = role.create_role(name="voluntariado", id=4)
    _ = role.create_role(name="ecuestre", permissions=[rider_index, rider_show], id=5)


    #USUARIOS
    admin = user.create_user(email="admin@admin.com", password="admin", role_id=1, alias="admin")
    luca = user.create_user(email="luca@mail.com", password="123456", role_id=2, alias="Luca")


    _ = user.create_user(email="1@mail.com", password="123456", role_id=2, alias="1")
    _ = user.create_user(email="2@mail.com", password="123456", role_id=2, alias="2")
    _ = user.create_user(email="3@mail.com", password="123456", role_id=2, alias="1")
    _ = user.create_user(email="4@mail.com", password="123456", role_id=2, alias="2")
    _ = user.create_user(email="5@mail.com", password="123456", role_id=2, alias="1")
    _ = user.create_user(email="6@mail.com", password="123456", role_id=2, alias="2")

    #EMPLEADOS
    luca = employee.create_employee(name="Luca", surname="Perez", dni="12345679", email="luca1@gmail.com", start_date="2021-01-01",  active=True)  


    #PAGOS
    pago1 = models.create_payment(amount=1000, beneficiary_id=1, type="Honorarios", description="Pago de honorarios")

    #JINETES/AMAZONAS
    jinete1 = models.create_rider(nombre="Juan", apellido="Perez", dni=51321513, edad=25, fecha_nacimiento="1996-01-01", lugar_nacimiento="CABA", domicilio="Av. Siempre Viva 123", telefono="123456789", contacto_emergencia="Maria", tel_contacto="123456789", becado=False, porcentaje_beca=0, profesionales="Dr. Juan Perez", documentacion={"dni": "url", "certificado_discapacidad": "url"})

    #CABALLOS
    caballo = models.create_horse(nombre="Caballo1", fecha_nacimiento="2010-01-01", sexo="Macho", raza="Criollo", pelaje="Blanco", compra_donacion="Compra", sede_asignada="Sede1", entrenador_id=1, tipo_ja_asignados="Hipoterapia", documentacion={"certificado_veterinario": "url"})

    #RECIBOS
    recibo = models.create_receipt(ja_id=1, monto=1000, medio_pago="Efectivo", empleado_id=1, observaciones="Sin observaciones") 

    print("Seed ejecutado correctamente")
    
