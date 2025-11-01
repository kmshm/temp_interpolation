# Aplikacja do Interpolacji Temperatury na Czujniku Światłowodowym

## Opis

Aplikacja z graficznym interfejsem użytkownika (GUI) służąca do interpolacji wartości temperatury na długości czujnika światłowodowego na podstawie punktowych pomiarów z czujników temperatury.

## Funkcjonalności

- Dodawanie punktowych czujników temperatury ręcznie lub **import masowy z pliku CSV**
- Ustawianie parametrów światłowodu (długość, rozdzielczość przestrzenna)
- Wybór dowolnego stopnia wielomianu interpolacyjnego
- Automatyczne obliczanie współczynników wielomianu interpolacyjnego
- Wyświetlanie wzoru wielomianu w formie tekstowej z informacją o zakresach
- **Wsparcie dla ekstrapolacji** - możliwość prognozowania temperatury poza zakresem czujników
- **Wirtualne czujniki** - automatyczne dodawanie punktów referencyjnych dla płaskiej ekstrapolacji (temp. = skrajne czujniki)
- **Wizualne oznaczenie obszarów interpolacji i ekstrapolacji** na wykresie
- **Ręczne ustawianie skali osi Y** dla lepszej kontroli nad wizualizacją
- Wizualizacja graficzna rozkładu temperatury na wykresie z odróżnieniem rzeczywistych i wirtualnych czujników
- Zarządzanie listą czujników (dodawanie, usuwanie)

## Wymagania

### Biblioteki Python

Aplikacja wykorzystuje następujące biblioteki:

1. **tkinter** - wbudowana biblioteka do tworzenia interfejsu graficznego (GUI)
   - Nie wymaga instalacji, jest częścią standardowej dystrybucji Pythona

2. **numpy** - biblioteka do obliczeń numerycznych i interpolacji wielomianowej
   - Wymaga instalacji

3. **matplotlib** - biblioteka do tworzenia wykresów i wizualizacji danych
   - Wymaga instalacji

### Wersja Python

- Python 3.8 lub nowszy

## Instalacja

### Opcja 1: Bez środowiska wirtualnego (prostsze)

Jeśli masz tylko jeden projekt Python lub nie zależy Ci na izolacji zależności:

```bash
pip install numpy matplotlib
```

Następnie uruchom aplikację:

```bash
python interpolacja_temperatury.py
```

### Opcja 2: Ze środowiskiem wirtualnym (zalecane)

Środowisko wirtualne jest **zalecane**, ale **nie jest konieczne**. Zapewnia izolację zależności projektu.

#### Windows:

```bash
# Utworzenie środowiska wirtualnego
python -m venv venv

# Aktywacja środowiska
venv\Scripts\activate

# Instalacja zależności
pip install -r requirements.txt

# Uruchomienie aplikacji
python interpolacja_temperatury.py
```

#### Linux/macOS:

```bash
# Utworzenie środowiska wirtualnego
python3 -m venv venv

# Aktywacja środowiska
source venv/bin/activate

# Instalacja zależności
pip install -r requirements.txt

# Uruchomienie aplikacji
python interpolacja_temperatury.py
```

## Instrukcja użytkowania

### 1. Ustawienie parametrów światłowodu

W sekcji "Parametry Światłowodu" wprowadź:
- **Długość światłowodu [m]**: całkowita długość czujnika (np. 100)
- **Rozdzielczość [m]**: krok między punktami interpolacji (np. 0.5)
- **Stopień wielomianu**: stopień wielomianu interpolacyjnego (np. 3)
- **Skala osi Y**:
  - Zaznacz "Automatyczna" dla automatycznego dopasowania skali (domyślnie)
  - Odznacz, aby ręcznie ustawić **Y min** i **Y max** w stopniach Celsjusza
