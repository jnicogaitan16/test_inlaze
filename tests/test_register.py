import pytest
from selenium.webdriver.support import expected_conditions as EC
from tests.page_objects.register_page import RegisterPage
from tests.utils.test_data import TestDataGenerator, get_registro_test_data

class TestRegister:
    """Pruebas de funcionalidad de registro de usuarios"""

    def test_password_match_validation(self, driver):
        """Verificar la validación de coincidencia de contraseñas"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        test_data = get_registro_test_data()['mismatched_passwords']
        success, message = register_page.register(
            test_data['name'],
            test_data['email'],
            test_data['password'],
            test_data['confirm_password']
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
        (TestDataGenerator.generar_nombre(1), "", "", "", "El nombre debe contener nombre y apellido"),
        (TestDataGenerator.generar_nombre(), "", "", "", "El correo electrónico es obligatorio"),
        (TestDataGenerator.generar_nombre(), "correo.invalido", "", "", "El formato del correo electrónico no es válido"),
        (TestDataGenerator.generar_nombre(), TestDataGenerator.generar_email(), TestDataGenerator.generar_password_invalido('longitud'), TestDataGenerator.generar_password_invalido('longitud'), "La contraseña debe tener al menos 8 caracteres"),
        (TestDataGenerator.generar_nombre(), TestDataGenerator.generar_email(), TestDataGenerator.generar_password_invalido('mayuscula'), TestDataGenerator.generar_password_invalido('mayuscula'), "La contraseña debe contener al menos una mayúscula"),
        (TestDataGenerator.generar_nombre(), TestDataGenerator.generar_email(), TestDataGenerator.generar_password_invalido('especial'), TestDataGenerator.generar_password_invalido('especial'), "La contraseña debe contener al menos un carácter especial"),
        (TestDataGenerator.generar_nombre(), TestDataGenerator.generar_email(), TestDataGenerator.generar_password_valido(), "Password124!", "Las contraseñas no coinciden")
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
        test_data = get_registro_test_data()['valid_user']
        success, mensaje = register_page.register(
            test_data['name'],
            test_data['email'],
            test_data['password'],
            test_data['confirm_password']
        )
        assert success, f"No se pudo completar el registro con datos válidos\nError: {mensaje}\nPor favor, verifica los datos e intenta nuevamente."
        
        # Intentar registrar el mismo correo con diferentes datos
        register_page.navigate()
        otro_usuario = TestDataGenerator.generar_usuario_prueba()
        success, error_msg = register_page.register(
            otro_usuario['name'],
            test_data['email'],  # Usar el mismo email del primer registro
            otro_usuario['password'],
            otro_usuario['password']
        )
        
        assert not success, "El registro permitió un correo electrónico que ya está en uso"
        assert error_msg and "correo electrónico ya está registrado" in error_msg.lower(), \
            f"Validación incorrecta de correo duplicado\nEsperado: 'Este correo electrónico ya está registrado en el sistema'\nObtenido: {error_msg}"

    def test_password_requirements(self, driver):
        """Verificar los requisitos de seguridad para las contraseñas"""
        register_page = RegisterPage(driver)
        register_page.navigate()
        
        # Usar datos de prueba válidos para el usuario
        test_data = get_registro_test_data()['valid_user']
        
        # Probar diferentes casos de contraseñas
        test_cases = [
            (TestDataGenerator.generar_password_invalido('longitud'), "La contraseña debe tener al menos 8 caracteres"),
            (TestDataGenerator.generar_password_invalido('mayuscula'), "La contraseña debe contener al menos una mayúscula"),
            (TestDataGenerator.generar_password_invalido('minuscula'), "La contraseña debe contener al menos una minúscula"),
            (TestDataGenerator.generar_password_invalido('numero'), "La contraseña debe contener al menos un número"),
            (TestDataGenerator.generar_password_invalido('especial'), "La contraseña debe contener al menos un carácter especial"),
            (test_data['password'], None)  # Caso válido
        ]
        
        for password, expected_error in test_cases:
            success, error_msg = register_page.register(
                test_data['name'],
                test_data['email'],
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
