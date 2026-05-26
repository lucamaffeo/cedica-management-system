# 🐎 Sistema de Gestión – CEDICA

Aplicación web desarrollada en equipo para la gestión integral de una organización sin fines de lucro dedicada a terapias asistidas con caballos.

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución](#ejecución)
- [Conceptos Aplicados](#conceptos-aplicados)

## 📝 Descripción General

Sistema integral de gestión para CEDICA (Centro de Equitación para Discapacitados con Caballos Asistentes), una organización dedicada a terapias asistidas con caballos. La plataforma permite gestionar usuarios, jinetes/amazonas, equipo, caballos, cobros y generar reportes estadísticos.

El proyecto está dividido en dos partes principales:
- **Admin (Backend)**: API REST desarrollada con Python y Flask
- **Portal (Frontend)**: Aplicación web pública desarrollada con Vue.js

## ⚙️ Características Principales

- ✅ Sistema de autenticación robusto (sin librerías externas)
- ✅ Control de accesos basado en roles y permisos
- ✅ Gestión de usuarios, jinetes/amazonas y equipo terapéutico
- ✅ Registro de pagos y cobros
- ✅ Reportes estadísticos con gráficos
- ✅ Gestión de caballos y documentación asociada
- ✅ API REST completa para integración frontend
- ✅ Portal público desarrollado en Vue.js
- ✅ Escalabilidad con arquitectura modular

## 🚀 Tecnologías Utilizadas

### Backend
- **Python** 3.12+
- **Flask** 3.0+ - Framework web
- **SQLAlchemy** - ORM para base de datos
- **PostgreSQL** - Base de datos
- **MinIO** - Almacenamiento de objetos
- **Marshmallow** - Serialización de datos
- **Pytest** - Testing
- **Poetry** - Gestor de dependencias

### Frontend
- **Vue.js** 3.5+ - Framework JavaScript
- **Vue Router** - Enrutamiento
- **Pinia** - State management
- **Tailwind CSS** - Framework CSS
- **Axios** - Cliente HTTP
- **Vite** - Build tool
- **reCAPTCHA v2** - Protección contra bots

### Infraestructura
- **Git** - Control de versiones
- **PostgreSQL** - Base de datos relacional

## 📁 Estructura del Proyecto

```
cedica-management-system/
├── admin/                      # Backend (API REST con Flask)
│   ├── src/
│   │   ├── core/              # Configuración y lógica central
│   │   │   ├── config.py      # Configuración de la app
│   │   │   ├── database.py    # Configuración de BD
│   │   │   ├── seeds.py       # Datos iniciales
│   │   │   ├── models/        # Modelos de datos (ORM)
│   │   │   ├── repositories/  # Acceso a datos
│   │   │   └── validation/    # Validaciones
│   │   └── web/               # Interfaz web
│   │       ├── api/           # Endpoints de API
│   │       ├── controllers/   # Controladores
│   │       ├── handlers/      # Manejo de errores
│   │       ├── helpers/       # Funciones auxiliares
│   │       ├── schemas/       # Esquemas de validación
│   │       └── templates/     # Templates HTML
│   ├── static/                # Recursos estáticos
│   ├── app.py                 # Entrada de la aplicación
│   ├── pyproject.toml         # Configuración de Poetry
│   └── README.md              # Documentación del backend
│
├── portal/                     # Frontend (Vue.js)
│   ├── src/
│   │   ├── components/        # Componentes Vue reutilizables
│   │   ├── views/             # Vistas/páginas
│   │   ├── router/            # Configuración de rutas
│   │   ├── stores/            # Estado (Pinia)
│   │   ├── assets/            # Estilos y recursos
│   │   ├── App.vue            # Componente raíz
│   │   └── main.js            # Punto de entrada
│   ├── public/                # Archivos públicos estáticos
│   ├── index.html             # HTML principal
│   ├── package.json           # Dependencias npm
│   ├── vite.config.js         # Configuración de Vite
│   ├── tailwind.config.js     # Configuración de Tailwind
│   ├── postcss.config.js      # Configuración de PostCSS
│   └── README.md              # Documentación del frontend
│
├── calculator/                # Módulo de cálculos (utilidad)
│   ├── src/
│   │   ├── suma.py
│   │   ├── resta.py
│   │   ├── multiplicacion.py
│   │   └── division.py
│   └── main.py
│
└── README.md                  # Este archivo
```

## 📦 Requisitos Previos

Antes de empezar, asegúrate tener instalado:

### Para el Backend
- **Python** 3.12 o superior
- **PostgreSQL** 12 o superior
- **Poetry** (gestor de dependencias Python)

### Para el Frontend
- **Node.js** 18+ y **npm** 9+

### Servicios Externos
- **MinIO** (para almacenamiento de objetos)
- **Google OAuth** (para autenticación opcional)

## 🔧 Instalación y Configuración

### Requisitos Previos ✓

Asegúrate de tener instalado:
- **PostgreSQL 12+** corriendo en `localhost:5432`
- **Python 3.12+**
- **Node.js 18+** y **npm 9+**

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd cedica-management-system
```

### 2. Configurar Backend (Admin)

#### 2.1 Instalar Dependencias

```bash
cd admin
pip install flask psycopg2-binary flask-sqlalchemy minio marshmallow google-auth google-auth-oauthlib google-auth-httplib2 flask-cors matplotlib pytest
```

#### 2.2 Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `admin/`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/grupo10
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
FLASK_ENV=development
SECRET_KEY=dev-secret-key
```

**Nota:** Ajusta `postgres` y `grupo10` según tu configuración local.

#### 2.3 Crear Base de Datos

Usa **MINGW64**, **Git Bash** o **PowerShell**:

```bash
psql -U postgres -c "CREATE DATABASE grupo10;"
```

#### 2.4 Inicializar Base de Datos

```bash
cd admin
flask --app app.py reset-db
flask --app app.py seeds-db
```

Esto creará todas las tablas y cargará datos iniciales (roles, permisos, usuarios de prueba).

### 3. Configurar Frontend (Portal)

#### 3.1 Instalar Dependencias

```bash
cd portal
npm install
```

#### 3.2 Configurar Variables de Entorno (Opcional)

Crea un archivo `.env.local` en la carpeta `portal/` si necesitas conectar a un endpoint específico:

```env
VITE_API_URL=http://localhost:5000
```

Por defecto ya está configurado para conectar al backend en `localhost:5000`.

## 🚀 Ejecución

### Opción A: Ejecutar Ambas Partes (Recomendado)

Abre **dos terminales** en la carpeta raíz del proyecto:

**Terminal 1 - Backend:**
```bash
cd admin
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd portal
npm run dev
```

La aplicación estará disponible en:
- **Frontend:** `http://localhost:5173`
- **Backend API:** `http://localhost:5000`

### Opción B: Ejecutar Solo el Backend

```bash
cd admin
python app.py
```

API disponible en `http://localhost:5000`

### Opción C: Ejecutar Solo el Frontend

```bash
cd portal
npm run dev
```

Frontend disponible en `http://localhost:5173`

### Build para Producción

**Frontend:**
```bash
cd portal
npm run build
```

Los archivos compilados estarán en `portal/dist/`

## 📝 Credenciales de Prueba

Una vez iniciada la aplicación, puedes login con:

```
System Admin:
  Email: admin@admin.com
  Contraseña: admin

Administración:
  Email: rol2@mail.com
  Contraseña: 123456

Técnica:
  Email: rol3@mail.com
  Contraseña: 123456

Voluntariado:
  Email: rol4@mail.com
  Contraseña: 123456

Ecuestre:
  Email: rol5@mail.com
  Contraseña: 123456

Editor:
  Email: rol6@mail.com
  Contraseña: 123456
```

## 🔗 Integración Frontend-Backend

El frontend está configurado para conectar automáticamente al backend en `http://localhost:5000`. Para cambiar esto, edita el archivo `.env.local` en la carpeta `portal`.

## ⚠️ Notas Importantes

- **PostgreSQL debe estar corriendo** en `localhost:5432` antes de iniciar el backend
- **Usa MINGW64 o Git Bash** en Windows si necesitas usar `psql` desde terminal
- El archivo `flake.nix` es para usuarios Linux/macOS con Nix; en Windows no es necesario
- Las variables de entorno en `.env` (backend) y `.env.local` (frontend) son opcionales si usas los valores por defecto

## 🧪 Testing

### Backend

```bash
cd admin
pytest
```

### Frontend (Linting)

```bash
cd portal
npm run lint
npm run format
```

## 🧠 Conceptos Aplicados

- **Arquitectura MVC** - Separación clara de responsabilidades
- **REST API** - Endpoints RESTful bien diseñados
- **ORM (SQLAlchemy)** - Mapeo objeto-relacional
- **Validaciones** - Cliente y servidor
- **Seguridad Web**
  - Protección contra XSS
  - CSRF tokens
  - Protección contra SQL Injection
  - Hash seguro de contraseñas
- **Control de Accesos** - Basado en roles y permisos
- **State Management** - Pinia para Vue.js
- **Almacenamiento de Objetos** - MinIO para archivos
- **Trabajo en Equipo** - Versionado semántico y Git workflow
- **Componentes Reutilizables** - Componentes Vue modulares
- **CI/CD Ready** - Estructura preparada para integración continua

## 📚 Documentación Adicional

- [Documentación del Backend](./admin/README.md)
- [Documentación del Frontend](./portal/README.md)

## 👥 Equipo de Desarrollo

Proyecto desarrollado en equipo como parte de un trabajo académico.

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

