import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from tests.page_objects.login_page import LoginPage
from tests.page_objects.register_page import RegisterPage
from tests.utils.test_data import TestDataGenerator, get_login_test_data

class TestLogin:
    """Pruebas de funcionalidad de inicio de sesión"""

    def test_password_field_input(self, driver):
        """Verificar las validaciones del campo de contraseña"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        test_data = get_login_test_data()
        valid_user = test_data['valid_user']
        
        for validation in test_data['password_validations']:
            success, error = login_page.login(valid_user['email'], validation['password'])
            assert not success, f"El login fue exitoso con contraseña inválida: {validation['password']}"
            assert validation['expected_error'] in error, \
                f"Error esperado: {validation['expected_error']}, Error obtenido: {error}"
        
        password = valid_user['password']
        login_page.type_text(*login_page.PASSWORD_INPUT, password)
        input_value = login_page.get_element_attribute(*login_page.PASSWORD_INPUT, "value")
        assert input_value == password, \
            f"Error en el campo de contraseña. Esperado: {password}, Obtenido: {input_value}"

    @pytest.mark.parametrize("email,password,expected_error", [
        ("", "", "Todos los campos son obligatorios"),
        ("test@example.com", "", "La contraseña es obligatoria"),
        ("", "Password123!", "El correo electrónico es obligatorio"),
        ("correo.invalido", "Password123!", "El formato del correo electrónico no es válido"),
        ("test@example.com", "123", "La contraseña debe tener al menos 8 caracteres"),
        ("test@example.com", "password", "La contraseña debe contener al menos una mayúscula"),
        ("test@example.com", "PASSWORD", "La contraseña debe contener al menos una minúscula"),
        ("test@example.com", "Password", "La contraseña debe contener al menos un número"),
        ("test@example.com", "Password123", "La contraseña debe contener al menos un carácter especial")
    ])
    def test_login_validation(self, driver, email, password, expected_error):
        """Verificar las validaciones del formulario de inicio de sesión"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        success, error_msg = login_page.login(email, password)
        
        assert not success, "El inicio de sesión no debería ser exitoso con datos inválidos"
        assert error_msg and expected_error.lower() in error_msg.lower(), \
            f"Error esperado: {expected_error}, Error obtenido: {error_msg}"

    def test_invalid_credentials(self, driver):
        """Verificar el manejo de credenciales inválidas"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        test_data = get_login_test_data()['invalid_credentials']
        success, error_msg = login_page.login(test_data['email'], test_data['password'])
        
        assert not success, "El inicio de sesión no debería ser exitoso con credenciales inválidas"
        assert error_msg and "Las credenciales ingresadas no son válidas" in error_msg, \
            f"Error inesperado: {error_msg}"

    def test_logout_functionality(self, driver):
        """Verificar la funcionalidad de cierre de sesión"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        datos_usuario = TestDataGenerator.generar_usuario_prueba()
        success, _ = register_page.register(
            datos_usuario['name'],
            datos_usuario['email'],
            datos_usuario['password'],
            datos_usuario['password']
        )
        assert success, "No se pudo registrar el usuario de prueba. Por favor, verifica los datos e intenta nuevamente."
        
        login_page = LoginPage(driver)
        login_page.navigate()
        success, _ = login_page.login(datos_usuario['email'], datos_usuario['password'])
        assert success, "No se pudo iniciar sesión con las credenciales proporcionadas. Por favor, verifica e intenta nuevamente."
        
        nombre_mostrado = login_page.get_user_name()
        assert nombre_mostrado == datos_usuario['name'], \
            f"El nombre mostrado no coincide. Esperado: {datos_usuario['name']}, Obtenido: {nombre_mostrado}"
        
        login_page.logout()
        assert login_page._wait_for_condition(
            EC.url_contains("/sign-in"),
            message="No se pudo redireccionar a la página de inicio de sesión"
        )
        
        try:
            assert not login_page.get_user_name(), "La sesión no se cerró correctamente. El nombre de usuario sigue siendo visible."
        except TimeoutException:
            pass

    def test_navigation_to_register(self, driver):
        """Verificar la navegación entre páginas de registro e inicio de sesión"""
        login_page = LoginPage(driver)
        login_page.navigate()
        
        login_page.go_to_register()
        
        assert login_page._wait_for_condition(
            EC.url_contains("/sign-up"),
            message="No se pudo navegar a la página de registro"
        ), "No se pudo completar la navegación a la página de registro"