- **Ekstrapolacja**:
  - Zaznacz "Wirtualne czujniki" (domyślnie włączone) dla płaskiej ekstrapolacji
  - Wirtualne czujniki dodają punkty referencyjne przed i za obszarem pomiarów
  - Wirtualny czujnik lewy ma temperaturę pierwszego czujnika
  - Wirtualny czujnik prawy ma temperaturę ostatniego czujnika

### 2. Dodawanie czujników

#### Sposób 1: Ręczne dodawanie pojedynczych czujników

W sekcji "Dodaj Czujnik":
- Wprowadź **nazwę czujnika** (np. T1, T2, Sensor_A)
- Podaj **pozycję [m]** na światłowodzie (np. 10, 25.5)
- Wprowadź **temperaturę [°C]** odczytaną z czujnika (np. 20.5)
- Kliknij "Dodaj Czujnik"

Czujnik pojawi się na liście w sekcji "Lista Czujników".

#### Sposób 2: Import z pliku CSV (NOWOŚĆ!)

Zamiast ręcznego wpisywania każdego czujnika, możesz zaimportować wszystkie dane z pliku CSV:

1. Przygotuj plik CSV z 3 kolumnami: **nazwa**, **pozycja**, **temperatura**
2. W sekcji "Lista Czujników" kliknij **"Importuj z CSV"**
3. Wybierz swój plik CSV
4. Aplikacja automatycznie doda wszystkie czujniki do listy

**Format pliku CSV:**

Z nagłówkiem (zalecane):
```csv
nazwa,pozycja,temperatura
T1,10,22.0
T2,30,35.0
T3,60,28.0
T4,90,24.0
```

Bez nagłówka (również działa):
```csv
T1,10,22.0
T2,30,35.0
T3,60,28.0
T4,90,24.0
```

**Uwagi:**
- Separator: przecinek `,`
- Kodowanie: UTF-8
- Aplikacja automatycznie wykrywa czy pierwszy wiersz to nagłówek
- Błędne wiersze są pomijane, a po imporcie wyświetlany jest raport
- Plik przykładowy: `przyklad_czujniki.csv` (dołączony do projektu)

### 3. Zarządzanie czujnikami

- **Usuwanie**: zaznacz czujnik na liście i kliknij "Usuń Zaznaczony"
- **Czyszczenie**: kliknij "Wyczyść Wszystko", aby usunąć wszystkie czujniki i wyniki

### 4. Obliczanie interpolacji

- Gdy masz co najmniej 2 czujniki, kliknij "Oblicz Interpolację"
- Aplikacja obliczy współczynniki wielomianu i wyświetli:
  - **Wzór wielomianu** w formie matematycznej
  - **Wykres** pokazujący punkty pomiarowe i krzywą interpolacji

### 5. Interpretacja wyników

W sekcji "Wzór Wielomianu Interpolacyjnego" zobaczysz:
- Równanie wielomianu T(x) w postaci rozwiniętej
- Dokładne wartości współczynników
- Stopień wielomianu
- **Zakresy interpolacji i ekstrapolacji**
- Ostrzeżenie o obszarach ekstrapolacji (jeśli występują)

Na wykresie:
- **Czerwone kropki**: rzeczywiste pomiary z czujników z etykietami nazw
- **Zielone kwadraty**: wirtualne czujniki (jeśli włączone) z etykietami "Wirt. (lewy)" i "Wirt. (prawy)"
- **Niebieska linia ciągła**: krzywa w obszarze interpolacji (między czujnikami)
- **Niebieska linia przerywana**: krzywa w obszarach ekstrapolacji
- **Pomarańczowe zacieniowanie**: obszary ekstrapolacji
- **Szare pionowe linie kropkowane**: granice zakresu rzeczywistych czujników (min i max)

## Przykłady użycia

### Przykład 1: Interpolacja bez ekstrapolacji

