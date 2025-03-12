import os
import shutil
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pytest_configure():
    """Configuración inicial de pytest
    
    Prepara el directorio para reportes y capturas de pantalla de errores
    
    Note:
        - Limpia reportes anteriores
        - Crea estructura de directorios necesaria
        - Las capturas se guardan en reports/screenshots
    """
    reports_dir = os.path.join(os.getcwd(), 'reports')
    if os.path.exists(reports_dir):
        shutil.rmtree(reports_dir)
    os.makedirs(os.path.join(reports_dir, 'screenshots'), exist_ok=True)

@pytest.fixture(scope="session")
def chrome_options():
    """Configuración del navegador Chrome para las pruebas
    
    Returns:
        Options: Opciones configuradas para Chrome
    """
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

@pytest.fixture(scope="class")
def driver(chrome_options, request):
    """Fixture principal para el navegador web
    
    Args:
        chrome_options: Opciones de configuración de Chrome
        request: Objeto de solicitud de pytest
    
    Yields:
        WebDriver: Instancia configurada del navegador Chrome
    
    Note:
        - Timeout de carga de página: 30 segundos
        - Tiempo de espera implícito: 10 segundos
        - Captura automática de pantalla en caso de fallo
    """
    screenshots_dir = os.path.join('reports', 'screenshots')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.set_window_size(1920, 1080)
    
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    driver.wait = WebDriverWait(driver, 10)
    
    driver.test_name = request.node.name if request else "prueba_desconocida"
    
    yield driver
    
    try:
        if request.node.rep_call.failed:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(
                screenshots_dir,
                f"error_{request.node.name}_{timestamp}.png"
            )
            driver.save_screenshot(screenshot_path)
    except AttributeError:
        pass
    
    driver.quit()



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para generar reportes de pruebas
    
    Permite acceder al resultado de la prueba para tomar capturas
    de pantalla en caso de fallo
    
    Args:
        item: Item de prueba
        call: Llamada de prueba
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)  # Guardar resultado para uso posterior
