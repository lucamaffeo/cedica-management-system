from src.core.repositories import user, employee, role, permission, horse
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

    #Horses: index, show, update, create, destroy
    horse_index = permission.create_permission(name="horse_index")
    horse_show = permission.create_permission(name="horse_show")
    horse_update = permission.create_permission(name="horse_update")
    horse_create = permission.create_permission(name="horse_create")
    horse_destroy = permission.create_permission(name="horse_destroy")

    #Receipt: index, show, update, create, destroy
    receipt_index = permission.create_permission(name="receipt_index")
    receipt_show = permission.create_permission(name="receipt_show")
    receipt_update = permission.create_permission(name="receipt_update")
    receipt_create = permission.create_permission(name="receipt_create")
    receipt_destroy = permission.create_permission(name="receipt_destroy")


    # Roles
    _ = role.create_role(name="system_admin", permissions=[user_index, user_show, user_update, user_create, user_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy,employee_create, employee_destroy, employee_index, employee_show, employee_update, receipt_index, receipt_show, receipt_update, receipt_create, receipt_destroy, horse_create, horse_destroy, horse_index, horse_show, horse_update], id=1)
    _ = role.create_role(name="administracion", permissions=[receipt_index, receipt_show, receipt_update, receipt_create, receipt_destroy , payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy, employee_index, employee_show, employee_update, horse_index, horse_show], id=2)
    _ = role.create_role(name="tecnica",permissions=[horse_index, horse_show, receipt_index, receipt_show], id=3)
    _ = role.create_role(name="voluntariado", id=4)
    _ = role.create_role(name="ecuestre", permissions=[horse_index, horse_show, horse_update, horse_create, horse_destroy], id=5)


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
    luca = employee.create_employee(name="Luca", surname="Perez", dni="12345679", email="luca1@gmail.com", start_date="2021-01-01",  active=True, job_position = "Conductor")
    luca2 = employee.create_employee(name="adf", surname="dah", dni="150", email="laa0@gmail.com", start_date="2021-01-01",  active=True, job_position = "Entrenador de Caballos")  
    

    #PAGOS
    pago1 = models.create_payment(amount=1000, beneficiary_id=1, type="Honorarios", description="Pago de honorarios")

    #JINETES/AMAZONAS
    jinete1 = models.create_rider(nombre="Juan", apellido="Perez", dni=51321513, edad=25, fecha_nacimiento="1996-01-01", lugar_nacimiento="CABA", domicilio="Av. Siempre Viva 123", telefono="123456789", contacto_emergencia="Maria", tel_contacto="123456789", becado=False, porcentaje_beca=0, profesionales="Dr. Juan Perez", documentacion={"dni": "url", "certificado_discapacidad": "url"})

    #CABALLOS
    caballo1 = horse.create_horse(name="Caballo1", birth_date="2020-01-01",purchase_donation="Compra",gender = "Macho", assigned_activities_ja="Hipoterapia")
    #RECIBOS
    recibo = models.create_receipt(ja_id=jinete1.id, monto=1000, medio_pago="Efectivo", empleado_id=luca.id, observaciones="Sin observaciones") 

    print("Seed ejecutado correctamente")
