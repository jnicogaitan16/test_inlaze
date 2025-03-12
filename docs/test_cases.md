# Documentación de Casos de Prueba

## Pruebas de Registro

### CP-R01: Registro de Usuario Válido
- **Descripción**: Verificar que un usuario puede registrarse exitosamente con información válida
- **Precondiciones**: Usuario está en la página de registro
- **Pasos de Prueba**:
  1. Ingresar nombre completo válido (nombre y apellido)
  2. Ingresar dirección de correo electrónico válida
  3. Ingresar contraseña válida que cumpla todos los requisitos
  4. Confirmar contraseña
  5. Hacer clic en el botón de registro
- **Resultado Esperado**: Usuario se registra exitosamente y es redirigido a la página de inicio de sesión
- **Datos de Prueba**: 
  - Nombre: Generado dinámicamente (dos palabras)
  - Email: Correo electrónico válido generado dinámicamente
  - Contraseña: Cumple todos los requisitos (8+ caracteres, mayúscula, minúscula, número, carácter especial)

### CP-R02: Validación de Nombre
- **Descripción**: Verificar que el campo nombre requiere al menos dos palabras
- **Pasos de Prueba**:
  1. Ingresar nombre de una sola palabra
  2. Llenar otros campos con datos válidos
  3. Enviar formulario
- **Resultado Esperado**: Formulario muestra mensaje de error sobre el requisito del nombre

### CP-R03: Validación de Fortaleza de Contraseña
- **Descripción**: Verificar cumplimiento de requisitos de contraseña
- **Pasos de Prueba**:
  1. Ingresar nombre y correo válidos
  2. Ingresar contraseña débil
  3. Enviar formulario
- **Resultado Esperado**: Sistema muestra error sobre requisitos de contraseña

### CP-R04: Validación de Coincidencia de Contraseñas
- **Descripción**: Verificar coincidencia en la confirmación de contraseña
- **Pasos de Prueba**:
  1. Ingresar nombre y correo válidos
  2. Ingresar contraseña válida
  3. Ingresar confirmación de contraseña diferente
  4. Enviar formulario
- **Resultado Esperado**: Sistema muestra error sobre no coincidencia de contraseñas

## Pruebas de Inicio de Sesión

### CP-L01: Inicio de Sesión Exitoso
- **Descripción**: Verificar inicio de sesión exitoso con credenciales válidas
- **Precondiciones**: Usuario está registrado
- **Pasos de Prueba**:
  1. Ingresar correo válido
  2. Ingresar contraseña correcta
  3. Hacer clic en botón de inicio de sesión
- **Resultado Esperado**: Usuario inicia sesión y ve su nombre

### CP-L02: Validación de Campos Vacíos
- **Descripción**: Verificar validación de formulario para campos vacíos
- **Pasos de Prueba**:
  1. Dejar todos los campos vacíos
  2. Hacer clic en botón de inicio de sesión
- **Resultado Esperado**: Formulario muestra errores de validación

### CP-L03: Credenciales Inválidas
- **Descripción**: Verificar respuesta del sistema ante intentos de inicio de sesión inválidos
- **Pasos de Prueba**:
  1. Ingresar correo y contraseña inválidos
  2. Hacer clic en botón de inicio de sesión
- **Resultado Esperado**: Sistema muestra error de credenciales inválidas

### CP-L04: Funcionalidad de Cierre de Sesión
- **Descripción**: Verificar funcionalidad de cierre de sesión
- **Precondiciones**: Usuario ha iniciado sesión
- **Pasos de Prueba**:
  1. Hacer clic en botón de cierre de sesión
- **Resultado Esperado**: Usuario cierra sesión y es redirigido a página de inicio de sesión
