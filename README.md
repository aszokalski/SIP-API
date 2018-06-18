# SIPapi
Nieoficjalne API Systemu Informacji Pasażerskiej w Warszawie.

Wersja: v1.0

Stan: Produkcja (offline)
# Dokumentacja API v1.0
## Pobierz tabelę tramwajów nadjeżdżających na dany przystanek w formacie JSON
`/sip/api/{wersja API}/przystanek/{numer identyfikacyjny przystanku}`

Wyjście: 
### Przykład
Wersja API = v1.0

ID przystanku = 605905 (Metro Młociny [05])

`curl 127.0.0.1:5000/sip/api/v1.0/przystanek/605905`

Wyjście: 
``` JSON
{
  "605905": [
    {
      "czas_do_odjazdu": "",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "35"
    },
    {
      "czas_do_odjazdu": "2 min",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "22"
    },
    {
      "czas_do_odjazdu": "3 min",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "24"
    },
    {
      "czas_do_odjazdu": "11 min",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "26"
    },
    {
      "czas_do_odjazdu": "19 min",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "35"
    },
    {
      "czas_do_odjazdu": "20 min",
      "kierunek": "ZET \u017bOLIBORZ",
      "linia": "33"
    }
  ]
}
````
Oczywistym problemem wersji v1.0 jest brak polskich znaków, które zamierzam dodać w następnej wersji API. Pierwsza wersja również nie posiada, żadnych zabezpieczeń przed nieprawidłowym ID.

## Jak zdobyć ID przystanku?
Wystarczy wejść na stronę https://tw.waw.pl/sip/#/wg-przystankow i wybrać przystanek, który nas interesuje. Jak załaduje nam się strona to ID znajduje się w linku. `https://tw.waw.pl/sip/#/przystanek/{ID}`

## Problemy, których nie mogę rozwiązać
1.  Od momentu wywołania komendy `curl` do zwrócenia danych przez API mija około 6 sekund. Jest to spowodowane długim ładowaniem na stronie https://tw.waw.pl/sip. 
2.  API działa na systemie MacOS i Windows. Na linuxie mam problemy z webdriverem.
