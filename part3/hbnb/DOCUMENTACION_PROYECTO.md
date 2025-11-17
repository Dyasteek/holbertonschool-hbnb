# Documentación del Proyecto HBnB - API REST

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Conceptos y Definiciones](#conceptos-y-definiciones)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Modelos de Datos](#modelos-de-datos)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Patrones de Diseño Implementados](#patrones-de-diseño-implementados)
8. [Seguridad y Autenticación](#seguridad-y-autenticación)
9. [Flujo de Datos](#flujo-de-datos)
10. [Tecnologías Utilizadas](#tecnologías-utilizadas)

---

## Descripción General

**HBnB** es una aplicación REST API desarrollada en Python utilizando Flask que simula una plataforma de alquiler de alojamientos (similar a Airbnb). El sistema permite gestionar usuarios, lugares (places), reseñas (reviews), amenidades (amenities) y ubicaciones (locations) a través de una API RESTful completa.

### Características Principales:
- **API REST completa** con operaciones CRUD para todas las entidades
- **Autenticación JWT** para seguridad de endpoints
- **Documentación automática** con Swagger/OpenAPI
- **Arquitectura en capas** (Modelos, Persistencia, Servicios, API)
- **Almacenamiento en memoria** durante la sesión de la aplicación
- **Validación de relaciones** entre entidades
- **Hashing de contraseñas** con bcrypt

---

## Arquitectura del Sistema

El proyecto sigue una **arquitectura en capas (Layered Architecture)** que separa las responsabilidades en diferentes niveles:

```
┌─────────────────────────────────────┐
│         Capa de Presentación        │
│    (API Endpoints - Flask-RESTX)    │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Capa de Servicios/Facade       │
│    (Lógica de Negocio - Facade)     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Capa de Persistencia           │
│    (Repository Pattern)             │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Capa de Modelos                │
│    (Domain Models)                  │
└─────────────────────────────────────┘
```

### Ventajas de esta Arquitectura:
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Mantenibilidad**: Cambios en una capa no afectan directamente a las otras
- **Testabilidad**: Cada capa puede ser probada independientemente
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin modificar código existente

---

## Conceptos y Definiciones

### 1. **API REST (Representational State Transfer)**
**Definición**: Un estilo de arquitectura de software para sistemas distribuidos que utiliza métodos HTTP estándar (GET, POST, PUT, DELETE) para realizar operaciones sobre recursos identificados por URLs.

**En este proyecto**: Todos los endpoints siguen los principios REST:
- `GET /api/v1/users/` - Obtener todos los usuarios
- `POST /api/v1/users/` - Crear un nuevo usuario
- `GET /api/v1/users/<id>` - Obtener un usuario específico
- `PUT /api/v1/users/<id>` - Actualizar un usuario
- `DELETE /api/v1/users/<id>` - Eliminar un usuario

### 2. **CRUD (Create, Read, Update, Delete)**
**Definición**: Las cuatro operaciones básicas que se pueden realizar sobre datos persistentes:
- **Create**: Crear nuevos registros
- **Read**: Leer/consultar registros existentes
- **Update**: Modificar registros existentes
- **Delete**: Eliminar registros

**En este proyecto**: Todas las entidades (Users, Places, Reviews, Amenities, Locations) implementan operaciones CRUD completas.

### 3. **Flask**
**Definición**: Framework web ligero de Python que permite crear aplicaciones web y APIs de manera rápida y sencilla. Es un microframework que proporciona las herramientas esenciales sin imponer decisiones de diseño.

**En este proyecto**: Flask se utiliza como el servidor web principal y se configura mediante el patrón Factory (`create_app`).

### 4. **Flask-RESTX**
**Definición**: Extensión de Flask que simplifica la construcción de APIs REST. Proporciona:
- **Namespaces**: Organización de endpoints relacionados
- **Models**: Validación y documentación de datos
- **Swagger UI**: Documentación interactiva automática

**En este proyecto**: Se utiliza para definir los endpoints, validar datos de entrada y generar documentación automática en `/api/v1/`.

### 5. **Patrón Facade**
**Definición**: Patrón de diseño estructural que proporciona una interfaz simplificada a un subsistema complejo. Oculta la complejidad de múltiples clases y proporciona un punto de entrada único.

**En este proyecto**: La clase `HBnBFacade` actúa como fachada que:
- Encapsula la lógica de negocio
- Proporciona métodos simples para operaciones complejas
- Abstrae la interacción con múltiples repositorios
- Centraliza la creación y gestión de entidades

**Ejemplo**:
```python
facade.create_place(place_data)  # Internamente maneja repositorios, validaciones, etc.
```

### 6. **Repository Pattern (Patrón Repositorio)**
**Definición**: Patrón de diseño que abstrae la lógica de acceso a datos. Actúa como una capa intermedia entre la lógica de negocio y la fuente de datos, proporcionando una interfaz uniforme para operaciones CRUD.

**En este proyecto**: La clase `Repository` implementa este patrón:
- `create(obj)`: Almacena un objeto
- `get(obj_id)`: Obtiene un objeto por ID
- `get_all()`: Obtiene todos los objetos
- `update(obj_id, data)`: Actualiza un objeto
- `delete(obj_id)`: Elimina un objeto
- `get_by_attribute(attr_name, attr_value)`: Búsqueda por atributo

**Ventajas**:
- Desacopla la lógica de negocio del almacenamiento
- Facilita cambiar el sistema de persistencia (memoria → base de datos)
- Centraliza la lógica de acceso a datos

### 7. **Modelo de Dominio (Domain Model)**
**Definición**: Representación de conceptos del negocio en código. Los modelos encapsulan datos y comportamientos relacionados con entidades del dominio.

**En este proyecto**: Cada modelo (User, Place, Review, Amenity, Location) representa una entidad del negocio con:
- Atributos que definen sus propiedades
- Métodos que encapsulan comportamientos
- Relaciones con otros modelos

### 8. **Herencia (Inheritance)**
**Definición**: Mecanismo de programación orientada a objetos que permite que una clase (clase hija) herede atributos y métodos de otra clase (clase padre).

**En este proyecto**: Todos los modelos heredan de `BaseModel`:
- `BaseModel` proporciona: `id`, `created_at`, `updated_at`, `save()`, `update()`, `delete()`, `to_dict()`
- Los modelos hijos (User, Place, etc.) extienden esta funcionalidad base

### 9. **UUID (Universally Unique Identifier)**
**Definición**: Identificador único de 128 bits que garantiza unicidad sin necesidad de coordinación central. Se representa como una cadena hexadecimal.

**En este proyecto**: Cada entidad recibe un `id` único generado con `uuid.uuid4()` al momento de su creación, garantizando identificadores únicos sin necesidad de secuencias o contadores.

### 10. **JWT (JSON Web Token)**
**Definición**: Estándar abierto (RFC 7519) que define una forma compacta y autocontenida de transmitir información entre partes como un objeto JSON. Se utiliza para autenticación y autorización.

**Componentes de un JWT**:
- **Header**: Tipo de token y algoritmo de firma
- **Payload**: Datos (claims) como user_id, is_admin, etc.
- **Signature**: Firma que verifica la integridad del token

**En este proyecto**: 
- Se genera un token JWT al hacer login (`/api/v1/auth/login`)
- El token contiene `identity` (user_id) y `additional_claims` (is_admin)
- Los endpoints protegidos requieren el token en el header `Authorization: Bearer <token>`

### 11. **Flask-JWT-Extended**
**Definición**: Extensión de Flask que proporciona funcionalidades JWT avanzadas:
- Creación y validación de tokens
- Decoradores para proteger endpoints (`@jwt_required`)
- Extracción de información del token (`get_jwt_identity()`)

**En este proyecto**: Se utiliza para:
- Generar tokens de acceso en el login
- Proteger endpoints que requieren autenticación
- Obtener el ID del usuario autenticado

### 12. **Bcrypt**
**Definición**: Algoritmo de hash de contraseñas diseñado específicamente para ser lento y resistente a ataques de fuerza bruta. Es parte de la librería Flask-Bcrypt.

**En este proyecto**: 
- Las contraseñas se hashean con `bcrypt.generate_password_hash()` al crear/actualizar usuarios
- Se verifican con `bcrypt.check_password_hash()` durante el login
- **Nunca se almacenan contraseñas en texto plano**

### 13. **Flask-Bcrypt**
**Definición**: Extensión de Flask que proporciona funciones de hashing y verificación de contraseñas usando bcrypt.

**En este proyecto**: Se inicializa en `app/__init__.py` y se utiliza en el modelo `User` para:
- `set_password(password)`: Hashea y almacena la contraseña
- `check_password(password)`: Verifica si una contraseña coincide con el hash

### 14. **App Factory Pattern (Patrón Factory de Aplicación)**
**Definición**: Patrón de diseño que utiliza una función factory para crear instancias de la aplicación Flask. Permite:
- Múltiples instancias de la app con diferentes configuraciones
- Testing más fácil (crear apps de prueba)
- Configuración flexible

**En este proyecto**: La función `create_app()` en `app/__init__.py`:
- Crea y configura la instancia de Flask
- Inicializa extensiones (bcrypt, jwt)
- Registra namespaces de la API
- Retorna la app configurada

### 15. **Namespace (Flask-RESTX)**
**Definición**: Mecanismo de Flask-RESTX para agrupar endpoints relacionados bajo una ruta base común. Facilita la organización y versionado de APIs.

**En este proyecto**: Cada recurso tiene su namespace:
- `users` → `/api/v1/users`
- `places` → `/api/v1/places`
- `reviews` → `/api/v1/reviews`
- `amenities` → `/api/v1/amenities`
- `locations` → `/api/v1/locations`
- `auth` → `/api/v1/auth`

### 16. **Resource (Flask-RESTX)**
**Definición**: Clase en Flask-RESTX que representa un recurso REST. Los métodos de la clase corresponden a métodos HTTP:
- `get()` → GET
- `post()` → POST
- `put()` → PUT
- `delete()` → DELETE

**En este proyecto**: Cada endpoint está definido como una clase `Resource` con métodos que manejan las peticiones HTTP correspondientes.

### 17. **Model (Flask-RESTX)**
**Definición**: Esquema de datos en Flask-RESTX que define la estructura y validación de los datos de entrada/salida. Se utiliza para:
- Validar datos de peticiones
- Generar documentación Swagger automática
- Serialización/deserialización

**En este proyecto**: Cada endpoint define modelos para:
- Creación: `user_create_model`, `place_model`, etc.
- Actualización: `user_update_model`, etc.
- Validación automática con `@api.expect(model, validate=True)`

### 18. **Almacenamiento en Memoria (In-Memory Storage)**
**Definición**: Sistema de persistencia que almacena datos en la memoria RAM del servidor. Los datos se pierden cuando la aplicación se detiene.

**En este proyecto**: El `Repository` utiliza un diccionario Python (`self._storage = {}`) para almacenar objetos en memoria. Esto es útil para:
- Desarrollo y testing
- Prototipado rápido
- Aplicaciones con datos temporales

**Limitación**: Los datos no persisten entre reinicios del servidor.

### 19. **Validación de Relaciones**
**Definición**: Verificación que asegura que las referencias entre entidades son válidas antes de crear o actualizar registros.

**En este proyecto**: 
- Al crear un `Place`, se valida que `location_id` y `owner_id` existan
- Al crear un `Review`, se valida que `place_id` y `user_id` existan
- Si las referencias no existen, se retorna error 400

### 20. **Decorador `@jwt_required`**
**Definición**: Decorador de Flask-JWT-Extended que protege un endpoint requiriendo un token JWT válido en la petición. Si el token es inválido o falta, retorna 401 Unauthorized.

**En este proyecto**: Aunque está importado, actualmente no todos los endpoints lo utilizan. Se puede aplicar a endpoints que requieren autenticación.

### 21. **Códigos de Estado HTTP**
**Definición**: Códigos numéricos de 3 dígitos que indican el resultado de una petición HTTP:
- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos o error del cliente
- **401 Unauthorized**: No autenticado o credenciales inválidas
- **404 Not Found**: Recurso no encontrado

**En este proyecto**: Todos los endpoints retornan códigos de estado apropiados según el resultado de la operación.

### 22. **Swagger/OpenAPI**
**Definición**: Especificación estándar para documentar APIs REST. Flask-RESTX genera automáticamente documentación Swagger a partir de los modelos y endpoints definidos.

**En este proyecto**: La documentación interactiva está disponible en `/api/v1/` y permite:
- Ver todos los endpoints
- Probar endpoints directamente desde el navegador
- Ver modelos de datos y validaciones

### 23. **Configuración por Entorno**
**Definición**: Sistema que permite diferentes configuraciones según el entorno (desarrollo, producción, testing).

**En este proyecto**: `config.py` define:
- `Config`: Clase base con configuración común
- `DevelopmentConfig`: Configuración para desarrollo (DEBUG=True)
- `config`: Diccionario que mapea nombres de entorno a clases de configuración

### 24. **Singleton Pattern (Patrón Singleton)**
**Definición**: Patrón de diseño que asegura que una clase tenga solo una instancia y proporciona un punto de acceso global a ella.

**En este proyecto**: En `app/services/__init__.py`, el facade se implementa como singleton:
- `_facade_instance`: Variable global que almacena la única instancia
- `get_facade()`: Función que retorna la misma instancia siempre
- `facade`: Instancia global exportada

### 25. **Método `to_dict()`**
**Definición**: Método que convierte un objeto a un diccionario Python, útil para serialización JSON.

**En este proyecto**: Todos los modelos implementan `to_dict()` que:
- Hereda campos base de `BaseModel` (id, created_at, updated_at)
- Agrega campos específicos del modelo
- Convierte fechas a formato ISO string
- Maneja referencias a otros objetos (retorna IDs)

### 26. **Método `update()`**
**Definición**: Método que actualiza los atributos de un objeto con datos de un diccionario.

**En este proyecto**: `BaseModel.update()`:
- Itera sobre los pares clave-valor del diccionario
- Actualiza solo atributos existentes (`hasattr()`)
- Llama a `save()` para actualizar `updated_at`

### 27. **Timestamp Automático**
**Definición**: Sistema que registra automáticamente cuándo se crea y modifica un objeto.

**En este proyecto**: `BaseModel` mantiene:
- `created_at`: Fecha de creación (se establece en `__init__`)
- `updated_at`: Fecha de última modificación (se actualiza en `save()`)

### 28. **Relaciones entre Modelos**
**Definición**: Conexiones lógicas entre diferentes entidades del dominio.

**En este proyecto**:
- **User ↔ Place**: Un usuario puede tener múltiples lugares (propietario)
- **User ↔ Review**: Un usuario puede escribir múltiples reseñas
- **Place ↔ Review**: Un lugar puede tener múltiples reseñas
- **Place ↔ Location**: Un lugar pertenece a una ubicación
- **Place ↔ Amenity**: Un lugar puede tener múltiples amenidades (many-to-many)

### 29. **Métodos Helper en Modelos**
**Definición**: Métodos auxiliares que encapsulan lógica específica del modelo.

**En este proyecto**:
- `User.add_place()`: Agrega un lugar a la lista de lugares del usuario
- `User.get_reviews()`: Obtiene todas las reseñas del usuario
- `Place.add_amenity()`: Agrega una amenidad al lugar
- `Place.add_review()`: Agrega una reseña al lugar
- `Location.add_place()`: Agrega un lugar a la ubicación

### 30. **Payload de API**
**Definición**: Datos enviados en el cuerpo de una petición HTTP (generalmente en formato JSON).

**En este proyecto**: `api.payload` (Flask-RESTX) contiene los datos JSON enviados en peticiones POST/PUT, que se validan contra los modelos definidos.

---

## Estructura del Proyecto

```
hbnb/
├── app/
│   ├── __init__.py              # Factory de aplicación Flask
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py           # Endpoints de autenticación
│   │       ├── users.py          # Endpoints de usuarios
│   │       ├── places.py         # Endpoints de lugares
│   │       ├── reviews.py        # Endpoints de reseñas
│   │       ├── amenities.py      # Endpoints de amenidades
│   │       └── locations.py     # Endpoints de ubicaciones
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py         # Modelo base con funcionalidad común
│   │   ├── user.py               # Modelo de usuario
│   │   ├── place.py              # Modelo de lugar
│   │   ├── review.py             # Modelo de reseña
│   │   ├── amenity.py            # Modelo de amenidad
│   │   └── location.py           # Modelo de ubicación
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py         # Patrón Repository para almacenamiento
│   └── services/
│       ├── __init__.py           # Singleton del facade
│       └── facade.py             # Capa de servicios (lógica de negocio)
├── config.py                     # Configuración por entornos
├── run.py                        # Punto de entrada de la aplicación
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Documentación básica
```

---

## Modelos de Datos

### BaseModel
**Ubicación**: `app/models/base_model.py`

**Atributos**:
- `id`: UUID único generado automáticamente
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última modificación

**Métodos**:
- `save()`: Actualiza `updated_at`
- `update(data)`: Actualiza atributos del objeto
- `delete()`: Marca para eliminación (implementación básica)
- `to_dict()`: Convierte a diccionario

### User
**Ubicación**: `app/models/user.py`

**Atributos**:
- Hereda de `BaseModel`
- `first_name`: Nombre del usuario
- `last_name`: Apellido del usuario
- `email`: Email único del usuario
- `password_hash`: Hash de la contraseña (bcrypt)
- `is_admin`: Boolean que indica si es administrador
- `places`: Lista de lugares propiedad del usuario
- `reviews`: Lista de reseñas escritas por el usuario

**Métodos**:
- `set_password(password)`: Hashea y almacena la contraseña
- `check_password(password)`: Verifica si la contraseña es correcta
- `add_place(place)`: Agrega un lugar a la lista
- `get_reviews()`: Retorna todas las reseñas del usuario
- `to_dict()`: Serializa a diccionario (sin password_hash)

### Place
**Ubicación**: `app/models/place.py`

**Atributos**:
- Hereda de `BaseModel`
- `title`: Título del lugar
- `description`: Descripción del lugar
- `price`: Precio por noche
- `max_guest`: Número máximo de huéspedes
- `location`: Referencia al objeto Location
- `owner`: Referencia al objeto User (propietario)
- `amenities`: Lista de amenidades del lugar
- `reviews`: Lista de reseñas del lugar

**Métodos**:
- `add_amenity(amenity)`: Agrega una amenidad
- `add_review(review)`: Agrega una reseña
- `get_amenities()`: Retorna todas las amenidades
- `get_reviews()`: Retorna todas las reseñas
- `to_dict()`: Serializa incluyendo location_id y owner_id

### Review
**Ubicación**: `app/models/review.py`

**Atributos**:
- Hereda de `BaseModel`
- `title`: Título de la reseña
- `text`: Contenido de la reseña
- `rating`: Calificación (1-5)
- `place`: Referencia al objeto Place
- `user`: Referencia al objeto User (autor)

**Métodos**:
- `to_dict()`: Serializa incluyendo place_id y user_id

### Amenity
**Ubicación**: `app/models/amenity.py`

**Atributos**:
- Hereda de `BaseModel`
- `name`: Nombre de la amenidad
- `description`: Descripción opcional
- `places`: Lista de lugares que tienen esta amenidad

**Métodos**:
- `add_place(place)`: Agrega un lugar a la lista
- `to_dict()`: Serializa a diccionario

### Location
**Ubicación**: `app/models/location.py`

**Atributos**:
- Hereda de `BaseModel`
- `address`: Dirección específica
- `city`: Ciudad
- `country`: País
- `places`: Lista de lugares en esta ubicación

**Métodos**:
- `add_place(place)`: Agrega un lugar a la lista
- `to_dict()`: Serializa a diccionario

---

## Endpoints de la API

### Autenticación

#### POST `/api/v1/auth/login`
**Descripción**: Autentica un usuario y retorna un token JWT

**Body**:
```json
{
  "email": "usuario@example.com",
  "password": "contraseña123"
}
```

**Respuesta Exitosa (200)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta Error (401)**:
```json
{
  "error": "Invalid credentials"
}
```

### Usuarios

#### GET `/api/v1/users/`
**Descripción**: Obtiene todos los usuarios

**Respuesta (200)**:
```json
[
  {
    "id": "uuid",
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan@example.com"
  }
]
```

#### POST `/api/v1/users/`
**Descripción**: Crea un nuevo usuario

**Body**:
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com",
  "password": "contraseña123"
}
```

**Respuesta (201)**:
```json
{
  "id": "uuid",
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com"
}
```

#### GET `/api/v1/users/<user_id>`
**Descripción**: Obtiene un usuario específico

#### PUT `/api/v1/users/<user_id>`
**Descripción**: Actualiza un usuario

#### DELETE `/api/v1/users/<user_id>`
**Descripción**: Elimina un usuario

### Lugares (Places)

#### GET `/api/v1/places/`
**Descripción**: Obtiene todos los lugares

#### POST `/api/v1/places/`
**Descripción**: Crea un nuevo lugar

**Body**:
```json
{
  "title": "Hermoso apartamento",
  "description": "Apartamento en el centro",
  "price": 100,
  "max_guest": 4,
  "location_id": "uuid-location",
  "owner_id": "uuid-user"
}
```

**Validaciones**:
- `location_id` debe existir
- `owner_id` debe existir

#### GET `/api/v1/places/<place_id>`
**Descripción**: Obtiene un lugar específico

#### PUT `/api/v1/places/<place_id>`
**Descripción**: Actualiza un lugar

#### DELETE `/api/v1/places/<place_id>`
**Descripción**: Elimina un lugar

### Reseñas (Reviews)

#### GET `/api/v1/reviews/`
**Descripción**: Obtiene todas las reseñas

#### POST `/api/v1/reviews/`
**Descripción**: Crea una nueva reseña

**Body**:
```json
{
  "title": "Excelente lugar",
  "text": "Muy cómodo y bien ubicado",
  "rating": 5,
  "place_id": "uuid-place",
  "user_id": "uuid-user"
}
```

**Validaciones**:
- `place_id` debe existir
- `user_id` debe existir

#### GET `/api/v1/reviews/<review_id>`
**Descripción**: Obtiene una reseña específica

#### PUT `/api/v1/reviews/<review_id>`
**Descripción**: Actualiza una reseña

#### DELETE `/api/v1/reviews/<review_id>`
**Descripción**: Elimina una reseña

### Amenidades (Amenities)

#### GET `/api/v1/amenities/`
**Descripción**: Obtiene todas las amenidades

#### POST `/api/v1/amenities/`
**Descripción**: Crea una nueva amenidad

#### GET `/api/v1/amenities/<amenity_id>`
**Descripción**: Obtiene una amenidad específica

#### PUT `/api/v1/amenities/<amenity_id>`
**Descripción**: Actualiza una amenidad

#### DELETE `/api/v1/amenities/<amenity_id>`
**Descripción**: Elimina una amenidad

### Ubicaciones (Locations)

#### GET `/api/v1/locations/`
**Descripción**: Obtiene todas las ubicaciones

#### POST `/api/v1/locations/`
**Descripción**: Crea una nueva ubicación

**Body**:
```json
{
  "address": "Calle Principal 123",
  "city": "Madrid",
  "country": "España"
}
```

#### GET `/api/v1/locations/<location_id>`
**Descripción**: Obtiene una ubicación específica

#### PUT `/api/v1/locations/<location_id>`
**Descripción**: Actualiza una ubicación

#### DELETE `/api/v1/locations/<location_id>`
**Descripción**: Elimina una ubicación

### Health Check

#### GET `/health`
**Descripción**: Endpoint de salud de la aplicación

**Respuesta**: `"Hola, bienvenido."`

---

## Patrones de Diseño Implementados

### 1. **Repository Pattern**
**Implementación**: `app/persistence/repository.py`

**Propósito**: Abstraer el acceso a datos

**Ventajas**:
- Facilita cambiar el sistema de persistencia
- Centraliza la lógica de acceso a datos
- Desacopla la lógica de negocio del almacenamiento

### 2. **Facade Pattern**
**Implementación**: `app/services/facade.py`

**Propósito**: Proporcionar una interfaz simplificada al sistema

**Ventajas**:
- Oculta la complejidad de múltiples repositorios
- Proporciona métodos de alto nivel
- Facilita el mantenimiento

### 3. **Factory Pattern (App Factory)**
**Implementación**: `app/__init__.py` → `create_app()`

**Propósito**: Crear instancias de la aplicación con configuración flexible

**Ventajas**:
- Múltiples instancias con diferentes configuraciones
- Facilita testing
- Configuración por entorno

### 4. **Singleton Pattern**
**Implementación**: `app/services/__init__.py`

**Propósito**: Asegurar una única instancia del facade

**Ventajas**:
- Consistencia de datos
- Eficiencia de memoria
- Punto de acceso global

### 5. **Template Method Pattern (implícito)**
**Implementación**: `BaseModel` con métodos que los hijos pueden sobrescribir

**Propósito**: Definir estructura común con variaciones

**Ejemplo**: `to_dict()` en BaseModel es extendido por cada modelo hijo

---

## Seguridad y Autenticación

### 1. **Hashing de Contraseñas**
- **Algoritmo**: Bcrypt
- **Implementación**: `User.set_password()` y `User.check_password()`
- **Seguridad**: Las contraseñas nunca se almacenan en texto plano

### 2. **JWT (JSON Web Tokens)**
- **Generación**: Al hacer login exitoso
- **Contenido**: `identity` (user_id) y `additional_claims` (is_admin)
- **Uso**: Protección de endpoints sensibles

### 3. **Validación de Datos**
- **Flask-RESTX Models**: Validación automática de tipos y campos requeridos
- **Validación de Relaciones**: Verificación de existencia de referencias

### 4. **Manejo de Errores**
- Códigos HTTP apropiados (400, 401, 404)
- Mensajes de error descriptivos
- Validación de entrada antes de procesar

---

## Flujo de Datos

### Flujo de Creación de un Lugar:

```
1. Cliente → POST /api/v1/places/
   Body: {title, description, price, max_guest, location_id, owner_id}

2. Flask-RESTX valida el payload contra place_model

3. Endpoint (places.py) → facade.create_place(place_data)

4. Facade valida que location_id y owner_id existan
   - facade.get_location(location_id)
   - facade.get_user(owner_id)

5. Facade crea el objeto Place
   - place = Place(**place_data)

6. Facade almacena en el repositorio
   - place_repo.create(place)

7. Repository almacena en memoria
   - self._storage[place.id] = place

8. Respuesta JSON con el lugar creado (201)
```

### Flujo de Autenticación:

```
1. Cliente → POST /api/v1/auth/login
   Body: {email, password}

2. Endpoint (auth.py) obtiene credenciales
   - credentials = api.payload

3. Facade busca usuario por email
   - user = facade.get_user_by_email(email)

4. Se verifica la contraseña
   - user.check_password(password)

5. Si es válido, se genera JWT
   - create_access_token(identity=user.id, claims={"is_admin": user.is_admin})

6. Respuesta con access_token (200)
```

---

## Tecnologías Utilizadas

### Backend Framework
- **Flask 2.x**: Framework web de Python
- **Flask-RESTX**: Extensión para APIs REST

### Autenticación y Seguridad
- **Flask-JWT-Extended**: Manejo de tokens JWT
- **Flask-Bcrypt**: Hashing de contraseñas

### Base de Datos (Futuro)
- **SQLAlchemy**: ORM (incluido en requirements pero no implementado aún)

### Estándares y Protocolos
- **REST**: Arquitectura de la API
- **HTTP/HTTPS**: Protocolo de comunicación
- **JSON**: Formato de intercambio de datos
- **JWT**: Estándar de autenticación
- **OpenAPI/Swagger**: Documentación de API

---

## Puntos Clave para la Defensa

### 1. **Arquitectura en Capas**
- Separación clara de responsabilidades
- Facilita mantenimiento y escalabilidad
- Cada capa tiene un propósito específico

### 2. **Patrones de Diseño**
- Repository: Abstracción de persistencia
- Facade: Simplificación de la interfaz
- Factory: Creación flexible de la app
- Singleton: Instancia única del facade

### 3. **Seguridad**
- Contraseñas hasheadas con bcrypt
- Autenticación JWT
- Validación de datos de entrada

### 4. **Buenas Prácticas**
- Código organizado y modular
- Documentación automática (Swagger)
- Manejo apropiado de errores HTTP
- Validación de relaciones entre entidades

### 5. **Extensibilidad**
- Fácil agregar nuevos modelos
- Fácil cambiar sistema de persistencia (memoria → BD)
- Configuración por entornos

### 6. **RESTful**
- Endpoints siguen convenciones REST
- Métodos HTTP apropiados
- Códigos de estado correctos
- Recursos identificados por URLs

---

## Conclusión

Este proyecto demuestra una comprensión sólida de:
- Arquitectura de software en capas
- Patrones de diseño (Repository, Facade, Factory, Singleton)
- Desarrollo de APIs RESTful
- Autenticación y seguridad (JWT, bcrypt)
- Framework Flask y sus extensiones
- Programación orientada a objetos en Python
- Buenas prácticas de desarrollo

La estructura modular y la separación de responsabilidades facilitan el mantenimiento, testing y escalabilidad del sistema.

