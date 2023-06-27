# Chips and Circuits
Microchips vind je overal om je heen. In je laptop, je telefoon en zelfs in je auto. Chips bestaan uit een siliconen plaatje met daarop een aantal gates verbonden door draden. Om een zo snel en goedkoop mogelijke chip te maken, is het noodzakelijk om de gates met zo kort mogelijke draden te verbinden. Tevens zorgt een kruising van draden voor ontzettend hoge kosten en dus kunnen die ook het beste vermeden worden.

Dit programma kan op basis van een vooraf gegeven lijst met gate-coordinaten en gate-verbindingen (zie voorbeeld in "Chips-and-Circuits-Project/data/") een valide chipconfiguratie geven die alle gates met elkaar verbind d.m.v. draden. Valide oplossingen zijn oplossingen waarbij een draad zich binnen de kaders van de chip begeeft, en zonder zichzelf te kruisen een connectie maakt tussen zijn oorsprong-gate en bestemming-gate. Een draad kan in principe iedere richting in, vooruit, achteruit, links, rechts, naar boven en naar onderen. De uiteindelijke chipconfiguratie is dan ook een 3D representatie. Het programma slaat ook data op in een door-de-gebruiker-gespecificeerce output folder (terug te vinden in "Chips-and_Circuits-Project/output/").

De totale kosten van de chipconfiguratie worden gebaseerd op het totaal aantal draden dat gelegd is en het totaal aantal keer dat een draad kruist met een andere draad.

Dit wordt berekend met de volgende formule:

```
totale kosten = aantal draden + 300 * aantal draadkruisingen
```

<br></br>
## Structuur
Hieronder worden de belangrijkste mappen in het project uitgelicht:

- **Chips-and-Circuits-Project/data**: Bevat de csv-bestanden die nodig zijn om de chips te laden en uiteindelijk te visualiseren.
- **Chips-and-Circuits-Project/code**: Bevat alle code van dit project
    - **Chips-and-Circuits-Project/code/algorithms/**: Bevat alle code voor de algoritmes.
    - **Chips-and-Circuits-Project/code/classes/**: Bevat alle code voor de classes, nodig om de datastructuur te bouwen.
    - **Chips-and-Circuits-Project/code/analysis/**: Bevat alle code voor het maken van grafieken voor data analyse.
    - **Chips-and-Circuits-Project/code/visualisation/**: Bevat alle code voor het maken van een visualisatie van de chip.
- **Chips-and-Circuits-Project/output/**: Bevat een mapje met daarin:

    -   Een csv-bestand met:
        -   Het aantal iteraties die een algoritme heeft gemaakt
        -   Het aantal gelegde stukken draad
        -   Het aantal draadkruisingen
        -   De totale kosten van de chipconfiguratie
        -   De tijdsduur per iteratie
        -   De cumulatieve tijdsduur
<br></br>
    -   Een grafiek met daarin een visualisatie van de nuttige informatie uit het csv-bestand.

    -   Een 3D visualisatie van de beste chipconfiguratie die het algoritme heeft kunnen vinden in zijn run.

<br></br>
## Vereisten 
De codebase is volledig geschreven in Python 3.10.8. In de file requirements.txt staan alle modules die nodig zijn voor het runnen van het programma. Deze zijn eenvoudig te installeren door het volgende command te runnen vannuit de root directory van dit programma ("Chips-and-Circuits-Project/").

```
pip install -r requirements.txt
```

<br></br>
## Gebruik
Allereerst moet er genavigeerd worden naar de "code" directory.

```
cd code
```

Hierna kan het programma aangeroepen worden met een chip, netlist en algoritme naar keuze.

```
python3 main.py [chip nummer] [netlist nummer] [algoritmenaam] [output foldernaam]
```

In de praktijk kan dit er dan uit zien als volgt.

```
python3 main.py 2 9 astar results_astar
```

Deze command runt dan het a-star algoritme over chip 2, netlist 9, en slaat de data en visualisaties op in het mapje "Chips-and-Circuits-Project/output/results_astar/"

Mogelijke algoritmes om te runnen zijn:
```
random, hillclimbing, simulatedannealing, astar
```

-   **BELANGRIJK**: Bij het runnen van  de algoritmes "random", "hillclimbing" en "simulatedannealing" moet de gebruiker zelf het programma stopzetten door op 'ctrl-C' te drukken. "astar" stopt vanzelf bij het vinden van een oplossing. Hierna is alle data die het programma gegenereerd heeft terug te vinden in de output folder. De chipvisualisatie is een visualisatie van de goedkoopste chipconfiguratie die het gekozen algoritme heeft kunnen vinden tijdens zijn run.

-   **EXTRA**: Bij het runnen van het algoritme "astar" kunnen twee extra command line arguments meegegeven worden: [sortingmode] en [heuristic]. Hierbij kan gekozen worden voor:
    -   sortingmode: [ascending] of [descending]
        -   ascending: begint met het leggen van draden bij gates die een korte afstand hebben tot hun bestemming-gate.
        -   descending: begint met het leggen van draden bij gates die een lange afstand hebben tot hun bestemming-gate.
    -   heuristic: [avoid_gates] of [avoid_low] of [all]
        -   avoid_gates: zorgt ervoor dat draden ruim om gates heengaan die niet hun bestemming zijn, om ruimte te maken voor andere draden.
        -   avoid_low: zorgt ervoor dat draden hogere lagen van de chip prefereren, om onderin ruimte vrij te laten voor de uiteindelijke connectie aan een gate.
        -   all: past zowel avoid_gates, als avoid_low toe.

<br></br>
## Auteurs
- Casper Leenaars
- Max Riemens
- Olivier Tichler