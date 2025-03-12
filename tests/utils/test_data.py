import random
import string
from datetime import datetime

class TestDataGenerator:
    """Generador de datos de prueba para validaciones de registro e inicio de sesión
    
    Esta clase proporciona métodos para generar datos de prueba válidos e inválidos,
    incluyendo nombres, correos electrónicos y contraseñas que cumplen o incumplen
    los requisitos del sistema.
    """

    CARACTERES_ESPECIALES = '!@#$%^&*(),.?":{}|<>'
    MIN_LONGITUD_PASSWORD = 8
    MAX_LONGITUD_PASSWORD = 20
    MIN_LONGITUD_NOMBRE = 3
    MAX_LONGITUD_NOMBRE = 50
    
    @staticmethod
    def generar_nombre(num_palabras=2):
        """Generar un nombre completo aleatorio válido

        Args:
            num_palabras: Número de palabras en el nombre (por defecto 2: nombre y apellido)

        Returns:
            str: Nombre completo con formato válido (cada palabra con mayúscula inicial)
            
        Note:
            El nombre generado cumple con los requisitos:
            - Solo contiene letras
            - Cada palabra tiene mayúscula inicial
            - Mínimo dos palabras (nombre y apellido)
            - Longitud mínima de 3 caracteres por palabra
        """
        palabras = []
        for _ in range(num_palabras):
            longitud = random.randint(3, 10)
            palabra = ''.join([
                random.choice(string.ascii_uppercase) if i == 0 
                else random.choice(string.ascii_lowercase)
                for i in range(longitud)
            ])
            palabras.append(palabra)
        return ' '.join(palabras)
    
    @staticmethod
    def generar_email(nombre=None):
        """Generar un correo electrónico único y válido

        Args:
            nombre: Nombre base para generar el correo (opcional)

        Returns:
            str: Correo electrónico con formato válido y único
            
        Note:
            El correo generado:
            - Usa el nombre proporcionado o genera uno nuevo
            - Reemplaza espacios por puntos
            - Agrega timestamp para garantizar unicidad
            - Usa el dominio @inlaze.test
        """
        if not nombre:
            nombre = TestDataGenerator.generar_nombre()
        email_base = nombre.lower().replace(' ', '.')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{email_base}_{timestamp}@inlaze.test"
    
    @staticmethod
    def generar_password_valido():
        """Generar una contraseña que cumple todos los requisitos de seguridad

        Returns:
            str: Contraseña válida con:
                - Mínimo 8 caracteres
                - Al menos una mayúscula
                - Al menos una minúscula
                - Al menos un número
                - Al menos un carácter especial
        """
        longitud = random.randint(
            TestDataGenerator.MIN_LONGITUD_PASSWORD,
            TestDataGenerator.MAX_LONGITUD_PASSWORD
        )
        
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(TestDataGenerator.CARACTERES_ESPECIALES)
        ]
        
        caracteres_validos = string.ascii_letters + string.digits + TestDataGenerator.CARACTERES_ESPECIALES
        password.extend([random.choice(caracteres_validos) for _ in range(longitud - len(password))])
        
        random.shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def generar_password_invalido(tipo_error='longitud'):
        """Generar una contraseña que incumple un requisito específico de seguridad

        Args:
            tipo_error: Tipo de validación a incumplir:
                - 'longitud': Menos de 8 caracteres
                - 'mayuscula': Sin mayúsculas
                - 'minuscula': Sin minúsculas
                - 'numero': Sin números
                - 'especial': Sin caracteres especiales (!@#$%^&*(),.?\":{|}|<>)

        Returns:
            str: Contraseña inválida que genera el mensaje de error esperado
            
        Note:
            La contraseña generada:
            - Mantiene una longitud mínima de 8 caracteres (excepto si tipo_error es 'longitud')
            - Cumple todos los requisitos excepto el especificado
            - Tiene caracteres en posiciones aleatorias
        """
        if tipo_error == 'longitud':
            return ''.join(random.choices(string.ascii_letters, k=5))
        
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(TestDataGenerator.CARACTERES_ESPECIALES)
        ]
        
        if tipo_error == 'mayuscula':
            password[0] = random.choice(string.ascii_lowercase)
        elif tipo_error == 'minuscula':
            password[1] = random.choice(string.ascii_uppercase)
        elif tipo_error == 'numero':
            password[2] = random.choice(string.ascii_letters)
        elif tipo_error == 'especial':
            password[3] = random.choice(string.ascii_letters)
        
        while len(password) < TestDataGenerator.MIN_LONGITUD_PASSWORD:
            password.append(random.choice(string.ascii_letters))
        
        random.shuffle(password)
        return ''.join(password)
    
    @classmethod
    def generar_usuario_prueba(cls):
        """Generar datos completos para un usuario de prueba

        Returns:
            dict: Datos del usuario con formato:
                - name: Nombre completo
                - email: Correo electrónico único
                - password: Contraseña válida
        """
        nombre = cls.generar_nombre()
        return {
            'name': nombre,
            'email': cls.generar_email(nombre),
            'password': cls.generar_password_valido()
        }
    
    @classmethod
    def generar_usuarios_prueba(cls, cantidad):
        """Generar datos para múltiples usuarios de prueba

        Args:
            cantidad: Número de usuarios a generar

        Returns:
            list: Lista de diccionarios con datos de usuarios
        """
        return [cls.generar_usuario_prueba() for _ in range(cantidad)]

