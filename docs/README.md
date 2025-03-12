# Prueba de Automatización QA Inlaze

Este repositorio contiene pruebas automatizadas para el sistema de autenticación de Inlaze utilizando Selenium con Python.

## Estructura del Proyecto

```
inlaze-qa-test/
├── tests/              # Casos de prueba
├── page_objects/       # Clases del Modelo de Objetos de Página
├── utils/             # Funciones auxiliares y utilidades
├── reports/           # Informes de ejecución de pruebas
├── requirements.txt   # Dependencias del proyecto
└── README.md         # Documentación del proyecto
```

## Requisitos

- Python 3.8+
- Chrome browser
- ChromeDriver

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/inlaze-qa-test.git
cd inlaze-qa-test
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar Pruebas

Para ejecutar todas las pruebas:
```bash
python -m pytest tests/
```

Para generar un informe HTML:
```bash
python -m pytest tests/ --html=reports/report.html
```

## Documentación de Casos de Prueba

La documentación detallada de los casos de prueba se puede encontrar en el archivo [Documentación de Casos de Prueba](./test_cases.md).

## Informes de Errores

Los errores encontrados durante las pruebas están documentados en el archivo [Informes de Errores](./bug_reports.md).
