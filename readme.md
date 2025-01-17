# Documentation ChromeScrapper

## Description
ChromeScrapper est une classe Python qui permet d'automatiser la navigation web en utilisant Chrome. Elle utilise Selenium WebDriver et peut fonctionner avec votre profil Chrome existant, permettant ainsi d'accéder à des sites où vous êtes déjà connecté.

## Prérequis

### Installation des dépendances
```bash
pip install selenium webdriver-manager
```

### Configuration requise
- Google Chrome doit être installé sur votre système
- **Important** : Toutes les instances de Chrome doivent être fermées avant d'utiliser ChromeScrapper avec un profil utilisateur

## Importation
```python
from chrome_scrapper import ChromeScrapper
```

## Initialisation

### Syntaxe
```python
scrapper = ChromeScrapper(
    chrome_path=None,    # Optionnel : chemin vers l'exécutable Chrome
    headless=False,      # Optionnel : mode sans interface graphique
    use_profile=True     # Optionnel : utiliser le profil Chrome existant
)
```

### Paramètres
- `chrome_path` (str, optionnel) : Chemin vers l'exécutable Chrome
- `headless` (bool, optionnel) : Lance Chrome en mode headless si True
  - Note : Le mode headless ne fonctionne pas avec `use_profile=True`
- `use_profile` (bool, optionnel) : Utilise le profil Chrome par défaut de l'utilisateur

### Exemple d'initialisation
```python
# Utilisation basique avec le profil utilisateur
scrapper = ChromeScrapper()

# Utilisation sans profil utilisateur
scrapper = ChromeScrapper(use_profile=False)

# Spécifier un chemin Chrome personnalisé
scrapper = ChromeScrapper(chrome_path="/chemin/vers/chrome")
```

## Méthodes principales

### navigate_to(url, timeout=30)
Navigate vers une URL spécifique.

```python
scrapper.navigate_to("https://www.example.com", timeout=30)
```
- `url` (str) : URL à visiter
- `timeout` (int, optionnel) : Temps maximum d'attente en secondes

### get_html()
Récupère le code HTML de la page courante.

```python
html = scrapper.get_html()
```
Retourne une chaîne contenant le HTML de la page.

### wait_for_element(by, value, timeout=10)
Attend qu'un élément soit présent sur la page.

```python
from selenium.webdriver.common.by import By

# Attendre un élément avec l'ID "login"
element = scrapper.wait_for_element(By.ID, "login")

# Attendre un élément avec la classe "button"
element = scrapper.wait_for_element(By.CLASS_NAME, "button")
```
- `by` : Type de sélecteur (By.ID, By.CLASS_NAME, By.CSS_SELECTOR, etc.)
- `value` (str) : Valeur du sélecteur
- `timeout` (int, optionnel) : Temps maximum d'attente en secondes

## Gestion des ressources

### Fermeture manuelle
Il est recommandé de fermer explicitement le navigateur après utilisation :
```python
try:
    scrapper = ChromeScrapper()
    # Votre code ici
finally:
    del scrapper  # Ferme automatiquement le navigateur
```

### Utilisation avec with
Pour une meilleure gestion des ressources, vous pouvez implémenter le context manager :
```python
class ChromeScrapper:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

# Utilisation
with ChromeScrapper() as scrapper:
    scrapper.navigate_to("https://www.example.com")
    html = scrapper.get_html()
```

## Exemple complet
```python
from chrome_scrapper import ChromeScrapper
from selenium.webdriver.common.by import By

# S'assurer que toutes les instances de Chrome sont fermées
try:
    with ChromeScrapper(headless=False, use_profile=True) as scrapper:
        # Navigation vers un site (sera connecté si vous l'étiez dans Chrome)
        scrapper.navigate_to("https://www.facebook.com")
        
        # Attendre un élément spécifique
        feed = scrapper.wait_for_element(By.CLASS_NAME, "feed-container")
        
        # Récupérer le HTML
        html = scrapper.get_html()
        
        # Sauvegarder le HTML
        with open("page.html", "w", encoding='utf-8') as f:
            f.write(html)
except Exception as e:
    print(f"Une erreur s'est produite : {str(e)}")
```

## Dépannage

### Erreurs courantes

1. **Chrome déjà en cours d'exécution**
   - Erreur : "Chrome failed to start: already running on a different instance"
   - Solution : Fermez toutes les instances de Chrome avant d'exécuter le script

2. **Profil verrouillé**
   - Erreur : "User data directory is already in use"
   - Solution : 
     - Fermez toutes les instances de Chrome
     - Vérifiez qu'aucun autre processus Chrome n'est en cours
     - Supprimez le fichier "Lock" dans le dossier du profil si nécessaire

3. **Version du ChromeDriver incompatible**
   - Solution : Le webdriver-manager devrait gérer cela automatiquement
   - Alternative : Mettez à jour Chrome ou spécifiez une version spécifique du ChromeDriver

### Bonnes pratiques

1. Toujours utiliser un bloc try/finally ou with pour assurer la fermeture propre du navigateur
2. Fermer toutes les instances de Chrome avant d'exécuter le script
3. Éviter le mode headless avec use_profile=True
4. Utiliser des timeouts appropriés pour votre cas d'usage
5. Gérer les exceptions de manière appropriée

## Limitations connues

1. Le mode headless ne fonctionne pas avec l'utilisation du profil utilisateur
2. Une seule instance peut utiliser un profil utilisateur à la fois
3. Certains sites peuvent détecter l'automatisation malgré les mesures anti-détection