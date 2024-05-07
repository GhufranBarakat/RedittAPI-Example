# RedittAPI-Sample
Dieses Projekt ist ein einfaches Beispiel für die Verwendung der Reddit API. Es verwendet Python (Flask) für den Server und die Backend-Logik sowie HTML/CSS/JavaScript für die Benutzeroberfläche.

***Hinweis: Dieses Beispiel ist für Lernzwecke gedacht und zeigt nur die Grundlagen der Reddit-API-Nutzung***

## Struktur
### 
    api.py: Flask-Server und Backend-Logik.
    static/: Enthält statische Dateien wie HTML, CSS und JavaScript.
        index.html: Haupt-HTML-Datei für die Benutzeroberfläche.
        styles.css: CSS-Datei für das Styling der Benutzeroberfläche.
        scripts.js: JavaScript-Datei für die Interaktion mit der Benutzeroberfläche.
    settings.json: Konfigurationsdatei für Reddit-API-Zugangsdaten.

## Einrichtung
### Bevor das Projekt ausführen, sicherstellen, dass Python installiert ist. 
    [Python Paket Installation]
    pip install Flask

### Reddit API-Zugriff
    [Reddit-Konto erstellen]
    [In Reddit-Entwicklerseite sich regestrieren]

### Generierung des Access Tokens
    Neue Anfrage in Postmann erstellen.
    POST-Methode auswählen und folgende URL hinzufügen: https://www.reddit.com/api/v1/access_token.
    Zu Registerkarte "Body" gehen und "x-www-form-urlencoded" wählen.
    Erforderlichen Parameter hinzufügen: grant_type (mit dem Wert password), username, password, client_id und client_secret.
    Auf "Senden" klicken, um die Anfrage zu senden.
    Der Access-Token wird in der Antwort angezeigt.

## Ausführung
    python api.py

## Verwendung
    Im Browser http://localhost:5000 eingeben