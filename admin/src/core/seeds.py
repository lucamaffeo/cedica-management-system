from src.core import auth
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
    luca = auth.create_user(email="luca@mail.com", password="123456", role_id=1, alias="Luca")
    
    print("Seed ejecutado correctamente")
    

    

    