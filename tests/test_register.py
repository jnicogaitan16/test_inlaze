import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from tests.page_objects.register_page import RegisterPage
from tests.utils.test_data import TestDataGenerator

class TestRegister:
    """Pruebas de funcionalidad de registro de usuarios"""

    def test_password_match_validation(self, driver):
        """Verificar la validación de coincidencia de contraseñas"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        success, message = register_page.register(
            "Nicolas Gaitan",  # Nombre con mayúsculas iniciales
            "jnicogaitan@gmail.com",
            "Password1*",
            "DifferentPass1*"
        )
        
        assert not success, "El registro fue exitoso con contraseñas que no coinciden"
        assert "coinciden" in message.lower(), \
            f"Mensaje de error incorrecto\nEsperado: 'Las contraseñas ingresadas no coinciden'\nRecibido: {message}"
        assert register_page._wait_for_condition(
            EC.url_contains("/sign-in"),
            message="No se pudo verificar la redirección después del registro. Por favor, verifica la URL."
        )

    @pytest.mark.parametrize("name,email,password,confirm_password,expected_error", [
        ("", "", "", "", "Todos los campos son obligatorios"),
        ("John", "", "", "", "El nombre debe contener nombre y apellido"),
        ("John Doe", "", "", "", "El correo electrónico es obligatorio"),
        ("John Doe", "invalid", "", "", "El formato del correo electrónico no es válido"),
        ("John Doe", "test@example.com", "short", "short", "La contraseña debe tener al menos 8 caracteres"),
        ("John Doe", "test@example.com", "password123", "password123", "La contraseña debe contener al menos una mayúscula"),
        ("John Doe", "test@example.com", "Password123", "Password123", "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)"),
        ("John Doe", "test@example.com", "Password123!", "Password124!", "Las contraseñas no coinciden")
    ])
    def test_registration_validation(self, driver, name, email, password, confirm_password, expected_error):
        """Verificar las validaciones del formulario de registro con diferentes casos"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        success, error_msg = register_page.register(name, email, password, confirm_password)
        
        assert not success, f"El registro fue exitoso con datos inválidos:\nNombre: {name}\nCorreo: {email}"
        assert error_msg and expected_error.lower() in error_msg.lower(), \
            f"Validación incorrecta\nEsperado: {expected_error}\nObtenido: {error_msg}"

    def test_duplicate_email_registration(self, driver):
        """Verificar que no se permita registrar un correo electrónico duplicado"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        # Primer registro con datos válidos
        user_data = TestDataGenerator.generar_usuario_prueba()
        success, mensaje = register_page.register(
            user_data['name'],
            user_data['email'],
            user_data['password'],
            user_data['password']
        )
        assert success, f"No se pudo completar el registro con datos válidos\nError: {mensaje}\nPor favor, verifica los datos e intenta nuevamente."
        
        # Intentar registrar el mismo correo con diferentes datos
        register_page.navigate()
        success, error_msg = register_page.register(
            "Otro Usuario",
            user_data['email'],
            "OtroPass123!",
            "OtroPass123!"
        )
        
        assert not success, "El registro permitió un correo electrónico que ya está en uso"
        assert error_msg and "correo electrónico ya está registrado" in error_msg.lower(), \
            f"Validación incorrecta de correo duplicado\nEsperado: 'Este correo electrónico ya está registrado en el sistema'\nObtenido: {error_msg}"

    def test_password_requirements(self, driver):
        """Verificar los requisitos de seguridad para las contraseñas"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        user_data = TestDataGenerator.generar_usuario_prueba()
        test_cases = [
            ("short", "La contraseña debe tener al menos 8 caracteres"),
            ("password123", "La contraseña debe contener al menos una mayúscula"),
            ("PASSWORD123", "La contraseña debe contener al menos una minúscula"),
            ("Password", "La contraseña debe contener al menos un número"),
            ("Password123", "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{|}|<>)"),
            ("Password123!", None)  # Caso válido
        ]
        
        for password, expected_error in test_cases:
            success, error_msg = register_page.register(
                user_data['name'],
                user_data['email'],
                password,
                password
            )
            
            if expected_error:
                assert not success, \
                    f"El registro fue exitoso con una contraseña inválida: {password}"
                assert error_msg and expected_error.lower() in error_msg.lower(), \
                    f"Validación incorrecta para '{password}'\nEsperado: {expected_error}\nObtenido: {error_msg}"
            else:
                assert success, \
                    f"El registro falló con una contraseña que cumple todos los requisitos: {password}"
            
            register_page.navigate()

    def test_navigation_to_login(self, driver):
        """Verificar la navegación desde registro hacia inicio de sesión"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        register_page.go_to_login()
        
        assert register_page._wait_for_condition(
            EC.url_contains("/sign-in"),
            message="No se pudo navegar a la página de inicio de sesión. Por favor, verifica la URL e intenta nuevamente."
        ), "No se pudo completar la navegación a la página de inicio de sesión. Por favor, verifica la conexión e intenta nuevamente."
