# 🎬 MovieHub

**MovieHub** es una aplicación web desarrollada con Django que permite a los usuarios buscar películas utilizando la API de TMDB, filtrarlas por distintos criterios, marcarlas como favoritas y gestionar comentarios personales sobre ellas. Incluye autenticación de usuarios, diseño con Bootstrap y operaciones CRUD completas sobre comentarios.

## 🚀 Funcionalidades principales

- ✅ Registro, inicio y cierre de sesión de usuarios
- ✅ Búsqueda de películas por nombre con integración a la API de TMDB
- ✅ Filtros por género, año de estreno y puntaje mínimo
- ✅ Marcado de películas como favoritas (únicamente para usuarios logueados)
- ✅ Listado y eliminación de películas favoritas
- ✅ Comentarios personales para cada película favorita
- ✅ Edición y eliminación de comentarios
- ✅ Mensajes de feedback de éxito y error con `django.contrib.messages`
- ✅ Estilo visual claro y responsive con Bootstrap 5
- ✅ Protección de vistas mediante `@login_required`

---

## 🛠️ Tecnologías utilizadas

- **Python 3.12**
- **Django 5.2.5**
- **SQLite3** como base de datos
- **Bootstrap 5** para la interfaz visual
- **TMDB API** para la búsqueda de películas

---

## 📦 Instalación local

Clonar el repositorio:
git clone https://github.com/TU_USUARIO/moviehub.git
cd moviehub


Crear y activar entorno virtual:
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate


Instalar dependencias:
pip install -r requirements.txt


Crear archivo .env y definir tu clave de TMDB:
TMDB_API_KEY=tu_clave_api


Ejecutar migraciones:
python manage.py migrate


Correr el servidor:
python manage.py runserver


Autor:
Matías Bordon
