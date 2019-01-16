# Dokumentacja projektowa

### Aplikacja webowa umożliwiająca zamówienie kuriera w celu wysłania przesyłki oraz analiza i wizualizacja danych dotyczących wykorzystania serwisu przez użytkowników.


# Spis treści
1. [Opis projektu](#opis-projektu)
  - [Analiza wymagań funkcjonalnych](#analiza-wymagań-funkcjonalnych)
    - [Gość](#gość)
    - [Użytkownik](#użytkownik)
    - [Admin](#admin)
  - [Wykorzystane technologie oraz biblioteki](#wykorzystane-technologie-oraz-biblioteki)
    - [Lista technologii wykorzystanych w projekcie](#lista-technologii-wykorzystanych-w-projekcie)
    - [Biblioteki wykorzystane do generowania wykresów](#biblioteki-wykorzystane-do-generowania-wykresów)
2. [Przykładowe użycie aplikacji](#przykładowe-użycie-aplikacji)
  - [Przeglądanie statystyk](#przeglądanie-statystyk)
  - [Proces zamówienia kuriera](#proces-zamówienia-kuriera)
  - [Przegląd rankingu kurierów](#przegląd-rankingu-kurierów)
# Opis projektu
Stworzona przez nas aplikacja webowa umożliwia zamówienie kuriera w celu
wysłania przesyłki. Każdy gość odwiedzający nasz serwis uzyskuje możliwość wyceny
przesyłki bez rejestracji. Może przeglądać ranking kurierów, opinie na temat firm kurierskich
oraz ranking ich popularności. Jeżeli gość zdecyduje się na skorzystanie z naszych usług
najpierw musi zarejestrować się w naszym serwisie. Po rejestracji użytkownik może przejść
do procesu zamówienia przesyłki. Składa się on z podania informacji o przesyłce, wyboru
interesującego nas kuriera, podania danych nadawcy i odbiorcy oraz zatwierdzenia
zamówienia. Dodatkowo po każdym złożonym zamówieniu klient otrzymuje punkty premium,
które może wykorzystać w sklepie premium, w celu odebrania nagrody. Użytkownik może
przeglądać wszystkie złożone przez niego zamówienia, oraz ocenić każde zamówienie
w formie wystawienia opinii dla wybranej przez niego firmy kurierskiej. Jeżeli przesyłka nie
została jeszcze wysłana ma możliwość anulowania zamówienia. Po zalogowaniu na konto
admina możemy zarządzać serwisem zamawiania paczek m.in. zmieniać status zamówień,
dodawać nowych kurierów do bazy, dodawać prezenty oraz modyfikować bazę danych.
Ważną funkcjonalnością admina jest również analiza danych dotyczących wykorzystywania
serwisu przez użytkowników. Realizowana jest ona w formie wykresów, które generowane
są na podstawie informacji zawartych w bazie danych.

### Analiza wymagań funkcjonalnych
#### Gość
- Gość może utworzyć konto w naszej aplikacji.
- Gość może przeglądać dostępnych kurierów oraz cennik.
- Gość może obliczyć cenę przesyłki.
- Gość może przeglądać ranking kurierów.
- Gość może przeglądać opinie dotyczące kurierów.
#### Użytkownik
- Użytkownik może tworzyć/edytować/aktualizować swoje dane adresowe.
- Użytkownik może zamówić kuriera, by nadać paczkę.
- Użytkownik może wybrać kuriera z listy kurierów.
- Użytkownik może wyświetlać swoje zamówienia.
- Użytkownik może anulować swoje zamówienie.
- Użytkownik może obliczyć koszty wysłania paczki.
- Użytkownik może wystawiać opinie po złożonym zamówieniu
- Użytkownik może zbierać punkty premium.
- Użytkownik może użyć punktów premium do odebrania prezentów.
#### Admin
- Admin może przeglądać statystyki realizowane w formie wykresów.
- Admin może zarządzać bazą danych.


### Wykorzystane technologie oraz biblioteki
Aplikacja webowa została stworzona w oparciu o framework Django przeznaczony
do tworzenia aplikacji internetowych. System zarządzania bazą danych wykorzystywany
w naszym projekcie to SQLlite.
#### Lista technologii wykorzystanych w projekcie:
- Python: 3.6.6
- Django: 2.1.2
- HTML5
- CSS3
- JavaScript
- JQuery: 3.1
- Bootstrap: 4.1.3
#### Biblioteki wykorzystane do generowania wykresów:
- FusionCharts
- GoogleCharts
- Plotly

# Przykładowe użycie aplikacji
### Przeglądanie statystyk
- Logujemy się do aplikacji jako administrator aby podglądnąć statystyki serwisu.
<br />![1](screenshots/Image-1.png) <br/>
- Po kliknięciu w zakładkę “Wykresy” przenosimy się do podstrony ze statystykami.
<br />![1](screenshots/Image-2.png) <br/>
- Wykres słupkowy obrazujący liczbę wszystkich zamówień dla wszystkich firm kurierskich w naszym serwisie.
<br />![1](screenshots/Image-3.png) <br/>
- Wykres liniowo-punktowy obrazujący szczegółowo liczbę zamówień w każdym dniu.
<br />![1](screenshots/Image-4.png) <br/>
- Wykres słupkowy przedstawiający liczbę zamówionych przesyłek w danym miesiącu
po wybraniu konkretnego roku kalendarzowego.
<br />![1](screenshots/Image-5.png) <br/>
- Wykres słupkowy obrazujący z jakiej miejscowości są użytkownicy
<br />![1](screenshots/Image-6.png) <br/>
- Wykres punktowo-liniowy obrazujący przychody w danym miesiącu kalendarzowym
<br />![1](screenshots/Image-7.png) <br/>
- Wykres słupkowy przedstawiający średnią ocenę firm kurierskich wystawianych
przez użytkowników
<br />![1](screenshots/Image-8.png) <br/>

### Proces zamówienia kuriera
- Rozpoczynamy od wyboru rodzaju przesyłki.
<br />![1](screenshots/Image-9.png) <br/>
- Następnie wybieramy firmę kurierską. Każda firma posiada inny cennik.
<br />![1](screenshots/Image-10.png) <br/>
- Kolejny krokiem jest podanie adresu nadawcy.
<br />![1](screenshots/Image-11.png) <br/>
- Następnie podajemy adres odbiorcy.
<br />![1](screenshots/Image-12.png) <br/>
- Gdy uzupełniliśmy wszystkie dane poprawnie możemy potwierdzić nasze
zamówienie.
<br />![1](screenshots/Image-13.png) <br/>
- Gdy złożymy zamówienie, możemy sprawdzić jego stan w zakładce zamówienia -
możemy również dodać ocenę lub anulować zamówienie.
<br />![1](screenshots/Image-14.png) <br/>
- Przykładowe wystawienie oceny dla wcześniejszego zamówienia
<br />![1](screenshots/Image-15.png) <br/>
- W zakładce “Cennik” możemy zobaczyć opinie dla danych firm.
<br />![1](screenshots/Image-16.png) <br/>

### Przegląd rankingu kurierów
Każdy użytkownik serwisu może przeglądnąć nasz ranking firm kurierskich.
- 5 Najpopularniejsz firm kurierskich (procentowy udział w liczbie zamówień)
<br />![1](screenshots/Image-17.png) <br/>
- Wykres kołowy przedstawia procentowo powyższe dane
<br />![1](screenshots/Image-18.png) <br/>
