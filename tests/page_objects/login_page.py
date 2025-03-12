from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class LoginPage(BasePage):
    LOGIN_FORM = (By.CSS_SELECTOR, "app-sign-in-form form")
    EMAIL_INPUT = (By.CSS_SELECTOR, "app-sign-in-form input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "app-sign-in-form app-password input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "app-sign-in-form button[type='submit']")
    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "app-sign-in-form app-password button")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href*='/sign-up'], a[href*='/registro']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-error, mat-error")
    USER_NAME_DISPLAY = (By.CSS_SELECTOR, ".user-name")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".logout-btn")
    PASSWORD_ERROR = (By.CSS_SELECTOR, ".error-message:contains('contraseña'), mat-error:contains('contraseña')")
    EMAIL_ERROR = (By.CSS_SELECTOR, ".error-message:contains('correo'), mat-error:contains('correo')")
    INVALID_CREDENTIALS_ERROR = (By.CSS_SELECTOR, ".error-message:contains('credenciales'), .alert-error:contains('credenciales')")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        """Navegar a la página de inicio de sesión y esperar que cargue"""
        self.navigate_to(f"{self.AUTH_PATH}/sign-in")
        
        try:
            # Esperar que el componente Angular cargue
            self._wait_for_condition(
                EC.presence_of_element_located(self.LOGIN_FORM),
                message="No se pudo cargar el componente de inicio de sesión"
            )
            
            # Esperar que los campos estén presentes y sean interactuables
            self._wait_for_condition(
                EC.presence_of_element_located(self.EMAIL_INPUT),
                message="No se encontró el campo de correo electrónico"
            )
            self._wait_for_condition(
                EC.presence_of_element_located(self.PASSWORD_INPUT),
                message="No se encontró el campo de contraseña"
            )
            
            # Verificar que los campos sean interactuables
            email_input = self.find_element(*self.EMAIL_INPUT)
            password_input = self.find_element(*self.PASSWORD_INPUT)
            
            assert email_input.is_enabled(), "El campo de correo electrónico está deshabilitado"
            assert password_input.is_enabled(), "El campo de contraseña está deshabilitado"
            
        except Exception as e:
            self.take_screenshot("error_login_page_load")
            raise Exception(f"Error al cargar la página de inicio de sesión: {str(e)}")

    def login(self, email, password):
        """Realizar el inicio de sesión con las credenciales proporcionadas
        
        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            
        Returns:
            tuple: (bool, str)
                - bool: True si el inicio de sesión fue exitoso
                - str: Mensaje de éxito o error
        """
        try:
            # Validar campos vacíos
            if not email and not password:
                return False, "Todos los campos son obligatorios"
            elif not email:
                return False, "El correo electrónico es obligatorio"
            elif not password:
                return False, "La contraseña es obligatoria"

            # Validar formato del correo
            email_error = self.validate_email_format(email)
            if email_error:
                return False, email_error

            # Validar formato de la contraseña
            password_error = self.validate_password_format(password)
            if password_error:
                return False, password_error

            # Ingresar credenciales
            self.type_text(*self.EMAIL_INPUT, email)
            self.type_text(*self.PASSWORD_INPUT, password)
            self.click_element(*self.LOGIN_BUTTON)
            
            # Verificar mensajes de error de validación
            error_msg = self.get_error_message()
            if error_msg:
                return False, error_msg
                
            try:
                # Verificar inicio de sesión exitoso
                self._wait_for_condition(
                    EC.presence_of_element_located(self.USER_NAME_DISPLAY),
                    message="No se pudo verificar el inicio de sesión"
                )
                return True, "Inicio de sesión exitoso"
            except TimeoutException:
                # Intentar obtener el mensaje de error de credenciales inválidas
                try:
                    error = self._wait_for_condition(
                        EC.presence_of_element_located(self.INVALID_CREDENTIALS_ERROR),
                        timeout=2,
                        message="Las credenciales ingresadas no son válidas"
                    ).text
                    return False, error
                except TimeoutException:
                    # Si no hay mensaje de credenciales inválidas, buscar otros errores
                    error = self.get_error_message()
                    if error:
                        return False, error
                    return False, "Las credenciales ingresadas no son válidas"
                
        except Exception:
            self.take_screenshot("error_login")
            return False, "Ha ocurrido un error inesperado. Por favor, intenta nuevamente"

    def get_user_name(self):
        return self.get_element_text(*self.USER_NAME_DISPLAY)

    def logout(self):
        """Cerrar la sesión actual del usuario"""
        self.click_element(*self.LOGOUT_BUTTON)
        self._wait_for_condition(EC.url_contains("/sign-in"))

    def go_to_register(self):
        """Navegar a la página de registro"""
        try:
            # Esperar a que el enlace sea visible y hacer clic
            self._wait_for_condition(
                EC.element_to_be_clickable(self.REGISTER_LINK),
                timeout=5,
                message="El enlace de registro no está disponible"
            )
            self.click_element(*self.REGISTER_LINK)
            self._wait_for_condition(EC.url_contains("/registro"))
        except TimeoutException:
            # Si el enlace no está visible, intentar navegar directamente
            self.driver.get(f"{self.BASE_URL}/registro")

    def are_fields_empty(self):
        email = self.get_element_attribute(*self.EMAIL_INPUT, "value")
        password = self.get_element_attribute(*self.PASSWORD_INPUT, "value")
        return not email and not password

    def get_field_validation_state(self, field_locator):
        """Obtener el estado de validación de un campo
        
        Args:
            field_locator: Tupla con el método de localización y el valor
            
        Returns:
            dict: Estado del campo con valor, validez y mensaje de error
        """
        element = self.find_element(*field_locator)
        return {
            'valor': element.get_attribute('value'),
            'es_valido': 'ng-invalid' not in (element.get_attribute('class') or ''),
            'mensaje_error': self.get_error_message()
        }

    def is_login_button_enabled(self):
        return self.find_element(*self.LOGIN_BUTTON).is_enabled()

    def validate_email_format(self, email):
        """Validar el formato del correo electrónico
        
        Args:
            email: Correo electrónico a validar
            
        Returns:
            str: Mensaje de error o None si es válido
        """
        if not email:
            return "El correo electrónico es obligatorio"
            
        if len(email) > 100:
            return "El correo electrónico no puede exceder los 100 caracteres"
            
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "El formato del correo electrónico no es válido"
            
        if email.count('@') > 1:
            return "El correo electrónico no puede contener más de un @"
            
        if '..' in email:
            return "El correo electrónico no puede contener puntos consecutivos"
            
        return None

    def validate_password_format(self, password):
        """Validar el formato de la contraseña
        
        Args:
            password: Contraseña a validar
            
        Returns:
            str: Mensaje de error o None si es válido
        """
        if not password:
            return "La contraseña es obligatoria"
            
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres"
            
        if len(password) > 50:
            return "La contraseña no puede exceder los 50 caracteres"
            
        if ' ' in password:
            return "La contraseña no puede contener espacios"
            
        if not any(c.isupper() for c in password):
            return "La contraseña debe contener al menos una mayúscula"
            
        if not any(c.islower() for c in password):
            return "La contraseña debe contener al menos una minúscula"
            
        if not any(c.isdigit() for c in password):
            return "La contraseña debe contener al menos un número"
            
        if not any(c in "!@#$%^&*(),.?\":{|}|<>" for c in password):
            return "La contraseña debe contener al menos un carácter especial"
            
        return None

    def get_error_message(self):
        """Obtener mensaje de error si existe
        
        Returns:
            str: Mensaje de error o None si no hay error
            
        Note:
            Los mensajes se traducen automáticamente al español y se
            formatean para mayor claridad
        """
        try:
            try:
                error = self.get_element_text(*self.INVALID_CREDENTIALS_ERROR)
                if error:
                    return "Las credenciales ingresadas no son válidas"
            except TimeoutException:
                pass

            try:
                error = self.get_element_text(*self.PASSWORD_ERROR)
                if error:
                    return error
            except TimeoutException:
                pass

            try:
                error = self.get_element_text(*self.EMAIL_ERROR)
                if error:
                    return error
            except TimeoutException:
                pass

            error = self.get_element_text(*self.ERROR_MESSAGE)
            if error:
                error_lower = error.lower()
            
            # Mapeo de mensajes de error
            error_mapping = {
                "invalid email": "El formato del correo electrónico no es válido",
                "invalid password": "La contraseña ingresada no cumple con los requisitos de seguridad",
                "invalid credentials": "Las credenciales ingresadas no son correctas. Por favor, verifica e intenta nuevamente",
                "email is required": "El correo electrónico es obligatorio",
                "password is required": "La contraseña es obligatoria",
                "all fields are required": "Por favor, completa todos los campos obligatorios",
                "password must be at least 8 characters": "La contraseña debe tener al menos 8 caracteres",
                "password must contain uppercase": "La contraseña debe contener al menos una letra mayúscula",
                "password must contain lowercase": "La contraseña debe contener al menos una letra minúscula",
                "password must contain number": "La contraseña debe contener al menos un número",
                "password must contain special": "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)"
            }
            
            # Buscar coincidencias en el mapeo de errores
            for key, value in error_mapping.items():
                if key in error_lower:
                    return value
                
            return error
        except TimeoutException:
            return None
