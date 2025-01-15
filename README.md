# Symulacja procesu wentylacji powietrza w pomieszczeniach

## Opis
Program symuluje dynamikę przepływu powietrza w środowisku 2D za pomocą metody Lattice Boltzmann (LBM). Symulacja odbywa się na mapie zdefiniowaniej w pliku JSON, którą można utworzyć za pomocą dedykowanego edytora. Mapa określa układ środowiska, w tym przeszkody i otwarte przestrzenie. Można również określić początkowy przepływ powietrza. Wizualizacja wyników pokazuje pole prędkości przepływu powietrza w czasie.

## Uruchomienie projektu

Przed uruchomieniem projektu zalecane jest stworzenie środowiska wirtualnego za pomocą komendy:
```bash
    python -m venv venv
```
Następnie należy aktywować środowisko:
```bash
    # Windows
    venv\Scripts\activate

    # Linux / Mac
    source venv/bin/activate
```
Kolejnym krokiem jest zainstalowanie niezbędnych pakietów do uruchomienia symulacji:
```bash
    pip install -r requirements.txt
```
Uruchom za pomocą pythona plik _interface.py_
```bash
    python interface.py
```
W konsoli uruchomi się interfejs potrzebny do uruchomienia symulacji.

## Opis modelu symulacji

W każdym węźle siatki znajduje się 9 kierunków prędkości. Są 4 połączenia: w górę, dół, lewo, i prawo, 4 połączenia po przekątnych oraz 1 połączenie reprezentujące zerową prędkość. Każdy węzeł siatki ma przypisaną wagę ω<sub>i</sub>

![Lattices](img/lattices.webp)

Mikroskopowe cząstki tworzące płyn można opisać za pomocą funkcji rozkładu _f(x,v)_, która opisuje gęstość przestrzeni fazowej płynu w lokalizacji x poruszając się z prędkością _v_.
Cząstki przepływają i zderzają się. Zachowanie może być uchwycone za pomocą aproksymacji BGK (Bhatnagar–Gross–Krook):

![Formula](img/formula.webp)

W tej aproksymacji _τ_ jest skalą czasową, w której zachodzą zderzenia, a funkcja rozkładu _f_ dąży do pewnego stanu równowagi _f<sup>eq</sup>_.

Równanie można zdyskretyzować na siatce w następujący sposób:

![Discrete fromula](img/discrete_formula.webp)

### Momenty funkcji rozkładu
__Gęstość__:

![Moment](img/moment.webp)

__Pęd__

![Momentum](img/momentum.webp)

### Zderzenia

Definiujemy stan równowagi w wyniku zderzeń. Zakładamy płyn o stałej temperaturze, który ma stałą prędkość dźwięku. Jednostki zdefiniowane są tak, że prędkość na siatce wynosi _c = 1_.

![Equilibrum](img/equilibrium.webp)

Co odpowiada równaniom Naviera-Stokesa dla płynu izotermicznego o dynamicznej lepkości:

![Navier-Stokes](img/navier-stokes.webp)

### Warunki brzegowe
W miejscach przeszkód cząstki zachowują się inaczej. Cząstki odbijają się, więc po prostu zmieniamy kierunki siatki.

![Navier-Stokes](img/fifj.webp)

Dodatkowo granice mapy zostały ustawione na absorbujące. Żeby uniknąć "teleportacji" cząsteczek na drugą stronę mapy, parametry krańcowych cząsteczek zostają ustawione na równe cząsteczkom, które je poprzedzają.


## Źródła
https://medium.com/swlh/create-your-own-lattice-boltzmann-simulation-with-python-8759e8b53b1c