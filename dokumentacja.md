# Temat 

Zbadanie funkcjonalności dostępnej w środowisku R/Python dotyczącej regresji przestrzennej, w tym autoregresji. Celem zadania jest ocena dostępnych metod pod kątem ich przydatności do analizy danych przestrzennych: poprawność działania, czas wykonania w zależności od wielkości danych, łatwość użycia, dostępność materiałów pomocniczych.


# Metody reprezentacji i wizualizacji

## Reprezentacja

Tabelaryczne dane przestrzenne to najprościej ujmując tabele, które w jednej z kolumn przechowują informacje przestrzenne, czyli informacje o typie geometrii, współrzędnych, kształcie obiektów. Na przykład mogą to być punkty na mapie (typ: punkt; współrzędne) lub obszary na mapie (typ: wielokąt; współrzędne wierzchołów obszaru).
Najpopularniejsze pakiety do operowania na tabelarycznych danych przestrzennych w językach Python i R to odpowiednio *GeoPandas* i *sf*. 

![Tabela w sf](https://hackmd.io/_uploads/ryMzvqpvp.png)

![Tabela w GeoPandas](https://hackmd.io/_uploads/H1ZfDcTDp.png)

## Wizualizacja

Jeśli chodzi o *sf* bardzo łatwo jest wizualizować geometrie. *sf* oferuje wbudowany wizualizator danych, który można według potrzeb konfigurować. Wystarczy wywołać `plot(spatial_data)`, by otrzymać poniższe wykresy.

![Wizualizacja map w R](https://hackmd.io/_uploads/B1hgcj6wp.png)

Oprócz tego, tabele *sf* mogą być rysowane przez inne R-owe pakiety do wizualizacji takie jak *mapview, tmap, ggplot2*

Analogicznie *GeoPandas* ma wbudowaną standardową wizualizację `spatial_data.plot()`. Obrazy generowane są przez pakiet Matplotlib, który również umożliwia konfigurację według potrzeb.


![Wizualizacja map w Matplotlib](https://hackmd.io/_uploads/HJ-My3TPa.png)

\pagebreak

Przed wizualizacją dane można przetwarzać. Na przykład w przypadku danych będących punktami przestrzennymi możemy wyznaczyć sąsiedztwo punktów i uwzględnić je na rysunku.

`neigbours.plot(spatial_data)`

![Wizualizacja sąsiedztwa punktów w Matplotlib](https://hackmd.io/_uploads/Hkh8bnaP6.png)


# Środowisko

Instrukcja przygotowania środowiska znajduje się w README.md w repozytorium z kodem źródłowym.

# Zbiory danych

### Baltimore
Dane zawierające charakterystykę oraz ceny sprzedanych domów w Baltimore w roku 1978; 17 kolumny, 211 wiersze.

### Berlin
Dane z serwisu AirBnB z dzielnicy Berlina Prenzlauer Berg. Zawierają statystyki wynajmów poprzez AirBnB; 9 kolumny, 2203 wiesze.


### California
Wycena wartości domów w Kaliforni w podziale na gminy z 2000 roku; 29 kolumny, 7049 wiersze.


# Eksperymenty
Celem eksperymentów było zbadanie szybkości oraz skuteczności modeli autoregresji przestrzennej na zbiorach zawierających nieuwzględnione podczas treningu obiekty testowe. Do eksperymentów zostały najpopularniejsze pakiety do regresji przestrzennej, które oferują języki Python oraz R, czyli odpowiednio, *pysal* oraz *spatialreg*. Badane modele to 

- OLS (Ordinary Least Squares), czyli zwykła regresja liniowa.
- Spatial Lag Model, Spatial Error Model, czyli modele autoregresji przestrzennej. Oba są optymalizowane przez algorytm Maximum Likelihood Estimation, który maksymalizuje współczynniki regresji, tak aby najbardziej pasowały do obserwacji (danych treningowych). Różnica pomiędzy nimi polega na tym, że zależności przestrzenne pomiędzy obszarami sąsiadującymi w Lag Model są modelowane na podstawie podobieństwa zmiennej objaśnianej, a w Error Model na podstawie podobieństwa wartości błędu podczas przewidywania zmiennej objaśnianej na danych treningowych.

Oba badane pakiety oferują implementacje powyższych modeli.

Zbiory danych są dzielone na rozłączne podzbiory treningowy i testowy.
Szybkość modeli jest liczona podczas treningu, a skuteczność modeli na zbiorze testowym metryką jakości: `średni błąd bezwzględny / średnia wartość zmiennej objaśnianej`, która aproksymuje procentowe pomyłki modelu. 

# Problemy
- Liczne konflikty pomiędzy wersjami pakietów pythonowych, nigdzie przez autorów nieopisane, które trzeba było rozwiązywać metodą prób i błędów oraz doświadczeniem innych użytkowników w intenecie. Ostatecznie po wielu godzinach udało się wypracować plik *requirements.txt*.
- Okazało się, że modele regresji przestrzennej nie są przystosowane do wykonywania przewidywań na danych nieznanych (out-of-sample), a bardziej do wyjaśniania zależności pomiędzy danymi znanymi (in-sample). Modele z *pysal.spreg* w ogóle nie wystawiają API do wykonywania predykcji. Próbowałem grzebać w kodzie źródłowym i zrobić to "własnoręcznie" mnożąc wyznaczone współczynniki regresji przez dane testowe, ale było to możliwe tylko dla modelu OLS. 

![Modele autoregresji nie są przystosowane przewidywań](https://hackmd.io/_uploads/BkzUo60wT.png)

- W R jest możliwe wykonywanie predykcji out-of-sample, ale jest to funkcjonalność słabo wspierana i generowała dziwne błędy (pierwszy obrazek poniżej). Które ostatecznie po analizie kodu źródłowego (drugi obrazek poniżej) pakietu *spatialreg* udało się obejść, by jakiekolwiek wyniki wygenerować.

![Stack trace opisanego błędu w R](https://hackmd.io/_uploads/ByzUsa0v6.png)

![Linijki odpowiedzialne za błąd](https://hackmd.io/_uploads/HyMUs6RD6.png)

- Błędy związane z charakterystyką danych (wyspy, brak połączeń pomiędzy sąsiadami). Ostatecznie rozwiązane zastosowaniem flag, ale lepszym rozwiązaniem byłby preprocessing danych.
- Pierwornie do reprezentacji danych przestrzennych w R wybrałem pakiet *terra*. Generowało to problemy podczas przetwarzania danych i uczenia modelu, więc konieczne było zastosować alternatywę (popularniejszy pakiet) *sf*.




# Wyniki

## Szybkość (sekundy)

|Dataset (N)| pysal_OLS | pysal_Lag | pysal_Error |  R_OLS | R_Lag | R_Error |  
| -------- | -------- | -------- | --- |-------- | -------- | --- |
| Baltimore (221)    | 0.017     | 0.022     |  0.021 | 0.001 | 0.494 | 0.254
| Berlin   (2203)   | 0.079     | 1.148     | 1.375 | 0.001| 32.505 | 25.084
| California  (7049)   | 0.0386     | 24.510     | 55.337 | 0.008| 465.36 | 606,73

## Skuteczność ( MAE(Y, Y_pred) / mean(Y) )

|Dataset| R_OLS | R_Lag | R_Error |  
| --- |-------- | -------- | --- |
| Baltimore | 0.235 | 0.336 | 0.225
| Berlin  | 0.328| 0.330 |  0.328
| California| 0.258| 0.596 | 0.326

# Wnioski

- Dostępne modele autoregresyjne są bardziej przystosowane do badań eksploracyjnych na danych (wyjaśnianie charakterystyki i zależności w danych), niż do przewidywań. Przewidywanie tego typu modelami jest umożliwone tylko w języku R, ale to dobrze rozwinięta gałąź nauki. Szybkość modeli oraz skuteczność wskazuje, że do predykcji bezpieczniej jest używać standardowych modeli uczenia maszynowego.
- Z drugiej strony badania eksploracyjne oraz wizualizacja danych przestrzenych jest wspierana na szeroką skalę i łatwa w użytkowaniu.
- Lepiej udokumentowane i w mojej opini lepiej zrobione (mniej błędów, więcej możliwości, łatwiejsza instalacja) są pakiety R, niż Pythona.


# Kod źródłowy

[https://github.com/BartlomiejOlber/spreg](https://github.com/BartlomiejOlber/spreg)
