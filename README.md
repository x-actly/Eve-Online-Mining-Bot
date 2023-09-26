# Mining Bot Alpha Owl-Edition

Der Mining Bot Alpha Owl-Edition ist ein Python-Programm, das entwickelt wurde, um das Mining in EVE Online zu automatisieren. Dieser Bot verwendet das Tkinter-Framework für die Benutzeroberfläche und erfordert einige externe Python-Module, die in der `requirements.txt`-Datei aufgeführt sind.

## Features

- Automatisiertes Mining in EVE Online
- Benutzerfreundliche GUI für die Konfiguration
- Einfache Steuerung von Start und Stopp des Bots
- Anzeige der aktuellen Mausposition auf dem Bildschirm

## Anforderungen

Um den Mining Bot Alpha Owl-Edition auszuführen, müssen Sie die erforderlichen Python-Module installieren. Verwenden Sie dazu den folgenden Befehl:

```bash
pip install -r requirements.txt
```

## Verwendung

1. Stellen Sie sicher, dass Sie die erforderlichen Module gemäß den Anforderungen installiert haben.

2. Starten Sie das Programm, indem Sie die main.py-Datei ausführen.
   ```bash
   python main.py
   ```

3. Konfigurieren Sie die verschiedenen Einstellungen in der Benutzeroberfläche:

   - Mining Time: Geben Sie die gewünschte Dauer des Mining-Vorgangs in Minuten an.
   - Belt Time (Sekunden): Tragen Sie die berechnete "Belt Time" (ohne Nachkommastellen) gemäß dem Cargovolumen und der Abbaurate ein (siehe unten für die Berechnungsformel).
   - Undock-Position: Setzen Sie die Maus Koordinate des Undock Buttons auf der Station
   - Docking-Position: Setzen sie die Maus Koordinate der Station in der Overview, diese muss ganz oben stehen, wenn das Schiff wieder auf dem Grid der Station ist.
   - Clear-Cargo-Position: Geben Sie die Maus Position zum Entladen des Cargos an. Dieser zieht den Inhalt des Mining Hold in das darüber liegende Fenster, wo sich dein Stations Inventar befindet.
   - Target-One-Position: Setzen Sie die erste Maus Koordinate auf die Asteroiden in der Overview.
   - Target-Two-Position: Definieren Sie die zweite Koordinate in der Overview.
   - Target-Reset-Position: Geben Sie die Position für das Zurücksetzen der Miningziele an (Position im Space, wo sich kein Fenster, oder sonstiges befindet).
   - Drone-Reset-Position: Definieren Sie die Position zum Zurücksetzen der Drohnen ((Position im Space, wo sich kein Fenster, oder sonstiges befindet).
   - Home Bookmark: Setzen Sie die Koordinaten für das Stations Bookmark.
   - Belt Bookmarks: Tragen Sie die Koordinaten für Ihre Belt Bookmarks ein (jeweils eine Zeile pro Bookmark).
    
4. Für alle Positionsfelder gibt es ein kleines Diskettensymbol. Klicken Sie darauf, um die eingegebenen Koordinaten zu speichern, damit diese auch Session-übergreifend bestehen bleiben. 

5. Klicken Sie auf die "Start"-Schaltfläche, um den Mining-Bot zu starten.

6. Um den Bot zu stoppen, klicken Sie auf die "Stop"-Schaltfläche.

## Anzeige der Mausposition

Die GUI-Anwendung zeigt kontinuierlich die aktuelle Position der Maus auf dem Bildschirm an. Dies kann hilfreich sein, um die Koordinaten für die oben genannten Positionen genau zu bestimmen.

## Berechnung der Belt Time

Die "Belt Time" bezieht sich auf die Zeit, die benötigt wird, um das Cargovolumen in Ihrem Mining-Schiff unter Verwendung Ihrer Mininglaserrate abzubauen. Die Berechnung erfolgt wie folgt:
```
Belt Time (Sekunden) = Cargovolumen (m³) / (Anzahl der Mininglaser * Abbaurate pro Sekunde (m³/s))
```
Beispiel:

Angenommen, Sie verwenden eine Venture mit einem Cargovolumen von 5000 m³ und zwei Mininglasern, die jeweils mit einer Abbaurate von 1,5 m³ pro Sekunde arbeiten. Die Berechnung würde wie folgt aussehen:
```
Belt Time = 5000 m³ / (2 * 1,5 m³/s) = 1666 Sekunden
```
In diesem Fall dauert es etwa 1666 Sekunden, um das gesamte Cargovolumen abzubauen. Fügen Sie die berechnete "Belt Time" in Sekunden (ohne Nachkommastellen) in das entsprechende Feld in der GUI ein, um den Mining-Bot gemäß Ihrer Konfiguration auszuführen.

## Anmerkungen
Dies ist ein Open-Source-Projekt und wird ohne jegliche Garantien bereitgestellt. Verwenden Sie es auf eigenes Risiko.

Bitte stellen Sie sicher, dass Sie EVE Online und seine Nutzungsbedingungen und Richtlinien einhalten. Die Verwendung von Bots oder Automatisierung kann gegen die Nutzungsbedingungen des Spiels verstoßen.



