from datetime import datetime
import io
from src.core.database import db
from src.core.repositories import user, employee, role, permission, horse, assignment, tutor, day, document, receipt, payment, riders, report, contact, content


def run():

    # Permissions

    # User: index, show, update, create, destroy
    user_index = permission.create_permission(name="user_index")
    user_show = permission.create_permission(name="user_show")
    user_update = permission.create_permission(name="user_update")
    user_create = permission.create_permission(name="user_create")
    user_destroy = permission.create_permission(name="user_destroy")

    # Payment: index, show, update, create, destroy
    payment_index = permission.create_permission(name="payment_index")
    payment_show = permission.create_permission(name="payment_show")
    payment_update = permission.create_permission(name="payment_update")
    payment_create = permission.create_permission(name="payment_create")
    payment_destroy = permission.create_permission(name="payment_destroy")

    # Employees: index, show, update, create, destroy
    employee_index = permission.create_permission(name="employee_index")
    employee_show = permission.create_permission(name="employee_show")
    employee_update = permission.create_permission(name="employee_update")
    employee_create = permission.create_permission(name="employee_create")
    employee_destroy = permission.create_permission(name="employee_destroy")

    # Horses: index, show, update, create, destroy
    horse_index = permission.create_permission(name="horse_index")
    horse_show = permission.create_permission(name="horse_show")
    horse_update = permission.create_permission(name="horse_update")
    horse_create = permission.create_permission(name="horse_create")
    horse_destroy = permission.create_permission(name="horse_destroy")

    # Riders: index, show, update, create, destroy
    rider_index = permission.create_permission(name="rider_index")
    rider_show = permission.create_permission(name="rider_show")
    rider_update = permission.create_permission(name="rider_update")
    rider_create = permission.create_permission(name="rider_create")
    rider_destroy = permission.create_permission(name="rider_destroy")

    # Receipt: index, show, update, create, destroy
    receipt_index = permission.create_permission(name="receipt_index")
    receipt_show = permission.create_permission(name="receipt_show")
    receipt_update = permission.create_permission(name="receipt_update")
    receipt_create = permission.create_permission(name="receipt_create")
    receipt_destroy = permission.create_permission(name="receipt_destroy")

    # Contact: index, show, update, create, destroy
    contact_index = permission.create_permission(name="contact_index")
    contact_show = permission.create_permission(name="contact_show")
    contact_update = permission.create_permission(name="contact_update")
    contact_create = permission.create_permission(name="contact_create")
    contact_destroy = permission.create_permission(name="contact_destroy")

    # Content: index, show, update, create, destroy
    content_index = permission.create_permission(name="content_index")
    content_show = permission.create_permission(name="content_show")
    content_update = permission.create_permission(name="content_update")
    content_create = permission.create_permission(name="content_create")
    content_destroy = permission.create_permission(name="content_destroy")

    # Grafic: index, show
    grafic_index = permission.create_permission(name="grafic_index")
    grafic_show = permission.create_permission(name="grafic_show")

    # Report: index, show
    report_index = permission.create_permission(name="report_index")
    report_show = permission.create_permission(name="report_show")

    # Roles
    _ = role.create_role(name="system_admin", permissions=[grafic_index, grafic_show, report_index, report_show, user_index, user_show, user_update, user_create, user_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy, employee_index, employee_show, employee_update, receipt_index, receipt_show,
                         receipt_update, receipt_create, receipt_destroy, horse_create, horse_destroy, horse_index, horse_show, horse_update, rider_show, rider_index, rider_update, rider_destroy, rider_create, contact_index, contact_show, contact_update, contact_create, contact_destroy, content_index, content_show, content_update, content_create, content_destroy])
    _ = role.create_role(name="administracion", permissions=[grafic_index, grafic_show, report_index, report_show, receipt_index, receipt_show, receipt_update, receipt_create, receipt_destroy, payment_index, payment_show, payment_update, payment_create, payment_destroy, employee_create, employee_destroy,
                         employee_index, employee_show, employee_update, horse_index, horse_show, rider_show, rider_index, rider_update, rider_destroy, rider_create, contact_index, contact_show, contact_update, contact_create, contact_destroy, content_index, content_show, content_update, content_create, content_destroy])

    _ = role.create_role(name="tecnica", permissions=[grafic_index, grafic_show, report_index, report_show, horse_index,
                         horse_show, receipt_index, receipt_show, rider_index, rider_create, rider_destroy, rider_show, rider_update])
    _ = role.create_role(name="voluntariado")
    _ = role.create_role(name="ecuestre", permissions=[
                         horse_index, horse_show, horse_update, horse_create, horse_destroy, rider_index, rider_show])
    _ = role.create_role(name="editor", permissions=[
                         content_index, content_show, content_update, content_create])
    # Asignaciones
    assignment1 = assignment.create_assignment(
        name="Asignación Universal por hijo")
    assignment2 = assignment.create_assignment(
        name="Asignación Universal por hijo con Discapacidad")
    assignment3 = assignment.create_assignment(
        name="Asignación por ayuda escolar anual")

    # Días
    lunes = day.create_day(name="Lunes")
    martes = day.create_day(name="Martes")
    miercoles = day.create_day(name="Miercoles")
    jueves = day.create_day(name="Jueves")
    viernes = day.create_day(name="Viernes")
    sabado = day.create_day(name="Sabado")
    domingo = day.create_day(name="Domingo")

    # USUARIOS
    admin = user.create_user(email="admin@admin.com",
                             password="admin", role_id=1, alias="admin")
    luca = user.create_user(email="rol2@mail.com",
                            password="123456", role_id=2, alias="Luca")

    tres = user.create_user(email="rol3@mail.com",
                            password="123456", role_id=3, alias="1")
    cuatro = user.create_user(email="rol4@mail.com",
                              password="123456", role_id=4, alias="2")
    cinco = user.create_user(email="rol5@mail.com",
                             password="123456", role_id=5, alias="3")
    seis = user.create_user(email="rol6@mail.com",
                            password="123456", role_id=6, alias="Editor")

    _ = user.create_user(email="test@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="test2@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="tes@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="te@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="t@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="testaa@mail.com",
                         password="123456", role_id=5, alias="3")
    _ = user.create_user(email="testa@mail.com",
                         password="123456", role_id=5, alias="3")

    # EMPLEADOS
    luca2 = employee.create_employee(name="adf", surname="dah", dni="150", email="laa0@gmail.com",
                                     start_date="2021-01-01",  active=True, job_position="Entrenador de Caballos")
    profesor = employee.create_employee(name="Carlos", surname="Gomez", dni="12345678", email="carlos@gmail.com", start_date="2021-01-01", active=True, job_position="Profesor", address="Calle Falsa 123",
                                        city="Ciudad", telephone="123456789", profession="Psicólogo/a", emergency_contact_info="Maria Gomez - 123456789", social_work="OSDE", associate_number="123456", condition="Personal Rentado")
    terapeuta = employee.create_employee(name="Ana", surname="Lopez", dni="87654321", email="ana@gmail.com", start_date="2021-02-01", active=True, job_position="Terapeuta", address="Calle Verdadera 456",
                                         city="Ciudad", telephone="987654321", profession="Médico/a", emergency_contact_info="Juan Lopez - 987654321", social_work="Swiss Medical", associate_number="654321", condition="Personal Rentado")
    conductor = employee.create_employee(name="Luis", surname="Martinez", dni="11223344", email="luis@gmail.com", start_date="2021-03-01", active=True, job_position="Conductor", address="Avenida Siempre Viva 789",
                                         city="Ciudad", telephone="1122334455", profession="Psicomotricista", emergency_contact_info="Pedro Martinez - 1122334455", social_work="Galeno", associate_number="112233", condition="Voluntario")
    auxiliar_pista = employee.create_employee(name="Pedro", surname="Fernandez", dni="55667788", email="pedro@gmail.com", start_date="2021-04-01", active=True, job_position="Auxiliar de pista", address="Calle Real 101",
                                              city="Ciudad", telephone="5566778899", profession="Docente", emergency_contact_info="Laura Fernandez - 5566778899", social_work="Medicus", associate_number="556677", condition="Voluntario")
    entrenador = employee.create_employee(name="Jorge", surname="Perez", dni="99887766", email="jorge@gmail.com", start_date="2021-05-01", active=True, job_position="Entrenador", address="Calle Principal 202",
                                          city="Ciudad", telephone="9988776655", profession="Otro", emergency_contact_info="Sofia Perez - 9988776655", social_work="OSDE", associate_number="998877", condition="Personal Rentado")
    entrenador2 = employee.create_employee(name="Jorge", surname="Peres", dni="99887767", email="jorge1@gmail.com", start_date="2019-05-01", active=True, job_position="Entrenador", address="Calle Principal 202",
                                           city="Ciudad", telephone="9988776665", profession="Otro", emergency_contact_info="Sofia Perez - 9988776655", social_work="OSDE", associate_number="998878", condition="Personal Rentado")

    # PAGOS
    pago_honorarios = payment.create_payment(
        amount=2000, beneficiary_id=profesor.id, type="Honorarios", description="Pago de honorarios")
    pago_proveedor = payment.create_payment(
        amount=1500, beneficiary_id=None, type="Proveedor", description="Pago a proveedor")
    pago_gastos_varios = payment.create_payment(
        amount=500, beneficiary_id=None, type="Gastos varios", description="Gastos varios")


    # CABALLOS
    caballo1 = horse.create_horse(name="Caballo1", birth_date="2020-01-01", purchase_donation="Compra",
                                  gender="Macho", assigned_activities_ja="Hipoterapia", association=[entrenador, conductor])

    # JINETES/AMAZONAS
    jinete1 = riders.create_rider(name="Juan", surname="Perez", dni=51321513, age=25, birthdate="1996-01-01", birth_place="CABA", address="Av. Siempre Viva 123", phone="123456789", emergency_contact="Maria", emergency_contact_phone_number="123456789", scholarship=False, scholarship_percentage=0, professionals="Dr. Juan Perez", disability_certificate=False, diagnosis="ECNE", other="Otro", disability_type="Mental", family_assignment=True, pension="Provincial", health_insurance="OSDE",
                                  affiliate_number="123456", guardianship=False, observations="Sin observaciones", school_institution="Escuela 123", institution_address="Av. Siempre Viva 123", grade="Primero", institution_phone="123456789", institution_observations="Sin observaciones", horse_id=caballo1.id, horse_conductor_id=conductor.id, track_assistant_id=auxiliar_pista.id, therapist_teacher_id=terapeuta.id, work_proposal="Hipoterapia", condition="Regular", headquarters="CASJ", days=[lunes.id, martes.id], tutors=[{'relationship': 'Padre', 'name': 'Juan', 'surname': 'Perez', 'dni': '87654321', 'address': 'Calle Falsa 456', 'cellphone': '987654321', 'email': 'emailtutor2@mail.com', 'educational_level': 'Secundario', 'occupation': 'Ingeniero'}, {'relationship': 'Madre', 'name': 'Ana', 'surname': 'Martinez', 'dni': '11223344', 'address': 'Calle Verdadera 789', 'cellphone': '1122334455', 'email': 'emailtutor3@mail.com', 'educational_level': 'Terciario', 'occupation': 'Doctora'}], assignments=['Asignación Universal por hijo'])
    jinete2 = riders.create_rider(name="Pedro", surname="Gonzalez", dni=98765432, age=30, birthdate="1991-01-01", birth_place="CABA", address="Calle Falsa 456", phone="987654321", emergency_contact="Ana", emergency_contact_phone_number="987654321", scholarship=False, scholarship_percentage=0, professionals="Dr. Pedro Gonzalez", disability_certificate=False, diagnosis="ECNE", other="Otro", disability_type="Sensorial", family_assignment=True, pension="Provincial",
                                  health_insurance="OSDE", affiliate_number="654321", guardianship=False, observations="Sin observaciones", school_institution="Escuela 456", institution_address="Calle Falsa 456", grade="Segundo", institution_phone="987654321", institution_observations="Sin observaciones", horse_id=caballo1.id, horse_conductor_id=conductor.id, track_assistant_id=auxiliar_pista.id, therapist_teacher_id=terapeuta.id, work_proposal="Hipoterapia", condition="Regular", headquarters="CASJ", days=[miercoles.id, jueves.id], tutors=[{'relationship': 'Madre', 'name': 'Maria', 'surname': 'Gomez', 'dni': '12345678', 'address': 'Av. Siempre Viva 123', 'cellphone': '123456789', 'email': 'emailtutor@mail.com', 'educational_level': 'Universitario', 'occupation': 'Profesora'}, {'relationship': 'Padre', 'name': 'Juan', 'surname': 'Perez', 'dni': '87654321', 'address': 'Calle Falsa 456', 'cellphone': '987654321', 'email': 'emailtutor2@mail.com', 'educational_level': 'Secundario', 'occupation': 'Ingeniero'}], assignments=['Asignación Universal por hijo con Discapacidad'])

    # RECIBOS
    recibo = receipt.create_receipt(
        ja_id=1, quantity=1000, payment_method="Efectivo", employee_id=profesor.id, remarks="Sin observaciones")
    recibo2 = receipt.create_receipt(ja_id=1, quantity=1000, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 1, 15))
    recibo3 = receipt.create_receipt(ja_id=1, quantity=1100, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 2, 15))
    recibo4 = receipt.create_receipt(ja_id=1, quantity=1200, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 3, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1300, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 4, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1400, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 5, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1500, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 6, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1600, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 7, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1700, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 8, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1800, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2024, 9, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1800, payment_method="Efectivo",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2020, 12, 15))
    recibo_ = receipt.create_receipt(ja_id=1, quantity=1800, payment_method="Transferencia",
                                     employee_id=profesor.id, remarks="Sin observaciones", payment_date=datetime(2020, 12, 15))

    # DOCUMENTOS

    # Etapa 2
    # CONTACTO
    # ESTADOS
    _ = contact.create_status(name="Nuevo")
    _ = contact.create_status(name="En progreso")
    _ = contact.create_status(name="Finalizado")

    # CONTENIDOS
    # ESTADOS
    _ = content.create_status(name="Borrador")
    _ = content.create_status(name="Publicado")
    _ = content.create_status(name="Archivado")

    # Contenidos
    contenido1 = content.create_content(title="Titulo1", summary="Resumen1",
                                        content="Contenido1", author_id=1, status_id=2, publication_date="2024-01-01")
    contenido3 = content.create_content(title="Titulo3", summary="Resumen3",
                                        content="Contenido3", author_id=1, status_id=2, publication_date="2024-03-01")
    contenido4 = content.create_content(title="Titulo4", summary="Resumen4",
                                        content="Contenido4", author_id=1, status_id=2, publication_date="2024-04-01")
    contenido5 = content.create_content(title="Titulo5", summary="Resumen5",
                                        content="Contenido5", author_id=1, status_id=2, publication_date="2024-05-01")
    contenido6 = content.create_content(title="Titulo6", summary="Resumen6",
                                        content="Contenido6", author_id=1, status_id=2, publication_date="2024-06-01")
    contenido7 = content.create_content(title="Titulo7", summary="Resumen7",
                                        content="Contenido7", author_id=1, status_id=2, publication_date="2024-07-01")
    contenido8 = content.create_content(title="Titulo8", summary="Resumen8",
                                        content="Contenido8", author_id=1, status_id=2, publication_date="2024-08-01")
    contenido7 = content.create_content(
        title="Titulo7", summary="Resumen7", content="Contenido7", author_id=1)
    contenido8 = content.create_content(
        title="Titulo8", summary="Resumen8", content="Contenido8", author_id=1)
    contenido9 = content.create_content(
        title="Titulo9", summary="Resumen9", content="Contenido9", author_id=1)
    contenido10 = content.create_content(
        title="Titulo10", summary="Resumen10", content="Contenido10", author_id=6)
    contenido11 = content.create_content(
        title="Titulo11", summary="Resumen11", content="Contenido11", author_id=6)
    contenido12 = content.create_content(
        title="Titulo12", summary="Resumen12", content="Contenido12", author_id=6)
    contenido13 = content.create_content(
        title="Titulo13", summary="Resumen13", content="Contenido13", author_id=6)
    contenido14 = content.create_content(
        title="Leo Messi",
        summary="Noticia sobre Leo Messi",
        content="Lionel Messi ha hablado recientemente sobre el futuro de su carrera, destacando su amor por el fútbol y su deseo de aprovechar cada momento mientras se acerca al final de su trayectoria profesional. En una entrevista, mencionó que tomará la decisión de retirarse cuando sienta que es el momento adecuado, pero por ahora sigue disfrutando cada instante en el campo. También expresó su gratitud por haber cumplido sueños importantes, como ganar el Mundial con Argentina y numerosos títulos con sus clubes. En el ámbito internacional, Messi estuvo presente en los últimos partidos de eliminatorias con la selección argentina, jugando en un Monumental lleno y siendo ovacionado por los fanáticos. Reflejó sobre las dificultades y los éxitos de su carrera, valorando cada momento más que nunca mientras continúa luchando por nuevos logros.",
        author_id=1,
        status_id=2,
        publication_date="2024-09-01"
    )

    print("Seed ejecutado correctamente")