1. Długość światłowodu: 100 m
2. Rozdzielczość: 0.5 m
3. Stopień wielomianu: 3
4. Czujniki:
   - T1: pozycja 0 m, temperatura 20°C
   - T2: pozycja 25 m, temperatura 35°C
   - T3: pozycja 50 m, temperatura 28°C
   - T4: pozycja 75 m, temperatura 32°C
   - T5: pozycja 100 m, temperatura 22°C

Aplikacja wygeneruje wielomian 3. stopnia opisujący rozkład temperatury. Ponieważ czujniki pokrywają cały zakres 0-100 m, nie będzie ekstrapolacji.

### Przykład 2: Interpolacja z ekstrapolacją

1. Długość światłowodu: 100 m
2. Rozdzielczość: 0.5 m
3. Stopień wielomianu: 3
4. Czujniki:
   - T1: pozycja 10 m, temperatura 22°C
   - T2: pozycja 30 m, temperatura 35°C
   - T3: pozycja 60 m, temperatura 28°C
   - T4: pozycja 90 m, temperatura 24°C

W tym przypadku:
- **Ekstrapolacja lewa**: 0-10 m (pomarańczowe zacieniowanie)
- **Interpolacja**: 10-90 m (bez zacieniowania)
- **Ekstrapolacja prawa**: 90-100 m (pomarańczowe zacieniowanie)

Wielomian będzie "rozciągnięty" poza zakres czujników, ale wyniki w obszarach ekstrapolacji mogą być mniej dokładne.

## Uwagi techniczne

### Stopień wielomianu

- **Brak górnego ograniczenia** - możesz użyć dowolnego stopnia wielomianu
- Stopień musi być co najmniej 1
- Aplikacja wyświetli ostrzeżenie dla stopnia > 10 ze względu na możliwą niestabilność numeryczną
- Im wyższy stopień, tym bardziej wielomian "dopasowuje się" do punktów pomiarowych
- Zbyt wysoki stopień może prowadzić do:
  - Nadmiernego dopasowania (overfitting)
  - Oscylacji Rungego (gwałtowne wahania między punktami)
  - Niestabilności numerycznej
- **Zalecane**: stopień 2-4 dla większości zastosowań
- Dla większej liczby punktów można rozważyć wyższe stopnie, ale ostrożnie

### Ekstrapolacja

- **Ekstrapolacja** = przewidywanie wartości poza zakresem czujników
- Obszary ekstrapolacji są wizualnie oznaczone na wykresie:
  - Pomarańczowe zacieniowanie
  - Przerywana linia krzywej
  - Pionowe linie na granicach zakresu czujników
- **UWAGA**: Wyniki ekstrapolacji są **mniej pewne** niż interpolacja
- Im dalej od skrajnych czujników, tym większa niepewność
- Wielomiany wysokich stopni mogą dawać nierealistyczne wyniki w ekstrapolacji
- **Dobre praktyki**:
  - Używaj **wirtualnych czujników** dla stabilnej ekstrapolacji (zalecane!)
  - Używaj niższych stopni wielomianu przy ekstrapolacji (2-3)
  - Nie ekstrapoluj zbyt daleko poza zakres czujników
  - Zawsze weryfikuj, czy wyniki mają sens fizyczny

### Wirtualne czujniki (NOWOŚĆ!)

**Co to jest?**
- Automatycznie dodawane **3 punkty referencyjne** przed pierwszym i **3 za ostatnim** czujnikiem
- **Lewe wirtualne czujniki** (wszystkie 3) mają temperaturę równą **pierwszemu rzeczywistemu czujnikowi**
- **Prawe wirtualne czujniki** (wszystkie 3) mają temperaturę równą **ostatniemu rzeczywistemu czujnikowi**
- Umieszczone na pozycjach:
  - Lewe: **(min_czujnik - 3), (min_czujnik - 2), (min_czujnik - 1) m**
  - Prawe: **(max_czujnik + 1), (max_czujnik + 2), (max_czujnik + 3) m**

