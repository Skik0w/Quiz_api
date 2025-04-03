#🎓 PSI - Aplikacja do Tworzenia Quizów

## Kluczowe Funkcjonalności

### Tworzenie i zarządzanie quizami — projektuj własne quizy, edytuj je i udostępniaj innym użytkownikom.

### Historia rozgrywek — śledź swoje postępy i przeglądaj zakończone gry.

### Turnieje — organizuj turnieje, w których N użytkowników rywalizuje w N quizach.

### System nagród i giełda — zdobywaj nagrody i wymieniaj je z innymi użytkownikami za pomocą wbudowanej giełdy.

# Przydatne polecenia

- Instalacja zależności produkcyjnych: `pip install -r requirements.txt`
- Instalacja zależności developerskich: `pip install -r requirements-dev.txt`
- Uruchomienie serwera aplikacyjnego: `uvicorn airportapi.main:app --host 0.0.0.0 --port 8000`
- Dokumentacja API (Swagger): `http://localhost:8000/docs`
- Zbudowanie projektu za pomocą Docker'a: `docker compose build` (w przypadku odświeżenia cache: `docker compose build --no-cache`)
- Uruchomienie projektu za pomocą Docker'a: `docker compose up` (w przypadku nieodświeżonego cache: `docker compose up --force-recreate`)
