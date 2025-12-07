# Główny schemat przepływu danych systemu 
```mermaid
graph LR
    %% Zmiana kierunku na LR (Left-Right) zapobiega ścisku i nachodzeniu okienek
    
    subgraph Local_Network [Strefa Lokalna / Użytkownik]
        direction TB
        User((Użytkownik))
        
        subgraph Devices [Urządzenia]
            direction TB
            Mobile[Aplikacja Mobilna<br>React Native / Expo]
            Cube[Intelligent Cube<br>Raspberry Pico Pi + Gyro + OLED]
        end
    end

    subgraph Cloud_Infrastructure [Google Cloud Platform]
        direction TB
        Server[ Backend Server<br>Python Flask / Cloud Run]
        DB[(Baza Danych<br>PostgreSQL)]
        Redis[(Cache<br>Redis)]
    end

    %% --- RELACJE ---
    
    %% 1. Użytkownik i jego urządzenia
    User -->|"1. Konfiguracja<br>& Postępy"| Mobile
    User -->|"2. Obrót /<br>Przyciski"| Cube
    Cube -->|"3. Feedback:<br>LED / Dźwięk"| User

    %% 2. Komunikacja z Serwerem
    Mobile -->|"HTTPS: API Requests"| Server
    
    %% 3. Cykl życia zadania (Cube <-> Server)
    Cube -->|"HTTPS: POST /complete"| Server
    
    Server -->|"Response: 200 OK"| Cube

    %% 4. Backend Logic
    Server <-->|CRUD| DB
    Server <-->|Cache| Redis

    classDef userFill fill:#fff59d,stroke:#333,stroke-width:2px,color:#000;
    classDef deviceFill fill:#90caf9,stroke:#333,stroke-width:2px,color:#000;
    classDef cloudFill fill:#ce93d8,stroke:#333,stroke-width:2px,color:#000;
    classDef dbFill fill:#a5d6a7,stroke:#333,stroke-width:2px,color:#000;

    class User userFill;
    class Mobile,Cube deviceFill;
    class Server cloudFill;
    class DB,Redis dbFill;
```
## Interakcja z kostką - wykonywanie i potwierdzanie nawyków 
Diagram przedstawia proces interakcji użytkownika z kostką: od wykonania nawyku (obrót/przycisk), poprzez weryfikację na backendzie i aktualizację statystyk, aż po informację zwrotną (LED/dźwięk). Uwzględniono również nową funkcjonalność: pobieranie listy nawyków poprzez naciśnięcie dwóch przycisków.
```mermaid
graph TD
    A[START: Interakcja Użytkownika] --> DECISION{Rodzaj wejścia?}

    %% --- ŚCIEŻKA 1: WYKONANIE NAWYKU (STARA) ---
    DECISION -- Obrót / 1 Przycisk --> B(Intelligent Cube: Wykrycie ścianki i wysłanie POST /api/v1/habits/id/complete)
    B --> C(Backend: Pobierz Habit - habit_id)
    C -- Brak Nawyku --> Z404[Zwróć 404: Habit not found]

    subgraph Weryfikacja i Zadanie
        C -- Nawyk OK --> D{Backend: Czy wykonano dzisiaj?}
        D -- Tak --> Z400[Zwróć 400: Już wykonano dzisiaj]
        D -- Nie --> E(Backend: Utwórz HabitTask i dodaj do sesji)
    end

    subgraph Aktualizacja Statystyk i Grywalizacja
        E --> F(Backend: Pobierz/Utwórz HabitStatistics)
        F --> G(Backend: Aktualizuj total_completions, last_completed)
        
        %% GAMIFICATION
        G --> G1(Backend: Oblicz zdobyte XP i sprawdź Level Up)
        
        G1 --> H{Backend: Sprawdź ukończenie poprzedniego Zadania}
        H -- Różnica 1 dnia --> I(current_streak += 1)
        H -- Inny przypadek --> J(current_streak = 1)
        I --> K(Backend: Aktualizuj Best Streak)
        J --> K
    end

    K --> L(DB: Commit - Zapisz Task, Stats i XP)
    L -- Błąd Commit/DB --> Z500[DB: Rollback i Zwróć 500]

    L --> M(Backend: Zwróć 200 OK + zdobyte XP)
    M --> N(Intelligent Cube: Uruchom Feedback Motywacyjny LED, Dźwięk)
    N --> O[KONIEC: Wykonanie Potwierdzone]

    %% --- ŚCIEŻKA 2: POBRANIE LISTY NAWYKÓW (NOWA) ---
    DECISION -- Naciśnięcie 2 Przycisków --> REQ_FETCH(Intelligent Cube: Wyślij GET /api/v1/habits/active)
    
    subgraph Synchronizacja Danych
        REQ_FETCH --> BE_FETCH(Backend: Zapytanie o Aktywne Nawyki)
        BE_FETCH --> DB_FETCH(DB: Pobierz habits WHERE active=true)
        DB_FETCH --> RESP_FETCH(Backend: Zwróć 200 OK + Lista JSON)
    end
```
## Konfiguracja i Dodawanie nowego nawyku
Diagram ilustruje proces tworzenia nowego nawyku w aplikacji mobilnej, weryfikację danych na serwerze, zapis do bazy oraz synchronizację konfiguracji z kostką.
```mermaid
graph TD
    A[START: Użytkownik chce utworzyć nowy nawyk] --> B(Aplikacja Mobilna: POST /api/v1/habits z JSON);

    subgraph Walidacja Danych i DTO
        B --> C1{Backend: Waliduj format deadline_time HH:MM};
        C1 -- Błąd formatu / Nieprawidłowa Częstotliwość --> Z400[Zwróć 400: Nieprawidłowe dane wejściowe];
        C1 -- OK --> C2{Backend: Waliduj częstotliwość FrequencyType};
        C2 -- OK --> D(Backend: Utwórz i waliduj CreateHabitDTO);
    end

    D -- Błąd Walidacji --> Z400;
    D -- Walidacja OK --> E(Backend: Utwórz obiekt Habit);

    subgraph Transakcja Bazodanowa
        E --> F1(DB: Dodaj Habit flush by ID);
        F1 --> F2(DB: Utwórz HabitStatistics z habit_id);
        F2 --> G(DB: Commit - Zapisz oba rekordy);
        G -- Błąd Commit/DB --> Z500[DB: Rollback i Zwróć 500];
    end

    G --> H(Backend: Zwróć 201 Created);
    
    subgraph Akcje Po Utworzeniu
        H --> H1(Usługa Powiadomień: Zaplanuj Przypomnienia na podstawie Częstotliwości);
        H --> I(Aplikacja Mobilna: Potwierdzenie Sukcesu);
        I --> J{Async: Backend wysyła konfig do Kostki};
        J --> K(Intelligent Cube: Aktualizuj Ekrany/Lokalną Konfigurację);
    end

    K --> L[KONIEC: Nowy nawyk gotowy];

    Z400 --> ZK[KONIEC: Proces zakończony błędem];
    Z500 --> ZK;
```
## Monitorowanie progresu wykonywania nawyków i statystyki
Diagram prezentuje przepływ danych podczas przeglądania listy nawyków oraz szczegółowych statystyk w aplikacji mobilnej, z uwzględnieniem filtrowania dat.
```mermaid
graph TD
    A[START: Użytkownik otwiera Aplikację Mobilną] --> B{Użytkownik: Widok Listy czy Szczegóły?};

    subgraph Lista Nawyków
        B -- Lista (GET /habits) --> B1(Aplikacja Mobilna: GET /api/v1/habits);
        B1 --> B2(Backend: Habit.query.all);
        B2 -- Błąd DB --> Z500_G[Zwróć 500];
        B2 -- OK --> B3(Backend: Konwertuj na listę Habit DTO);
        B3 --> B4(Aplikacja Mobilna: Wyświetl Listę);
    end

    subgraph Szczegóły Nawyku z Filtrami
        B -- Szczegóły (GET /habits/id) --> C0{Sprawdź: Czy zastosowano filtry dat?};
        
        C0 -- Tak --> C1_F(Aplikacja Mobilna: GET /api/v1/habits/id?start_date=X&end_date=Y);
        C0 -- Nie --> C1(Aplikacja Mobilna: GET /api/v1/habits/id);
        
        C1_F --> C2(Backend: Pobierz Habit z DB);
        C1 --> C2;

        C2 -- Habit nie znaleziony --> Z404_G[Zwróć 404];
        C2 -- OK --> C3(Backend: Dołącz HabitStatistics);
        
        C3 --> C3_A{Filtrować Zadania po Dacie?};
        C3_A -- Tak --> C3_B(Backend: Filtruj zapytanie HabitTasks po zakresie);
        C3_A -- Nie --> C3_C(Backend: Pobierz ostatnie HabitTasks);
        
        C3_B --> C4(Backend: Zwróć Habit DTO ze Statystykami i Filtrowaną Historią);
        C3_C --> C4;
        
        C4 --> C5(Aplikacja Mobilna: Wyświetl Statystyki i Historię);
    end

    C5 --> K[KONIEC: Dane Wyświetlone];
    B4 --> K;
    Z500_G --> K_E[KONIEC: Błąd];
    Z404_G --> K_E;
```