def generate_test_user():
    """Función auxiliar para generar datos de un usuario de prueba válido

    Returns:
        dict: Datos completos del usuario:
            - name: Nombre completo (nombre y apellido)
            - email: Correo electrónico único
            - password: Contraseña que cumple requisitos de seguridad
    """
    return TestDataGenerator.generar_usuario_prueba()

def get_registro_test_data():
    """Obtener datos de prueba específicos para casos de registro
    
    Returns:
        dict: Conjunto de datos de prueba para diferentes escenarios de registro:
            - valid_user: Usuario con datos válidos
            - mismatched_passwords: Usuario con contraseñas que no coinciden
    """
    return {
        'valid_user': {
            'name': 'Nicolas Gaitan',
            'email': 'jnicogaitan@gmail.com',
            'password': 'Password1*',
            'confirm_password': 'Password1*'
        },
        'mismatched_passwords': {
            'name': 'Nicolas Gaitan',
            'email': 'jnicogaitan@gmail.com',
            'password': 'Password1*',
            'confirm_password': 'DifferentPass1*'
        }
    }

def get_login_test_data():
    """Obtener datos de prueba específicos para casos de inicio de sesión
    
    Returns:
        dict: Conjunto de datos de prueba para diferentes escenarios de login:
            - valid_user: Usuario con credenciales válidas
            - invalid_credentials: Usuario con credenciales incorrectas
            - password_validations: Casos de prueba para validaciones de contraseña
    """
    return {
        'valid_user': {
            'email': 'jnicogaitan@gmail.com',
            'password': 'Password1*'
        },
        'invalid_credentials': {
            'email': 'usuario.invalido@test.com',
            'password': 'Test1234!'
        },
        'password_validations': [
            {'password': '', 'expected_error': 'La contraseña es obligatoria'},
            {'password': 'Abc1*', 'expected_error': 'La contraseña debe tener al menos 8 caracteres'},
            {'password': 'password123!', 'expected_error': 'La contraseña debe contener al menos una mayúscula'},
            {'password': 'PASSWORD123!', 'expected_error': 'La contraseña debe contener al menos una minúscula'},
            {'password': 'Password!', 'expected_error': 'La contraseña debe contener al menos un número'},
            {'password': 'Password123', 'expected_error': 'La contraseña debe contener al menos un carácter especial'},
            {'password': 'Password 1*', 'expected_error': 'La contraseña no puede contener espacios'}
        ]
    }
