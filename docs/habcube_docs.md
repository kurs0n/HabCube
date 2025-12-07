# Spis Treści

1. [Zespół](#zespół)
2. [Hardware & OBSW](#habcube---dokumentacja-hardware--obsw)
3. [Baza Danych](#baza-danych)
4. [Backend (API)](#habcube---dokumentacja-backendu)
5. [Aplikacja Mobilna](#dokumentacja-aplikacji-mobilnej-habcube)
6. [Projekt 3D i Obudowa](#dokumentacja-projektu-3d-i-obudowy---habcube)

---
# Zespół

| Imię i nazwisko | Rola | Zakres obowiązków |
|------|------|---------------|
| **Patryk Kurek** | Hardware Lead & Tech Manager | Schematy elektroniczne, montaż podzespołów, rozwój oprogramowania wbudowanego (OBSW), captive portal, dokumentacja |
| **Piotr Ziobrowski** | Embedded Developer | Projekt obudowy 3D, implementacja Wi-Fi, testowanie |
| **Aleksy Dąda** | Backend Lead | Rozwój API, wdrożenie (deployment) w Google Cloud, Docker |
| **Paweł Klocek** | Backend Architect | Schemat bazy danych, endpointy backendowe, dokumentacja |
| **Szymon Domagała** | Frontend Lead | UI/UX aplikacji mobilnej, implementacja w React Native |

---

# HabCube - Dokumentacja Hardware & OBSW 

> **Project:** Intelligent Habit Tracking Cube
> **Version:** 2.0
> **Last Updated:** December 7, 2025
> **Authors:** Patryk Kurek, Piotr Ziobrowski

## Przegląd systemu
HabCube to urządzenie IoT oparte na mikrokontrolerze Raspberry Pi Pico WH. Urządzenie integruje czujniki ruchu (IMU), podwójny interfejs wizualny (OLED) oraz systemy interakcji użytkownika (przyciski, buzzer) w kompaktowej obudowie 3D. Całość zasilana jest napięciem 5V.

## Komponenty Sprzętowe

### Mikrokontroler

**Płytka:** [Raspberry Pi Pico WH](https://botland.com.pl/moduly-i-zestawy-do-raspberry-pi-pico/21575-raspberry-pi-pico-wh-rp2040-arm-cortex-m0-cyw43439-wifi-ze-zlaczami-5056561800196.html)

**Specyfikacja:**
- **Procesor:** Dwurdzeniowy ARM Cortex-M0+ (RP2040)
- **Taktowanie:** Do 133 MHz
- **Pamięć:** 264 KB SRAM, 2 MB Flash
- **WiFi:** Układ bezprzewodowy CYW43439 2.4GHz 802.11n
- **GPIO:** 26 pinów wielofunkcyjnych z wlutowanymi złączami (headers)
- **Interfejsy:** 2x UART, 2x SPI, 2x I2C, 16x kanałów PWM

**Dokumentacja techniczna (Datasheets):**
- [RP2040 Technical Reference](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
- [Pico W Datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf)

---

### Czujniki i Peryferia

#### Czujnik Ruchu (IMU)
**Model:** SparkFun MPU-9250 9DoF (9 stopni swobody)

**Specyfikacja:**
- **Żyroskop:** 3-osiowy, ±250 do ±2000 °/s
- **Akcelerometr:** 3-osiowy, ±2g do ±16g
- **Magnetometr:** 3-osiowy kompas AK8963
- **Interfejs:** I2C (adres 0x68)
- **Rozdzielczość:** 16-bit ADC
- **Częstotliwość odświeżania:** Do 8 kHz (gyro/accel)

**Przeznaczenie:** Wykrywa obrót kostki w celu wyzwolenia zatwierdzenia nawyku.

**Dokumentacja:** [Specyfikacja MPU-9250](https://botland.com.pl/index.php?controller=attachment&id_attachment=2716)

---

#### System Wyświetlania
**Model:** Ekran OLED 1.3" (128x64 pikseli) - Sterownik SH1106

**Specyfikacja:**
- **Rozdzielczość:** 128x64 pikseli (monochromatyczny)
- **Układ sterujący:** SH1106
- **Interfejs:** SPI (4-przewodowy)
- **Napięcie:** 3.3V - 5V
- **Kąt widzenia:** >160°
- **Kontrast:** Regulowany programowo

**Konfiguracja:** Pojedynczy wyświetlacz (zoptymalizowany względem poprzedniej konfiguracji z dwoma ekranami).

**Przeznaczenie:** Wyświetlanie ikon nawyków, nazw, komunikatów statusu oraz animacji.

**Zasoby:**
- [Nota katalogowa SH1106](https://sklep.msalamon.pl/download/127859/?tmstv=1756190702)
- [Instrukcja uruchomienia](https://sklep.msalamon.pl/blog/instrukcja-uruchomienia-wyswietlacza-oled-128x64-sh1106/)
- [Instrukcja generatora bitmap](https://sklep.msalamon.pl/blog/instrukcja-tworzenia-bitmap-z-obrazow-na-bazie-generatora-online/)

---

#### Interfejs Użytkownika
**Model:** [2x Przycisk Membranowy (Samoprzylepny)](https://botland.com.pl/klawiatury-arduino/17118-klawiatura-membranowa-1-szary-klawisz-samoprzylepna-5904422326920.html)

**Specyfikacja:**
- **Typ:** Klawiatura membranowa jednoprzyciskowa
- **Montaż:** Podkład samoprzylepny
- **Kolor:** Szary
- **Działanie:** Sygnał dotykowy (tactile feedback)
- **Interfejs:** Proste zwarcie przełącznika (aktywny stanem niskim)

**Funkcje Przycisków:**
- **Przycisk 1 (GPIO 17):** Przejście do poprzedniego nawyku
- **Przycisk 2 (GPIO 16):** Przejście do następnego nawyku
- **Oba wciśnięte:** Przeładowanie aktywnych nawyków z serwera

**Link do produktu:** [Klawiatura Membranowa](https://botland.com.pl/klawiatury-arduino/17118-klawiatura-membranowa-1-szary-klawisz-samoprzylepna-5904422326920.html)

---

#### Sygnalizacja Dźwiękowa (Audio Feedback)
**Model:** Buzzer Pasywny Grove (Seeedstudio 107020109)

**Specyfikacja:**
- **Typ:** Pasywny buzzer piezoelektryczny
- **Zakres częstotliwości:** 2kHz - 5kHz
- **Napięcie pracy:** 3.3V - 5V
- **Ciśnienie akustyczne:** ≥85dB @ 10cm
- **Częstotliwość rezonansowa:** 2.7kHz ± 300Hz

**Przeznaczenie:** Odtwarzanie motywu muzycznego Mario po wykonaniu nawyku (melodie sterowane PWM).

**Dokumentacja:** [Buzzer MLT-8530](https://files.seeedstudio.com/products/107020109/document/MLT_8530_datasheet.pdf)

---

### Przypisanie Pinów GPIO

#### Wyświetlacz SPI (OLED)
| Funkcja | Pin GPIO | Opis |
|----------|----------|-------------|
| SCK | 2 | Zegar SPI |
| MOSI | 3 | Master Out Slave In (Dane) |
| CS | 4 | Chip Select (aktywny niski) |
| DC | 5 | Wybór Dane/Komenda |
| RST | 6 | Reset Sprzętowy |
| **Magistrala** | SPI0 | Sprzętowy kontroler SPI |

#### Żyroskop I2C (MPU-9250)
| Funkcja | Pin GPIO | Opis |
|----------|----------|-------------|
| SDA | 0 | Linia Danych I2C |
| SCL | 1 | Linia Zegarowa I2C |
| **Magistrala** | I2C0 | Sprzętowy kontroler I2C |
| **Adres** | 0x68 | Domyślny adres I2C |

#### Interfejs Użytkownika
| Komponent | Pin GPIO | Konfiguracja |
|-----------|----------|---------------|
| Przycisk 1 | 17 | WEJŚCIE z PULL_UP |
| Przycisk 2 | 16 | WEJŚCIE z PULL_UP |
| Buzzer (PWM) | 22 | Wyjście PWM |

**Uwaga:** Przyciski są aktywne w stanie niskim (wciśnięty = 0, zwolniony = 1).

---

### Specyfikacja Zasilania

**Wejście:** 5V USB-C (standard Raspberry Pi Pico WH)

**Pobór Prądu:**
- **Pico W (WiFi aktywne):** 80-100 mA
- **Wyświetlacz OLED:** 20 mA
- **MPU-9250:** 3.5 mA (wszystkie czujniki)
- **Buzzer (Aktywny):** 30 mA (szczytowo)
- **Razem (Typowo):** ~110-125 mA @ 5V = **0.55-0.62W**
- **Razem (Szczytowo):** ~155 mA @ 5V = **0.78W** (podczas odtwarzania dźwięku)

---

## Schemat Elektroniczny

### Lokalizacja plików schematu
- **PDF:** `docs/schema/Schematic_IOT2025_2025-10-29.pdf`
- **PNG:** `docs/schema/Schematic_IOT2025_2025-10-29.png`
- **SVG:** `docs/schema/Schematic_IOT2025_2025-10-29.svg`

### Podsumowanie połączeń

```text
Raspberry Pi Pico WH (RP2040)
    │
    ├─── I2C0 (GPIO 0,1) ────► Żyroskop MPU-9250
    │
    ├─── SPI0 (GPIO 2,3,4,5,6) ────► Wyświetlacz OLED SH1106
    │
    ├─── GPIO 16 ────► Przycisk 2 (Następny Nawyk)
    │
    ├─── GPIO 17 ────► Przycisk 1 (Poprzedni Nawyk)
    │
    ├─── GPIO 22 (PWM) ────► Buzzer Pasywny
    │
    └─── WiFi (CYW43439) ────► Backend w Chmurze (Google Cloud Run)
```
---

### Struktura Projektu Hardware

```
obsw/
├── main.py                         # Application entry point & main loop
├── captive/
│   └── captive.py                 # WiFi captive portal system
├── display/
│   └── display.py                 # OLED display management
├── drivers/
│   ├── gyroscope/
│   │   ├── mpu9250.py            # Main 9DoF sensor driver
│   │   ├── mpu6500.py            # Gyro/Accel component
│   │   └── ak8963.py             # Magnetometer component
│   └── oled/
│       ├── sh1106.py             # SH1106 OLED driver (SPI/I2C)
│       └── sh1106.pyi            # Type hints
├── music.py                       # Audio playback (Mario theme)
├── icons.py                       # Habit icon generator (vector graphics)
├── gif/                           # Animation frames (55 BMP files)
│   ├── resized_0.bmp
│   ├── resized_1.bmp
│   └── ... (resized_54.bmp)
├── clear.py                       # Utility script
└── wlan.info                      # WiFi credentials (auto-generated)
```

---
## Kluczowe Systemy (Core Systems)

### 1. Konfiguracja WiFi (Captive Portal)

**Plik:** `captive/captive.py`

#### Cel
Umożliwia bezproblemową konfigurację WiFi, gdy urządzenie nie może połączyć się przy użyciu zapisanych danych uwierzytelniających. Tworzy punkt dostępu (AP) z interfejsem webowym do konfiguracji sieci.

#### Funkcje
- Automatyczne przejście w tryb AP w przypadku błędu połączenia
- Skanowanie sieci z deduplikacją SSID
- Responsywny interfejs webowy HTML5
- Walidacja i zapisywanie danych logowania
- Automatyczny restart po udanym nawiązaniu połączenia

#### Szczegóły Implementacji
**Access Point Configuration:**
```python
ap.config(essid="HabCube", password="habcube2115")
```

**Network Scanning:**
```python
def fetch_networks(wlan):
    scan_results = wlan.scan()
    found_ssids = set()  # Deduplication
    for result in scan_results:
        ssid = result[0].decode('utf-8')
        if ssid and ssid not in found_ssids:
            found_ssids.add(ssid)
            ssid_options += f'<option value="{ssid}">{ssid}</option>'
    return ssid_options
```

**Web Server:**
- **Port:** 80 (HTTP)
- **Socket Timeout:** 2 seconds
- **Method:** POST for credential submission
- **Persistent Storage:** `wlan.info` file (space-separated SSID and password)

**HTML Interface Highlights:**
- Modern CSS3 with flexbox layout
- Mobile-responsive (viewport meta tag)
- Dropdown network selector (auto-populated)
- Password input with type="password"
- Visual feedback during connection attempt

**Przepływ połączenia:**
```
1. Użytkownik łączy się z siecią WiFi "HabCube"
2. Otwiera przeglądarkę → Wykrycie Captive Portal
3. Wybiera sieć docelową z listy rozwijanej
4. Wpisuje hasło
5. Klika "Połącz"
6. Urządzenie weryfikuje dane (timeout 10s)
7. Sukces: Zapisuje dane do wlan.info → Wykonuje restart
8. Błąd: Wyświetla komunikat "Wrong Credentials!" (Błędne dane)
```
### 2. System Zarządzania Wyświetlaczem

**Plik:** `display/display.py`

#### Aktualizacja Architektury
**Optymalizacja:** Przeprowadzono refaktoryzację z obsługi dwóch wyświetlaczy na **pojedynczą instancję wyświetlacza** w celu poprawy wydajności i zmniejszenia zużycia pamięci.

**Inicjalizacja Wyświetlacza:**
```python
spi_oled1 = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3))
cs_oled1 = Pin(4, Pin.OUT, value=1)
dc_oled1 = Pin(5, Pin.OUT)
rst_oled1 = Pin(6, Pin.OUT)

displays = SH1106_SPI(128, 64, spi_oled1, dc_oled1, rst_oled1, cs_oled1,
                      rotate=0, delay=0)
```

#### Key Functions
```python 
def display_text_centered(text):
    displays.fill(0)

    MAX_CHARS_PER_LINE = 16
    lines = [text[i:i+MAX_CHARS_PER_LINE]
             for i in range(0, len(text), MAX_CHARS_PER_LINE)]

    total_text_height = len(lines) * 8  
    y_start = (64 - total_text_height) //

    for i, line in enumerate(lines):
        x_pos = (128 - len(line) * 8) // 2  
        y_pos = y_start + (i * 8)
        displays.text(line, x_pos, y_pos, 1)

    displays.show()
```
Zastosowanie:
- Status połączenia WiFi
- Komunikaty błędów

- Ekrany ładowania

##### 2. Wyświetlanie aktywnych nawyków

```python
def display_active_habit(active_habits, active_habit_index):
    # Safety check for empty list
    if len(active_habits) <= 0:
        display_text_centered("No active habits try adding one in mobile app")
        return

    habit_name = active_habits[active_habit_index]["name"]
    displays.fill(0)

    # Icon positioning (80x48px icons)
    x_icon = (128 - 80) // 2  # Center horizontally

    # Icon selection based on habit type
    habit_type = active_habits[active_habit_index]["type"]
    if habit_type == "water":
        displays.blit(icons.fb_glass, x_icon, 0)
    elif habit_type == "sport":
        displays.blit(icons.fb_sport, x_icon, 0)
    elif habit_type == "language":
        displays.blit(icons.fb_lang, x_icon, 0)
    elif habit_type == "read":
        displays.blit(icons.fb_glasses, x_icon, 0)
    elif habit_type == "code":
        displays.blit(icons.fb_code, x_icon, 0)

    # Text truncation (NEW: prevents overflow)
    max_chars = 16
    if len(habit_name) > max_chars:
        habit_name = habit_name[:max_chars - 3] + "..."

    # Centered text below icon
    text_length = len(habit_name) * 8
    x_text = max(0, (128 - text_length) // 2)
    displays.text(habit_name, x_text, 52, 1)
    displays.show()
```

**Wspierane typy nawyków:**
| Typ | Ikona | Opis |
|------|------|-------------|
| `water` | Glass | Przypomnienie o piciu wody |
| `sport` | Dumbbell | Uprawianie sportu |
| `language` | Book/Flag | Nauka języków |
| `read` | Glasses | Nawyk czytania |
| `code` | Terminal | Nauka programowaia |

##### 3. Wyświetlenie Animacji
```python
def play_animation(frame_delay_ms=5):
    
    frame_number = 1
    while True:
        filename = f"resized_{frame_number}.bmp"
        try:
            with open(filename, "rb") as f:
                f.seek(10)  
                data_offset = int.from_bytes(f.read(4), "little")
                f.seek(data_offset)
                buffer = f.read()

                fb = framebuf.FrameBuffer(bytearray(buffer), 128, 64,
                                         framebuf.MONO_HLSB)

                displays.fill(0)
                displays.blit(fb, 0, 0)
                displays.show()

                utime.sleep_ms(frame_delay_ms)
                frame_number += 1
        except OSError:
            break  
```

**Szczegóły animacji:**
- **Frame Count:** 55 frames
- **Resolution:** 128x64 monochrome
- **Format:** Windows BMP (1-bit)
- **Frame Rate:** 200 FPS (5ms delay)
- **Total Duration:** ~275ms per loop
- **Trigger:** Habit completion celebration

### 3. Gyroscope-Based Rotation Detection

**File:** `main.py` (lines 91-99, 128-183)

#### Algorytm Kalibracji
**Cel:** Wyeliminowanie odchylenia i dryftu czujnika, aby zapewnić dokładne śledzenie obrotu kostki

```python
def calibrate_gyro(samples=200):
    """
    Averages 200 gyroscope readings to calculate Z-axis offset.
    Must be performed with device stationary.
    """
    print("Calibrate gyroscope...")
    sum_z = 0
    for _ in range(samples):
        sum_z += sensor.gyro[2]  # Z-axis (vertical rotation)
        utime.sleep_ms(5)

    offset_z = sum_z / samples
    print(f"Calibrated gyroscope. Offset Z: {offset_z}")
    return offset_z
```

**Parametry Kalibracji:**
- **Liczba próbek:** 200
- **Częstotliwość próbkowania:** 200 Hz (interwał 5 ms)
- **Całkowity czas:** 1 sekunda
- **Cel:** Eliminacja statycznego przesunięcia (bias) wynikającego z tolerancji produkcyjnych

#### Integracja z obrotem

```python
# Main loop (runs at ~100 Hz)
current_time = utime.ticks_ms()
dt = utime.ticks_diff(current_time, last_time) / 1000.0  # Time delta in seconds
last_time = current_time

gyro_z_raw = sensor.gyro[2]  # Read Z-axis gyro (rad/s)

# Apply calibration offset
gyro_z_rad = gyro_z_raw - gyro_offset_raw

# Convert to degrees/second
gyro_z_deg = gyro_z_rad * 57.296  # 180/π

# Dead-zone filtering (eliminate drift from micro-vibrations)
if abs(gyro_z_deg) < 0.5:
    gyro_z_deg = 0

# Integration: angle = angle + angular_velocity * time
angle_z += gyro_z_deg * dt
```

**Parametery:**
- **Dead Zone:** 0.5 °/s (zapobiega fałszywym wynikom)
- **Threshold:** obrót o 160°
- **Direction:** dwukierunkowy (|angle| >= 160)

#### Wykonany nawyk
```python
if abs(angle_z) >= 160:
    print("Rotation detected!")

    # Non-blocking audio (separate thread)
    _thread.start_new_thread(music.play_mario_main_theme, (buzzer,))

    # Visual feedback (5 loops of 55-frame animation)
    play_sui_animation()

    # Backend API call
    complete_and_switch_habit()

    # Update display
    display.display_active_habit(active_habits, active_habit_index)

    # Reset rotation tracker
    angle_z = 0.0
    utime.sleep_ms(1000)  # Debounce period
    last_time = utime.ticks_ms()
```

### 4. Audio Feedback System

**Plik:** `music.py`

#### Implementacja Mario Theme
**Kompozycja:** 75-nutowa melodia w dynamicznym tempie

**Tabela częstotliwości:**
```python
NOTES = {
    'REST': 0,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392,
    'C7': 2093, 'E7': 2637, 'G7': 3136,  # High octave notes
    # ... (88 total note definitions)
}
```

**Funkcja odgrywania muzyki:**
```python
def play_tone(frequency, duration, buzzer):
    if frequency == 0:  # Rest
        buzzer.duty_u16(0)
        time.sleep(duration)
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)  # 50% duty cycle
        time.sleep(duration)
        buzzer.duty_u16(0)  # Stop
```

**Struktura Main Theme:**
```python
def play_mario_main_theme(buzzer):
    melody_notes = [
        'E7', 'E7', 'REST', 'E7', 'REST', 'C7', 'E7', 'REST',
        'G7', 'REST', 'REST', 'REST', 'G6', 'REST', ...
    ]
    tempo_values = [12, 12, 12, 12, 12, 12, 12, 12, ...]

    for _ in range(PLAY_COUNT):  # Play 3 times
        for i in range(len(melody_notes)):
            note_duration_s = (1000 / tempo_values[i]) / 1000.0
            frequency = NOTES[melody_notes[i]]
            play_tone(frequency, note_duration_s, buzzer)

            # Note separation (30% of duration)
            pause = note_duration_s * 0.30
            time.sleep(pause)
```

**Wykonanie:**
- **Czas trwania:** ~8 seconds (3 loops)
- **Liczba nut:** 75 
- **Tempo:** Zmienne (9-12 BPM)
- **Wątek:** Działa w tle (nioe blokuje)

---

### 5. System Generowania Ikon

**File:** `icons.py`

#### Generowanie Grafiki Wektorowej
**Metoda:** Rysowanie programowe z wykorzystaniem FrameBuffer primitives

**Specyfikacja ikon:**
- **Rozdzielczość:** 80x48 pikseli
- **Format:** Monochromatyczny (1 bit)
- **Rozmiar bufora:** 480 bajtów każdy

**Przykład: Ikona szklanki**
```python
def configure_water_icon():
    # Glass dimensions
    TOP_Y, BOT_Y = 5, 42
    TOP_W, BOT_W = 44, 24
    WATER_LEVEL = 0.5  # 50% full

    center_x = 40
    x1_top = center_x - (TOP_W // 2)
    x2_top = center_x + (TOP_W // 2)
    x1_bot = center_x - (BOT_W // 2)
    x2_bot = center_x + (BOT_W // 2)

    # Draw glass outline (trapezoid)
    fb_glass.line(x1_top, TOP_Y, x1_bot, BOT_Y, 1)  # Left edge
    fb_glass.line(x2_top, TOP_Y, x2_bot, BOT_Y, 1)  # Right edge
    fb_glass.line(x1_bot, BOT_Y, x2_bot, BOT_Y, 1)  # Bottom

    # Fill water (gradient fill simulation)
    water_height_px = int((BOT_Y - TOP_Y) * WATER_LEVEL)
    water_surface_y = BOT_Y - water_height_px

    for y in range(BOT_Y - 1, water_surface_y, -1):
        ratio = (BOT_Y - y) / (BOT_Y - TOP_Y)
        current_half_w = (BOT_W // 2) + int((TOP_W - BOT_W) // 2 * ratio)
        fb_glass.hline(center_x - current_half_w + 1, y,
                       current_half_w * 2 - 2, 1)
```

**Przykłady innych ikon:**
- **Kod:** Okno terminala z monitem i kursorem
- **Sport:** Hantle (sztanga z ciężarkami)
- **Język:** Pokrywające się książki z tłumaczeniami
- **Okulary:** Okulary do czytania (dwie soczewki + mostek)

---
---

## Integracja API 

### Backend Endpoint
**URL:** `https://backend-1089871134307.europe-west1.run.app`

### Użyte Endpointy

#### 1. GET /api/v1/habits/active
**Cel:** Wyświetlenie aktualnie aktywnych nawyków

**Request:**
```python
response = requests.get(
    "https://backend-1089871134307.europe-west1.run.app/api/v1/habits/active"
)
```

**Response (200 OK):**
```json
{
  "habits": [
    {
      "id": 1,
      "name": "Drink Water",
      "type": "water",
      "description": "Drink 8 glasses",
      "deadline_time": "21:00",
      "frequency": "daily"
    },
    {
      "id": 2,
      "name": "Morning Exercise",
      "type": "sport",
      "description": "30 min workout",
      "deadline_time": "09:00",
      "frequency": "daily"
    }
  ]
}
```

**Implementacja:**
```python
def load_active_habits():
    global active_habits
    response = requests.get(
        "https://backend-1089871134307.europe-west1.run.app/api/v1/habits/active"
    )
    content = response.content
    habits = json.loads(content)
    active_habits = habits["habits"]
```

#### 2. POST /api/v1/habits/{id}/complete
**Cel:** Ustawienie nawyku jako wykonany

**Request:**
```python
response = requests.post(
    f"https://backend-1089871134307.europe-west1.run.app/api/v1/habits/{habit_id}/complete",
    json={}
)
```

**Response (200 OK):**
```json
{
  "message": "Habit completed successfully",
  "habit_id": 1,
  "completion_time": "2025-12-07T14:30:00Z",
  "current_streak": 5,
  "total_completions": 42
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Already completed today"
}
```

**Implementacja z kontrolą:**
```python
def complete_and_switch_habit():
    # NEW: Safety check for empty list
    if len(active_habits) <= 0:
        return

    habit_id = str(active_habits[active_habit_index]["id"])
    response = requests.post(
        f"https://backend-1089871134307.europe-west1.run.app/api/v1/habits/{habit_id}/complete",
        json={}
    )
    print(response.content)

    # Only remove habit on successful completion
    if response.status_code == 200:
        active_habits.pop(active_habit_index)
        switch_next_habit()
```

---

## Przepływ systemu 

### Sekwencja uruchomienia

```
1. Inicjalizacja 
   ├─ Konfiguracja I2C (GPIO 0,1) dla żyroskopu
   ├─ Konfiguracja SPI (GPIO 2-6) dla wyświetlacza
   ├─ Konfiguracja GPIO 16,17 dla przycisków (PULL_UP)
   ├─ Konfiguracja PWM (GPIO 22) dla buzzera
   └─ Inicjalizacja ikon w buforach ramki (framebuffers)

2. Połączenie Sieciowe
   ├─ Próba odczytu pliku wlan.info
   ├─ Jeśli istnieje:
   │   ├─ Parsowanie SSID i hasła
   │   ├─ Łączenie z WiFi (timeout 10s)
   │   └─ Jeśli błąd → Uruchomienie Captive Portal
   └─ Jeśli nie istnieje → Uruchomienie Captive Portal

3. Synchronizacja Danych
   ├─ Pobranie aktywnych nawyków z API
   └─ Wyświetlenie pierwszego nawyku (jeśli dostępny)

4. Kalibracja Czujników
   ├─ Próbkowanie żyroskopu 200 razy (1 sekunda)
   ├─ Obliczenie offsetu osi Z
   └─ Inicjalizacja śledzenia obrotu

5. Wejście do Głównej Pętli
```

### Operacja głownej pętli systemu

**Loop Frequency:** ~100 Hz (10ms cycle time)

```python
while True:
    # 1. Button Handling
    if button1.value() == 0 and button2.value() == 0:
        # Both pressed: Reload habits
        display.show_loading_screen()
        load_active_habits()
        display.display_active_habit(active_habits, active_habit_index)
        angle_z = 0

    elif button1.value() == 0:
        # Previous habit
        switch_previous_habit()
        display.display_active_habit(active_habits, active_habit_index)
        utime.sleep_ms(100)  # Debounce
        angle_z = 0

    elif button2.value() == 0:
        # Next habit
        switch_next_habit()
        display.display_active_habit(active_habits, active_habit_index)
        utime.sleep_ms(100)
        angle_z = 0

    # 2. Gyroscope Reading
    current_time = utime.ticks_ms()
    dt = utime.ticks_diff(current_time, last_time) / 1000.0
    last_time = current_time

    gyro_z_raw = sensor.gyro[2]
    gyro_z_rad = gyro_z_raw - gyro_offset_raw
    gyro_z_deg = gyro_z_rad * 57.296  # rad → deg

    # Dead-zone filter
    if abs(gyro_z_deg) < 0.5:
        gyro_z_deg = 0

    # Integration
    angle_z += gyro_z_deg * dt

    # 3. Completion Detection
    if abs(angle_z) >= 160:
        print("Rotation detected!")

        # Parallel audio playback
        _thread.start_new_thread(music.play_mario_main_theme, (buzzer,))

        # Visual animation (5 loops)
        play_sui_animation()

        # API call + state update
        complete_and_switch_habit()

        # Display update
        display.display_active_habit(active_habits, active_habit_index)

        # Reset
        angle_z = 0.0
        utime.sleep_ms(1000)
        last_time = utime.ticks_ms()

    utime.sleep_ms(10)  # 100 Hz loop
```

### Przepływ Nawigacji Nawyków

```
Wciśnięcie Przycisku 1:
    → active_habit_index -= 1
    → if (index < 0): index = len(habits) - 1
    → Aktualizacja wyświetlacza
    → Reset kąta obrotu

Wciśnięcie Przycisku 2:
    → active_habit_index += 1
    → if (index >= len(habits)): index = 0
    → Aktualizacja wyświetlacza
    → Reset kąta obrotu

Wciśnięcie Obu Przycisków:
    → Wyświetlenie komunikatu "Loading Habits..."
    → GET /api/v1/habits/active
    → Parsowanie odpowiedzi JSON
    → Aktualizacja listy active_habits
    → Wyświetlenie pierwszego nawyku
    → Reset kąta obrotu
```
---

## Credits & Licenses

### Third-Party Libraries

**MPU-9250 Driver**
- Author: Mika Tuupola (@tuupola)
- Repository: [micropython-mpu9250](https://github.com/tuupola/micropython-mpu9250)
- License: MIT
- Version: 0.4.0

**SH1106 OLED Driver**
- Authors: Radomir Dopieralski, Robert Hammelrath, Tim Weber
- License: MIT

**Captive Portal**
- Inspiration: [amora-labs/micropython-captive-portal](https://github.com/amora-labs/micropython-captive-portal)

### Podsumowanie Specyfikacji
| Component | Model | Interface | GPIO/Address | Current Draw | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MCU** | Raspberry Pi Pico WH | - | - | 80-100mA | Main controller |
| **Gyroscope** | MPU-9250 9DoF | I2C | SDA=0, SCL=1 | 3.5mA | Rotation detection |
| **Display** | SH1106 OLED 128x64 | SPI0 | CS=4, DC=5, RST=6 | 20mA | Visual output |
| **Button 1** | Membrane Switch | GPIO | Pin 17 (PULL_UP) | <1mA | Previous habit |
| **Button 2** | Membrane Switch | GPIO | Pin 16 (PULL_UP) | <1mA | Next habit |
| **Buzzer** | Grove Passive Buzzer | PWM | Pin 22 | 30mA (peak) | Audio feedback |
| **WiFi** | CYW43439 | Built-in | - | 80mA (active) | Network connectivity |
---
# Baza Danych 
> **Project:** Intelligent Habit Tracking Cube
> **Version:** 2.0
> **Last Updated:** December 7, 2025
> **Authors:** Paweł Klocek, Aleksy Dąda


## 1. Przegląd Techniczny

Warstwa danych systemu HabCube została zaprojektowana w oparciu o relacyjną bazę danych **PostgreSQL** oraz system cache'owania **Redis** dla zapewnienia wysokiej wydajności przy częstych zapytaniach z urządzeń IoT.

### Stos Technologiczny
* **Silnik Bazy Danych:** PostgreSQL 13+
* **Hosting:** Google Cloud SQL (Produkcja) / Docker (Lokalnie)
* **ORM (Object-Relational Mapping):** SQLAlchemy (Python)
* **Zarządzanie Migracjami:** Alembic (Flask-Migrate)
* **Cache:** Redis (Google Cloud Memorystore)

---

## Diagram ERD (Entity Relationship Diagram)

Poniższy diagram przedstawia relacje między głównymi encjami w systemie.
<img width="870" height="1519" alt="habcube" src="https://github.com/user-attachments/assets/507469fd-fc35-4608-a7fe-3554f73e3079" />

---

### Table: habits
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unikalny identyfikator nawyku.|
| `name` | VARCHAR(100) | Nazwa nawyku (np. "Picie wody"). |
| `description` | TEXT | Opcjonalny opis lub motywacja. |
| `deadline_time` | TIME | Ostateczna godzina wykonania nawyku (np. 21:00). |
| `frequency` | ENUM | Częstotliwość: `daily`, `weekly`, `monthly`, `hourly`, etc. |
| `active` | BOOLEAN | Czy nawyk jest aktywny (Domyślnie: `TRUE`) |
| `created_at` | TIMESTAMP | Znacznik czasu utworzenia (Default: `CURRENT_TIMESTAMP`). |
| `color` | VARCHAR(10) | Kolor przypisany do nawyku (dla UI/LED). |
| `icon` | ENUM | Identyfikator ikony dla interfejsu użytkownika. |

### Table: habit_tasks
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unikalny identyfikator zadania. |
| `habit_id` | INTEGER FK | Klucz obcy odnoszący się do `habits(id)`. |
| `date` | DATE | Data, na którą nawyk był zaplanowany/wykonany. |
| `completed` | BOOLEAN | Status ukończenia (Default: `FALSE`). |
| `completion_time` | TIMESTAMP | Dokładny znacznik czasu ukończenia (UTC). |

### Table: habit_statistics
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unikalny identyfikator rekordu statystyk. |
| `habit_id` | INTEGER FK | Klucz obcy odnoszący się do `habits(id)`. |
| `total_completions` | INTEGER | Całkowita liczba udanych wykonań. |
| `current_streak` | INTEGER | Aktualna liczba wykonań z rzędu (passa). |
| `best_streak` | INTEGER | Najwyższa passa kiedykolwiek osiągnięta dla tego nawyku. |
| `success_rate` | FLOAT | Procent udanych wykonań w stosunku do okazji. |
| `last_completed` | DATE | Data ostatniego udanego wykonania. |
| `updated_at` | TIMESTAMP | Czas ostatniego przeliczenia statystyk. |


# HabCube - Dokumentacja Backendu
> **Project:** Intelligent Habit Tracking Cube
> **Version:** 2.0
> **Last Updated:** December 7, 2025
> **Authors:** Paweł Klocek, Aleksy Dąda

## Struktura Projektu

Projekt **HabCube** zorganizowany jest w strukturze monorepo, dzieląc kod na część backendową (API), frontendową (aplikacja mobilna) oraz dokumentację. Poniżej przedstawiono szczegółowe drzewo plików dla backendu.

### Drzewo Katalogów

```text
HabCube/
├── .venv/                   # Lokalne wirtualne środowisko Python
├── backend/                 # Główny katalog API (Flask)
│   ├── app/                 # Kod źródłowy aplikacji
│   │   ├── docs/            # Definicje Swagger/OpenAPI (pliki YAML)
│   │   │   ├── complete_habit.yml
│   │   │   ├── create_habit.yml
│   │   │   ├── finished_habits.yml
│   │   │   ├── get_habit.yml
│   │   │   ├── get_habits.yml
│   │   │   └── statistics.yml
│   │   ├── models/          # Warstwa danych (ORM & DTO)
│   │   │   ├── __init__.py
│   │   │   ├── dto.py       # Obiekty transferu danych (walidacja wejścia)
│   │   │   ├── enums.py     # Typy wyliczeniowe (np. FrequencyType, HabitIcon)
│   │   │   └── habit.py     # Modele bazy danych (Habit, HabitTask, Statistics)
│   │   ├── routes/          # Kontrolery / Endpointy API
│   │   │   ├── __init__.py
│   │   │   └── habits.py    # Logika biznesowa zarządzania nawykami
│   │   ├── __init__.py      # Inicjalizacja aplikacji (Factory Pattern)
│   │   ├── cli.py           # Niestandardowe komendy CLI
│   │   ├── config.py        # Konfiguracja zmiennych środowiskowych i bazy
│   │   └── swagger.py       # Konfiguracja generatora dokumentacji API
│   ├── logs/                # Katalog na pliki logów serwera
│   ├── migrations/          # Skrypty migracyjne bazy danych (Alembic)
│   ├── tests/               # Testy jednostkowe i integracyjne
│   ├── .dockerignore        # Pliki ignorowane przez Docker context
│   ├── .pylintrc            # Konfiguracja lintera kodu (Pylint)
│   ├── Dockerfile           # Instrukcja budowania obrazu kontenera
│   ├── requirements.txt     # Lista zależności bibliotecznych Python
│   ├── setup.cfg            # Konfiguracja narzędzi (flake8, mypy)
│   └── wsgi.py              # Punkt wejścia dla serwera WSGI (Gunicorn)
├── docs/                    # Ogólna dokumentacja projektowa i schematy
└── frontend/                # Kod źródłowy aplikacji mobilnej (React Native)
```
## Logika Biznesowa i Endpointy
Moduł odpowiedzialny za zarządzanie nawykami, ich harmonogramem, śledzeniem postępów i statystykami.

## Spis Endpointów

| Metoda | Endpoint | Opis |
| :--- | :--- | :--- |
| `GET` | `/habits` | Pobiera listę wszystkich nawyków. |
| `GET` | `/habits/active` | Pobiera nawyki gotowe do wykonania (zgodnie z harmonogramem). |
| `GET` | `/finished-habits` | Pobiera zakończone nawyki wraz ze statusem sukcesu. |
| `GET` | `/statistics` | Pobiera ogólne statystyki użytkownika. |
| `GET` | `/habits/<id>` | Pobiera szczegóły pojedynczego nawyku. |
| `POST` | `/habits` | Tworzy nowy nawyk. |
| `POST` | `/habits/<id>/complete` | Oznacza nawyk jako wykonany. |

---

## Szczegółowy Opis

### 1. Pobierz wszystkie nawyki
Zwraca listę wszystkich nawyków zapisanych w bazie danych.

- **URL:** `/habits`
- **Metoda:** `GET`
- **Odpowiedź sukcesu (200 OK):**
  ```json
  {
    "habits": [
      {
        "id": 1,
        "name": "Bieganie",
        "description": "30 min rano",
        "active": true,
        ...
      }
    ]
  }
    ```
#### Kod Python
```python
@habits_bp.route("/habits", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "get_habits.yml"))
def get_habits():
    try:
        habits = Habit.query.all()
        return jsonify({"habits": [habit.to_dict() for habit in habits]}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch habits: {str(e)}"}), 500
```

### 2. Pobierz aktywne nawyki (Do wykonania)
Zwraca listę nawyków, które są aktywne i gotowe do wykonania w danym momencie. Dostępność zależy od częstotliwości nawyku i czasu ostatniego wykonania.

- **URL:** /habits/active

- **Metoda:** : GET

- **Logika dostępności**:
    - Nigdy niewykonane: Zawsze dostępne.
    - Co 30 min / 1h / 3h / 6h: Dostępne po upływie określonego czasu od ostatniego wykonania.
    - Dziennie (Daily): Dostępne, jeśli ostatnie wykonanie było przed dniem dzisiejszym.
    - Tygodniowo (Weekly): Dostępne po 7 dniach.
    - Miesięcznie (Monthly): Dostępne po 30 dniach.

#### Kod Python
```python
@habits_bp.route("/habits/active", methods=["GET"])
def get_active_habits():
    try:
        now = datetime.utcnow()
        today = date.today()

        # Get all active habits
        active_habits = Habit.query.filter_by(active=True).all()

        ready_habits = []
        for habit in active_habits:
            # Get last completion
            last_task = HabitTask.query.filter_by(
                habit_id=habit.id,
                completed=True
            ).order_by(HabitTask.completion_time.desc()).first()

            is_ready = False

            if not last_task:
                # Never completed, always ready
                is_ready = True
            else:
                last_completion = last_task.completion_time
                time_diff = now - last_completion

                # Check based on frequency
                if habit.frequency == FrequencyType.EVERY_30_MIN.value:
                    is_ready = time_diff.total_seconds() >= 30 * 60
                elif habit.frequency == FrequencyType.HOURLY.value:
                    is_ready = time_diff.total_seconds() >= 60 * 60
                elif habit.frequency == FrequencyType.EVERY_3_HOURS.value:
                    is_ready = time_diff.total_seconds() >= 3 * 60 * 60
                elif habit.frequency == FrequencyType.EVERY_6_HOURS.value:
                    is_ready = time_diff.total_seconds() >= 6 * 60 * 60
                elif habit.frequency == FrequencyType.DAILY.value:
                    # Ready if last completion was before today
                    is_ready = last_task.date < today
                elif habit.frequency == FrequencyType.WEEKLY.value:
                    # Ready if last completion was 7+ days ago
                    is_ready = (today - last_task.date).days >= 7
                elif habit.frequency == FrequencyType.MONTHLY.value:
                    # Ready if last completion was 30+ days ago
                    is_ready = (today - last_task.date).days >= 30

            if is_ready:
                ready_habits.append(habit.to_dict())

        return jsonify({"habits": ready_habits}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch active habits: {str(e)}"}), 500
```
### 3. Pobierz zakończone nawyki
Zwraca listę nawyków oznaczonych jako nieaktywne (`active=False`). Oblicza, czy nawyk zakończył się sukcesem.

- **URL:** /finished-habits

- **Metoda:** GET

- **Kryterium sukcesu:** Pole success_status jest true, jeśli najlepsza seria (best_streak) wynosiła 21 dni lub więcej.

- **Przykładowa odpowiedź:**
```json
{
  "habits": [
    {
      "id": 10,
      "name": "Joga",
      "best_streak": 25,
      "success_status": true,
      "finish_date": "Tue, 10 Oct 2023 00:00:00 GMT"
    }
  ]
}
```
#### Kod Python
```python
@habits_bp.route("/finished-habits", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "finished_habits.yml"))
def get_finished_habits():
    try:
        habits = Habit.query.filter_by(active=False).all()
        finished_habits = []
        for habit in habits:
            finished_habit = {}
            habit_dict = habit.to_dict()
            finished_habit["id"] = habit_dict["id"]
            finished_habit["name"] = habit_dict["name"]
            finished_habit["description"] = habit_dict["description"]
            finished_habit["icon"] = habit_dict["icon"]

            if habit.statistics:
                stats_data = habit.statistics.to_dict()
                best_streak = stats_data.get("best_streak", 0)
                finished_habit["best_streak"] = best_streak
                if int(best_streak) >= 21:
                    finished_habit["success_status"] = True
                else:
                    finished_habit["success_status"] = False
                finished_habit["finish_date"] = stats_data["last_completed"]
            else:
                finished_habit["best_streak"] = 0
                finished_habit["success_status"] = False
                finished_habit["finish_date"] = ''

            finished_habits.append(finished_habit)

        return jsonify({"habits": finished_habits}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Failed to fetch habits: {str(e)}"}), 500
```

### 4. Statystyki ogólne
Zwraca zagregowane dane statystyczne dla wszystkich nawyków.

- **URL:** `/statistics`

- **Metoda:** `GET`

- **Zwracane dane:**
    - `total_habits`: Łączna liczba nawyków.
    - `active_habits_count`: Liczba trwających nawyków.
    - `completed_habits_count`: Liczba zakończonych nawyków.
    - `longest_streak`: Najdłuższa seria (streak) w historii użytkownika.
    - `average_completion_rate`: Średni wskaźnik sukcesu (zaokrąglony do 2 miejsc po przecinku).
#### Kod Python:
```python
@habits_bp.route("/statistics", methods=["GET"])
def get_habits_statistics():
    try:
        total_habits = db.session.query(func.count(Habit.id)).scalar()

        active_habits_count = db.session.query(Habit).filter_by(active=True).count()
        inactive_habits_count = total_habits - active_habits_count

        longest_streak = db.session.query(func.max(HabitStatistics.best_streak)).scalar()

        if longest_streak is None:
            longest_streak = 0

        average_completion_rate = db.session.query(
            func.avg(HabitStatistics.success_rate)
        ).scalar()

        if average_completion_rate is None:
            average_completion_rate = 0.0
        else:
            average_completion_rate = round(average_completion_rate, 2)

        response_data = {
            "total_habits": total_habits,
            "active_habits_count": active_habits_count,
            "completed_habits_count": inactive_habits_count,
            "longest_streak": longest_streak,
            "average_completion_rate": average_completion_rate
        }

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error fetching global statistics: {e}")
        return jsonify({"error": f"Failed to fetch statistics: {str(e)}"}), 500
```

### 5. Pobierz szczegóły nawyku
Pobiera pełne dane pojedynczego nawyku, w tym jego indywidualne statystyki.

- **URL:** `/habits/<int:habit_id>`

- **Metoda:** `GET`

- **Błędy:** `404` jeśli nawyk nie istnieje.

#### Kod Python
```python
@habits_bp.route("/habits/<int:habit_id>", methods=["GET"])
@swag_from(os.path.join(DOCS_DIR, "get_habit.yml"))
def get_habit(habit_id):
    try:
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        response_data = habit.to_dict()

        # Include statistics if available
        if habit.statistics:
            response_data["statistics"] = habit.statistics.to_dict()

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch habit: {str(e)}"}), 500

```
### 6. Utwórz nowy nawyk
Tworzy nowy nawyk i inicjalizuje dla niego statystyki.

- **URL:** `/habits`

- **Metoda:** `POST`

- **Body** (JSON):

    - `name` (string, wymagane)
    - `description` (string, opcjonalne)
    - `deadline_time` (string "HH:MM", opcjonalne)
    - `frequency` (enum, domyślnie "DAILY")
    - `icon` (enum, domyślnie "STAR")
    - `type` (enum, domyślnie "WATER")

#### Walidacja:
Sprawdza poprawność formatu godziny.
Weryfikuje czy `frequency`, `icon` i `type` są zgodne z dozwolonymi wartościami (Enum).

#### Kod Python
```python
@habits_bp.route("/habits", methods=["POST"])
@swag_from(os.path.join(DOCS_DIR, "create_habit.yml"))
def create_habit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Parse deadline_time if provided
        deadline_time = None
        if "deadline_time" in data and data["deadline_time"]:
            try:
                deadline_time = datetime.strptime(data["deadline_time"], "%H:%M").time()
            except ValueError:
                return (
                    jsonify({"error": "Invalid deadline_time format. Use HH:MM"}),
                    400,
                )

        # Validate frequency
        frequency = data.get("frequency", FrequencyType.DAILY.value)
        if not FrequencyType.is_valid(frequency):
            return (
                jsonify(
                    {
                        "error": f"Invalid frequency. Must be one of: {', '.join(FrequencyType.choices())}"
                    }
                ),
                400,
            )

        # Validate icon
        icon = data.get("icon", HabitIcon.STAR.value)
        if icon and not HabitIcon.is_valid(icon):
            return (
                jsonify({"error": "Invalid icon"}),
                400,
            )

        # Validate type
        from app.models.enums import HabitType
        habit_type = data.get("type", HabitType.WATER.value)
        if habit_type and not HabitType.is_valid(habit_type):
            return (
                jsonify(
                    {
                        "error": f"Invalid type. Must be one of: {', '.join(HabitType.choices())}"
                    }
                ),
                400,
            )

        # Create DTO and validate
        dto = CreateHabitDTO(
            name=data.get("name"),
            description=data.get("description"),
            deadline_time=deadline_time,
            frequency=frequency,
            icon=icon,
        )

        is_valid, error_message = dto.validate()
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Create new habit
        habit = Habit(
            name=dto.name,
            description=dto.description,
            deadline_time=dto.deadline_time,
            frequency=dto.frequency,
            icon=dto.icon,
            type=habit_type,
            active=True,
        )

        db.session.add(habit)
        db.session.flush()

        # Create initial statistics record
        statistics = HabitStatistics(habit_id=habit.id)
        db.session.add(statistics)

        db.session.commit()

        return (
            jsonify(
                {"message": "Habit created successfully", "habit": habit.to_dict()}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create habit: {str(e)}"}), 500

```

### 7. Wykonaj nawyk
Oznacza nawyk jako wykonany ("odkliknięty") w dniu dzisiejszym.

- **URL:** `/habits/<int:habit_id>/complete`

- **Metoda:** `POST`

- **Logika biznesowa:**

    - Blokuje podwójne wykonanie tego samego dnia (chyba że częstotliwość na to pozwala - uwaga: w kodzie jest twarda blokada `Habit already completed today` dla wpisów z tą samą datą).

    - **Aktualizacja serii (Streak):**

        - Pierwsze wykonanie: Streak = 1.

        - Wykonanie dzień po dniu: Streak + 1.

        - Przerwa w wykonaniu (>1 dzień): Reset Streak do 1.

    - Aktualizuje `best_streak` jeśli obecna seria jest rekordowa.

#### Kod Python
```python
@habits_bp.route("/habits/<int:habit_id>/complete", methods=["POST"])
@swag_from(os.path.join(DOCS_DIR, "complete_habit.yml"))
def complete_habit(habit_id):
    try:
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        completion_date = date.today()

        # Check if already completed today
        existing_task = HabitTask.query.filter_by(
            habit_id=habit_id, date=completion_date
        ).first()

        if existing_task and existing_task.completed:
            return jsonify({"error": "Habit already completed today"}), 400

        # Create completion task
        task = HabitTask(
            habit_id=habit_id,
            date=completion_date,
            completed=True,
            completion_time=datetime.utcnow(),
        )
        db.session.add(task)

        # Update statistics
        statistics = habit.statistics
        if not statistics:
            statistics = HabitStatistics(habit_id=habit_id)
            db.session.add(statistics)

        statistics.total_completions += 1
        statistics.last_completed = completion_date
        statistics.updated_at = datetime.utcnow()

        # Update streak
        if statistics.total_completions == 1:
            statistics.current_streak = 1
        else:
            # Check previous completion
            previous_task = (
                HabitTask.query.filter_by(habit_id=habit_id, completed=True)
                .filter(HabitTask.date < completion_date)
                .order_by(HabitTask.date.desc())
                .first()
            )
            if previous_task:
                days_diff = (completion_date - previous_task.date).days
                if days_diff == 1:
                    statistics.current_streak += 1
                else:
                    statistics.current_streak = 1
            else:
                statistics.current_streak = 1

        # Update best streak
        if statistics.current_streak > statistics.best_streak:
            statistics.best_streak = statistics.current_streak

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Habit completed successfully",
                    "task": task.to_dict(),
                    "statistics": statistics.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to complete habit: {str(e)}"}), 500
```

### 6. Dokumentacja API (Swagger)
Aplikacja wykorzystuje bibliotekę Flasgger. Definicje endpointów są oddzielone od kodu i znajdują się w katalogu `app/docs/*.yml`.

Po uruchomieniu serwera, pełna interaktywna dokumentacja dostępna jest pod adresem:

`http://localhost:5000/api/docs/`

#### Przykładowa konfiguracja pliku `yml`:
```yml
tags:
  - Habits
summary: Get a single habit by ID
description: Returns habit details including statistics if available
parameters:
  - name: habit_id
    in: path
    type: integer
    required: true
    description: ID of the habit
responses:
  200:
    description: Habit details with statistics
    examples:
      success:
        id: 1
        name: "Drink water"
        description: "Drink 8 glasses of water daily"
        deadline_time: "21:00:00"
        frequency: "daily"
        active: true
        created_at: "2025-10-15T10:30:00"
        statistics:
          id: 1
          habit_id: 1
          total_completions: 15
          current_streak: 5
          best_streak: 10
          success_rate: 85.5
          last_completed: "2025-10-14"
          updated_at: "2025-10-14T22:15:00"
  404:
    description: Habit not found
    examples:
      error:
        error: "Habit not found"
  500:
    description: Server error

```

## Wdrożenie (Google Cloud Run)

Poniższy plik konfiguracyjny (`cloudbuild.yaml`) definiuje kompletny pipeline wdrożeniowy dla backendu aplikacji. Proces ten realizuje podejście **Infrastructure as Code** i jest uruchamiany automatycznie przez Google Cloud Build.

## Proces

1.  **Build (Budowanie Obrazu):**
    System tworzy obraz Docker na podstawie kodu z katalogu `./backend`, oznaczając go odpowiednim tagiem.

2.  **Push (Wypchnięcie do Rejestru):**
    Gotowy obraz jest przesyłany do **Google Artifact Registry**, skąd będzie dostępny dla usług chmurowych.

3.  **Deploy (Wstępne Wdrożenie na Cloud Run):**
    Nowa wersja aplikacji jest instalowana na serwerze, ale z flagą `--no-traffic` (nie jest jeszcze publicznie dostępna).
    * **Integracja z bazą:** Usługa jest łączona z instancją Cloud SQL (`--add-cloudsql-instances`).
    * **Bezpieczeństwo:** Hasła i klucze (DB_PASSWORD, SECRET_KEY) są bezpiecznie wstrzykiwane z **Secret Manager**.

4.  **Database Migration (Automatyczna Migracja Bazy):**
    Kluczowy moment procesu. System tworzy i uruchamia jednorazowe zadanie (**Cloud Run Job**) o nazwie `backend-migrate`.
    * Zadanie wykonuje komendę `flask db upgrade`.
    * Dzięki temu struktura bazy danych jest aktualizowana do nowej wersji kodu *zanim* użytkownicy zaczną z niej korzystać.

5.  **Traffic Switch (Przełączenie Ruchu):**
    Dopiero po pomyślnej migracji bazy, 100% ruchu użytkowników jest przekierowywane na nową, przetestowaną wersję aplikacji.

---

## Pełna Konfiguracja (`cloudbuild.yaml`)

```yaml
steps:
  # 1. Build Docker image
  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "${_IMAGE_TAG}", "./backend"]

  # 2. Push Docker image to Artifact Registry
  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "${_IMAGE_TAG}"]

  # 3. Deploy to Cloud Run (bez ruchu publicznego)
  - name: "gcr.io/[google.com/cloudsdktool/cloud-sdk](https://google.com/cloudsdktool/cloud-sdk)"
    entrypoint: "bash"
    args:
      - "-c"
      - |
        gcloud run deploy backend \
          --image "${_IMAGE_TAG}" \
          --region "${_REGION}" \
          --service-account "${_SERVICE_ACCOUNT}" \
          --memory=4Gi \
          --cpu=2 \
          --timeout=300 \
          --add-cloudsql-instances "${_CLOUD_SQL_CONNECTION_NAME}" \
          --set-env-vars "FLASK_ENV=production,DB_HOST=/cloudsql/${_CLOUD_SQL_CONNECTION_NAME},DB_PORT=5432,DB_USER=${_DB_USER},DB_NAME=${_DB_NAME}" \
          --update-secrets "DB_PASSWORD=db-password:latest,SECRET_KEY=flask-key:latest,JWT_SECRET_KEY=jwt-key:latest" \
          --no-traffic

  # 4. Database Migration (Flask DB Upgrade)
  - name: "gcr.io/[google.com/cloudsdktool/cloud-sdk](https://google.com/cloudsdktool/cloud-sdk)"
    entrypoint: "bash"
    args:
      - "-c"
      - |
        set -e
        gcloud run jobs delete backend-migrate --region "${_REGION}" --quiet || true
        gcloud run jobs create backend-migrate \
          --image "${_IMAGE_TAG}" \
          --region "${_REGION}" \
          --service-account "${_SERVICE_ACCOUNT}" \
          --set-cloudsql-instances "${_CLOUD_SQL_CONNECTION_NAME}" \
          --set-env-vars "FLASK_ENV=production,FLASK_APP=wsgi:app,DB_HOST=/cloudsql/${_CLOUD_SQL_CONNECTION_NAME},DB_PORT=5432,DB_USER=${_DB_USER},DB_NAME=${_DB_NAME}" \
          --update-secrets "DB_PASSWORD=db-password:latest,SECRET_KEY=flask-key:latest,JWT_SECRET_KEY=jwt-key:latest" \
          --command "flask" --args "db","upgrade" \
          --task-timeout 10m
        gcloud run jobs execute backend-migrate --region "${_REGION}" --wait
        
  # 5. Switch traffic to new revision (Upublicznienie)
  - name: "gcr.io/[google.com/cloudsdktool/cloud-sdk](https://google.com/cloudsdktool/cloud-sdk)"
    entrypoint: "bash"
    args:
      - "-c"
      - |
        gcloud run services update-traffic backend \
          --region "${_REGION}" \
          --to-latest

substitutions:
  _REGION: "europe-west1"
  _IMAGE_TAG: "europe-west1-docker.pkg.dev/project-5291a779-124c-4d04-8a5/cloud-run-source-deploy/habcube-backend:latest"
  _SERVICE_ACCOUNT: "1089871134307-compute@developer.gserviceaccount.com"
  _CLOUD_SQL_CONNECTION_NAME: "project-5291a779-124c-4d04-8a5:europe-west1:habcube"
  _DB_USER: "postgres"
  _DB_NAME: "postgres"

options:
  logging: CLOUD_LOGGING_ONLY
```
## Uruchomienie Deweloperskie

### Konfigutacja środowiska


**Ważne:**
Najpierw uruchom skrypt instalacyjny, który automatycznie doda `export CURRENT_UID` do `~/.bashrc` (pozwoli to uniknąć późniejszych problemów z uprawnieniami do plików i folderów):

```bash
./setup-env.sh
source ~/.bashrc
```

### Pierwsze uruchomienie
```bash
# 1. Zbudowanie obrazu docker
docker-compose up -d --build

# 2. Sprawdzenie statusu kontenera
docker-compose ps

# 3. Logi
docker-compose logs -f backend

# 4. Sprawdzenie statusu `health` aplikacji
curl http://localhost:5000/health
```
### Uruchomienie aplikacji
```bash
# Start
docker-compose up -d

# Stop
docker-compose down
```
### Makefile (Rekomendowane)
Plik Makefile automatycznie eksportuje CURRENT_UID:
```bash
make init # Pierwsze uruchomienie / Inicjalizacja
make up # Uruchom usługi
make down # Zatrzymaj usługi
make logs # Wyświetl logi
make test # Uruchom testy
make help # Wyświetl wszystkie polecenia
```
### Dostęp do serwisu
Backend: http://localhost:5000

Adminer (DB UI): http://localhost:8080

PostgreSQL: localhost:5432

Redis: localhost:6379
### Podstawowe komendy
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

# Dokumentacja Aplikacji Mobilnej HabCube
> **Project:** Intelligent Habit Tracking Cube
> **Version:** 2.0
> **Last Updated:** December 7, 2025
> **Author:** Szymon Domagała

## 1. Przegląd
Aplikacja mobilna HabCube to wieloplatformowe rozwiązanie zbudowane w oparciu o **React Native (Expo)** oraz **TypeScript**. Pełni ona rolę głównego interfejsu użytkownika do konfiguracji nawyków, śledzenia postępów oraz wizualizacji statystyk pochodzących z urządzenia IoT Cube.

## 2. Stack Technologiczny

* **Framework:** React Native (Expo) – umożliwia szybki rozwój na Androida, iOS oraz Web.
* **Język:** TypeScript (5.9.2) – zapewnia statyczne typowanie kodu.
* **Narzędzia Buildowania:** Expo CLI / EAS (Expo Application Services).
* **Nawigacja:** React Navigation (Native Stack).
* **Klient HTTP:** Axios.
* **Zarządzanie Stanem:** React Hooks (`useState`, `useEffect`, Custom Hooks).
* **Kluczowe Biblioteki:**
    * `@react-native-picker/picker` – natywne listy wyboru.
    * `react-native-toast-message` – obsługa powiadomień i alertów.
    * `react-native-vector-icons` – zestaw ikon (Ionicons).
    * `@react-native-community/datetimepicker` – wybór daty i czasu.

## 3. Struktura Projektu

Projekt podąża za strukturą opartą na funkcjonalnościach i komponentach (`Feature-based`):

```text
src/
├── api/                  # Warstwa komunikacji z API
│   ├── client.ts         # Konfiguracja instancji Axios
│   ├── endpoints.ts      # Stałe z adresami URL
│   └── habits.api.ts     # Funkcje serwisowe (GET, POST)
├── assets/
│   ├── data/             # Dane statyczne (np. lista dostępnych ikon)
│   └── ...               # Obrazy i zasoby graficzne
├── components/           # Komponenty UI i Ekrany
│   ├── AddHabit/         # Ekran tworzenia nawyku (logika formularza)
│   ├── AppLogo/          # Reużywalny komponent logo
│   ├── BottomNavbar/     # Dolny pasek nawigacyjny
│   ├── FinishedHabits/   # Ekran historii i archiwum
│   ├── HabitsStats/      # Ekran statystyk globalnych
│   ├── MainPage/         # Dashboard (Aktywne nawyki)
│   └── WelcomeScreen.tsx # Ekran powitalny
├── constants/
│   └── config.ts         # Konfiguracja środowiskowa (URL backendu)
├── hooks/                # Logika biznesowa (Custom Hooks)
│   ├── useCreateHabit.ts
│   ├── useHabits.ts
│   └── ...
└── types/
    └── habit.types.ts    # Interfejsy i typy TypeScript (DTO)
```

### 4. Architektura i Przepływ Danych
Aplikacja wykorzystuje wzorzec Service-Hook-Component w celu separacji odpowiedzialności:

- **Warstwa API (src/api):** Obsługuje bezpośrednią komunikację HTTP przez Axios. Definiuje endpointy i surowe funkcje pobierania danych.

- **Warstwa Hooków (src/hooks):** Hermetyzuje logikę biznesową. Wywołuje warstwę API i wystawia proste zmienne (data, loading, error) dla UI.

- **Warstwa UI (src/components):** Komponenty prezentacyjne, które konsumują Hooki do wyświetlania danych.

**Konfiguracja** (`src/constants/config.ts`)
Plik konfiguracyjny pozwala na łatwe dostosowanie adresu backendu. Aplikacja może wykrywać środowisko, ale zaleca się ręczne ustawienie adresu IP w przypadku testów na fizycznym urządzeniu (jeśli backend nie jest w chmurze).

### 5. Szczegółowy Opis Komponentów

#### Ekran Dodawania Nowego Nawyku (`src/components/AddHabit/index.tsx`)
Jest to kluczowy moduł odpowiedzialny za logikę tworzenia nowych instancji nawyków.

**Funkcjonalności formularza:** Użytkownik wprowadza następujące dane:
- Nazwa (np. `"Picie wody"`)
- Opis (szczegóły celu)
- Ikona (wybór z wizualnej listy)
- Typ (np. `"Zdrowie"`, `"Sport"`)
- Częstotliwość (np. `"Codziennie"`, `"Tygodniowo"` - obsługa przez `Picker`)
- Data startu (obsługa przez `DateTimePicker`)

Logika Procesu (`handleSubmit`): Funkcja handleSubmit jest sercem tego ekranu i realizuje następujący przepływ:
- Zbieranie Danych: Agreguje dane z pól formularza do obiektu habitData.
- Walidacja: Sprawdza kompletność wymaganych pól.
- Komunikacja: Wywołuje hook addHabit (POST request).

Feedback:
- **Sukces:** Wyświetla powiadomienie Toast ("Habit created") i przekierowuje na MainPage.
- **Błąd:** Wyświetla powiadomienie Toast z treścią błędu, pozwalając na ponowną próbę.

Ekran Dodawania Nawyku (`src/components/AddHabit/index.tsx`)
Interaktywny formularz umożliwiający użytkownikowi zdefiniowanie nowego nawyku. Komponent obsługuje wprowadzanie danych tekstowych, wybór parametrów z list oraz komunikację z API.

#### Kluczowe funkcjonalności w kodzie:

1. Zarządzanie Stanem Formularza: Komponent wykorzystuje useState do przechowywania wartości wprowadzanych przez użytkownika (nazwa, opis, typ, częstotliwość, data startu).

2. Obsługa Złożonych Kontrolek UI:
    - **Wybór Ikony**: Renderowanie siatki ikon (AVAILABLE_ICONS) z wizualnym podświetleniem wybranego elementu.
    - **Pickery**: Wykorzystanie @react-native-picker/picker do wyboru typu aktywności i częstotliwości.
    - **Data:** Integracja z natywnym DateTimePicker.

3. Logika Wysyłania (`handleSubmit`): Funkcja buduje obiekt DTO, wysyła go do backendu, a następnie obsługuje informację zwrotną (Toast) i nawigację.
```tsx
// Przygotowanie danych i wysyłka do API
const handleSubmit = async () => {
  // Konstrukcja obiektu zgodnego z DTO backendu
  const habitData: ICreateHabitDTO = {
    name: habitName,
    description: habitDescription,
    icon: habitIcon,          // Ikona wybrana z siatki
    frequency: habitFrequency,// np. 'daily', 'weekly'
    created_at: habitStartDate.toISOString(),
    type: habitIconType,
  };

  try {
    // Wywołanie custom hooka obsługującego żądanie POST
    const response = await addHabit(habitData);

    if (response) {
      // Pozytywny feedback i przekierowanie po opóźnieniu
      Toast.show({
        type: 'success',
        text1: 'Habit added successfully!',
        position: 'bottom',
        visibilityTime: 2000,
      });
      setTimeout(() => {
        navigation.navigate("MainPage");
      }, 2500);
    }
  } catch (err) {
    // Obsługa błędów
    Toast.show({
      type: 'error',
      text1: 'Failed to add habit.',
      position: 'bottom',
    });
  }
};  
```
#### Dashboard Główny (`src/components/MainPage/index.tsx`)
Centrum dowodzenia użytkownika.
* **Funkcje:** Wyświetla listę aktywnych nawyków pobranych z API.
* **Interakcja:** Kliknięcie w nawyk oznacza go jako wykonany (wysyła żądanie `COMPLETE` do backendu).
* **Wizualizacja:** Prezentuje pasek postępu (Progress Bar) dążący do celu 21 dni oraz licznik obecnej serii (Streak).

**Dashboard Główny** (src/components/MainPage/index.tsx)
Centrum dowodzenia użytkownika. Odpowiada za wyświetlanie listy aktywnych nawyków, ich statusu oraz postępów.

### Kluczowe funkcjonalności w kodzie:

1. Automatyczne odświeżanie danych: Wykorzystanie useFocusEffect zapewnia, że lista nawyków jest zawsze aktualna po powrocie z innych ekranów (np. po dodaniu nowego nawyku).
```tsx
const { fetchHabits, habits } = useHabits();

useFocusEffect(
  React.useCallback(() => {
    fetchHabits(); // Pobranie danych przy każdym wejściu na ekran
  }, [])
);
```

2. **Renderowanie Karty Nawyku i Paska Postępu:** Dynamiczne obliczanie szerokości paska postępu (na podstawie celu 21 dni) oraz wyświetlanie aktualnej serii (Streak).
```tsx
const renderHabitItem = (habit: IHabit) => (
  <View key={habit.id} style={styles.habitCard}>
    {/* ... Nagłówek i Ikona ... */}

    <View style={styles.habitInfo}>
      <Text style={styles.habitName}>{habit.name}</Text>
      <Text style={styles.habitFrequency}>
        {/* Wyświetlanie częstotliwości i serii */}
        {habit.frequency} • Streak: {habit.statistics?.current_streak} days
      </Text>
    </View>

    {/* Przycisk wykonania (zmiana stylu jeśli zrobione dzisiaj) */}
    <TouchableOpacity
      style={[
        styles.checkButton,
        // Sprawdzenie czy data ostatniego wykonania to "dzisiaj"
        habit.statistics?.last_completed === new Date().toISOString().split('T')[0] 
          && styles.checkButtonCompleted,
      ]}
      onPress={() => handleCompleteHabit(habit.id)}
    >
       {/* ... Ikona checkmark ... */}
    </TouchableOpacity>

    {/* Pasek Postępu (Progress Bar) */}
    <View style={styles.progressContainer}>
      <View style={styles.progressBarBackground}>
        <View
          style={[
            styles.progressBarFill,
            // Obliczanie % ukończenia celu 21 dni
            { width: `${(habit.statistics?.total_completions / 21) * 100}%` },
          ]}
        />
      </View>
      <Text style={styles.progressText}>
        {habit.statistics?.total_completions} / 21 days
      </Text>
    </View>
  </View>
);
```

#### Statystyki (`src/components/HabitsStats/index.tsx`)
Ekran analityczny.
* **Dane:** Agreguje dane globalne: łączna liczba nawyków, najdłuższa seria, średnia skuteczność.
* **Odświeżanie:** Wykorzystuje `useFocusEffect` do odświeżania danych przy każdym wejściu na ekran.

Ekran analityczny, który agreguje i wizualizuje globalne postępy użytkownika w aplikacji.

#### Kluczowe funkcjonalności w kodzie:

1. Pobieranie Danych Agregowanych: Komponent korzysta z dedykowanego hooka `useStatsHabits`, który komunikuje się z endpointem `/statistics` backendu. Zwraca on gotowy obiekt ze statystykami, co oddziela warstwę prezentacji od logiki pobierania danych.
```tsx
// Pobranie danych statystycznych z API
const { stats, loading, error } = useStatsHabits();
```
2. Prezentacja Kluczowych Wskaźników (KPI): Dane są wyświetlane w przejrzystych kartach, prezentując cztery główne metryki: liczbę aktywnych nawyków, średnią skuteczność, najdłuższą serię oraz liczbę zakończonych nawyków.
```tsx
// Przykład renderowania kart statystyk
<View style={styles.statCard}>
  <Text style={styles.statLabel}>Active habits</Text>
  <Text style={styles.statValue}>{stats?.active_habits_count}</Text>
</View>

<View style={styles.statCard}>
  <Text style={styles.statLabel}>Average completion rate</Text>
  {/* Wyświetlanie sformatowanej wartości procentowej */}
  <Text style={styles.statValue}>{stats?.average_completion_rate}%</Text>
</View>

<View style={styles.statCard}>
  <Text style={styles.statLabel}>Longest streak (days)</Text>
  <Text style={styles.statValue}>{stats?.longest_streak}</Text>
</View>
```

#### Archiwum (`src/components/FinishedHabits/index.tsx`)
Historia nawyków.
* **Widok:** Lista kafelków z nawykami, które zostały zakończone lub porzucone.
* **Status Sukcesu:** Wizualne rozróżnienie (kolor/ikona) dla nawyków, które osiągnęły cel 21 dni.

Archiwum (`src/components/FinishedHabits/index.tsx`)
Ekran historii prezentujący listę nawyków, które zostały zakończone lub porzucone. Jego głównym celem jest wizualizacja ostatecznego rezultatu – czy użytkownikowi udało się zbudować nawyk (osiągnąć cel 21 dni), czy też nie.

#### Kluczowe funkcjonalności w kodzie:

1. **Pobieranie i Formatowanie Danych**: Dane są pobierane przez hook useFinishedHabits. Komponent zawiera również funkcję pomocniczą formatDate do czytelnej prezentacji daty zakończenia.

2. **Warunkowa Wizualizacja Sukcesu (`Status Logic`)**: Komponent dynamicznie renderuje ikonę statusu w zależności od flagi success_status otrzymanej z backendu.
    - Sukces: Zielona ikona (checkmark-circle).
    - Porażka: Czerwona ikona (close-circle).
```tsx
// Warunkowe renderowanie ikony statusu
<View style={styles.habitNameRow}>
  <Text style={styles.habitName}>{habit.name}</Text>
  <Icon
    // Wybór ikony: sukces vs porażka
    name={habit.success_status ? "checkmark-circle" : "close-circle"}
    size={30}
    // Dobór koloru: zielony vs czerwony
    color={habit.success_status ? "#4CAF50" : "#F44336"}
  />
</View>
```
### 6. Przewodnik Instalacji i Uruchomienia
#### Wymagania Wstępne
- Node.js (wersja LTS)
- npm lub yarn
- Zainstalowane Expo CLI
- Backend (Flask) uruchomiony na porcie `5000` (lub w chmurze)

#### Instalacja
1. Przejdź do katalogu projektu:
```bash
cd habcube-mobile
```
2. Zainstaluj zależności:

```bash
npm install
```

#### Uruchamianie (Development)
Uruchom serwer deweloperski Metro Bundler:

```bash
npm start
```

- Naciśnij `a`, aby uruchomić na emulatorze Androida.
- Naciśnij `i`, aby uruchomić na symulatorze iOS (tylko macOS).
- Zeskanuj kod QR aplikacją Expo Go, aby uruchomić na fizycznym telefonie.

#### Budowanie Aplikacji (Produkcja)
Projekt wykorzystuje **EAS (Expo Application Services)** do budowania paczek instalacyjnych.

Aby zbudować plik `.apk` dla Androida:
```bash
eas build -p android --profile preview
```

## 7. Rozwiązywanie Problemów (Troubleshooting)

### Problem: `Network Request Failed` na Androidzie
Emulator Androida nie widzi `localhost`.
* **Rozwiązanie:** W pliku `config.ts` upewnij się, że adres backendu to `http://10.0.2.2:5000` zamiast `localhost`.

### Problem: Zmiany w kodzie nie są widoczne
* **Rozwiązanie:** Wyczyść cache Metro Bundlera:
    ```bash
    npm start -- --reset-cache
    ```

### Problem: Błąd budowania EAS
* **Rozwiązanie:** Upewnij się, że jesteś zalogowany do konta Expo:
    ```bash
    eas login
    ```

# HabCube Projekt 3D kostki
 > **Project:** Intelligent Habit Tracking Cube
> **Version:** 1.0
> **Last Updated:** December 7, 2025
> **Author:** Piotr Ziobrowski

# Dokumentacja Projektu 3D i Obudowy - HabCube

## 1. Przegląd
Fizyczna obudowa HabCube została zaprojektowana tak, aby być kompaktową, ergonomiczną i wytrzymałą. Mieści w sobie centralny mikrokontroler, cztery ekrany OLED, czujniki (żyroskop) oraz układ zasilania. Projekt koncentruje się na modułowości i łatwości montażu przy użyciu standardowej technologii druku 3D (FDM).

## 2. Ewolucja Projektu (Proces Projektowy)

Projekt obudowy przeszedł trzy kluczowe fazy rozwoju, ewoluując od prostej wizualizacji do precyzyjnego modelu inżynierskiego.

### Faza 1: Wstępne Demo (Tinkercad)
Pierwszy etap polegał na szybkim prototypowaniu koncepcyjnym.
* **Cel:** Wizualizacja rozmieszczenia komponentów i weryfikacja ogólnych gabarytów kostki.
* **Realizacja:** Wykorzystano proste bryły geometryczne w środowisku Tinkercad, aby sprawdzić, czy cztery ekrany i płytka Raspberry Pi Pico zmieszczą się w założonej przestrzeni 60x60mm.
* **Wnioski:** Potwierdzono wykonalność projektu, ale zidentyfikowano potrzebę użycia bardziej zaawansowanego narzędzia do precyzyjnego spasowania elementów.

### Faza 2: Pierwszy Projekt (Autodesk Fusion 360)
Przeniesienie koncepcji do środowiska CAD.
* **Cel:** Stworzenie parametrycznego modelu z uwzględnieniem grubości ścianek i mocowań.
* **Realizacja:** Zaprojektowano pierwszą wersję bryły `new_cube.stl`.
* **Problemy:** Podczas próbnego montażu zauważono, że otwory na ekrany OLED były zbyt ciasne (brak tolerancji druku), a brak dedykowanych wycięć na przyciski utrudniał obsługę urządzenia.

### Faza 3: Wersja Finalna (Autodesk Fusion 360)
Ostateczna, dopracowana wersja obudowy, gotowa do produkcji.
* **Kluczowe zmiany i poprawki:**
    * **Poprawione wycięcia na ekrany OLED:** Zwiększono tolerancję otworów oraz dodano wewnętrzne podpory, co pozwala na idealne osadzenie wyświetlaczy 0.96" bez konieczności szlifowania wydruku.
    * **Integracja przycisków:** Dodano precyzyjne wycięcia na guziki (Tact Switches), umożliwiające łatwy dostęp do funkcji sterowania bez konieczności otwierania obudowy.
    * **Zarządzanie kablami:** Zoptymalizowano wewnętrzne kanały, aby przewody nie kolidowały z mechanizmem zamykania wieczka.

## 3. Narzędzia i Pliki Źródłowe
* **Oprogramowanie CAD:** Tinkercad (prototyp), Autodesk Fusion 360 (finalny projekt).
* **Pliki źródłowe:** `HabCube.f3z` (Zawiera pełne złożenie, historię parametryczną i wiązania komponentów).
* **Format eksportu:** `.stl` (Stereolitografia) do slicera i druku.

## 4. Budowa Komponentów

Obudowa składa się z dwóch głównych części zaprojektowanych do ścisłego dopasowania:

### 4.1 Korpus Główny (`new_cube.stl`)
Główny element konstrukcyjny urządzenia.
* **Funkcja:** Mieści elektronikę (Mikrokontroler, Multiplexer, Żyroskop, Baterię) i utrzymuje panele wyświetlaczy.
* **Kluczowe cechy:**
    * **Sloty OLED:** Cztery precyzyjne otwory dopasowane do wyświetlaczy 0.96" OLED (I2C/SPI) na bocznych ścianach.
    * **Interfejs Użytkownika:** Dedykowane otwory na przyciski sterujące.
    * **Mocowania:** Wewnętrzne wsporniki/szyny do stabilizacji PCB i modułu Mikrokontroler.
    * **Zatoka sensorów:** Dedykowane miejsce na żyroskop MPU6050, zapewniające jego stabilną pozycję dla dokładnego śledzenia rotacji.

### 4.2 Wieczko Górne (`new_cap.stl`)
Mechanizm zamykający obudowę.
* **Funkcja:** Uszczelnia urządzenie, chroniąc komponenty wewnętrzne przed kurzem i uszkodzeniami.
* **Kluczowe cechy:**
    * **Dostęp:** Zaprojektowane tak, aby być zdejmowalne w celu konserwacji lub wymiany baterii (zatrzask lub pasowanie na wcisk).
    * **Grill głośnika:** (Opcjonalnie) Perforacje umożliwiające wyraźne wydobywanie się dźwięku z wewnętrznego buzzera.

## 5. Specyfikacja Techniczna

| Cecha | Specyfikacja |
| :--- | :--- |
| **Wymiary** | Ok. 1000mm x 1000mm x 1000mm (Standardowy rozmiar kostki podręcznej) |
| **Grubość ścianki** | 2.0mm - 3.0mm (Optymalizacja sztywności vs czas druku) |
| **Tolerancja** | 0.2mm luzu dla elementów pasowanych |
| **Materiał** | PLA (Polylactic Acid) lub PETG |

## 6. Wytyczne Druku 3D

Zalecane ustawienia dla drukarek FDM (np. Prusa i3, Ender 3, Bambu Lab):

### Ustawienia Ogólne
* **Średnica dyszy:** 0.4mm
* **Wysokość warstwy:** 0.2mm (Jakość) lub 0.24mm (Draft)
* **Wypełnienie (Infill):** 15% - 20% (Wzór Grid lub Gyroid dla wytrzymałości)
* **Obrysy (Walls):** 3 (Aby zapewnić wytrzymałość ścianek przy otworach montażowych)

### Instrukcje Szczegółowe
* **Podpory (Supports):**
    * *Korpus:* Wymagane dla mostków okiennych OLED oraz otworów na przyciski. Zalecane użycie "Tree Supports" (podpory drzewiaste) dla łatwiejszego usuwania.
    * *Wieczko:* Zazwyczaj drukuje się na płasko bez podpór.
* **Orientacja:** Drukuj korpus największą płaską powierzchnią do dołu (zazwyczaj podstawą), aby zmaksymalizować przyczepność do stołu.

## 7. Instrukcja Montażu
1.  **Przygotowanie:** Usuń materiał podporowy i w razie potrzeby oszlifuj krawędzie otworów na przyciski i ekrany.
2.  **Montaż Ekranów:** Wsuń 4 ekrany OLED w odpowiednie sloty w finalnej wersji korpusu. Zabezpiecz klejem na gorąco lub małymi śrubami M2 (zależnie od otworów w PCB ekranu).
3.  **Elektronika:** Umieść wiązkę przewodów i Raspberry Pico w centrum. Upewnij się, że przyciski trafiają w przygotowane wycięcia.
4.  **Zamknięcie:** Zatrzaśnij lub przykręć `new_cap.stl` na `new_cube.stl`.

