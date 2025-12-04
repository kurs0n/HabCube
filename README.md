# HabCube

## Description

The "Intelligent Cube" is an IoT device that supports users in forming and maintaining daily habits. Habits are defined in a mobile application, which allows for configuration and the presentation of statistics regarding progress.

## Introduction

The goal of this project is to create a complete Internet of Things (IoT) system designed to operate on a local network. The system combines hardware (the physical cube) with a mobile application that allows users to define, configure, and track their habits, as well as view statistics on their progress.

The project integrates knowledge from electronics, computer science, network programming, and embedded systems engineering. The work covers both the hardware layer (the cube's design and implementation) and the software layer (server-side communication, backend, mobile user interface, and overall system integration).

## Project Goals

### General Goals
- To create a fully functional IoT system operating within a local network.
- To achieve high effectiveness in helping users build and sustain positive habits.
- To design a system that increases user motivation and engagement in the process of self-improvement.
- To develop a final product that genuinely improves users' quality of life by supporting them in achieving their habit-related goals.

### Educational Goals
- To understand the practical aspects of building end-to-end IoT systems.
- To learn how to integrate hardware and software into a single cohesive system.
- To develop teamwork and project management skills.
- To gain experience in planning, implementing, testing, and documenting a complex technical project.
- To learn which motivational mechanisms are most effective in habit formation and how to design engaging and intuitive user interactions.

## Project Scope

### Key Features
- **Habit Configuration**: Defining and managing habits through a mobile application.
- **Progress Tracking**: Monitoring user progress and presenting it through statistics.
- **Motivational Feedback**: Providing users with visual, sound, and light-based "dopamine hits" to reinforce positive actions.

### System Architecture
The system consists of three main components:
1.  **The Intelligent Cube**: A physical device based on an ESP32 microcontroller that acts as the primary user interaction point.
2.  **Central Server**: A backend service responsible for handling communication with the cube, processing data, and storing user statistics.
3.  **Mobile Application**: A user interface for configuring the cube, defining habits, and viewing progress data.

All components communicate over a local Wi-Fi network.

---

## Tools and Technologies

### Software / Backend
* **Language:** Python 3.9+
* **Framework:** Flask
* **Database ORM:** SQLAlchemy
* **API Documentation:** Flasgger (Swagger UI)
* **Serialization:** Python Dataclasses (DTOs)
* **Deployment:** Google Cloud Run (Dockerized)

### Mobile App / UI
* **Technology:** React Native (To be determined/finalized)

### Database
* **Engine:** PostgreSQL 13+
* **Production:** Google Cloud SQL
* **Caching:** Redis (Google Cloud Memorystore)

### Hardware
* **Microcontroller:** ESP32
* **Peripherals:** 4 OLED Screens (I2C, SPI), Gyroscope, Multiplexer, 2 Tact switches, Audio amplifier, Speaker, LEDs.

### DevOps & Management
* **Containerization:** Docker, Docker Compose
* **CI/CD:** GitHub Actions
* **Version Control:** Git, GitHub
* **Project Management:** GitHub Projects (Kanban board)

---

## Development Setup

### Environment Configuration

It is recommended to enable pre-commit hooks (instructions below).

**IMPORTANT:**
First, run the setup script which automatically adds `export CURRENT_UID` to your `~/.bashrc` (this avoids permission issues with files and folders later):

```bash
./setup-env.sh
source ~/.bashrc
```

### First Run
```bash
# 1. Build the image
docker-compose up -d --build

# 2. Check container status (or use GUI)
docker-compose ps

# 3. View logs
docker-compose logs -f backend

# 4. Check app health
curl http://localhost:5000/health
```
### Running the Application
```bash
# You can run it via Docker Compose or using the MAKEFILE
docker-compose up -d

# Stop
docker-compose down
```
### Using Makefile (Recommended)
The Makefile automatically exports CURRENT_UID:
```bash
make init      # First run / Initialization
make up        # Start services
make down      # Stop services
make logs      # View logs
make test      # Run tests
make help      # View all commands
```
### Services Access
Backend: http://localhost:5000

Adminer (DB UI): http://localhost:8080

PostgreSQL: localhost:5432

Redis: localhost:6379
### Common Commands
```bash
# Basic Docker
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose ps

# Rebuild
docker-compose build
docker-compose up -d --build

# Shell Access
docker-compose exec backend bash

# Tests and Code Quality
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=app
docker-compose exec backend flake8 app/
docker-compose exec backend black app/
docker-compose exec backend pylint app/
docker-compose exec backend mypy app/

# Database Management
docker-compose exec postgres psql -U habcube_user -d habcube
docker-compose exec backend flask db migrate -m "description"
docker-compose exec backend flask db upgrade

# Makefile
make help
```
### Pre-commit Hook
The pre-commit hook runs code quality checks automatically.
```bash
# 1. Create a symlink to the hook
ln -sf ../../pre-commit .git/hooks/pre-commit

# 2. Grant permissions
chmod +x pre-commit
```
### Checks performed:

Black (formatting), isort (import sorting)

Flake8 (style), Pylint (quality), MyPy (types)

You can also run these manually:
```bash
make lint      # Check code
make format    # Auto-format
make test      # Run tests
make quality   # Run all checks
```

## Database Schema

### Table: habits
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique habit identifier. |
| `name` | VARCHAR(100) | Name of the habit (e.g., "Drink water"). |
| `description` | TEXT | Optional description or motivation. |
| `deadline_time` | TIME | Deadline for completing the habit (e.g., 21:00). |
| `frequency` | ENUM | Frequency: `daily`, `weekly`, `monthly`, `hourly`, etc. |
| `active` | BOOLEAN | Whether the habit is active (Default: `TRUE`). |
| `created_at` | TIMESTAMP | Creation timestamp (Default: `CURRENT_TIMESTAMP`). |
| `color` | VARCHAR(10) | Color associated with the habit (for UI/LEDs). |
| `icon` | ENUM | Icon identifier for the UI. |
| `type` | ENUM | Category type (e.g., `water`, `sport`, `code`). |

### Table: habit_tasks
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique task identifier. |
| `habit_id` | INTEGER FK | Foreign key referencing `habits(id)`. |
| `date` | DATE | The date the habit was intended for/completed. |
| `completed` | BOOLEAN | Completion status (Default: `FALSE`). |
| `completion_time` | TIMESTAMP | Exact timestamp of completion (UTC). |

### Table: habit_statistics
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique statistics record identifier. |
| `habit_id` | INTEGER FK | Foreign key referencing `habits(id)`. |
| `total_completions` | INTEGER | Total count of successful completions. |
| `current_streak` | INTEGER | Current count of consecutive completions. |
| `best_streak` | INTEGER | Highest streak ever achieved for this habit. |
| `success_rate` | FLOAT | Percentage of successful completions vs opportunities. |
| `last_completed` | DATE | Date of the last successful completion. |
| `updated_at` | TIMESTAMP | Last time statistics were recalculated. |

### ER Diagram:
<img width="578" height="487" alt="Image" src="https://github.com/user-attachments/assets/62d5e32d-f056-4b91-b551-dfae8bc929b0" />

## Data Flow
### Configuration and Creation of a New Habit
```mermaid
graph TD
    A[START: Użytkownik chce utworzyć nowy nawyk] --> B(Aplikacja Mobilna: POST /api/v1/habits z JSON);

    subgraph Walidacja Danych i DTO
        B --> C1{Backend: Walidacja Format deadline_time HH:MM};
        C1 -- Błąd formatu / Niepoprawna częstotliwość --> Z400[Zwróć 400: Invalid Input];
        C1 -- OK --> C2{Backend: Walidacja frequency FrequencyType};
        C2 -- OK --> D(Backend: Utworzenie i walidacja CreateHabitDTO);
    end

    D -- Błąd walidacji DTO --> Z400;
    D -- Walidacja OK --> E(Backend: Utworzenie obiektu Habit);

    subgraph Transakcja Bazodanowa
        E --> F1(DB: Dodaj Habit flush po ID);
        F1 --> F2(DB: Utwórz HabitStatistics z habit_id);
        F2 --> G(DB: Commit - Zapisz oba rekordy);
        G -- Błąd Commit/DB --> Z500[DB: Rollback i Zwróć 500];
    end

    G --> H(Backend: Zwróć 201 Created);
    H --> I(Aplikacja Mobilna: Potwierdzenie sukcesu);

    I --> J{Asynchronicznie: Backend wysyła konfigurację do Kostki};
    J --> K(Intelligent Cube: Aktualizacja Ekranów/Lokalnej Konfiguracji);
    K --> L[END: Nowy nawyk gotowy];

    Z400 --> ZK[END: Proces zakończony błędem];
    Z500 --> ZK;
```

### Execution and Confirmation of Habit (Cube Interaction)
```mermaid
graph TD
    A[START: Użytkownik obraca i naciska Tact Switch] --> B(Intelligent Cube: Wykrycie ściany i wysłanie POST /api/v1/habits/id/complete);
    B --> C(Backend: Pobierz Habit - habit_id);
    C -- Brak Habitu --> Z404[Zwróć 404: Habit not found];

    subgraph Weryfikacja i Task
        C -- Habit OK --> D{Backend: Sprawdź, czy nawyk ukończony dzisiaj?};
        D -- Tak --> Z400[Zwróć 400: Already completed today];
        D -- Nie --> E(Backend: Utwórz HabitTask i dodaj do sesji);
    end

    subgraph Aktualizacja Statystyk
        E --> F(Backend: Pobierz/Utwórz HabitStatistics);
        F --> G(Backend: Zaktualizuj total_completions, last_completed);
        G --> H{Backend: Sprawdź poprzednie ukończenie Task};
        H -- Różnica 1 dzień --> I(current_streak += 1);
        H -- Inny przypadek --> J(current_streak = 1);
        I --> K(Backend: Aktualizuj Best Streak);
        J --> K;
    end

    K --> L(DB: Commit - Zapisz Task i Statystyki);
    L -- Błąd Commit/DB --> Z500[DB: Rollback i Zwróć 500];

    L --> M(Backend: Zwróć 200 OK);
    M --> N(Intelligent Cube: Uruchom Motywacyjny Feedback LEDs, Sound);
    N --> O[END: Potwierdzenie wykonania];

    Z404 --> ZK[END: Błąd];
    Z400 --> ZK;
    Z500 --> ZK;
```
### Monitoring Progress and Statistics
```mermaid
graph TD
    A[START: Użytkownik otwiera Aplikację Mobilną] --> B{Użytkownik: Czy chce zobaczyć listę czy szczegóły?};

    subgraph Lista Nawykow
        B -- Lista (GET /habits) --> B1(Aplikacja Mobilna: GET /api/v1/habits);
        B1 --> B2(Backend: Habit.query.all);
        B2 -- Błąd DB --> Z500_G[Zwróć 500];
        B2 -- OK --> B3(Backend: Konwersja do listy Habit DTO);
        B3 --> B4(Aplikacja Mobilna: Wyświetlenie Listy);
    end

    subgraph Szczegoly Nawyku
        B -- Szczegóły (GET /habits/id) --> C1(Aplikacja Mobilna: GET /api/v1/habits/id);
        C1 --> C2(Backend: Pobierz Habit z DB);
        C2 -- Habit nie znaleziony --> Z404_G[Zwróć 404];
        C2 -- OK --> C3(Backend: Dołącz HabitStatistics);
        C3 --> C4(Backend: Zwróć Habit DTO ze Statystykami);
        C4 --> C5(Aplikacja Mobilna: Wyświetlenie Statystyk i Historii);
    end

    C5 --> K[END: Dane wyświetlone];
    B4 --> K;
    Z500_G --> K_E[END: Błąd];
    Z404_G --> K_E;
```


### Detailed Functionalities
| ID | Category | Functionality | Description |
| :--- | :--- | :--- | :--- |
| **A1** | **Habit Management** | **Create/Configure** | Enables adding a new habit (name, description), setting **frequency** (`daily`, `weekly`, etc.) and optional **deadline**. |
| **A2** | **Habit Management** | **Activate Daily Set** | User **manually activates** a list of habits to perform on a given day, which is then sent to the cube. |
| **A3** | **Habit Management** | **Edit/Delete** | Enables modification of existing habit parameters or removing it completely from the system. |
| **A4** | **Monitoring** | **Progress Visualization** | Presentation of statistics: **Total Completions**, **Current Streak**, **Best Streak**. |
| **A5** | **Monitoring** | **Completion History** | Displays a detailed calendar or task list (`HabitTask`) with completion dates/times. |
| **A6** | **Cube Interaction** | **Pairing/Config** | Enables connecting to the cube on the local network and **assigning habits to the cube's screens**. |

### Intelligent Cube (Hardware)
| ID | Category | Functionality | Description |
| :--- | :--- | :--- | :--- |
| **C1** | **State Display** | **Display Habits** | **OLED Screens** display the **active habit** for the day along with its current status. |
| **C2** | **Interaction** | **Change Active Habit** | **Pressing the Tact Switch** on the active face changes the displayed habit (e.g., "Reading" -> "Running"). |
| **C3** | **Interaction** | **Confirm Completion** | **Rotating the cube** onto a specific face (detected by **Gyroscope**) confirms task completion. |
| **C4** | **Motivation** | **Sensory Feedback** | Upon completion (C3), the cube provides **Motivational Feedback**: **LEDs** flash and **Speaker** plays a sound. |
| **C5** | **Communication** | **Send Data** | After confirmation, sends `POST /api/v1/habits/{id}/complete` to the Central Server. |
| **C6** | **Communication** | **Receive Configuration** | Cube receives active habits list from Central Server and updates displays dynamically. |

### Deployment on Google Cloud (FOR ADMIN A.D. ONLY)
The application is ready for deployment on Google Cloud Platform with the following services:
- Cloud Run - Serverless Flask backend
- Cloud SQL for PostgreSQL - Managed database
- Memorystore for Redis - Managed cache
- Secret Manager - Secure credential storage

### Using the API (GCLOUD)
- Authenticate:
```bash
gcloud auth login
```
- Generate Token:
```bash
TOKEN=$(gcloud auth print-identity-token)
```
- Test via Curl:
```bash
curl [https://backend-1089871134307.europe-west1.run.app/api/v1/habits](https://backend-1089871134307.europe-west1.run.app/api/v1/habits)
```

## API Reference (Endpoints)
### Habit Management Endpoints
| Method | Endpoint | Description | Required Data |
| :--- | :--- | :--- | :--- |
| **GET** | `/habits` | Retrieves a list of all defined habits. | - |
| **POST** | `/habits` | Creates a new habit. | JSON: `name`, `frequency`, `type`, etc. |
| **GET** | `/habits/{id}` | Retrieves details of a specific habit with stats. | `id` (int) in URL |
| **POST** | `/habits/{id}/complete` | Marks a habit as completed for today. | `id` (int) in URL |
| **GET** | `/habits/active` | Retrieves habits "ready" to be completed now. | - |
| **GET** | `/finished-habits` | Retrieves archived habits with success status. | - |

### System Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/statistics` | Returns global user statistics (total habits, streaks). |
| **GET** | `/health` | Health check - verifies service and DB status. |****

# HabCube Mobile Application Documentation

## 1. Overview
The HabCube mobile application is a cross-platform solution built with **React Native** and **TypeScript**. It acts as the primary user interface for configuring habits, tracking progress, and visualizing statistics from the IoT Cube.

## 2. Technology Stack

* **Framework:** React Native (0.81.4)
* **Language:** TypeScript (5.9.2)
* **Build Tool:** Expo / React Native CLI
* **Navigation:** React Navigation (Native Stack)
* **State Management:** React Hooks (`useState`, `useEffect`, Custom Hooks)
* **HTTP Client:** Axios
* **UI Libraries:**
    * `react-native-vector-icons` (Ionicons)
    * `react-native-safe-area-context`
    * `@react-native-picker/picker`
    * `@react-native-community/datetimepicker`
    * `react-native-toast-message`

## 3. Project Structure

The project follows a **Feature-based / Component-folder** structure:

```text
src/
├── api/                  # API communication layer
│   ├── client.ts         # Axios instance configuration
│   ├── endpoints.ts      # API URL constants
│   └── habits.api.ts     # Service functions (GET, POST)
├── assets/
│   ├── data/
│   │   └── icons.ts      # List of available habit icons
│   └── iconNoBg1.png     # Application logo
├── components/           # UI Components & Screens
│   ├── AddHabit/         # Habit creation screen
│   ├── AppLogo/          # Reusable logo component
│   ├── BottomNavbar/     # Custom bottom navigation bar
│   ├── FinishedHabits/   # History screen
│   ├── HabitsStats/      # Statistics screen
│   ├── MainPage/         # Dashboard (Active habits)
│   └── WelcomeScreen.tsx # Intro screen
├── constants/
│   └── config.ts         # Environment configuration (API URL)
├── hooks/                # Business Logic (Custom Hooks)
│   ├── useCreateHabit.ts
│   ├── useFinishedHabits.ts
│   ├── useHabits.ts
│   └── useStatsHabits.ts
└── types/
    └── habit.types.ts    # TypeScript interfaces
```
## 4. Architecture & Data Flow
### The application uses the Service-Hook-Component pattern to separate concerns:
- API Layer (src/api): Handles direct HTTP communication using Axios. It defines endpoints and raw data fetching functions.

- Hooks Layer (src/hooks): Encapsulates business logic and state management. It calls the API layer and exposes simple variables (data, loading, error) to the UI.

- UI Layer (src/components): Purely presentational components that consume Hooks to display data.

### Example Flow: Fetching Habits
- Component (MainPage) mounts and calls useHabits().

- Hook (useHabits) sets loading=true and calls getHabits() from API.

- API (habits.api.ts) performs GET /habits via Axios.

- Backend returns JSON data.

- Hook updates habits state and sets loading=false.

- Component re-renders with the habit list.

### Configuration (config.ts)
The application automatically detects the running environment to set the correct Backend URL:

- Android Emulator: Uses 10.0.2.2:5000 (Access to host localhost).

- iOS Simulator: Uses localhost:5000.

- Physical Device: Requires manual IP configuration or network tunneling (if not deployed to cloud).

### Key Components Description
| Component | Description |
| :--- | :--- |
| **WelcomeScreen** | Initial landing page with a "Start" button. |
| **MainPage** | The dashboard displaying active habits, current streaks, and a 21-day progress bar. Allows checking completion status. |
| **AddHabit** | A form to create new habits with validation. Users choose name, icon, frequency, and type. |
| **FinishedHabits** | A list of archived or completed habits showing final stats and success status. |
| **HabitsStats** | Global statistics dashboard (Total habits, Longest streak, Completion rate). |
| **BottomNavbar** | Custom navigation bar visible on main screens, handling routing. |
---

### 2. Instrukcja Instalacji Frontendu (`docs/FRONTEND_SETUP.md`)

Ten plik zawiera instrukcje dla deweloperów, jak uruchomić aplikację.

# Frontend Setup Guide

## Prerequisites

Before running the mobile application, ensure you have:

1.  **Node.js** (LTS version recommended) installed.
2.  **npm** or **yarn** package manager.
3.  **Mobile Development Environment:**
    * **Android:** Android Studio with configured Android SDK and Emulator.
    * **iOS (macOS only):** Xcode with iOS Simulator.
4.  **Backend Running:** The Flask backend must be running on port `5000`.

## Installation

1.  Navigate to the project root directory:
    ```bash
    cd habcube
    ```

2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  Link assets (if using React Native CLI specific fonts/icons):
    ```bash
    npx react-native-asset
    ```

## Running the Application

### 1. Start Metro Bundler
Start the JavaScript bundler in a dedicated terminal:
```bash
npm start
```
### 2. Run on Emulator/Simulator
For Android: Ensure your Android Emulator is running (visible in Android Studio Device Manager).
```bash
npm run android
```
### For iOS (macOS only):
```bash
npm run ios
```


Rebuild the app (npm run android / npm run ios).
## Changelog
2025-10-20
### Google Cloud Deployment Ready

- Backend Configuration

    - Updated config.py to support Cloud SQL (127.0.0.1) and Memorystore.

    - Added support for environment variables: DB_HOST, DB_USER, REDIS_HOST, etc.

    - Maintained compatibility with local Docker Compose.

- Dockerfile Improvements

    - Added support for the PORT variable (required by Cloud Run).

    - Updated CMD to use ${PORT:-5000}.

    - Health check now uses the dynamic port.

- Deployment Tools

    - Created deploy-gcloud.sh - interactive deployment script.

    - Created .env.gcloud.template - GCP configuration template.

### 2025-10-15
### Habits API - Initial Implementation

- Models

    - Created Habit model - stores user habits.

    - Created HabitTask model - registers habit executions.

    - Created HabitStatistics model - statistics and streaks.

    - Added database migrations.

- Enums and DTOs

    - FrequencyType enum: every_30_min, hourly, every_3_hours, every_6_hours, daily, weekly, monthly.

    - CreateHabitDTO - input data validation.

    - HabitResponseDTO - API response format.

- Endpoints

    - GET /api/v1/habits - list of all habits.

    - GET /api/v1/habits/{id} - habit details with statistics.

    - POST /api/v1/habits - create new habit.

    - POST /api/v1/habits/{id}/complete - mark habit as completed.

- Documentation

    - Swagger/Flasgger integration.
    
    - Request/Response examples for each endpoint.
    
    - Available at: http://localhost:5000/api/docs/

- Tests
    - Tests for all endpoints.

    - Data validation tests.

    - Error case tests (404, 400).

    - Statistics and streak tracking tests.

## Team
- Piotr Ziobrowski - Embedded programming, Cube 3D project

- Szymon Domagała - Frontend, UI

- Paweł Klocek - Database, Backend, Documentation

- Aleksy Dąda - Backend, Docker

- Patryk Kurek - Hardware, Embedded programming, Tech Lead

Special thanks to: https://github.com/amora-labs/micropython-captive-portal/blob/master/captive.py
