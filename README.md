# Pruebas Automatizadas - Inlaze QA Test

Framework de pruebas automatizadas para el sistema de autenticación de Inlaze utilizando Selenium con Python.

## Alcance del Proyecto

### Funcionalidades Cubiertas
- **Registro de Usuario**: 
  * Validación de nombre completo (2 palabras)
  * Validación de correo electrónico único
  * Validación de contraseña segura
  * Validación de campos obligatorios

- **Inicio de Sesión**: 
  * Validación de credenciales
  * Validación de campos obligatorios
  * Visualización del nombre de usuario
  * Cierre de sesión

### Cobertura de Pruebas
- Total de casos de prueba: 25
  * Registro de usuario: 13 casos
  * Inicio de sesión: 12 casos
- Validaciones de seguridad
- Validaciones de formato
- Validaciones de campos obligatorios

Estructura del Proyecto

```
inlaze-qa-test/
│
├── tests/                    # Pruebas automatizadas
│   ├── __init__.py
│   ├── conftest.py          # Configuración de pytest
│   ├── test_login.py        # Pruebas de inicio de sesión
│   ├── test_registration.py # Pruebas de registro
│   │
│   ├── page_objects/        # Objetos de página (Page Object Model)
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── register_page.py
│   │
│   └── utils/               # Utilidades para pruebas
│       ├── __init__.py
│       └── test_data.py
│
├── docs/                     # Documentación
│   ├── test_cases.md        # Casos de prueba detallados
│   └── bug_reports.md       # Plantilla de informes de errores
│
├── reports/                  # Informes de pruebas
│   ├── screenshots/         # Capturas de pantalla de errores
│   └── html/                # Informes HTML de pytest
│
├── venv/                    # Entorno virtual de Python
├── requirements.txt         # Dependencias del proyecto
└── run_tests.py            # Script para ejecutar pruebas
```

## Requisitos

- Python 3.8+
- Google Chrome
- ChromeDriver (se instalará automáticamente)

## Instalación

1. Clonar el repositorio:
```bash
https://github.com/jnicogaitan16/test_inlaze.git
cd inlaze-qa-test
```

2. Crear y activar entorno virtual:
```bash
# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# En Windows:
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar Pruebas

### Comandos Detallados

1. Ejecutar todas las pruebas con reporte completo:
```bash
# Reporte detallado con capturas y variables
pytest tests/ -v --html=reports/reporte_completo.html --capture=tee-sys --showlocals
```

2. Ejecutar pruebas específicas con reporte:
```bash
# Solo pruebas de inicio de sesión
pytest tests/test_login.py -v --html=reports/reporte_login.html --capture=tee-sys --showlocals

# Solo pruebas de registro
pytest tests/test_register.py -v --html=reports/reporte_registro.html --capture=tee-sys --showlocals
```

3. Ejecutar pruebas por funcionalidad:
```bash
# Pruebas de validación de contraseña
pytest -v -k "password" tests/

# Pruebas de validación de email
pytest -v -k "email" tests/

# Pruebas de campos obligatorios
pytest -v -k "required" tests/
```

### Opciones Adicionales

1. Modo verbose para ver más detalles:
```bash
python -m pytest -v tests/
```

2. Ejecutar pruebas en paralelo (más rápido):
```bash
python -m pytest -n auto tests/
```

3. Ejecutar pruebas con nombre específico:
```bash
python -m pytest -k "test_login" tests/
```

4. Capturar logs detallados:
```bash
python -m pytest --capture=tee-sys tests/
```

### Estructura de Reportes y Documentación

```
reports/
├── reporte_completo.html     # Reporte de todas las pruebas
├── reporte_login.html        # Reporte de inicio de sesión
├── reporte_registro.html     # Reporte de registro
└── screenshots/              # Capturas de pantalla de errores
    ├── error_login_*.png     # Errores de inicio de sesión
    └── error_registro_*.png  # Errores de registro

docs/
├── test_cases.md            # Descripción detallada de casos de prueba
└── bug_report.md            # Registro y seguimiento de bugs
```

Cada reporte HTML incluye:
- Resultados detallados de pruebas
- Trazas de error completas
- Variables locales en caso de fallo
- Enlaces a capturas de pantalla

### Guía de Solución de Problemas

1. **Errores Comunes**:
   - **No se encuentra el elemento**: La página no cargó completamente
   - **Tiempo de espera excedido**: La aplicación no responde
   - **Error del navegador**: Problemas con ChromeDriver

2. **Pasos para Solucionar**:
   - Revisar las capturas en `reports/screenshots/`
   - Verificar los logs en el reporte HTML
   - Consultar `docs/bug_report.md`

3. **Recomendaciones**:
   - Ejecutar en un ambiente limpio
   - Mantener ChromeDriver actualizado
   - Revisar reportes después de cada ejecución
   - Asegurar que el entorno virtual está activado
   - Verificar todas las dependencias instaladas

## Documentación

### Casos de Prueba

1. **Registro de Usuario**
   - Registro exitoso con datos válidos
   - Validación de nombre (mínimo 2 palabras)
   - Validación de formato de email
   - Validación de requisitos de contraseña
   - Validación de campos obligatorios
   - Validación de coincidencia de contraseñas

2. **Login de Usuario**
   - Login exitoso con credenciales válidas
   - Validación de campos obligatorios
   - Verificación de nombre de usuario
   - Funcionalidad de cierre de sesión

Para más detalles, consultar:
- [Casos de Prueba Detallados](docs/test_cases.md)
- [Reporte de Bugs](docs/bug_reports.md)

## Características

- Implementación del patrón Page Object Model
- Pruebas automatizadas de registro y login
- Generación de informes detallados en HTML
- Capturas de pantalla automáticas en caso de error
- Documentación completa de casos de prueba y bugs
- Validaciones robustas según requerimientos