**Dlaczego warto używać?**
- **Tworzą płaską ekstrapolację** - temperatura pozostaje stabilna poza zakresem pomiarów
- **Zapobiegają "górkom" i oscylacjom** wielomianu w obszarach ekstrapolacji
- Szczególnie przydatne dla wielomianów wyższych stopni (3+)
- **3 czujniki na każdym końcu** to minimalana liczba gwarantująca stabilność
- Odzwierciedlają realistyczne założenie, że temperatura przed pierwszym i za ostatnim czujnikiem jest podobna do skrajnych pomiarów

**Dlaczego 3 czujniki?**
- 1 wirtualny czujnik: wielomian może tworzyć "górkę" między skrajnym a wirtualnym
- 2 wirtualne czujniki: może wystąpić minimalna oscylacja
- **3 wirtualne czujniki: zapewniają stabilną, płaską ekstrapolację** ✅

**Kiedy używać?**
- ✅ **Włączone domyślnie** - zalecane dla większości zastosowań
- ✅ Gdy oczekujesz płaskiego przebiegu temperatury na skrajach
- ✅ Gdy pierwszy czujnik nie jest na pozycji 0 m lub ostatni nie na końcu światłowodu
- ✅ Gdy temperatura prawdopodobnie nie zmienia się gwałtownie poza obszarem pomiarów
- ✅ Dla wielomianów stopnia 3 i wyższych
- ❌ Wyłącz, jeśli wiesz, że temperatura zmienia się znacząco poza zakresem czujników

**Przykład:**
```
Długość światłowodu: 100 m
Czujniki: T1=10m (22°C), T2=30m (35°C), T3=60m (28°C), T4=90m (24°C)

Wirtualne czujniki:
- Lewe: pozycje 7m, 8m, 9m - wszystkie z temperaturą 22°C (= T1)
- Prawe: pozycje 91m, 92m, 93m - wszystkie z temperaturą 24°C (= T4)

Rezultat:
- Ekstrapolacja 0-10m: płaska, stabilna temperatura ~22°C
- Ekstrapolacja 90-100m: płaska, stabilna temperatura ~24°C
- Brak "górek" i niechcianych oscylacji
```

### Rozdzielczość przestrzenna

- Określa zagęszczenie punktów na wykresie (co ile metrów)
- Nie wpływa na dokładność samej interpolacji
- Mniejsza wartość = gładszy wykres, ale wolniejsze obliczenia i większy zużycie pamięci
- Zalecane: 0.1 - 1.0 m dla większości zastosowań

### Skala osi Y

- **Automatyczna** (domyślnie): skala dopasowuje się do zakresu danych
- **Ręczna**: możesz ustawić własne Y min i Y max
- Przydatne do:
  - Porównywania różnych zestawów danych na tej samej skali
  - Skupienia się na określonym zakresie temperatur
  - Lepszej wizualizacji małych zmian

### Ograniczenia

- Interpolacja wielomianowa działa najlepiej dla **gładkich danych** bez gwałtownych zmian
- Dla danych z **dużymi skokami** rozważ:
  - Interpolację przedziałami (piecewise)
  - Funkcje sklejane (splines)
  - Niższy stopień wielomianu
- Aplikacja używa metody najmniejszych kwadratów (numpy.polyfit)

## Rozwiązywanie problemów

### Błąd: "No module named 'numpy'" lub "No module named 'matplotlib'"

Zainstaluj brakujące biblioteki:
```bash
pip install numpy matplotlib
```

### Błąd: "No module named 'tkinter'"

Na systemach Linux może być potrzebna instalacja tkinter:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

### Wykres się nie wyświetla

- Upewnij się, że matplotlib jest poprawnie zainstalowany
- Sprawdź, czy używasz środowiska graficznego (GUI)

## Autor

Aplikacja stworzona do analizy rozkładów temperatury w czujnikach światłowodowych.

## Licencja

Darmowa do użytku edukacyjnego i badawczego.
