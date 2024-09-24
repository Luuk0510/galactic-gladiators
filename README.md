# Eindopdracht - Galactic Gladiators

### Avans Hogeschool, ’s-Hertogenbosch, studiejaar 2023/2024
Versie 1.0  
Docent: Reinout Versteeg

## Wat is de opdracht?
"**Galactic Gladiators**" is een digitaal, turn-based strategisch bordspel waarbij spelers het bevel hebben over een leger van eenheden met als doel de vlag van de tegenstander te veroveren. De opdracht is om een applicatie te bouwen voor dit spel, gebruikmakend van **Flask**, **PyGame**, of **Arcade**.

## Spelregels en Spelverloop

### Overzicht:
- **Spelbord**: Het bord bestaat uit een 10x10 raster waarop beide spelers hun eenheden positioneren.
- **Spelers**: Eén menselijke speler en één AI spelen tegen elkaar. Het doel is de vlag van de tegenstander te veroveren.
- **Elementen op het bord**:
  - **Verhoogde positie**: +1 bonus bij gevechten.
  - **Dekking**: Eenheden op dit vakje zijn immuun voor speciale krachten.
  - **Sensor**: Onthult tijdelijk het type van eenheden.
  - **Goudmijn**: Verzamelt goud voor de speler na 3 beurten.

### Eenheden:
- **Verkenner**: Infiltratie - Kan onzichtbaar worden voor 3 beurten.
- **Infanterist**: Geen speciale kracht.
- **Scherpschutter**: Precisieschot - Kan een vijandelijke eenheid op afstand uitschakelen.
- **Schilddrager**: Energieveld - Negeert vijandelijke speciale krachten voor 3 beurten.
- **Strijdmeester**: Strijdkreet - Geeft nabijgelegen eenheden een rangbonus.
- **Commando**: Sabotage - Kan een aangrenzende vijandelijke eenheid overnemen.
- **Vlag**: Heeft geen speciale krachten en kan niet bewegen.

### Spelverloop:
- Spelers zetten om de beurt een actie in gang:
  - **Bewegen**: Beweeg een eenheid naar een aangrenzend vakje (horizontaal/verticaal).
  - **Aanvallen**: Start een gevecht met een vijandelijke eenheid op een aangrenzend vakje.
  - **Speciale kracht**: Gebruik een speciale kracht van een eenheid.

Het spel eindigt wanneer de vlag van één van de spelers wordt veroverd. De winnaar wordt bepaald op basis van wie de meeste goudstukken heeft verzameld.

## Applicatie-eisen

### Functionele eisen:
1. Het spel moet volledig speelbaar zijn zoals beschreven.
2. Er moet een werkende AI zijn die tegen de speler speelt.
3. De mogelijkheid om het spel op te slaan en later verder te spelen.
4. De speler kan kiezen om een nieuw spel te starten of verder te spelen in een eerder opgeslagen spel.
5. Er is een cheatcode om alle eenheden zichtbaar te maken.
6. De applicatie moet stabiel zijn en niet crashen.

### Technische eisen:
1. De applicatie moet volledig in **Python** worden geschreven, gebruikmakend van **Flask**, **PyGame**, of **Arcade**.
2. Het ontwerp moet object-georiënteerd zijn, met klassen zoals:
   - `GameBoard`: Beheert het speelveld.
   - `Unit`: Basisklasse voor eenheden.
   - `Player / AIPlayer`: Beheert acties van de speler en AI.
3. Gebruik van Python-specifieke elementen zoals:
   - **Dunder methods**: Zoals `__init__`, `__str__`.
   - **Properties**: Voor veilige toegang tot attributen.
   - **List comprehensions**: Voor efficiënte datamanipulatie.
   - **Decorators**: Voor functies zoals het valideren van bewegingen.
4. Persistentie: Het spel moet kunnen worden opgeslagen en later hervat worden.
5. User Interface:
   - **Flask**: HTML/CSS voor weergave van de spelinterface.
   - **PyGame/Arcade**: Ontwerp een GUI die het bord en de spelstatus weergeeft.
6. Codekwaliteit en -documentatie: Zorg voor onderhoudbare, goed gedocumenteerde code.

## Beoordeling

Het eindresultaat wordt beoordeeld op basis van "voldaan" of "niet voldaan". De volgende criteria moeten worden gevolgd:
- Alle functionele en technische eisen moeten worden uitgevoerd.
- Beide studenten moeten de code volledig kunnen uitleggen tijdens het assessment. Het niet kunnen uitleggen van de code leidt tot een directe "niet voldaan".

## Instructies voor Installatie en Gebruik

1. Clone de repository:
   ```bash
   git clone [repository-url]
