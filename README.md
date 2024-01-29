# Schnittrechner 
Dieses Python-Skript berechnet den Durchschnitt von Noten aus einer PDF-Datei. Es ist speziell für Sammelzeugnisse der Universität Wien entwickelt worden. (Weitere Universitäten in Bearbeitung)

## Anforderungen 

- Python 3.*
- Die Python-Bibliotheken `os`, `numpy`, `fitz` und `re` müssen installiert sein.

## Installation

Um die benötigten Bibliotheken zu installieren, führen Sie den folgenden Befehl aus:
```console
pip3 install numpy PyMuPDF
```

## Vorbereitung 

Bevor Sie das Skript ausführen, erstellen Sie bitte einen Ordner namens "Daten" im selben Verzeichnis, in dem sich das Skript befindet. Platzieren Sie die PDF-Datei(en) mit den Sammelzeugnissen in diesem Ordner.

## Verwendung 

Führen Sie das Skript aus und geben Sie den Namen der PDF-Datei ein, wenn Sie dazu aufgefordert werden. Die PDF-Datei sollte sich im Ordner "Daten" befinden und die Noten und ECTS-Punkte sollten im Format "Note (Dezimalzahl) ECTS" angegeben sein.

Das Skript liest die PDF-Datei, extrahiert die Noten und ECTS-Punkte und berechnet den gewichteten Durchschnitt der Noten.

## Beispiel 
```console
Bitte gib den Namen der PDF Datei ein: Sammelzeugnis
Dein Notenschnitt ist: 2.7
```

In diesem Beispiel befindet sich die Datei "Sammelzeugnis.pdf" im Ordner "Daten". Das Skript berechnet den Durchschnitt der Noten und gibt "Dein Notenschnitt ist: 2.7" aus.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Das bedeutet, dass Sie es frei verwenden, ändern und verteilen können, solange Sie die Bedingungen der Lizenz einhalten. Eine Kopie der Lizenz finden Sie in der Datei [LICENSE](LICENSE) in diesem Repository.

Bitte beachten Sie, dass dieses Projekt ohne jegliche Garantie bereitgestellt wird. Die Autoren sind nicht verantwortlich für eventuelle Schäden oder Verluste, die durch die Verwendung des Projekts entstehen könnten.
