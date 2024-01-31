# Notenrechner
Dieses Python-Skript berechnet den Durchschnitt der Noten aus einer PDF-Datei. Es ist speziell für Sammelzeugnisse der Universität Wien konzipiert. (Weitere Universitäten in Arbeit)

## Anforderungen

- Python 3.*
- Die Python-Bibliotheken `os`, `numpy`, `fitz`, `re` und `PyQt5` müssen installiert sein.

## Installation

Um die erforderlichen Bibliotheken zu installieren, führen Sie den folgenden Befehl aus:
```console
pip3 install numpy PyMuPDF PyQt5
```

## Verwendung

Führen Sie das [Schnittrechner.py](Rechner/src/Schnittrechner.py) Skript aus. Ein Fenster öffnet sich, in dem Sie die PDF-Dateien auswählen können. Nachdem Sie die Dateien ausgewählt haben, klicken Sie auf den Button "Berechnen". Die PDF-Datei sollte sich im Ordner "Data" befinden und die Noten und ECTS-Punkte sollten im Format "Note (Dezimalzahl) ECTS" angegeben sein.

Das Skript liest die PDF-Datei, extrahiert die Noten und ECTS-Punkte und berechnet den gewichteten Durchschnitt.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Dies bedeutet, dass Sie es frei verwenden, ändern und verteilen können, solange Sie die Bedingungen der Lizenz einhalten. Eine Kopie der Lizenz finden Sie in der LICENSE-Datei in diesem Repository.

Bitte beachten Sie, dass dieses Projekt ohne jegliche Garantie zur Verfügung gestellt wird. Die Autoren sind nicht verantwortlich für Schäden oder Verluste, die durch die Verwendung des Projekts entstehen könnten.

Eine Kopie der Lizenz finden Sie [hier](LICENSE).


