from src.core.repositories import user, employee, role, permission, horse, assignment, tutor, day, action, document
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
    
    #Riders: index, show, update, create, destroy
    rider_index = permission.create_permission(name="rider_index")
    rider_show = permission.create_permission(name="rider_show")
    rider_update = permission.create_permission(name="rider_update")
    rider_create = permission.create_permission(name="rider_create")
    rider_destroy = permission.create_permission(name="rider_destroy")

    # Roles
    _ = role.create_role(name="system_admin", permissions=[user_index, user_show, user_update, user_create, user_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy,employee_create, employee_destroy, employee_index, employee_show, employee_update, horse_create, horse_destroy, horse_index, horse_show, horse_update, rider_show, rider_index, rider_update, rider_destroy, rider_create])
    _ = role.create_role(name="administracion", permissions=[payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy, employee_index, employee_show, employee_update, horse_index, horse_show, rider_show, rider_index, rider_update, rider_destroy, rider_create])
    _ = role.create_role(name="tecnica",permissions=[horse_index, horse_show, rider_index, rider_create, rider_destroy, rider_show, rider_update])
    _ = role.create_role(name="voluntariado")
    _ = role.create_role(name="ecuestre", permissions=[horse_index, horse_show, horse_update, horse_create, horse_destroy, rider_index, rider_show])

    # Asignaciones
    assignment1 = assignment.create_assignment(name="Asignación Universal por hijo")
    assignment2 = assignment.create_assignment(name="Asignación Universal por hijo con Discapacidad")
    assignment3 = assignment.create_assignment(name="Asignación por ayuda escolar anual")

    # Días
    lunes = day.create_day(name="Lunes")
    martes = day.create_day(name="Martes")
    miercoles = day.create_day(name="Miercoles")
    jueves = day.create_day(name="Jueves")
    viernes = day.create_day(name="Viernes")
    sabado = day.create_day(name="Sabado")
    domingo = day.create_day(name="Domingo")

    # Acciones
    editar = action.create_action(name="Editar")
    eliminar = action.create_action(name="Eliminar")
    descargar = action.create_action(name="Descargar")
    ir_al_documento = action.create_action(name="Ir al documento")

    #USUARIOS
    admin = user.create_user(email="admin@admin.com", password="admin", role_id=1, alias="admin")
    luca = user.create_user(email="luca@mail.com", password="123456", role_id=2, alias="Luca")


    _ = user.create_user(email="1@mail.com", password="123456", role_id=2, alias="1")
    _ = user.create_user(email="2@mail.com", password="123456", role_id=2, alias="2")
    _ = user.create_user(email="3@mail.com", password="123456", role_id=3, alias="3")
    _ = user.create_user(email="4@mail.com", password="123456", role_id=4, alias="4")
    _ = user.create_user(email="5@mail.com", password="123456", role_id=5, alias="5")
    _ = user.create_user(email="6@mail.com", password="123456", role_id=5, alias="6")

    #EMPLEADOS
    luca = employee.create_employee(name="Luca", surname="Perez", dni="12345679", email="luca1@gmail.com", start_date="2021-01-01",  active=True, job_position = "Conductor")  


    #PAGOS
    pago1 = models.create_payment(amount=1000, beneficiary_id=1, type="Honorarios", description="Pago de honorarios")

    #TUTOR
    tutor1 = tutor.create_tutor(name="Maria", surname="Gomez", dni="12345678", email="emailtutor@mail.com", address="Av. Siempre Viva 123", cellphone="123456789", educational_level="Universitario", occupation="Profesora")
    #DOCUMENTOS
    documento1 = document.create_document(file="Documento1", title="Titulo del documento", document_type="Entrevista", actions=[editar, eliminar, descargar])
    #JINETES/AMAZONAS
    jinete1 = models.create_rider(name="Juan", surname="Perez", dni=51321513, age=25, birthdate="1996-01-01", birth_place="CABA", address="Av. Siempre Viva 123", phone="123456789", emergency_contact="Maria", emergency_contact_phone_number="123456789", scholarship=False, scholarship_percentage=0, professionals="Dr. Juan Perez", tutors=[tutor1], documents=[documento1])

    #CABALLOS
    caballo1 = horse.create_horse(name="Caballo1", birth_date="2020-01-01",purchase_donation="Compra",gender = "Macho", trainer_id=luca.id, assigned_activities_ja="Hipoterapia")
    #RECIBOS
    recibo = models.create_receipt(ja_id=1, monto=1000, medio_pago="Efectivo", empleado_id=1, observaciones="Sin observaciones") 



    print("Seed ejecutado correctamente")
    
