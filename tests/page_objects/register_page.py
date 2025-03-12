from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class RegisterPage(BasePage):
    REGISTER_FORM = (By.CSS_SELECTOR, "app-sign-up-form form")
    NAME_INPUT = (By.CSS_SELECTOR, "app-sign-up-form input[formcontrolname='name']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "app-sign-up-form input[formcontrolname='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "app-sign-up-form app-password input[type='password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "app-sign-up-form app-password:nth-child(2) input[type='password']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "app-sign-up-form button[type='submit']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='/sign-in'], a[href*='/login']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-error, mat-error")
    NAME_ERROR = (By.CSS_SELECTOR, ".error-message:contains('nombre'), mat-error:contains('nombre')")
    EMAIL_ERROR = (By.CSS_SELECTOR, ".error-message:contains('correo'), mat-error:contains('correo')")
    PASSWORD_ERROR = (By.CSS_SELECTOR, ".error-message:contains('contraseña'), mat-error:contains('contraseña')")
    PASSWORD_REQUIREMENTS = (By.CSS_SELECTOR, ".password-requirements")
    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "app-sign-up-form app-password:first-of-type button")
    SHOW_CONFIRM_PASSWORD_BUTTON = (By.CSS_SELECTOR, "app-sign-up-form app-password:last-of-type button")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        self.navigate_to(f"{self.AUTH_PATH}/sign-up")
        self._wait_for_condition(
            EC.presence_of_element_located(self.REGISTER_FORM),
            message="No se pudo cargar el formulario de registro"
        )

    def register(self, name, email, password, confirm_password):
        """Registrar un nuevo usuario con validaciones completas
        
        Args:
            name: Nombre completo del usuario (nombre y apellido)
            email: Correo electrónico válido
            password: Contraseña que cumpla requisitos de seguridad
            confirm_password: Confirmación exacta de la contraseña
            
        Returns:
            tuple: (bool, str)
                - bool: True si el registro fue exitoso
                - str: Mensaje descriptivo del resultado o error
                
        Note:
            La contraseña debe cumplir con:
            - Mínimo 8 caracteres
            - Al menos una mayúscula
            - Al menos una minúscula
            - Al menos un número
            - Al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)
        """
        try:
            # Validación inicial de campos obligatorios
            if not all([name, email, password, confirm_password]):
                return False, "Todos los campos son obligatorios"

            # Validación y entrada del nombre
            try:
                self.type_text(*self.NAME_INPUT, name)
                name_error = self.validate_name_format()
                if name_error:
                    return False, name_error
            except Exception as e:
                self.take_screenshot("error_nombre_registro")
                return False, f"Error al procesar el nombre: {str(e)}"

            # Validación y entrada del correo
            try:
                self.type_text(*self.EMAIL_INPUT, email)
                email_error = self.validate_email_format()
                if email_error:
                    return False, email_error
            except Exception as e:
                self.take_screenshot("error_email_registro")
                return False, f"Error al procesar el correo electrónico: {str(e)}"

            # Validación y entrada de la contraseña
            try:
                self.type_text(*self.PASSWORD_INPUT, password)
                password_error = self.validate_password_requirements()
                if password_error:
                    return False, password_error
            except Exception as e:
                self.take_screenshot("error_password_registro")
                return False, f"Error al procesar la contraseña: {str(e)}"

            # Validación y entrada de la confirmación de contraseña
            try:
                self.type_text(*self.CONFIRM_PASSWORD_INPUT, confirm_password)
                confirm_error = self.validate_passwords_match(password, confirm_password)
                if confirm_error:
                    return False, confirm_error
            except Exception as e:
                self.take_screenshot("error_confirm_password_registro")
                return False, f"Error al procesar la confirmación de contraseña: {str(e)}"

            # Envío del formulario y validación del resultado
            try:
                self.click_element(*self.REGISTER_BUTTON)
                
                # Esperar redirección exitosa
                if self._wait_for_condition(
                    EC.url_contains("/sign-in"),
                    timeout=10,
                    message="Error al redireccionar después del registro"
                ):
                    return True, "Registro exitoso. Ya puedes iniciar sesión con tu correo y contraseña."
                
                # Verificar mensajes de error
                error = self.get_error_message()
                if error:
                    if "correo" in error.lower() and "registrado" in error.lower():
                        return False, "Este correo electrónico ya está registrado en el sistema"
                    if "error" in error.lower() and "inesperado" in error.lower():
                        return False, "Ha ocurrido un error en el servidor. Por favor, intenta más tarde."
                    return False, error
                
                # Verificar si seguimos en el formulario
                if self._wait_for_condition(
                    EC.presence_of_element_located(self.REGISTER_FORM),
                    timeout=2
                ):
                    return False, "No se pudo completar el registro. Por favor, verifica todos los campos."
                    
                return False, "Ha ocurrido un error durante el registro. Por favor, intenta nuevamente."
                
            except TimeoutException:
                self.take_screenshot("error_timeout_registro")
                return False, "Error de conexión. Por favor, verifica tu internet e intenta nuevamente."
            except Exception as e:
                self.take_screenshot("error_submit_registro")
                return False, f"Error al enviar el formulario: {str(e)}"
            
        except Exception as e:
            self.take_screenshot("error_registro_general")
            return False, f"Ha ocurrido un error inesperado: {str(e)}. Por favor, intenta más tarde."

    def validate_name_format(self):
        """Validar formato del nombre completo
        
        Returns:
            str: Mensaje de error o None si es válido
            
        Note:
            El nombre debe:
            - No estar vacío
            - Contener nombre y apellido
            - Solo contener letras (sin números ni caracteres especiales)
        """
        try:
            name = self.get_element_attribute(*self.NAME_INPUT, "value")
            if not name or not name.strip():
                return "El nombre es obligatorio"
            
            words = [w for w in name.split() if w.strip()]
            if len(words) < 2:
                return "El nombre debe contener nombre y apellido"
                
            if any(not w.replace(' ', '').isalpha() for w in words):
                return "El nombre solo puede contener letras"
                
            return None
        except Exception:
            return "Error al validar el formato del nombre"

    def validate_email_format(self):
        """Validar formato del correo electrónico
        
        Returns:
            str: Mensaje de error o None si es válido
        """
        try:
            email = self.get_element_attribute(*self.EMAIL_INPUT, "value")
            if not email or not email.strip():
                return "El correo electrónico es obligatorio"
                
            import re
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(email):
                return "El formato del correo electrónico no es válido"
                
            return None
        except Exception:
            return "Error al validar el formato del correo electrónico"

    def validate_password_requirements(self):
        """Validar requisitos de seguridad de la contraseña
        
        Returns:
            str: Mensaje de error o None si cumple todos los requisitos
        """
        password = self.get_element_attribute(*self.PASSWORD_INPUT, "value")
        if not password:
            return "Por favor, ingresa tu contraseña"
            
        requirements = [
            (len(password) >= 8, "La contraseña debe tener al menos 8 caracteres"),
            (any(c.isupper() for c in password), "La contraseña debe contener al menos una mayúscula"),
            (any(c.islower() for c in password), "La contraseña debe contener al menos una minúscula"),
            (any(c.isdigit() for c in password), "La contraseña debe contener al menos un número"),
            (any(c in "!@#$%^&*(),.?\":{|}|<>" for c in password), "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)"),
        ]
        
        for requirement_met, error_message in requirements:
            if not requirement_met:
                return error_message
                
        return None

    def validate_passwords_match(self, password, confirm_password):
        """Validar que las contraseñas coincidan
        
        Args:
            password: Contraseña original
            confirm_password: Confirmación de contraseña
            
        Returns:
            str: Mensaje de error o None si coinciden
        """
        if not confirm_password:
            return "Por favor, confirma tu contraseña"
            
        return "Las contraseñas no coinciden" if password != confirm_password else None

    def go_to_login(self):
        """Navegar a la página de inicio de sesión"""
        try:
            self._wait_for_condition(
                EC.element_to_be_clickable(self.LOGIN_LINK),
                timeout=5,
                message="El enlace de inicio de sesión no está disponible"
            )
            self.click_element(*self.LOGIN_LINK)
            self._wait_for_condition(
                EC.url_contains("/sign-in"),
                message="No se pudo redireccionar a la página de inicio de sesión"
            )
        except TimeoutException:
            self.driver.get(f"{self.BASE_URL}{self.AUTH_PATH}/sign-in")

    def are_fields_empty(self):
        name = self.get_element_attribute(*self.NAME_INPUT, "value")
        email = self.get_element_attribute(*self.EMAIL_INPUT, "value")
        password = self.get_element_attribute(*self.PASSWORD_INPUT, "value")
        confirm = self.get_element_attribute(*self.CONFIRM_PASSWORD_INPUT, "value")
        return not any([name, email, password, confirm])

    def get_field_errors(self):
        """Obtener todos los errores de validación de los campos
        
        Returns:
            dict: Diccionario con los errores por campo
            
        Note:
            Los errores se formatean de manera amigable y clara
            para el usuario final
        """
        errors = {}
        field_mapping = [
            ('nombre', self.NAME_ERROR, 'nombre completo'),
            ('email', self.EMAIL_ERROR, 'correo electrónico'),
            ('contraseña', self.PASSWORD_ERROR, 'contraseña')
        ]
        
        for field_id, locator, field_name in field_mapping:
            try:
                error = self.get_element_text(*locator)
                if error:
                    if "required" in error.lower():
                        errors[field_id] = f"Por favor, ingresa tu {field_name}"
                    elif "invalid" in error.lower():
                        errors[field_id] = f"El {field_name} no es válido"
                    else:
                        errors[field_id] = error
            except TimeoutException:
                continue
                
        return errors

    def is_register_button_enabled(self):
        """Verificar si el botón de registro está habilitado"""
        return self.is_element_enabled(*self.REGISTER_BUTTON)
