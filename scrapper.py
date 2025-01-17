import os
import platform
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChromeScrapper:
    def __init__(self, chrome_path=None, headless=False, use_profile=True):
        """
        Initialise le scrapper Chrome avec Selenium
        
        Args:
            chrome_path (str): Chemin vers l'exécutable Chrome (optionnel)
            headless (bool): Lancer Chrome en mode headless ou non
            use_profile (bool): Utiliser le profil Chrome par défaut de l'utilisateur
        """
        logger.info("Initialisation du ChromeScrapper")
        
        # Déterminer le chemin du profil Chrome selon l'OS
        system = platform.system().lower()
        if use_profile:
            if system == "windows":
                profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
            elif system == "darwin":  # MacOS
                profile_path = os.path.expanduser('~/Library/Application Support/Google/Chrome')
            else:  # Linux
                profile_path = os.path.expanduser('~/.config/google-chrome')
            
            logger.info(f"Utilisation du profil Chrome : {profile_path}")

        # Configuration des options Chrome
        self.options = Options()
        if headless:
            self.options.add_argument('--headless=new')
        
        if use_profile:
            # Utiliser le profil par défaut
            self.options.add_argument(f'--user-data-dir={profile_path}')
            # Utiliser le profil "Default" ou "Profile 1" selon votre configuration
            self.options.add_argument('--profile-directory=Default')
        
        # Options supplémentaires
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--enable-unsafe-swiftshader')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Utiliser webdriver_manager pour gérer le ChromeDriver
            logger.info("Installation/mise à jour du ChromeDriver")
            driver_path = ChromeDriverManager().install()
            self.service = Service(driver_path)
            
            logger.info("Démarrage du navigateur Chrome")
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            
            # Masquer que nous utilisons WebDriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome démarré avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du démarrage de Chrome: {str(e)}")
            raise

    def navigate_to(self, url, timeout=30):
        """
        Navigate vers une URL
        
        Args:
            url (str): URL à visiter
            timeout (int): Temps maximum d'attente en secondes
        """
        try:
            logger.info(f"Navigation vers : {url}")
            self.driver.set_page_load_timeout(timeout)
            self.driver.get(url)
            logger.info("Page chargée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la navigation vers {url}: {str(e)}")
            raise

    def get_html(self):
        """
        Récupère le HTML de la page courante
        
        Returns:
            str: Le code HTML de la page
        """
        try:
            logger.info("Récupération du HTML de la page")
            html = self.driver.page_source
            logger.info(f"HTML récupéré (taille: {len(html)} caractères)")
            return html
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du HTML: {str(e)}")
            raise

    def wait_for_element(self, by, value, timeout=10):
        """
        Attend qu'un élément soit présent sur la page
        """
        try:
            logger.info(f"Attente de l'élément: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.info("Élément trouvé")
            return element
        except Exception as e:
            logger.error(f"Erreur lors de l'attente de l'élément: {str(e)}")
            raise

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        try:
            if hasattr(self, 'driver'):
                logger.info("Fermeture du navigateur")
                self.driver.quit()
                logger.info("Navigateur fermé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture du navigateur: {str(e)}")


if __name__ == "__main__":
    scrapper = ChromeScrapper(headless=False, use_profile=True)
    
    scrapper.navigate_to("https://www.facebook.com")  # Devrait être déjà connecté
    html = scrapper.get_html()
    with open("facebook.html", "w", encoding='utf-8') as f:
        f.write(html)