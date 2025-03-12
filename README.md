Pruebas Automatizadas - Inlaze QA Test

Framework de pruebas automatizadas para el sistema de autenticación de Inlaze utilizando Selenium con Python.

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

### Comandos Básicos

1. Ejecutar todas las pruebas:
```bash
# Desde el directorio raíz del proyecto
python3 -m pytest tests/
```

2. Ejecutar con reporte HTML detallado:
```bash
python -m pytest tests/ --html=reports/report.html --self-contained-html
```

3. Ejecutar pruebas específicas:
```bash
# Ejecutar solo pruebas de login
python -m pytest tests/test_login.py

# Ejecutar solo pruebas de registro
python -m pytest tests/test_registration.py
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

### Ubicación de Reportes

Después de la ejecución, encontrarás:
- Reporte HTML: `reports/report.html`
- Capturas de pantalla de errores: `reports/screenshots/`

### Solución de Problemas

Si encuentras errores de importación, asegúrate de:
1. Tener el entorno virtual activado
2. Estar en el directorio raíz del proyecto
3. Tener todas las dependencias instaladas correctamente

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
