🐎 Sistema de Gestión – CEDICA

Aplicación web desarrollada en equipo para la gestión integral de una organización sin fines de lucro dedicada a terapias asistidas con caballos.

🚀 Tecnologías utilizadas
Backend: Python, Flask
Frontend: Vue.js
Base de datos: PostgreSQL
ORM: SQLAlchemy
Almacenamiento: MinIO
Control de versiones: Git

⚙️ Funcionalidades principales
Sistema de autenticación sin librerías externas
Control de accesos mediante roles y permisos
Gestión de usuarios, jinetes/amazonas y equipo
Registro de cobros y reportes estadísticos
Gestión de caballos y documentación asociada
API REST para integración con frontend
Portal público desarrollado en Vue.js

🧠 Conceptos aplicados
Arquitectura MVC
Validaciones cliente/servidor
Seguridad web (XSS, CSRF, SQL Injection)
Trabajo en equipo y versionado semántico


⚙️ Instalación
# Clonar repositorio
git clone https://github.com/lucamaffeo/cedica-management-system.git

# Backend
cd .\cedica-management-system\admin\ 

# Instalar dependencias con Poetry
poetry install

# Activar entorno
poetry env activate

# Ejecutar aplicación
poetry run python app.py

🔹 Frontend
cd portal
npm install
npm run dev
