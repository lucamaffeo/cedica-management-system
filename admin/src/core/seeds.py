import io
from src.core.repositories import user, employee, role, permission, horse, assignment, tutor, day, document, receipt, payment, riders
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
    
    #Receipt: index, show, update, create, destroy
    receipt_index = permission.create_permission(name="receipt_index")
    receipt_show = permission.create_permission(name="receipt_show")
    receipt_update = permission.create_permission(name="receipt_update")
    receipt_create = permission.create_permission(name="receipt_create")
    receipt_destroy = permission.create_permission(name="receipt_destroy")


    # Roles
    _ = role.create_role(name="system_admin", permissions=[user_index, user_show, user_update, user_create, user_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy,employee_create, employee_destroy, employee_index, employee_show, employee_update, receipt_index, receipt_show, receipt_update, receipt_create, receipt_destroy, horse_create, horse_destroy, horse_index, horse_show, horse_update, rider_show, rider_index, rider_update, rider_destroy, rider_create])
    _ = role.create_role(name="administracion", permissions=[receipt_index, receipt_show, receipt_update, receipt_create, receipt_destroy , payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy, employee_index, employee_show, employee_update, horse_index, horse_show, rider_show, rider_index, rider_update, rider_destroy, rider_create])
    _ = role.create_role(name="tecnica",permissions=[horse_index, horse_show, receipt_index, receipt_show, rider_index, rider_create, rider_destroy, rider_show, rider_update])
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

    #USUARIOS
    admin = user.create_user(email="admin@admin.com", password="admin", role_id=1, alias="admin")
    luca = user.create_user(email="rol2@mail.com", password="123456", role_id=2, alias="Luca")

    tres = user.create_user(email="rol3@mail.com", password="123456", role_id=3, alias="1")
    cuatro = user.create_user(email="rol4@mail.com", password="123456", role_id=4, alias="2")
    cinco = user.create_user(email="rol5@mail.com", password="123456", role_id=5, alias="3")

    _ = user.create_user(email="test@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="test2@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="tes@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="te@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="t@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="testaa@mail.com", password="123456", role_id=5, alias="3")
    _ = user.create_user(email="testa@mail.com", password="123456", role_id=5, alias="3")

    #EMPLEADOS
    luca2 = employee.create_employee(name="adf", surname="dah", dni="150", email="laa0@gmail.com", start_date="2021-01-01",  active=True, job_position = "Entrenador de Caballos")
    profesor = employee.create_employee(name="Carlos", surname="Gomez", dni="12345678", email="carlos@gmail.com", start_date="2021-01-01", active=True, job_position="Profesor", address="Calle Falsa 123", city="Ciudad", telephone="123456789", profession="Psicólogo/a", emergency_contact_info="Maria Gomez - 123456789", social_work="OSDE", associate_number="123456", condition="Personal Rentado", documentation={"doc1": "value1"})
    terapeuta = employee.create_employee(name="Ana", surname="Lopez", dni="87654321", email="ana@gmail.com", start_date="2021-02-01", active=True, job_position="Terapeuta", address="Calle Verdadera 456", city="Ciudad", telephone="987654321", profession="Médico/a", emergency_contact_info="Juan Lopez - 987654321", social_work="Swiss Medical", associate_number="654321", condition="Personal Rentado", documentation={"doc2": "value2"})
    conductor = employee.create_employee(name="Luis", surname="Martinez", dni="11223344", email="luis@gmail.com", start_date="2021-03-01", active=True, job_position="Conductor", address="Avenida Siempre Viva 789", city="Ciudad", telephone="1122334455", profession="Psicomotricista", emergency_contact_info="Pedro Martinez - 1122334455", social_work="Galeno", associate_number="112233", condition="Voluntario", documentation={"doc3": "value3"})
    auxiliar_pista = employee.create_employee(name="Pedro", surname="Fernandez", dni="55667788", email="pedro@gmail.com", start_date="2021-04-01", active=True, job_position="Auxiliar de pista", address="Calle Real 101", city="Ciudad", telephone="5566778899", profession="Docente", emergency_contact_info="Laura Fernandez - 5566778899", social_work="Medicus", associate_number="556677", condition="Voluntario", documentation={"doc4": "value4"})
    entrenador = employee.create_employee(name="Jorge", surname="Perez", dni="99887766", email="jorge@gmail.com", start_date="2021-05-01", active=True, job_position="Entrenador", address="Calle Principal 202", city="Ciudad", telephone="9988776655", profession="Otro", emergency_contact_info="Sofia Perez - 9988776655", social_work="OSDE", associate_number="998877", condition="Personal Rentado", documentation={"doc5": "value5"})

    #PAGOS
    pago_honorarios = payment.create_payment(amount=2000, beneficiary_id=profesor.id, type="Honorarios", description="Pago de honorarios")
    pago_proveedor = payment.create_payment(amount=1500, beneficiary_id=None, type="Proveedor", description="Pago a proveedor")
    pago_gastos_varios = payment.create_payment(amount=500, beneficiary_id=None, type="Gastos varios", description="Gastos varios")

    #TUTOR
    tutor1 = tutor.create_tutor(name="Maria", surname="Gomez", dni="12345678", email="emailtutor@mail.com", address="Av. Siempre Viva 123", cellphone="123456789", educational_level="Universitario", occupation="Profesora")

    #CABALLOS
    caballo1 = horse.create_horse(name="Caballo1", birth_date="2020-01-01",purchase_donation="Compra",gender = "Macho", assigned_activities_ja="Hipoterapia", association=[entrenador, conductor])

    #JINETES/AMAZONAS
    jinete1 = riders.create_rider(name="Juan", surname="Perez", dni=51321513, age=25, birthdate="1996-01-01", birth_place="CABA", address="Av. Siempre Viva 123", phone="123456789", emergency_contact="Maria", emergency_contact_phone_number="123456789", scholarship=False, scholarship_percentage=0, professionals="Dr. Juan Perez", tutors=[tutor1], disability_certificate=False, diagnosis="ECNE", other="Otro", disability_type="Mental", family_assignment=True, assignments=[assignment1, assignment2], pension="Provincial", health_insurance="OSDE", affiliate_number="123456", guardianship=False, observations="Sin observaciones", school_institution="Escuela 123", institution_address="Av. Siempre Viva 123", grade="Primero", institution_phone="123456789", institution_observations="Sin observaciones", days=[lunes, martes], horse_id=caballo1.id, horse_conductor_id=conductor.id, track_assistant_id=auxiliar_pista.id, therapist_teacher_id=terapeuta.id, work_proposal="Hipoterapia", condition="Regular", headquarters="CASJ")
    jinete2 = riders.create_rider(name="Jose", surname="Lopez", dni=1, age=25, birthdate="1996-01-01", birth_place="CABA", address="Av. Siempre Viva 123", phone="123456789", emergency_contact="Maria", emergency_contact_phone_number="123456789", scholarship=False, scholarship_percentage=0, professionals="Dr. Jose Lopez", tutors=[tutor1], disability_certificate=False, diagnosis="ECNE", other="Otro", disability_type="Mental", family_assignment=True, assignments=[assignment1, assignment2], pension="Provincial", health_insurance="OSDE", affiliate_number="123456", guardianship=False, observations="Sin observaciones", school_institution="Escuela 123", institution_address="Av. Siempre Viva 123", grade="Primero", institution_phone="123456789", institution_observations="Sin observaciones", days=[lunes, martes], horse_id=caballo1.id, horse_conductor_id=conductor.id, track_assistant_id=auxiliar_pista.id, therapist_teacher_id=terapeuta.id, work_proposal="Hipoterapia", condition="Regular", headquarters="CASJ")
    jinete2 = riders.create_rider(name="Pedro", surname="Gonzalez", dni=98765432, age=30, birthdate="1991-01-01", birth_place="CABA", address="Calle Falsa 456", phone="987654321", emergency_contact="Ana", emergency_contact_phone_number="987654321", scholarship=False, scholarship_percentage=0, professionals="Dr. Pedro Gonzalez", tutors=[], disability_certificate=False, diagnosis="ECNE", other="Otro", disability_type="Mental", family_assignment=True, assignments=[assignment1, assignment2], pension="Provincial", health_insurance="OSDE", affiliate_number="654321", guardianship=False, observations="Sin observaciones", school_institution="Escuela 456", institution_address="Calle Falsa 456", grade="Segundo", institution_phone="987654321", institution_observations="Sin observaciones", days=[lunes, martes], horse_id=caballo1.id, horse_conductor_id=conductor.id, track_assistant_id=auxiliar_pista.id, therapist_teacher_id=terapeuta.id, work_proposal="Hipoterapia", condition="Regular", headquarters="CASJ")

    #RECIBOS
    recibo = receipt.create_receipt(ja_id=1, quantity=1000, payment_method="Efectivo", employee_id=profesor.id, remarks="Sin observaciones")

    #DOCUMENTOS

    print("Seed ejecutado correctamente")
