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

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd cedica-management-system
```

### 2. Configurar Backend (Admin)

#### 2.1 Instalar Dependencias

```bash
cd admin
poetry install
```

#### 2.2 Configurar Variables de Entorno

Crear un archivo `.env` en la carpeta `admin`:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/cedica
SQLALCHEMY_ECHO=False

# MinIO (Almacenamiento)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=cedica

# Flask
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_muy_segura
FLASK_DEBUG=True

# Google OAuth (opcional)
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret

# reCAPTCHA (opcional)
RECAPTCHA_SECRET_KEY=tu_secret_key
```

#### 2.3 Crear Base de Datos

```bash
# Acceder a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE cedica;
```

#### 2.4 Inicializar Base de Datos

```bash
# Desde la carpeta admin
poetry run python
>>> from src.core.database import init_db
>>> init_db()
```

### 3. Configurar Frontend (Portal)

#### 3.1 Instalar Dependencias

```bash
cd portal
npm install
```

#### 3.2 Configurar Variables de Entorno

Crear un archivo `.env.local` en la carpeta `portal`:

```env
VITE_API_URL=http://localhost:5000
VITE_RECAPTCHA_SITE_KEY=tu_site_key
```

## 🚀 Ejecución

### Ejecutar el Backend

```bash
cd admin
poetry run python app.py
```

La API estará disponible en `http://localhost:5000`

**O usando Poetry shell:**

```bash
cd admin
poetry shell
python app.py
```

### Ejecutar el Frontend

**Modo Desarrollo:**

```bash
cd portal
npm run dev
```

El portal estará disponible en `http://localhost:5173`

**Build para Producción:**

```bash
cd portal
npm run build
```

Los archivos compilados estarán en `portal/dist/`

### Ejecutar Ambas Partes Simultáneamente

En dos terminales diferentes:

```bash
# Terminal 1 - Backend
cd admin
poetry run python app.py

# Terminal 2 - Frontend
cd portal
npm run dev
```

## 🧪 Testing

### Backend

```bash
cd admin
poetry run pytest
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

