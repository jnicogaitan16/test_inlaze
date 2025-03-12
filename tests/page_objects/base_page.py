import os
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)

class BasePage:
    BASE_URL = "https://test-qa.inlaze.com"
    ANGULAR_APP_LOADED = (By.CSS_SELECTOR, "app-root:not(:empty)")
    AUTH_PATH = "/auth"
    TIMEOUT = 10
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)
    
    def _wait_for_condition(self, condition, timeout=None, message=None):
        """Esperar hasta que se cumpla una condición en la página

        Args:
            condition: Condición a esperar (expected_condition)
            timeout: Tiempo máximo de espera en segundos (por defecto: TIMEOUT)
            message: Mensaje personalizado en caso de error

        Returns:
            El elemento o resultado esperado cuando se cumple la condición

        Raises:
            TimeoutException: Si la condición no se cumple en el tiempo especificado.
                             Se incluye captura de pantalla del error.
                             
        Note:
            Si no se especifica un mensaje de error, se usará uno genérico.
            La captura de pantalla se guarda en el directorio de reportes.
        """
        try:
            return self.wait.until(condition)
        except TimeoutException as e:
            screenshot_path = self.take_screenshot()
            error_msg = message or "La operación no se completó en el tiempo esperado"
            raise TimeoutException(
                f"{error_msg}\n" 
                f"Se ha guardado una captura de pantalla: {screenshot_path}\n"
                f"Por favor, verifica que la página esté cargada correctamente."
            ) from e
    
    def navigate_to(self, path):
        """Navegar a una ruta específica de la aplicación

        Args:
            path: Ruta relativa a navegar

        Raises:
            TimeoutException: Si la navegación no se completa correctamente
        """
        self.driver.get(f"{self.BASE_URL}{path}")
        
        # Esperar a que la aplicación Angular cargue
        self._wait_for_condition(
            EC.presence_of_element_located(self.ANGULAR_APP_LOADED),
            message="La aplicación Angular no cargó correctamente"
        )
        
        # Verificar que estamos en la ruta correcta
        self._wait_for_condition(
            EC.url_contains(path),
            message=f"Error al navegar a la página {path}"
        )

    def find_element(self, by, value):
        """Encontrar un elemento en la página

        Args:
            by: Método de localización (By.ID, By.XPATH, etc.)
            value: Valor del localizador

        Returns:
            WebElement encontrado

        Raises:
            TimeoutException: Si el elemento no se encuentra
        """
        return self._wait_for_condition(
            EC.presence_of_element_located((by, value)),
            message=f"No se encontró el elemento: {value}"
        )

    def find_clickable_element(self, by, value):
        """Encontrar un elemento clickeable en la página

        Args:
            by: Método de localización (By.ID, By.XPATH, etc.)
            value: Valor del localizador

        Returns:
            WebElement clickeable

        Raises:
            TimeoutException: Si el elemento no se encuentra o no es clickeable
        """
        return self._wait_for_condition(
            EC.element_to_be_clickable((by, value)),
            message=f"El elemento no está disponible para hacer clic: {value}"
        )

    def click_element(self, by, value):
        """Hacer clic en un elemento de la página

        Args:
            by: Método de localización (By.ID, By.XPATH, etc.)
            value: Valor del localizador

        Raises:
            TimeoutException: Si el elemento no se encuentra o no es clickeable
            WebDriverException: Si ocurre un error al hacer clic
        """
        element = self.find_clickable_element(by, value)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Intentar clic mediante JavaScript si el clic normal falla
            self.driver.execute_script("arguments[0].click();", element)
            self._wait_for_condition(
                lambda _: True,  # Esperar un momento para asegurar que el clic se procesó
                message=f"No se pudo hacer clic en el elemento: {value}"
            )

    def type_text(self, by, value, text):
        """Escribir texto en un campo de entrada

        Args:
            by: Método de localización (By.ID, By.XPATH, etc.)
            value: Valor del localizador
            text: Texto a escribir

        Raises:
            TimeoutException: Si el elemento no se encuentra
            WebDriverException: Si no se puede escribir en el elemento
        """
        element = self.find_element(by, value)
        try:
            # Asegurarse de que el elemento es interactuable
            self._wait_for_condition(
                lambda _: element.is_enabled() and element.is_displayed(),
                message=f"El campo {value} no está disponible para escribir"
            )
            
            # Limpiar el campo usando JavaScript
            self.driver.execute_script("arguments[0].value = '';", element)
            
            # Escribir el texto usando JavaScript para campos de contraseña
            if element.get_attribute("type") == "password":
                self.driver.execute_script(f"arguments[0].value = '{text}';", element)
            else:
                element.send_keys(text)
                
            # Verificar que el texto se escribió correctamente
            actual_value = element.get_attribute("value")
            if actual_value != text:
                raise Exception(f"El texto no se escribió correctamente. Esperado: {text}, Obtenido: {actual_value}")
                
        except Exception as e:
            self.take_screenshot("error_type_text")
            raise Exception(f"No se pudo escribir en el campo {value}: {str(e)}")

    def get_element_text(self, by, value):
        return self.find_element(by, value).text.strip()

    def get_element_attribute(self, by, value, attribute):
        return self.find_element(by, value).get_attribute(attribute)

    def get_error_message(self):
        """Obtener mensaje de error visible en la página

        Returns:
            str: Mensaje de error formateado o None si no hay error

        Note:
            - Busca mensajes en elementos con clases de error estándar
            - Formatea múltiples errores de forma legible
            - Traduce mensajes comunes al español
            - Prioriza mensajes específicos sobre genéricos
        """
        try:
            error_elements = self._wait_for_condition(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".error-message, .alert-error, .form-error, .validation-error")),
                message="No se encontraron mensajes de error en la página"
            )
            
            # Filtrar y formatear errores
            errors = [elem.text.strip() for elem in error_elements if elem.text.strip()]
            if not errors:
                return None
                
            # Si hay múltiples errores, combinarlos de forma legible
            if len(errors) > 1:
                return "Se encontraron los siguientes errores:\n- " + "\n- ".join(errors)
            
            error_msg = errors[0].lower()
            
            # Mapeo de mensajes de error comunes
            error_mapping = {
                "required": "Por favor, completa todos los campos obligatorios",
                "email is required": "Por favor, ingresa tu correo electrónico",
                "password is required": "Por favor, ingresa tu contraseña",
                "invalid email": "El formato del correo electrónico no es válido",
                "invalid credentials": "Las credenciales ingresadas no son válidas",
                "passwords do not match": "Las contraseñas ingresadas no coinciden",
                "name is required": "Ingresa tu nombre y apellido",
                "email already registered": "Este correo electrónico ya está registrado en el sistema"
            }
            
            # Mensajes de validación de contraseña
            if "password" in error_msg:
                if "8 characters" in error_msg:
                    return "La contraseña debe tener al menos 8 caracteres"
                if "uppercase" in error_msg:
                    return "La contraseña debe contener al menos una mayúscula"
                if "lowercase" in error_msg:
                    return "La contraseña debe contener al menos una minúscula"
                if "number" in error_msg:
                    return "La contraseña debe contener al menos un número"
                if "special" in error_msg:
                    return "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)"
            
            # Buscar coincidencias en el mapeo de errores
            for key, value in error_mapping.items():
                if key in error_msg:
                    return value
            
            return errors[0]
        except TimeoutException:
            return None

    def wait_for_url_contains(self, text):
        try:
            return bool(self._wait_for_condition(
                EC.url_contains(text),
                message=f"URL no contiene: {text}"
            ))
        except TimeoutException:
            return False

    def wait_for_element_visible(self, by, value):
        return self._wait_for_condition(
            EC.visibility_of_element_located((by, value)),
            message=f"Elemento no visible: {value}"
        )

    def take_screenshot(self, nombre_base=None):
        """Tomar una captura de pantalla

        Args:
            nombre_base: Nombre base para el archivo (opcional)

        Returns:
            str: Ruta relativa donde se guardó la captura

        Note:
            - Las capturas se guardan en reports/screenshots
            - El nombre del archivo incluye timestamp para evitar duplicados
            - Si no se especifica nombre_base, se usa el nombre del test actual
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_base = nombre_base or self.driver.test_name or 'test'
        nombre_archivo = f"error_{nombre_base}_{timestamp}.png"
        ruta_screenshot = os.path.join('reports', 'screenshots', nombre_archivo)
        self.driver.save_screenshot(ruta_screenshot)
        return ruta_screenshot
