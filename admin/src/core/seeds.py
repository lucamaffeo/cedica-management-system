from src.core import auth
def run():

    #ROLES
    Administracion = auth.create_role(name="administracion")
    Voluntario = auth.create_role(name="voluntario")
    Tecnica = auth.create_role(name="tecnica")
    Ecuestre = auth.create_role(name="ecuestre")

    #Administración: index, show, update, create, destroy. (PERMISIONS)


    #ROLE_PERMISSIONS


    #USUARIOS
    Luca = auth.create_user(email="luca@mail.com", password="123456", role_id=1, alias="Luca")
    
    print("Seed ejecutado correctamente")
    

    

    