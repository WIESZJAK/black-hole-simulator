import pygame
import math
import random
import sys
import datetime
import time
from pygame.locals import Rect

# Inicjalizacja Pygame – ładuje bibliotekę do obsługi grafiki i zdarzeń
pygame.init()

# Ustawienia ekranu – pobiera rozdzielczość ekranu i ustawia tryb pełnoekranowy
WIDTH = pygame.display.Info().current_w  # Szerokość ekranu w pikselach
HEIGHT = pygame.display.Info().current_h  # Wysokość ekranu w pikselach
# Tworzy okno w trybie pełnoekranowym
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(
    "BLACK HOLE")  # Ustawia tytuł okna

# Definicje kolorów – stałe RGB i RGBA używane w grafice
BLACK = (0, 0, 0)  # Czarny – tło
WHITE = (255, 255, 255)  # Biały – gwiazdy orbitujące, tekst
RED = (255, 0, 0)  # Czerwony – czarna dziura, orbity
GRAY = (50, 50, 50)  # Szary – panele UI
DARK_GRAY = (20, 20, 20)  # Ciemny szary – horyzont zdarzeń
GREEN = (0, 255, 0)  # Zielony – suwaki, podświetlony tekst
YELLOW = (255, 255, 0)  # Żółty – podświetlenie gwiazd
DARK_GREEN = (0, 150, 0)  # Ciemny zielony – nieużywany w kodzie
LIGHT_GRAY = (200, 200, 200)  # Jasny szary – ramki, podświetlenie
LIGHT_BLUE = (135, 206, 250)  # Jasny niebieski – gwiazdy przechwycone
OVERLAY_COLOR = (0, 0, 0, 150)  # Półprzezroczysty czarny – nakładki
BLUE = (0, 0, 255)  # Niebieski – przewidywane orbity
DARK_RED = (150, 0, 0)  # Ciemny czerwony dla ostatniej orbity

# Stałe symulacji – domyślne wartości parametrów fizycznych i wizualnych
GM_DEFAULT = 100000  # Domyślna stała grawitacyjna (GM) czarnej dziury
SIMULATION_SPEED_DEFAULT = 2.000  # Domyślna prędkość symulacji (1x rzeczywista)
TRAIL_LENGTH_DEFAULT = 50  # Domyślna długość śladu gwiazd w pikselach
# Maksymalna początkowa prędkość gwiazd przechwyconych
MAX_INITIAL_VELOCITY_DEFAULT = 100
PX_TO_KM_DEFAULT = 1e9  # Skala pikseli do kilometrów (1 px = 1e9 km)
C_DEFAULT = 299792  # Prędkość światła w km/s
# Skala czasu symulacji (do przeliczania na lata świetlne)
TIME_SCALE_DEFAULT = 3000
STAR_GM_FACTOR_DEFAULT = 0.001  # Siła interakcji grawitacyjnej między gwiazdami
MAX_STAR_ACCEL_DEFAULT = 10  # Maksymalne przyspieszenie gwiazd z interakcji
RELATIVITY_STRENGTH_DEFAULT = 0.0001  # Siła efektów OTW (precesja orbit)
# Czy gwiazdy mogą spadać do czarnej dziury
FALLING_STARS_ENABLED_DEFAULT = False
FALLING_STARS_PERCENTAGE_DEFAULT = 0  # Procentowa szansa na wpadnięcie gwiazdy
# Promień horyzontu zdarzeń zależny od GM
EVENT_HORIZON_RADIUS = int(math.sqrt(GM_DEFAULT) * 0.5)
# Podświetlanie gwiazd blisko horyzontu
CRITICAL_HIGHLIGHT_ENABLED_DEFAULT = False
# Włączenie efektów OTW (domyślnie wyłączone)
RELATIVITY_ENABLED_DEFAULT = False
# Wizualizacja efektów OTW (domyślnie wyłączona)
RELATIVITY_VISUALS_ENABLED_DEFAULT = False
# Interakcje grawitacyjne między gwiazdami
STAR_INTERACTION_ENABLED_DEFAULT = False
COLLISIONS_ENABLED_DEFAULT = False  # Zderzenia gwiazd (domyślnie wyłączone)
BLACK_HOLE_RADIUS_DEFAULT = 5  # Wizualny rozmiar czarnej dziury w pikselach
# Spadek siły grawitacji z odległością (r^GRAVITY_FALLOFF)
GRAVITY_FALLOFF_DEFAULT = 2.0
# Szansa ucieczki przechwyconych gwiazd (nieużywana)
CAPTURED_ESCAPE_CHANCE_DEFAULT = 0.05
ORBITS_ENABLED = False  # Domyślnie orbity włączone
orbit_point_counter = 0

# Zmienne globalne – aktualne wartości parametrów symulacji
GM = GM_DEFAULT  # Aktualna stała grawitacyjna
SIMULATION_SPEED = SIMULATION_SPEED_DEFAULT  # Aktualna prędkość symulacji
TRAIL_LENGTH = TRAIL_LENGTH_DEFAULT  # Aktualna długość śladu
MAX_INITIAL_VELOCITY = MAX_INITIAL_VELOCITY_DEFAULT  # Aktualna maksymalna prędkość początkowa
PX_TO_KM = PX_TO_KM_DEFAULT  # Aktualna skala pikseli do km
C = C_DEFAULT  # Aktualna prędkość światła
TIME_SCALE = TIME_SCALE_DEFAULT  # Aktualna skala czasu
STAR_GM_FACTOR = STAR_GM_FACTOR_DEFAULT  # Aktualna siła interakcji gwiazd
MAX_STAR_ACCEL = MAX_STAR_ACCEL_DEFAULT  # Aktualne maksymalne przyspieszenie gwiazd
RELATIVITY_STRENGTH = RELATIVITY_STRENGTH_DEFAULT  # Aktualna siła OTW
FALLING_STARS_ENABLED = FALLING_STARS_ENABLED_DEFAULT  # Stan spadania gwiazd
FALLING_STARS_PERCENTAGE = FALLING_STARS_PERCENTAGE_DEFAULT  # Procentowa szansa spadania
CRITICAL_HIGHLIGHT_ENABLED = CRITICAL_HIGHLIGHT_ENABLED_DEFAULT  # Stan podświetlania krytycznych gwiazd
RELATIVITY_ENABLED = RELATIVITY_ENABLED_DEFAULT  # Stan efektów OTW
RELATIVITY_VISUALS_ENABLED = RELATIVITY_VISUALS_ENABLED_DEFAULT  # Stan wizualizacji OTW
STAR_INTERACTION_ENABLED = STAR_INTERACTION_ENABLED_DEFAULT  # Stan interakcji gwiazd
COLLISIONS_ENABLED = COLLISIONS_ENABLED_DEFAULT  # Stan zderzeń gwiazd
BLACK_HOLE_RADIUS = BLACK_HOLE_RADIUS_DEFAULT  # Aktualny rozmiar czarnej dziury
GRAVITY_FALLOFF = GRAVITY_FALLOFF_DEFAULT  # Aktualny spadek grawitacji
CAPTURED_ESCAPE_CHANCE = CAPTURED_ESCAPE_CHANCE_DEFAULT  # Szansa ucieczki (nieużywana)
ORBITS_ENABLED = True  # Domyślnie orbity włączone

# Ustawienia kamery – początkowa pozycja i zoom
# Początkowa pozycja kamery (środek ekranu)
camera_x, camera_y = WIDTH / 2, HEIGHT / 2
camera_zoom = 1.0  # Początkowy zoom kamery
MIN_ZOOM, MAX_ZOOM = 0.2, 3.0  # Minimalny i maksymalny zoom
NUM_ORBITING = 0  # Liczba gwiazd orbitujących
NUM_CAPTURED = 0  # Liczba gwiazd przechwyconych
dragging_star = None  # Gwiazda aktualnie przeciągana
selected_star = None
stars = []  # Lista wszystkich gwiazd w symulacji
accretion_particles = []  # Lista cząsteczek w dysku akrecyjnym
DISK_RADIUS = 100  # Początkowa wielkość dysku akrecyjnego
dt_phys = 0.005  # Krok czasowy fizyki (zmniejszony dla większej dokładności)
# Maksymalna długość ostatniej orbity (nieużywana wprost)
LAST_ORBIT_LENGTH = 5000
prediction_length = 100  # Długość przewidywania orbity w krokach
# Kierunek ruchu przechwyconych gwiazd (domyślnie do BH)
captured_direction = "towards"
isometric_view = False  # Tryb widoku izometrycznego (domyślnie wyłączony)
new_star_type = "orbiting"  # Domyślny typ nowo tworzonej gwiazdy ("orbiting" lub "captured")
# Zasięg gradientu pola grawitacyjnego
STRONG_FIELD_RADIUS_DEFAULT = 100  # Domyślna wartość w pikselach
STRONG_FIELD_RADIUS = STRONG_FIELD_RADIUS_DEFAULT

# Klasa Star – reprezentuje pojedynczą gwiazdę w symulacji
class Star:
    def __init__(self, captured=False, used_names=None, name=None):
        # Inicjalizacja gwiazdy: czy jest przechwycona, lista użytych nazw, opcjonalna nazwa
        self.captured = captured  # Czy gwiazda jest przechwycona
        if used_names is None:
            used_names = set()  # Zbiór użytych nazw, jeśli nie podano
        if name:
            self.name = name  # Ustawienie podanej nazwy
            used_names.add(self.name)
        else:
            # Wybór losowej nazwy spośród dostępnych (pominięto pełną listę)
            available_names = [n for n in [
        "Rigel", "Betelgeza", "Syriusz", "Vega", "Aldebaran", "Procyon", "Antares", "Arktur",
        "Kapella", "Spika", "Deneb", "Altair", "Fomalhaut", "Regulus", "Polluks", "Mizar",
        "Alcyone", "Castor", "Bellatrix", "Mirfak", "Czarna Enigma", "Bezimienny Wędrowiec",
        "Sagittarius A*", "Tajemnica Andromedy", "Pulsar Żartowniś", "Nebuloid X", "Gwiazda Chaosu",
        "Eclipsia", "Centaurus Zonk", "Supernova LOL", "Czarny Kapitan",
        "Stella Obscura", "Gamma Tickler", "Nebula Zonk", "Quasar Q", "Astroclown", "Lunaticus",
        "Graviton Rex", "Polaris", "Sirrah", "Algol", "Mira", "Saiph", "Adhara", "Wezen",
        "Alnitak", "Alnilam", "Mintaka", "Hadar", "Acrux", "Gacrux", "Mimosa", "Shaula",
        "Kaus Australis", "Nunki", "Rukbat", "Zubenelgenubi", "Zubeneschamali", "Dschubba",
        "Agena", "Atria", "Sabik", "Rasalhague", "Eltanin", "Kaus Borealis", "Lesath",
        "Unukalhai", "Alya", "Thuban", "Alkaid", "Dubhe", "Merak", "Phecda", "Megrez",
        "Alioth", "Schedar", "Caph", "Ruchbah", "Navi", "Almach", "Hamal", "Menkar",
        "Diphda", "Mirach", "Alpheratz", "Scheat", "Markab", "Enif", "Sadalmelik",
        "Sadalsuud", "Alnair", "Albali", "Ancha", "Skat", "Zaurak", "Zosma", "Chertan",
        "Keplerian", "Newtonian", "Einsteinium", "Hawking's Paradox", "Event Horizon",
        "Quantum Drift", "Boson Peak", "Graviton Prime", "Planck Star", "Tachyon Blaze",
        "Strange Quark", "Photonis", "Schwarzschild", "Lagrange Point", "Eddington",
        "Feynman's Path", "Dirac's Echo", "Lorentzian", "Higgsfield", "Casimir", 
        "Penrose Singularity", "Fermi's Paradox", "Heisenberg", "Superstring", "M-Theory",
        "Chandrasekhar", "Bell's Theorem", "Copenhagen", "Kerr Horizon", "Noether's Arc",
        "Graviton Halo", "Cosmic Fabric", "Lambda Point", "Neutrino Pulse", "Turing Nexus",
        "Cauchy's Veil", "Boltzmann", "Quantum Foam", "Mandelbrot", "Riemann Rift",
        "Bose Haven", "Pauli's Exclusion", "Dirac Sea", "Eulerian", "Laplacean",
        "Maxwellian", "Schrodinger", "Causality", "Inflaton", "Dark Sector",
        "Einstein-Rosen", "Lorentz Drift", "Gauge Field", "Brane World", "Torsion Field",
        "Quantum Tide", "Faraday's Cage", "Kelvin Star", "Weyl's Window", "Hyperion",
        "Laplace Rift", "Cantorium", "Tachyon Arc", "Causal Nexus", "Hilbert's Edge",
        "Friedmann", "Ergosphere", "Entropy Wave", "Quantum Cascade", "Dirac's Bridge",
        "Curvature Singularity", "Hubble's Halo", "Wheeler's Conundrum", "Zeno's Paradox",
        "Superposition", "Quantum Entangle", "Bellatrix Nova", "Higgs Boson", "Dark Matter",
        "Photon Belt", "Eventum", "Neutronium", "Axion", "Wormhole", "Hyperbolic",
        "Radiant Quasar", "Quantum Flux", "Einstein's Lens", "Hermitian", "Null Zone",
        "Penrose", "Causal Loop", "Hawking's Rift", "Kerr Metric", "Braneworld",
        "Planck Horizon", "Einstein's Paradox", "Quantum Mirror", "Graviton Pulse",
        "Lense-Thirring", "Quantum Singularity", "Schrodinger's Path", "Cosmic Horizon"
    ] if n not in used_names]
            # Losowa nazwa lub generyczna
            self.name = random.choice(
                available_names) if available_names else f"Star_{len(used_names)}"
            used_names.add(self.name)

        # Rozmiar gwiazdy w pikselach (losowy)
        self.size = random.randint(2, 5)
        # Masa gwiazdy proporcjonalna do rozmiaru
        self.mass = self.size * random.uniform(0.8, 1.6)
        # Różne typy gwiazd
        self.type = random.choice(["normal", "small", "heavy"])
        if self.type == "small":
            self.size = 2
            self.mass = 0.5
        elif self.type == "heavy":
            self.size = 8
            self.mass = 5
        else:  # normal
            self.size = self.size
            self.mass = self.mass
        # Dodanie współrzędnej Z
        self.z = random.uniform(-200, 200)  # Początkowa współrzędna Z
        self.vz = 0.0  # Prędkość w osi Z

        self.trail = []  # Lista punktów śladu gwiazdy
        self.selected = False  # Czy gwiazda jest wybrana
        # Czas rozpoczęcia orbity (dla gwiazd przechwyconych)
        self.orbit_start_time = None
        self.orbit_count = 0  # Liczba pełnych orbit
        self.last_angle = None  # Ostatni kąt dla obliczeń orbity
        self.orbit_times = []  # Lista czasów orbit
        self.current_orbit_points = []  # Punkty bieżącej orbity
        self.last_orbit_points = []  # Punkty ostatniej orbity
        self.total_angle = 0.0  # Suma kątów dla detekcji orbity
        self.start_position = None  # Początkowa pozycja dla orbity

        self.is_approaching = True  # Początkowo gwiazda zbliża się
        self.previous_distance = None  # Poprzednia odległość od czarnej dziury
        self.orbits_completed = 0  # Licznik orbit dla gwiazd orbitujących
        self.critical = False

        if self.captured:
            # Ustawienie pozycji początkowej dla gwiazd przechwyconych w losowych miejscach
            self.x = random.uniform(0, WIDTH)
            self.y = random.uniform(0, HEIGHT)
            while math.hypot(self.x - WIDTH / 2, self.y - HEIGHT / 2) < EVENT_HORIZON_RADIUS + 50:  # Unikanie spawnienia zbyt blisko BH
                self.x = random.uniform(0, WIDTH)
                self.y = random.uniform(0, HEIGHT)

            dx = WIDTH / 2 - self.x  # Odległość x od centrum (czarna dziura)
            dy = HEIGHT / 2 - self.y  # Odległość y od centrum
            r = math.sqrt(dx**2 + dy**2)  # Odległość radialna od centrum

            v_circular = math.sqrt(GM / r)  # Prędkość orbitalna
            # Szerszy zakres prędkości początkowej
            v_initial = random.uniform(0.1 * v_circular, 2.0 * v_circular)
            angle = math.atan2(dy, dx)  # Kąt względem centrum
            if captured_direction == "towards":
                # Prędkość skierowana do czarnej dziury
                self.vx = v_initial * -math.sin(angle)
                self.vy = v_initial * math.cos(angle)
            elif captured_direction == "away":
                # Prędkość skierowana od czarnej dziury
                self.vx = v_initial * math.sin(angle)
                self.vy = v_initial * -math.cos(angle)
            else:
                # Losowy kierunek prędkości
                random_angle = random.uniform(0, 2 * math.pi)
                self.vx = v_initial * math.cos(random_angle)
                self.vy = v_initial * math.sin(random_angle)
        else:
            # Ustawienie pozycji i prędkości dla gwiazd orbitujących
            self.a = random.uniform(100, 600)  # Półoś wielka orbity
            e_max = min(0.95, 1 - (EVENT_HORIZON_RADIUS + 10) /
                        self.a)  # Maksymalna ekscentryczność
            self.e = random.uniform(0.0, e_max)  # Losowa ekscentryczność
            self.theta = random.uniform(0, 2 * math.pi)  # Kąt początkowy
            self.omega = random.uniform(0, 2 * math.pi)  # Kąt precesji
            self.r = self.a * (1 - self.e**2) / (1 + self.e *
                               math.cos(self.theta))  # Odległość radialna
            # Współrzędna x w układzie orbity
            x_orb = self.r * math.cos(self.theta)
            # Współrzędna y w układzie orbity
            y_orb = self.r * math.sin(self.theta)
            # Przekształcenie współrzędnych na ekran
            self.x = WIDTH / 2 + x_orb * \
                math.cos(self.omega) - y_orb * math.sin(self.omega)
            self.y = HEIGHT / 2 + x_orb * \
                math.sin(self.omega) + y_orb * math.cos(self.omega)
            h = math.sqrt(GM * self.a * (1 - self.e**2))  # Moment pędu
            v_r = (GM / h) * self.e * math.sin(self.theta)  # Prędkość radialna
            v_t = h / self.r  # Prędkość tangencjalna
            # Prędkość x w układzie orbity
            vx_orb = v_r * math.cos(self.theta) - v_t * math.sin(self.theta)
            # Prędkość y w układzie orbity
            vy_orb = v_r * math.sin(self.theta) + v_t * math.cos(self.theta)
            # Przekształcenie prędkości na ekran
            self.vx = vx_orb * math.cos(self.omega) - \
                                        vy_orb * math.sin(self.omega)
            self.vy = vx_orb * math.sin(self.omega) + \
                                        vy_orb * math.cos(self.omega)

        

    def compute_acceleration(self, stars=None):
        # Obliczanie przyspieszenia gwiazdy na podstawie grawitacji
        dx = (WIDTH / 2 - self.x)  # Odległość x od czarnej dziury
        dy = (HEIGHT / 2 - self.y)  # Odległość y od czarnej dziury
        dz = (0 - self.z)  # Odległość z od centrum (czarna dziura na z=0)
        r = math.sqrt(dx**2 + dy**2 + dz**2)  # Odległość radialna w 3D
        if r < 2:
            r = 2  # Minimalna odległość (zapobiega dzieleniu przez 0)
        # Siła grawitacji z uwzględnieniem spadku
        grav_factor = GM / (r**GRAVITY_FALLOFF)
        if self.captured:
            grav_factor *= 1.5  # Zwiększona grawitacja dla gwiazd przechwyconych
        ax = grav_factor * dx / r  # Przyspieszenie x
        ay = grav_factor * dy / r  # Przyspieszenie y
        az = grav_factor * dz / r  # Przyspieszenie z

        if RELATIVITY_ENABLED:
            # Dodanie efektów OTW (precesja orbit)
            precession_factor = RELATIVITY_STRENGTH * GM / (C * r**2)
            ax += precession_factor * self.vy  # Korekcja x
            ay -= precession_factor * self.vx  # Korekcja y
            # Brak korekcji dla Z w OTW w tej wersji

        if STAR_INTERACTION_ENABLED and stars:
            # Interakcje grawitacyjne między gwiazdami
            for other_star in stars:
                if other_star != self:
                    dx_star = other_star.x - self.x
                    dy_star = other_star.y - self.y
                    dz_star = other_star.z - self.z
                    r_star_squared = dx_star**2 + dy_star**2 + dz_star**2
                    if r_star_squared < 1000:  # Ograniczenie do gwiazd w promieniu 10 pikseli
                        r_star = math.sqrt(r_star_squared)
                        if r_star < 2:
                            r_star = 2  # Minimalna odległość
                        force = STAR_GM_FACTOR * GM * \
                            other_star.mass / (r_star**GRAVITY_FALLOFF)
                        ax += force * dx_star / r_star  # Przyspieszenie x od innej gwiazdy
                        ay += force * dy_star / r_star  # Przyspieszenie y od innej gwiazdy
                        az += force * dz_star / r_star  # Przyspieszenie z od innej gwiazdy
        return ax, ay, az  # Zwraca przyspieszenie w osiach x, y i z

    def draw(self, trail_surface, camera_x, camera_y, zoom):
        if ORBITS_ENABLED and len(self.trail) > 1:
            step = max(1, len(self.trail) // 50)  # Rysuj co n-ty punkt, aby ograniczyć liczbę linii
            for i in range(0, len(self.trail) - step, step):
                alpha = int(255 * (i / (len(self.trail) - 1)))
                color = (alpha, alpha, alpha)
                x1 = (self.trail[i][0] - camera_x) * zoom + WIDTH // 2
                y1 = (self.trail[i][1] - camera_y) * zoom + HEIGHT // 2
                x2 = (self.trail[i + step][0] - camera_x) * zoom + WIDTH // 2
                y2 = (self.trail[i + step][1] - camera_y) * zoom + HEIGHT // 2
                pygame.draw.line(trail_surface, color, (x1, y1), (x2, y2), 1)
        star_color = LIGHT_BLUE if self.captured else WHITE
        # Dostosowanie koloru do typu gwiazdy
        if self.type == "small":
            star_color = RED
        elif self.type == "heavy":
            star_color = BLUE
        return star_color

    def draw_isometric(self, screen, camera_x, camera_y, zoom):
        iso_x = (self.x - camera_x) * zoom + WIDTH // 2 + (self.z * 0.5) * zoom
        iso_y = (self.y - camera_y) * zoom + HEIGHT // 2 - (self.z * 0.5) * zoom
        star_color = LIGHT_BLUE if self.captured else WHITE
        if ORBITS_ENABLED and len(self.trail) > 1:
            step = max(1, len(self.trail) // 50)
            for i in range(0, len(self.trail) - step, step):
                alpha = int(255 * (i / (len(self.trail) - 1)))
                color = (alpha, alpha, alpha)
                x1 = (self.trail[i][0] - camera_x) * zoom + WIDTH // 2 + (self.z * 0.5) * zoom
                y1 = (self.trail[i][1] - camera_y) * zoom + HEIGHT // 2 - (self.z * 0.5) * zoom
                x2 = (self.trail[i + step][0] - camera_x) * zoom + WIDTH // 2 + (self.z * 0.5) * zoom
                y2 = (self.trail[i + step][1] - camera_y) * zoom + HEIGHT // 2 - (self.z * 0.5) * zoom
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 1)
        pygame.draw.circle(screen, star_color, (int(iso_x), int(iso_y)), int(self.size * zoom))
        return iso_x, iso_y, star_color

    def fall_probability(self):
        # Obliczanie prawdopodobieństwa wpadnięcia gwiazdy do czarnej dziury
        distance_to_bh = math.hypot(
            self.x - WIDTH / 2, self.y - HEIGHT / 2)  # Odległość od BH
        velocity = math.hypot(self.vx, self.vy)  # Całkowita prędkość gwiazdy
        radial_velocity = (self.vx * (self.x - WIDTH / 2) + self.vy * (self.y - HEIGHT / 2)
                           ) / distance_to_bh if distance_to_bh > 0 else 0  # Prędkość radialna
        escape_velocity = math.sqrt(
            2 * GM / distance_to_bh)  # Prędkość ucieczki
        if distance_to_bh <= EVENT_HORIZON_RADIUS and radial_velocity < 0 and velocity < escape_velocity:
            return 100.0  # 100% szansy na wpadnięcie wewnątrz horyzontu
        elif distance_to_bh <= EVENT_HORIZON_RADIUS * 1.5:
            # Prawdopodobieństwo w strefie bliskiej horyzontowi
            prob = min(100.0, max(0.0, 100 - (distance_to_bh - 
                       EVENT_HORIZON_RADIUS) / (EVENT_HORIZON_RADIUS * 0.5) * 100))
            if radial_velocity > 0:
                prob *= 0.5  # Zmniejszona szansa, jeśli gwiazda się oddala
            # Skalowane przez FALLING_STARS_PERCENTAGE
            return prob * FALLING_STARS_PERCENTAGE / 100.0
        else:
            return 0.0  # Brak szansy poza strefą krytyczną

    def draw_last_orbit(self, screen, camera_x, camera_y, zoom):
        if not ORBITS_ENABLED:
            return
        if self.orbit_count >= 1 and len(self.last_orbit_points) > 10:
            screen_last_orbit_points = []
            for point in self.last_orbit_points:
                if len(point) == 3:  # Używamy rzeczywistych Z
                    x, y, z = point
                else:
                    continue
                if isometric_view:
                    iso_x = (x - camera_x) * zoom + WIDTH // 2 + (z * 0.5) * zoom
                    iso_y = (y - camera_y) * zoom + HEIGHT // 2 - (z * 0.5) * zoom
                    screen_last_orbit_points.append((iso_x, iso_y))
                else:
                    screen_x = (x - camera_x) * zoom + WIDTH // 2
                    screen_y = (y - camera_y) * zoom + HEIGHT // 2
                    screen_last_orbit_points.append((screen_x, screen_y))
            if len(screen_last_orbit_points) > 2:
                color = DARK_RED if not self.captured else (LIGHT_BLUE if not self.critical else DARK_RED)
                pygame.draw.lines(screen, color, False, screen_last_orbit_points, 2)

    def predict_orbit(self, steps=prediction_length, step_size=5.0):
        points = []
        x, y, z = self.x, self.y, self.z
        vx, vy, vz = self.vx, self.vy, self.vz
        total_distance = 0.0

        for _ in range(steps):
            dx = WIDTH / 2 - x
            dy = HEIGHT / 2 - y
            dz = 0 - z
            r = math.sqrt(dx**2 + dy**2 + dz**2)
            if r < 2:
                r = 2
            grav_factor = GM / (r**GRAVITY_FALLOFF)
            if self.captured:
                grav_factor *= 1.5
            ax = grav_factor * dx / r
            ay = grav_factor * dy / r
            az = grav_factor * dz / r

            if RELATIVITY_ENABLED:
                precession_factor = RELATIVITY_STRENGTH * GM / (C * r**2)
                ax += precession_factor * vy
                ay -= precession_factor * vx

            if STAR_INTERACTION_ENABLED and stars:
                for other_star in stars:
                    if other_star != self:
                        dx_star = other_star.x - x
                        dy_star = other_star.y - y
                        dz_star = other_star.z - z
                        r_star_squared = dx_star**2 + dy_star**2 + dz_star**2
                        if r_star_squared < 100:
                            r_star = math.sqrt(r_star_squared)
                            if r_star < 2:
                                r_star = 2
                            force = STAR_GM_FACTOR * GM * other_star.mass / (r_star**GRAVITY_FALLOFF)
                            ax += force * dx_star / r_star
                            ay += force * dy_star / r_star
                            az += force * dz_star / r_star

            speed = math.sqrt(vx**2 + vy**2 + vz**2)
            if speed < 0.1:
                break
            dt = step_size / speed

            vx += ax * dt
            vy += ay * dt
            vz += az * dt
            x += vx * dt
            y += vy * dt
            z += vz * dt

            points.append((x, y, z))
            total_distance += step_size

            if total_distance > 2000:
                break

        return points

    def draw_orbit(self, screen, camera_x, camera_y, zoom):
        if not ORBITS_ENABLED:
            return None, None
        if not self.captured:
            if len(self.current_orbit_points) > 10:
                screen_points = []
                for point in self.current_orbit_points:
                    if len(point) == 2:  # Stare dane (x, y)
                        x, y = point
                        z = self.z
                    elif len(point) == 3:  # Nowe dane (x, y, z)
                        x, y, z = point
                    else:
                        continue
                    if isometric_view:
                        screen_x = (x - camera_x) * zoom + WIDTH // 2 + (z * 0.5) * zoom
                        screen_y = (y - camera_y) * zoom + HEIGHT // 2 - (z * 0.5) * zoom
                    else:
                        screen_x = (x - camera_x) * zoom + WIDTH // 2
                        screen_y = (y - camera_y) * zoom + HEIGHT // 2
                    screen_points.append((screen_x, screen_y))
                if len(screen_points) > 2:
                    return screen_points, RED  # Stały kolor czerwony
            return None, None
        else:
            predicted_points = self.predict_orbit(steps=prediction_length, step_size=5.0)
            screen_predicted = []
            for x, y, z in predicted_points:
                if isometric_view:
                    screen_x = (x - camera_x) * zoom + WIDTH // 2 + (z * 0.5) * zoom
                    screen_y = (y - camera_y) * zoom + HEIGHT // 2 - (z * 0.5) * zoom
                else:
                    screen_x = (x - camera_x) * zoom + WIDTH // 2
                    screen_y = (y - camera_y) * zoom + HEIGHT // 2
                screen_predicted.append((screen_x, screen_y))
            if len(screen_predicted) > 2:
                return screen_predicted, BLUE if not self.critical else DARK_RED
            return None, None

# Funkcje pomocnicze
def fade_out(screen, surface, duration=500):
    # Animacja zanikania ekranu do czerni
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    screen_copy = surface.copy()  # Kopia ekranu do animacji
    while True:
        elapsed = pygame.time.get_ticks() - start_time  # Czas od startu animacji
        # Przejrzystość (od 255 do 0)
        alpha = int(255 * (1 - elapsed / duration))
        if alpha <= 0:
            break  # Koniec animacji
        screen.blit(screen_copy, (0, 0))  # Rysowanie kopii ekranu
        overlay = pygame.Surface((WIDTH, HEIGHT))  # Nakładka
        overlay.set_alpha(255 - alpha)  # Ustawienie przejrzystości nakładki
        overlay.fill(BLACK)  # Wypełnienie czernią
        screen.blit(overlay, (0, 0))  # Rysowanie nakładki
        pygame.display.flip()  # Aktualizacja ekranu
        clock.tick(60)  # Ograniczenie do 60 FPS

# Animacja oddalania kamery na starcie symulacji
def zoom_out_animation(screen, stars, duration=2000):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    initial_zoom = 100  # Początkowy zoom (duży)
    final_zoom = 1.0  # Końcowy zoom (normalny)
    trail_surface = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA)  # Powierzchnia dla śladów

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()  # Zamknięcie gry
                sys.exit()  # Wyjście z programu

        elapsed = pygame.time.get_ticks() - start_time  # Czas od startu
        if elapsed >= duration:
            global camera_zoom
            camera_zoom = final_zoom  # Ustawienie końcowego zoomu
            break

        t = elapsed / duration  # Progres animacji (0 do 1)
        camera_zoom = initial_zoom - \
            (initial_zoom - final_zoom) * (1 - (1 - t)**3)  # Krzywa animacji

        screen.fill(BLACK)  # Czyszczenie ekranu
        trail_surface.fill((0, 0, 0, 0))  # Czyszczenie śladów

        bh_x = (WIDTH / 2 - camera_x) * camera_zoom + \
                WIDTH // 2  # Pozycja x czarnej dziury
        bh_y = (HEIGHT / 2 - camera_y) * camera_zoom + \
                HEIGHT // 2  # Pozycja y czarnej dziury
        # Promień horyzontu zdarzeń
        event_horizon_radius = int(math.sqrt(GM) * 0.5)
        pygame.draw.circle(screen, DARK_GRAY, (int(bh_x), int(bh_y)), int(
            event_horizon_radius * camera_zoom), 1)  # Rysowanie horyzontu
        pygame.draw.circle(screen, RED, (int(bh_x), int(bh_y)), int(
            BLACK_HOLE_RADIUS * camera_zoom))  # Rysowanie BH

        for star in stars:
            # Rysowanie śladu gwiazdy
            star_color = star.draw(
                trail_surface, camera_x, camera_y, camera_zoom)
            screen_x = (star.x - camera_x) * camera_zoom + \
                        WIDTH // 2  # Pozycja x gwiazdy
            screen_y = (star.y - camera_y) * camera_zoom + \
                        HEIGHT // 2  # Pozycja y gwiazdy
            pygame.draw.circle(screen, star_color, (int(screen_x), int(screen_y)), int(
                star.size * camera_zoom))  # Rysowanie gwiazdy

        screen.blit(trail_surface, (0, 0))  # Nakładanie śladów na ekran
        pygame.display.flip()  # Aktualizacja ekranu
        clock.tick(60)  # Ograniczenie do 60 FPS

# Renderowanie tekstu z podziałem na linie i przewijaniem
def render_textrect_with_scroll(font, text, color, rect, scroll_offset=0):
    lines = []  # Lista renderowanych linii
    current_line = ""  # Bieżąca linia tekstu

    for line in text.split('\n'):
        if line.startswith('# '):
            # Nagłówek o większej czcionce
            header_font = pygame.font.SysFont("monospace", 25)
            header_text = header_font.render(line[2:], True, color)
            lines.append(header_text)
        else:
            # Normalny tekst, dzielony na linie pasujące do szerokości
            words = line.split(' ')
            for word in words:
                if font.size(current_line + word)[0] < rect.width:
                    current_line += word + " "  # Dodawanie słowa do linii
                else:
                    if current_line.strip():
                        # Renderowanie pełnej linii
                        lines.append(font.render(
                            current_line.strip(), True, color))
                    current_line = word + " "  # Nowa linia z bieżącym słowem
            if current_line.strip():
                lines.append(font.render(current_line.strip(),
                             True, color))  # Ostatnia linia
            current_line = ""

    total_height = sum(line.get_height()
                       for line in lines)  # Całkowita wysokość tekstu
    surfaces = []  # Lista powierzchni do wyświetlenia
    y = rect.top - scroll_offset  # Początkowa pozycja y z przewijaniem

    for line in lines:
        if y + line.get_height() > rect.top and y < rect.bottom:
            surfaces.append((line, (rect.left, y)))  # Dodanie widocznej linii
        y += line.get_height()  # Przesunięcie y dla kolejnej linii

    return surfaces, total_height  # Zwraca powierzchnie i wysokość

# Ograniczenie pozycji kamery do granic ekranu
def clamp_camera():
    global camera_x, camera_y
    camera_x = max(0, min(camera_x, WIDTH))  # Ograniczenie x
    camera_y = max(0, min(camera_y, HEIGHT))  # Ograniczenie y

# Sprawdzanie, czy gwiazda jest poza granicami ekranu (z marginesem)
def check_star_bounds(star):
    if star.x < -500 or star.x > WIDTH + 500 or star.y < -500 or star.y > HEIGHT + 500:
        return True  # Gwiazda poza granicami
    return False  # Gwiazda w granicach

# Formatowanie czasu symulacji na czytelny format
def format_sim_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"  # Czas w sekundach
    elif seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}m:{secs:02d}s"  # Czas w minutach i sekundach
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        # Czas w godzinach, minutach i sekundach
        return f"{hours}h:{mins:02d}m:{secs:02d}s"

# Menu ustawień – pozwala na zmianę parametrów symulacji
def settings_menu():
    global C, camera_zoom, dt_phys, MAX_STAR_ACCEL, RELATIVITY_STRENGTH, GM, STAR_GM_FACTOR, captured_direction, MAX_INITIAL_VELOCITY, PX_TO_KM, TIME_SCALE, BLACK_HOLE_RADIUS, GRAVITY_FALLOFF
    font = pygame.font.SysFont("monospace", 20)  # Czcionka dla etykiet
    tiny_font = pygame.font.SysFont("monospace", 15)  # Czcionka dla opisów
    clock = pygame.time.Clock()
    dragging_slider = None  # Suwak aktualnie przeciągany

    # Słownik ustawień z wartościami, zakresami i opisami
    settings = {
        "Captured Direction": {"value": captured_direction, "options": ["towards", "away", "random"], "desc": "Kierunek ruchu przechwyconych gwiazd: 'towards' - do BH, 'away' - od BH, 'random' - losowy."},
        "Light Speed": {"value": C, "min": 100000, "max": 500000, "desc": "Prędkość światła w km/s - wpływa na efekty OTW, gdy włączone."},
        "Camera Zoom": {"value": camera_zoom, "min": 0.2, "max": 3.0, "desc": "Początkowy zoom kamery - zmienia skalę widoku."},
        "Physics Step": {"value": dt_phys, "min": 0.001, "max": 0.1, "desc": "Krok czasowy fizyki - mniejszy = wolniejsza, dokładniejsza symulacja."},
        "Max Star Accel": {"value": MAX_STAR_ACCEL, "min": 1, "max": 50, "desc": "Maksymalne przyspieszenie gwiazd - ogranicza niestabilność."},
        "Relativity Strength": {"value": RELATIVITY_STRENGTH, "min": 0.0, "max": 0.001, "desc": "Siła efektów OTW - wpływa na precesję orbit."},
        "Initial GM": {"value": GM, "min": 10000, "max": 200000, "desc": "Stała grawitacyjna BH - większa = silniejsza grawitacja."},
        "Star Interaction": {"value": STAR_GM_FACTOR, "min": 0.0, "max": 0.5, "desc": "Siła interakcji między gwiazdami - większa = więcej chaosu."},
        "Max Initial Vel": {"value": MAX_INITIAL_VELOCITY, "min": 50, "max": 200, "desc": "Maksymalna prędkość początkowa gwiazd przechwyconych."},
        "Px to Km": {"value": PX_TO_KM, "min": 1e8, "max": 1e10, "desc": "Skala pikseli do km - wpływa na jednostki odległości."},
        "Time Scale": {"value": TIME_SCALE, "min": 1000, "max": 5000, "desc": "Skala czasu w symulacji - większa = szybsze lata świetlne."},
        "BH Radius": {"value": BLACK_HOLE_RADIUS, "min": 1, "max": 20, "desc": "Rozmiar wizualny BH - tylko efekt estetyczny."},
        "Gravity Falloff": {"value": GRAVITY_FALLOFF, "min": 1.5, "max": 3.0, "desc": "Spadek grawitacji z odległością - większy = szybszy spadek."}
    }

    while True:
        screen.fill(BLACK)  # Czyszczenie ekranu
        title = font.render("Settings", True, WHITE)  # Tytuł menu
        # Wyśrodkowanie tytułu
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        for i, (key, setting) in enumerate(settings.items()):
            # Renderowanie każdego ustawienia
            if "options" in setting:
                # Etykieta z wartością
                label = font.render(f"{key}: {setting['value']}", True, WHITE)
                label_rect = label.get_rect(
                    topleft=(50, 100 + i * 150))  # Pozycja etykiety
                screen.blit(label, label_rect.topleft)
                desc = tiny_font.render(
                    setting["desc"], True, LIGHT_GRAY)  # Opis ustawienia
                screen.blit(desc, (50, 120 + i * 60))  # Pozycja opisu
                if label_rect.collidepoint(pygame.mouse.get_pos()):
                    # Podświetlenie przy najechaniu
                    pygame.draw.rect(screen, LIGHT_GRAY, label_rect, 2)
            else:
                # Renderowanie suwaka dla ustawienia numerycznego
                label = font.render(f"{key}: {setting['value']:.3f}" if isinstance(
                    setting['value'], float) else f"{key}: {setting['value']}", True, WHITE)
                screen.blit(label, (50, 100 + i * 60))  # Pozycja etykiety
                desc = tiny_font.render(setting["desc"], True, LIGHT_GRAY)
                screen.blit(desc, (50, 120 + i * 60))  # Pozycja opisu
                slider_rect = pygame.Rect(
                    380, 105 + i * 60, 300, 10)  # Prostokąt suwaka
                # Rysowanie suwaka
                pygame.draw.rect(screen, LIGHT_GRAY, slider_rect)
                slider_pos = slider_rect.left + (setting["value"] - setting["min"]) / (
                    # Pozycja wskaźnika
                    setting["max"] - setting["min"]) * slider_rect.width
                # Wskaźnik suwaka
                pygame.draw.rect(screen, GREEN, (slider_pos -
                                 5, slider_rect.top - 2, 10, 14))
                # Zapisywanie prostokąta dla obsługi zdarzeń
                setting["rect"] = slider_rect

        # Przyciski powrotu i resetu
        return_button = font.render("Back", True, WHITE)
        return_rect = return_button.get_rect(
            center=(WIDTH // 2 - 100, HEIGHT - 50))
        reset_button = font.render("Reset to Defaults", True, WHITE)
        reset_rect = reset_button.get_rect(
            center=(WIDTH // 2 + 100, HEIGHT - 50))

        if return_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_GRAY, return_rect,
                             2)  # Podświetlenie powrotu
        if reset_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_GRAY, reset_rect,
                             2)  # Podświetlenie resetu

        screen.blit(return_button, return_rect.topleft)
        screen.blit(reset_button, reset_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Zamknięcie gry
                sys.exit()  # Wyjście z programu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_rect.collidepoint(event.pos):
                    # Zapisanie zmienionych ustawień przy powrocie
                    captured_direction = settings["Captured Direction"]["value"]
                    C = settings["Light Speed"]["value"]
                    camera_zoom = settings["Camera Zoom"]["value"]
                    dt_phys = settings["Physics Step"]["value"]
                    MAX_STAR_ACCEL = settings["Max Star Accel"]["value"]
                    RELATIVITY_STRENGTH = settings["Relativity Strength"]["value"]
                    GM = settings["Initial GM"]["value"]
                    STAR_GM_FACTOR = settings["Star Interaction"]["value"]
                    MAX_INITIAL_VELOCITY = settings["Max Initial Vel"]["value"]
                    PX_TO_KM = settings["Px to Km"]["value"]
                    TIME_SCALE = settings["Time Scale"]["value"]
                    BLACK_HOLE_RADIUS = settings["BH Radius"]["value"]
                    GRAVITY_FALLOFF = settings["Gravity Falloff"]["value"]
                    return  # Wyjście z menu
                elif reset_rect.collidepoint(event.pos):
                    # Resetowanie ustawień do domyślnych
                    settings["Captured Direction"]["value"] = "towards"
                    settings["Light Speed"]["value"] = C_DEFAULT
                    settings["Camera Zoom"]["value"] = 1.0
                    settings["Physics Step"]["value"] = 0.005
                    settings["Max Star Accel"]["value"] = MAX_STAR_ACCEL_DEFAULT
                    settings["Relativity Strength"]["value"] = RELATIVITY_STRENGTH_DEFAULT
                    settings["Initial GM"]["value"] = GM_DEFAULT
                    settings["Star Interaction"]["value"] = STAR_GM_FACTOR_DEFAULT
                    settings["Max Initial Vel"]["value"] = MAX_INITIAL_VELOCITY_DEFAULT
                    settings["Px to Km"]["value"] = PX_TO_KM_DEFAULT
                    settings["Time Scale"]["value"] = TIME_SCALE_DEFAULT
                    settings["BH Radius"]["value"] = BLACK_HOLE_RADIUS_DEFAULT
                    settings["Gravity Falloff"]["value"] = GRAVITY_FALLOFF_DEFAULT
                for i, (key, setting) in enumerate(settings.items()):
                    if "options" in setting:
                        # Przełączanie opcji po kliknięciu
                        label_rect = font.render(f"{key}: {setting['value']}", True, WHITE).get_rect(
                            topleft=(50, 100 + i * 60))
                        if label_rect.collidepoint(event.pos):
                            current_index = setting["options"].index(
                                setting["value"])
                            setting["value"] = setting["options"][(
                                current_index + 1) % len(setting["options"])]
                    elif setting["rect"].collidepoint(event.pos):
                        dragging_slider = key  # Rozpoczęcie przeciągania suwaka
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_star = None  # Zakończenie przeciągania gwiazdy
                dragging_slider = None  # Zakończenie przeciągania
            elif event.type == pygame.MOUSEMOTION and dragging_slider is not None:
                # Aktualizacja wartości suwaka podczas przeciągania
                mx, _ = event.pos
                setting = settings[dragging_slider]
                setting["value"] = setting["min"] + (setting["max"] - setting["min"]) * (
                    mx - setting["rect"].left) / setting["rect"].width
                setting["value"] = max(setting["min"], min(
                    setting["max"], setting["value"]))

        pygame.display.flip()  # Aktualizacja ekranu
        clock.tick(60)  # Ograniczenie do 60 FPS

# Menu startowe – pozwala na wybór liczby gwiazd i przejście do symulacji
def start_menu():
    font = pygame.font.SysFont("monospace", 40)  # Czcionka tytułu
    small_font = pygame.font.SysFont("monospace", 20)  # Czcionka etykiet
    tiny_font = pygame.font.SysFont("monospace", 15)  # Czcionka opisów
    footer_font = pygame.font.SysFont("monospace", 12)  # Czcionka stopki
    input_orbiting = ""  # Pole wejściowe dla gwiazd orbitujących
    input_captured = ""  # Pole wejściowe dla gwiazd przechwyconych
    active_input = None  # Aktywne pole wejściowe

    # Stałe pozycje elementów UI
    TITLE_POS = (WIDTH // 2, HEIGHT // 4 - 50)
    ORBITING_LABEL_POS = (WIDTH // 2 - 200, HEIGHT // 2 - 50)
    ORBITING_INPUT_POS = (WIDTH // 2 - 10, HEIGHT // 2 - 52)
    ORBITING_DESC_POS = (WIDTH // 2 - 170, HEIGHT // 2 - 30)
    CAPTURED_LABEL_POS = (WIDTH // 2 - 200, HEIGHT // 2)
    CAPTURED_INPUT_POS = (WIDTH // 2 - 10, HEIGHT // 2 - 3)
    CAPTURED_DESC_POS = (WIDTH // 2 - 170, HEIGHT // 2 + 20)
    START_BUTTON_POS = (WIDTH // 2, HEIGHT // 2 + 100)
    INFO_BUTTON_POS = (WIDTH // 2 - 150, HEIGHT - 60)
    MORE_INFO_BUTTON_POS = (WIDTH // 2, HEIGHT - 60)
    SETTINGS_BUTTON_POS = (WIDTH // 2 + 150, HEIGHT - 60)
    ORBITING_STARS_POS = (170, HEIGHT // 2 - 50)
    CAPTURED_STARS_POS = (WIDTH - 450, HEIGHT // 2 - 50)
    LEGEND_LEFT_POS = (5, HEIGHT - 150)
    LEGEND_RIGHT_POS = (WIDTH - 140, HEIGHT - 150)
    COPYRIGHT_POS = (WIDTH // 2, HEIGHT - 30)

    magik_star = {"x": WIDTH // 2, "y": HEIGHT // 2 + 200,
        "angle": math.pi / 2, "size": 3}  # Animowana gwiazda dekoracyjna
    wiggle_time = 0  # Czas dla animacji wiggle

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0  # Czas klatki w sekundach
        wiggle_time += dt  # Aktualizacja czasu animacji

        screen.fill(BLACK)  # Czyszczenie ekranu
        title = font.render("Black Hole Simulator", True, WHITE)  # Tytuł
        orbiting_label = small_font.render(
            "Orbiting Stars:", True, WHITE)  # Etykieta gwiazd orbitujących
        orbiting_input = small_font.render(
            input_orbiting, True, WHITE)  # Pole wejściowe orbitujących
        orbiting_desc = tiny_font.render(
            "(na orbicie BH)", True, WHITE)  # Opis
        # Etykieta gwiazd przechwyconych
        captured_label = small_font.render("Captured Stars:", True, WHITE)
        captured_input = small_font.render(
            input_captured, True, WHITE)  # Pole wejściowe przechwyconych
        captured_desc = tiny_font.render("(przechwycone)", True, WHITE)  # Opis
        copyright_text = footer_font.render(
            "copyright by Magik 2025 Optimized by GROK", True, WHITE)  # Stopka
        info_button = tiny_font.render(
            "[i] Informacje", True, GREEN)  # Przycisk informacji
        more_info_button = tiny_font.render(
            "[m] Więcej informacji", True, GREEN)  # Przycisk szczegółów
        settings_button = tiny_font.render(
            "[s] Settings", True, GREEN)  # Przycisk ustawień
        info_rect = info_button.get_rect(center=INFO_BUTTON_POS)
        more_info_rect = more_info_button.get_rect(center=MORE_INFO_BUTTON_POS)
        settings_rect = settings_button.get_rect(center=SETTINGS_BUTTON_POS)

        mouse_pos = pygame.mouse.get_pos()  # Pozycja myszy
        start_button = font.render(
            "Go Black Hole Go!", True, WHITE)  # Przycisk startu
        start_rect = start_button.get_rect(center=START_BUTTON_POS)
        is_hovering = start_rect.collidepoint(mouse_pos) and input_orbiting.isdigit(
        # Czy mysz nad przyciskiem i dane poprawne
        ) and input_captured.isdigit()

        
        # Rysowanie elementów UI
        screen.blit(
            title, (TITLE_POS[0] - title.get_width() // 2, TITLE_POS[1]))
        screen.blit(orbiting_label, ORBITING_LABEL_POS)
        screen.blit(orbiting_input, ORBITING_INPUT_POS)
        screen.blit(orbiting_desc, ORBITING_DESC_POS)
        screen.blit(captured_label, CAPTURED_LABEL_POS)
        screen.blit(captured_input, CAPTURED_INPUT_POS)
        screen.blit(captured_desc, CAPTURED_DESC_POS)
        screen.blit(
            copyright_text, (COPYRIGHT_POS[0] - copyright_text.get_width() // 2, COPYRIGHT_POS[1]))
        screen.blit(info_button, info_rect.topleft)
        screen.blit(more_info_button, more_info_rect.topleft)
        screen.blit(settings_button, settings_rect.topleft)

        if is_hovering:
            # Animacja przy najechaniu na przycisk startu MAGIK
            start_button = font.render("Go Black Hole Go!", True, GREEN)
            pygame.draw.rect(screen, LIGHT_GRAY, start_rect, 2)
            magik_star["angle"] += 2 * dt  # Obrót gwiazdy
            radius_x = 150
            radius_y = 30
            magik_star["x"] = start_rect.centerx + \
                math.cos(magik_star["angle"]) * radius_x  # Pozycja x gwiazdy
            magik_star["y"] = start_rect.centery + 100 + \
                math.sin(magik_star["angle"]) * radius_y  # Pozycja y gwiazdy
            pygame.draw.circle(screen, WHITE, (int(magik_star["x"]), int(
                magik_star["y"])), magik_star["size"])  # Rysowanie gwiazdy
            pygame.draw.rect(screen, GREEN, (int(magik_star["x"] - magik_star["size"] - 5), int(
                # Ramka
                magik_star["y"] - magik_star["size"] - 5), magik_star["size"] * 2 + 10, magik_star["size"] * 2 + 10), 2)
            magik_text = tiny_font.render("MAGIK", True, GREEN)
            screen.blit(magik_text, (int(magik_star["x"] - magik_text.get_width() // 2), int(
                magik_star["y"] - magik_star["size"] - 20)))  # Tekst "MAGIK"
        screen.blit(start_button, start_rect.topleft)

        # Podświetlenie przycisków informacyjnych
        if info_rect.collidepoint(mouse_pos):
            info_button = tiny_font.render("[i] Informacje", True, LIGHT_GRAY)
            pygame.draw.rect(screen, LIGHT_GRAY, info_rect, 2)
            screen.blit(info_button, info_rect.topleft)
        if more_info_rect.collidepoint(mouse_pos):
            more_info_button = tiny_font.render(
                "[m] Więcej informacji", True, LIGHT_GRAY)
            pygame.draw.rect(screen, LIGHT_GRAY, more_info_rect, 2)
            screen.blit(more_info_button, more_info_rect.topleft)
        if settings_rect.collidepoint(mouse_pos):
            settings_button = tiny_font.render(
                "[s] Settings", True, LIGHT_GRAY)
            pygame.draw.rect(screen, LIGHT_GRAY, settings_rect, 2)
            screen.blit(settings_button, settings_rect.topleft)

        # Prostokąty pól wejściowych
        orbiting_input_rect = pygame.Rect(
            ORBITING_INPUT_POS[0], ORBITING_INPUT_POS[1], 50, 30)
        captured_input_rect = pygame.Rect(
            CAPTURED_INPUT_POS[0], CAPTURED_INPUT_POS[1], 50, 30)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if orbiting_input_rect.collidepoint(mouse_x, mouse_y):
            # Podświetlenie pola orbitujących
            pygame.draw.rect(screen, LIGHT_GRAY, orbiting_input_rect, 2)
        elif captured_input_rect.collidepoint(mouse_x, mouse_y):
            # Podświetlenie pola przechwyconych
            pygame.draw.rect(screen, LIGHT_GRAY, captured_input_rect, 2)

        if active_input == "orbiting":
            # Aktywne pole orbitujących
            pygame.draw.rect(screen, WHITE, orbiting_input_rect, 1)
        elif active_input == "captured":
            # Aktywne pole przechwyconych
            pygame.draw.rect(screen, WHITE, captured_input_rect, 1)

        # Obliczanie liczby gwiazd do wyświetlenia
        orbiting_count = int(input_orbiting) if input_orbiting.isdigit() else 0
        captured_count = int(input_captured) if input_captured.isdigit() else 0

        # Rysowanie miniaturek gwiazd orbitujących
        for i in range(min(orbiting_count, 200)):
            row = i // 15
            col = i % 15
            wiggle_x = math.sin(wiggle_time + i) * 2  # Animacja wiggle x
            wiggle_y = math.cos(wiggle_time + i) * 2  # Animacja wiggle y
            pygame.draw.circle(screen, WHITE, (int(ORBITING_STARS_POS[0] + col * 20 + wiggle_x), int(
                # Rysowanie gwiazd
                ORBITING_STARS_POS[1] + row * 20 + wiggle_y)), 3)

        # Rysowanie miniaturek gwiazd przechwyconych
        for i in range(min(captured_count, 200)):
            row = i // 15
            col = i % 15
            wiggle_x = math.sin(wiggle_time + i) * 2
            wiggle_y = math.cos(wiggle_time + i) * 2
            pygame.draw.circle(screen, LIGHT_BLUE, (int(
                CAPTURED_STARS_POS[0] + col * 20 + wiggle_x), int(CAPTURED_STARS_POS[1] + row * 20 + wiggle_y)), 3)

        # Legenda klawiszy (pominięto szczegóły dla skrócenia)
        legend_lines_left = [
            "Esc: Wyjdź",
            "P: Pauza",
            "R: Restart",
            "I: Ukryj interf.",
            "WASD: Kamera",
            "Q: Wł/Wył OTW",
            ",/.: Zoom"
        ]
        legend_lines_right = [
            "T/Y: Dł. śladu",
            "G/H: GM",
            "B/N: Rozm. BH",
            "+/-: Gwiazdy",
            "F: Statysty",
            "E: Eksperyment",
            "C: Zderzenia"
        ]

        for i, line in enumerate(legend_lines_left):
            legend_text = tiny_font.render(line, True, WHITE)
            # Rysowanie legendy lewej
            screen.blit(
                legend_text, (LEGEND_LEFT_POS[0], LEGEND_LEFT_POS[1] + i * 20))

        for i, line in enumerate(legend_lines_right):
            legend_text = tiny_font.render(line, True, WHITE)
            # Rysowanie legendy prawej
            screen.blit(
                legend_text, (LEGEND_RIGHT_POS[0], LEGEND_RIGHT_POS[1] + i * 20))

        # Obsługa zdarzeń w menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", 0, 0  # Wyjście z programu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "exit", 0, 0  # Wyjście z programu
                elif event.key == pygame.K_CAPSLOCK:
                    active_input = "captured" if active_input == "orbiting" else "orbiting" if active_input is None or active_input == "captured" else None  # Przełączanie pól
                elif event.key == pygame.K_BACKSPACE and active_input:
                    if active_input == "orbiting":
                        input_orbiting = input_orbiting[:-1]  # Usuwanie znaku
                    elif active_input == "captured":
                        input_captured = input_captured[:-1]
                elif event.unicode.isdigit() and active_input:
                    if active_input == "orbiting":
                        input_orbiting += event.unicode  # Dodawanie cyfry
                    elif active_input == "captured":
                        input_captured += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if orbiting_input_rect.collidepoint(mouse_x, mouse_y):
                    active_input = "orbiting"  # Aktywacja pola orbitujących
                elif captured_input_rect.collidepoint(mouse_x, mouse_y):
                    active_input = "captured"  # Aktywacja pola przechwyconych
                elif start_rect.collidepoint(mouse_x, mouse_y) and input_orbiting.isdigit() and input_captured.isdigit():
                    fade_out(screen, screen.copy())  # Animacja zanikania
                    # Przejście do symulacji
                    return "menu", int(input_orbiting), int(input_captured)
                elif info_rect.collidepoint(mouse_x, mouse_y):
                    info_screen()  # Otwarcie ekranu informacji
                elif more_info_rect.collidepoint(mouse_x, mouse_y):
                    more_info_screen()  # Otwarcie ekranu szczegółów
                elif settings_rect.collidepoint(mouse_x, mouse_y):
                    settings_menu()  # Otwarcie menu ustawień
                else:
                    active_input = None  # Dezaktywacja pola

        pygame.display.flip()  # Aktualizacja ekranu

    return "menu", 0, 0  # Domyślny zwrot, jeśli pętla się przerwie

# Ekran informacyjny – wyświetla podstawowe informacje o symulacji
def info_screen():
    font = pygame.font.SysFont("monospace", 20)
    tiny_font = pygame.font.SysFont("monospace", 12)
    clock = pygame.time.Clock()

    # Lista parametrów i wyjaśnień (pominięto szczegóły)
    params = [
        ("Skala odległości", "Dlaczego 1 px = 1e9 km?", 
         "By ujarzmić bezmiar kosmosu na ekranie, 1 piksel równa się miliardowi kilometrów. To technika kompresji przestrzeni, która maluje orbity gwiazd w czytelnej formie."),
        ("Newton kontra Einstein", "Mechanika uproszczona", 
         "Symulacja stawia na Newtona dla płynności – OTW jest zbyt gęsta obliczeniowo. Włącz Q, by poczuć relatywistyczny oddech Einsteina, choć w uproszczeniu."),
        ("GM = 20000", "Serce grawitacji", 
         "Przeskalowana stała grawitacyjna – nie masa BH w kg, lecz liczba rzeźbiąca symulację. Jej wartość balansuje pikselowy świat z kosmiczną siłą."),
        ("Event Horizon", "√(GM) w akcji", 
         "Promień horyzontu zdarzeń rodzi się z √(GM) – uproszczona zależność, która oddaje potęgę masy i wyznacza granicę nieuchronnego końca."),
        ("Prędkość ucieczki", "v_esc = √(2GM/r)", 
         "Klucz do losu gwiazd – obliczana klasycznie, porównuje ruch gwiazdy z siłą czarnej dziury, decydując o jej upadku lub wolności."),
        ("OTW (klawisz Q)", "Taniec peryhelium", 
         "Włączenie OTW (Q) budzi relatywistyczną precesję – orbity wyginają się pod wpływem GM/r², łamiąc stabilność elips na rzecz kosmicznego chaosu.")
    ]

    explanations = [
        ("Siła grawitacji", "F = GM * m / r²", 
         "Prawo Newtona napędza symulację – przyspieszenie a = GM * r / r³ rzeźbi trajektorie, od stabilnych orbit po desperackie ucieczki."),
        ("Mechanika wchłaniania", "P = f(v, v_esc, r_v)", 
         "Prawdopodobieństwo upadku to taniec liczb – v gwiazdy, v_esc = √(2GM/r) i radialna składowa (r_v) decydują, czy czarna dziura pochłonie kolejny łup."),
        ("Czas orbity", "T = 2π √(a³/GM)", 
         "III prawo Keplera w pełnej krasie – okres T zależy od półośi wielkiej (a) i GM. SIMULATION_SPEED skaluje go dla oczu użytkownika."),
        ("Energia i moment", "E_k = ½mv², L = mvr", 
         "Klasyka mechaniki – energia kinetyczna i moment pędu obliczane w pikselowych jednostkach, odsłaniają dynamikę układu w J i kg·km²/s."),
        ("Uproszczenie OTW", "Newton na straży", 
         "OTW jest uśpiona dla wydajności – dylatacja czasu czy zakrzywienie światła ustępują prostocie. Q budzi ich cień w precesji orbit."),
        ("Skala czasu", "Lata świetlne w Sim Time", 
         "Czas symulowany płynie w latach świetlnych – TIME_SCALE przekłada pikselowe kroki na kosmiczną skalę, łącząc matematykę z epicką narracją.")
    ]

    problem_text = """Wybór maksymalnej gwiazdy i implementacja integratora Leapfrog

    Dla wyboru maksymalnej gwiazdy upewnię się, że tekst jest renderowany w określonej pozycji i sprawdzę, czy kliknięcie mieści się w jego granicach.

    W stats_box linie są wyświetlane na pozycji (10, 10 + i * 30), więc dla i=4, linia "Max Star" jest na y = 10 + 4*30 = 130, ale ponieważ stats_box jest blitted na (10, HEIGHT // 2 - 90), rzeczywista pozycja y to HEIGHT // 2 - 90 + 130.

    Chwila, policzmy to dokładnie.
    Stats_box ma wymiary 300x180 i jest blitted na (10, HEIGHT // 2 - 90), więc tekst "Max Star" jest na (10 + 10, HEIGHT // 2 - 90 + 10 + 4*30) = (20, HEIGHT // 2 + 40).
    Czyli jego y to HEIGHT // 2 + 40, a x od 20 do 20 + szerokość tekstu.
    Będę musiał zapisać prostokąt dla tekstu "Max Star" i sprawdzić, czy kliknięcie jest w jego wnętrzu.
    Podobnie dla suwaków – zapiszę ich prostokąty i obsłużę przeciąganie.

    ## Fizyka i integrator Leapfrog

    Teraz przejdę do fizyki – zaimplementuję integrator Leapfrog.
    W klasie Star obecna metoda aktualizacji używa integracji Eulera: vx += ax * dt, vy += ay * dt, x += vx * dt, y += vy * dt.
    W Leapfrogu wygląda to tak:
    - v_half = v + a * dt / 2
    - x_new = x + v_half * dt
    - Obliczam a_new w x_new
    - v_new = v_half + a_new * dt / 2

    Muszę więc obliczyć przyspieszenie dwa razy: raz na początku i raz po aktualizacji pozycji.
    W main_simulation:
    - accelerations = [star.compute_acceleration(stars) for star in stars]
    - for star, (ax, ay) in zip(stars, accelerations):
      - vx_half = star.vx + ax * dt / 2
      - vy_half = star.vy + ay * dt / 2
      - star.x += vx_half * dt
      - star.y += vy_half * dt
    - new_accelerations = [star.compute_acceleration(stars) for star in stars]
    - for star, (ax, ay), (ax_new, ay_new) in zip(stars, accelerations, new_accelerations):
      - star.vx += (ax + ax_new) * dt / 2
      - star.vy += (ay + ay_new) * dt / 2

    To powinno być lepsze niż Euler i zachowa stabilność symulacji.
    """

    problem_button_text = tiny_font.render("Przykład problemu", True, GREEN)
    problem_button_rect = problem_button_text.get_rect(
        center=(WIDTH // 2, HEIGHT - 100))
    show_problem = False
    typing_text = ""
    typing_index = 0
    typing_speed = 900
    scroll_offset = 0
    last_update = pygame.time.get_ticks()

    while True:
        screen.fill(BLACK)  # Czyszczenie ekranu
        title = font.render("Informacje o symulacji", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))  # Tytuł

        # Rysowanie parametrów i wyjaśnień (pominięto szczegóły renderowania)
        left_rect = Rect(50, 100, WIDTH // 2 - 100, HEIGHT - 200)
        for i, (name, value, desc) in enumerate(params):
            name_text = tiny_font.render(name, True, WHITE)
            value_text = tiny_font.render(value, True, GREEN)
            desc_surfaces, _ = render_textrect_with_scroll(tiny_font, desc, LIGHT_GRAY, Rect(
                0, 0, left_rect.width - name_text.get_width() - value_text.get_width() - 20, 100), 0)
            screen.blit(name_text, (left_rect.left, left_rect.top + i * 120))
            screen.blit(value_text, (left_rect.left +
                        name_text.get_width() + 10, left_rect.top + i * 120))
            for surface, pos in desc_surfaces:
                screen.blit(surface, (left_rect.left + name_text.get_width() +
                            value_text.get_width() + 20, left_rect.top + i * 120 + pos[1]))

        right_rect = Rect(WIDTH // 2 + 50, 100, WIDTH // 2 - 100, HEIGHT - 200)
        for i, (name, formula, desc) in enumerate(explanations):
            name_text = tiny_font.render(name, True, WHITE)
            formula_text = tiny_font.render(formula, True, GREEN)
            desc_surfaces, _ = render_textrect_with_scroll(tiny_font, desc, LIGHT_GRAY, Rect(
                0, 0, right_rect.width - name_text.get_width() - formula_text.get_width() - 20, 100), 0)
            screen.blit(name_text, (right_rect.left, right_rect.top + i * 120))
            screen.blit(formula_text, (right_rect.left +
                        name_text.get_width() + 10, right_rect.top + i * 120))
            for surface, pos in desc_surfaces:
                screen.blit(surface, (right_rect.left + name_text.get_width() +
                            formula_text.get_width() + 20, right_rect.top + i * 120 + pos[1]))

        screen.blit(problem_button_text, problem_button_rect.topleft)
        if problem_button_rect.collidepoint(pygame.mouse.get_pos()):
            # Podświetlenie przycisku problemu
            pygame.draw.rect(screen, LIGHT_GRAY, problem_button_rect, 2)

        if show_problem:
            # Wyświetlanie tekstu problemu z animacją pisania (pominięto szczegóły)
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(OVERLAY_COLOR)
            screen.blit(overlay, (0, 0))
            problem_box = pygame.Surface((WIDTH // 2, HEIGHT // 2))
            problem_box.fill(GRAY)
            problem_box.set_alpha(128)
            problem_rect = problem_box.get_rect(
                center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(problem_box, problem_rect.topleft)

            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 1000 // typing_speed and typing_index < len(problem_text):
                typing_text += problem_text[typing_index]
                typing_index += 1
                last_update = current_time
                if typing_index == len(problem_text):
                    scroll_offset = 0

            problem_surfaces, total_height = render_textrect_with_scroll(tiny_font, typing_text, WHITE, Rect(
                0, 0, problem_rect.width - 20, problem_rect.height - 20), scroll_offset)
            for surface, pos in problem_surfaces:
                screen.blit(surface, (problem_rect.left + 10,
                            problem_rect.top + 10 + pos[1]))

            if total_height > problem_rect.height and typing_index == len(problem_text):
                scroll_offset += 1
                if scroll_offset > total_height - problem_rect.height:
                    scroll_offset = 0

        # Przycisk powrotu
        return_button = font.render("Powrót", True, WHITE)
        return_rect = return_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if return_rect.collidepoint(mouse_x, mouse_y):
            return_button = font.render("Powrót", True, GREEN)
            pygame.draw.rect(screen, LIGHT_GRAY, return_rect, 2)
        screen.blit(return_button, return_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_problem = False if show_problem else True  # Przełączanie widoku problemu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_rect.collidepoint(event.pos):
                    return  # Powrót do menu
                elif problem_button_rect.collidepoint(event.pos):
                    show_problem = not show_problem
                    if show_problem:
                        typing_text = ""
                        typing_index = 0
                        scroll_offset = 0

        pygame.display.flip()
        clock.tick(60)

# Ekran szczegółowych informacji o symulacji
def more_info_screen():
    font = pygame.font.SysFont("monospace", 20)
    tiny_font = pygame.font.SysFont("monospace", 15)
    clock = pygame.time.Clock()

    # Lista szczegółowych informacji (pominięto szczegóły)
    detailed_info = [
    ("Parametry globalne", "",
     "Oto szczegółowy przegląd fundamentów symulacji – zasad rządzących kosmicznym chaosem:"),
    ("GM", f"GM = {GM}", 
     "Przeskalowana stała grawitacyjna, serce przyciągania czarnej dziury. Rzeźbi dynamikę orbit i pożeranie gwiazd. Reguluj G/H, by zgłębić jej moc."),
    ("SIMULATION_SPEED", f"Prędkość symulacji: {SIMULATION_SPEED}x",
     "Kontroler czasu – definiuje, jak szybko wszechświat pulsuje na ekranie. Przy 2.0 odzwierciedla obecne tempo, manipuluj strzałkami lewo/prawo, by zwolnić lub przyspieszyć kosmos."),
    ("TRAIL_LENGTH", f"Długość śladu: {TRAIL_LENGTH}",
     "Ślady gwiazd w pikselach – mapa ich podróży przez przestrzeń. Dostosuj T/Y, by śledzić ich taniec w szczegółach."),
    ("MAX_INITIAL_VELOCITY", f"Maksymalna początkowa prędkość: {MAX_INITIAL_VELOCITY}",
     "Początkowy impet przechwyconych gwiazd – nadaje im życie na starcie, określając ich los w grawitacyjnej grze."),
    ("PX_TO_KM", f"Skala pikseli: 1 px = {PX_TO_KM} km",
     "Kosmiczna miarka – każdy piksel to miliardy kilometrów, tłumacząc ogrom przestrzeni na ekranową opowieść."),
    ("C", f"Prędkość światła: {C} km/s",
     "Granica wszechświata – stała OTW, strażnik prędkości w opcjonalnych efektach relatywistycznych."),
    ("TIME_SCALE", f"Skala czasu: {TIME_SCALE}",
     "Most między symulacją a latami świetlnymi – przelicza pikselowe kroki w epickie odcinki czasu."),
    ("STAR_GM_FACTOR", f"Siła interakcji gwiazd: {STAR_GM_FACTOR}",
     "Grawitacyjne więzy między gwiazdami – gdy STAR_INTERACTION_ENABLED żyje, definiuje ich wzajemny taniec."),
    ("MAX_STAR_ACCEL", f"Maksymalne przyspieszenie gwiazd: {MAX_STAR_ACCEL}",
     "Tarcza stabilności – ogranicza szaleństwo przyspieszeń między gwiazdami, chroniąc symulację przed chaosem."),
    ("RELATIVITY_STRENGTH", f"Siła efektów OTW: {RELATIVITY_STRENGTH}",
     "Puls Einsteina – gdy RELATIVITY_ENABLED działa, wprowadza subtelne zakrzywienia czasoprzestrzeni."),
    ("FALLING_STARS_ENABLED/FALLING_STARS_PERCENTAGE",
     f"Spadanie gwiazd: {FALLING_STARS_PERCENTAGE}%", 
     "Wyrok czarnej dziury – definiuje, jak często gwiazdy wpadają w jej objęcia i z jakim prawdopodobieństwem."),
    ("EVENT_HORIZON_RADIUS", f"Promień horyzontu zdarzeń: {EVENT_HORIZON_RADIUS}",
     "Granica bez powrotu – zależna od GM, wyznacza strefę, gdzie gwiazdy znikają w otchłani."),
    ("CRITICAL_HIGHLIGHT_ENABLED", "Podświetlenie krytyczne",
     "Latarnia w mroku – wyróżnia gwiazdy na krawędzi zagłady, ułatwiając obserwację ich ostatnich chwil."),
    ("RELATIVITY_ENABLED/RELATIVITY_VISUALS_ENABLED", "Efekty OTW",
     "Szept Einsteina – aktywuje relatywistyczne zakrzywienia i wizualne echa, jak przesunięcie ku czerwieni."),
    ("STAR_INTERACTION_ENABLED", "Interakcje gwiazd",
     "Kosmos w ruchu – włącza grawitacyjne dialogi między gwiazdami, tworząc złożone układy N-ciał."),
    ("COLLISIONS_ENABLED", "Zderzenia gwiazd",
     "Kosmiczne kolizje – pozwala gwiazdom się łączyć, zmieniając masę i trajektorie w dramatycznych spotkaniach."),
    ("BLACK_HOLE_RADIUS", f"Rozmiar czarnej dziury: {BLACK_HOLE_RADIUS}",
     "Cień otchłani – wizualna skala czarnej dziury, regulowana B/N dla pełnego efektu."),
    ("camera_x, camera_y, camera_zoom", "Kamera",
     "Oko obserwatora – WASD i ,/. sterują widokiem, przybliżając lub oddalając kosmiczną scenę.")
]

    while True:
        screen.fill(BLACK)
        title = font.render("Szczegółowe informacje o symulacji", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        # Rysowanie informacji (pominięto szczegóły renderowania)
        content_rect = Rect(50, 100, WIDTH - 100, HEIGHT - 200)
        for i, (name, value, desc) in enumerate(detailed_info):
            name_text = tiny_font.render(name, True, WHITE)
            value_text = tiny_font.render(
                value, True, GREEN) if value else tiny_font.render("", True, WHITE)
            desc_surfaces, _ = render_textrect_with_scroll(tiny_font, desc, LIGHT_GRAY, Rect(
                0, 0, content_rect.width - name_text.get_width() - value_text.get_width() - 20, 100), 0)
            screen.blit(name_text, (content_rect.left,
                        content_rect.top + i * 40))
            screen.blit(value_text, (content_rect.left +
                        name_text.get_width() + 10, content_rect.top + i * 40))
            for surface, pos in desc_surfaces:
                screen.blit(surface, (content_rect.left + name_text.get_width() +
                            value_text.get_width() + 20, content_rect.top + i * 40 + pos[1]))

        # Przycisk powrotu
        return_button = font.render("Powrót", True, WHITE)
        return_rect = return_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if return_rect.collidepoint(mouse_x, mouse_y):
            return_button = font.render("Powrót", True, GREEN)
            pygame.draw.rect(screen, LIGHT_GRAY, return_rect, 2)
        screen.blit(return_button, return_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_rect.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(60)

# Określanie stanu gwiazdy względem horyzontu zdarzeń
def get_star_state(star):
    distance_to_bh = math.hypot(
        star.x - WIDTH / 2, star.y - HEIGHT / 2)  # Odległość od BH
    radial_velocity = (star.vx * (star.x - WIDTH / 2) + star.vy * (star.y - HEIGHT / 2)
                       ) / distance_to_bh if distance_to_bh > 0 else 0  # Prędkość radialna
    critical_inner = EVENT_HORIZON_RADIUS  # Wewnętrzna granica krytyczna
    critical_outer = EVENT_HORIZON_RADIUS + 10  # Zewnętrzna granica krytyczna
    if distance_to_bh <= critical_inner:
        return "inside"  # Wewnątrz horyzontu
    elif critical_inner < distance_to_bh <= critical_outer:
        if radial_velocity < 0:
            return "approaching"  # Zbliżanie się
        elif radial_velocity > 0:
            return "exiting"  # Oddalanie się
    return None  # Poza strefą krytyczną

# Funkcja loading_screen (wklejam ją bez zmian, zakładam, że działa)
def loading_screen(screen):
    WIDTH, HEIGHT = screen.get_size()
    font_large = pygame.font.SysFont("monospace", 48, bold=True)
    font_small = pygame.font.SysFont("monospace", 16)
    message_font = pygame.font.SysFont("monospace", 14)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    GREEN = (0, 255, 0)

    quote = "Black holes are where God divided by zero."
    quote_author = "- Albert Einstein"
    quote_text = font_large.render(quote, True, WHITE)
    author_text = font_small.render(quote_author, True, GRAY)
    quote_rect = quote_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    author_rect = author_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    bar_width = 400
    bar_height = 10
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 100
    loading_progress = 0
    loading_speed = 50
    total_steps = 6
    progress_per_step = 100 / total_steps

    loading_messages = [
        ("Generowanie świata", 1.0),
        ("Przywracanie Stephena Hawkinga do życia", 2.0),
        ("Aplikowanie newtonowskich praw", 1.0),
        ("Obliczanie trajektorii orbit", 1.0),
        ("Sprowadzanie Einsteina na konsultacje", 2.0),
        ("Generowanie gwiazd na gotowo", 1.3)
    ]
    message_base_y = bar_y + bar_height + 20
    message_x = WIDTH // 2
    message_display_time = 1.5
    current_message_idx = 0
    message_timer = 0
    dot_timer = 0
    dot_cycle = 0
    dot_speed = 0.3
    dot_offset = 5

    prev_message_y = message_base_y
    prev_message_alpha = 0
    prev_message_text = None
    current_message_y = message_base_y + 20
    roll_speed = 40
    fade_out_speed = 255 / 0.5

    pause_timer = 0
    is_paused = False
    current_pause_time = loading_messages[0][1]

    alpha = 0
    fade_in_speed = 255 / 2
    clock = pygame.time.Clock()
    start_time = time.time()

    running = True
    finished_loading = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected, exiting")
                return False

        dt = clock.get_time() / 1000
        elapsed_time = time.time() - start_time

        if alpha < 255:
            alpha = min(255, alpha + fade_in_speed * dt)
            quote_text.set_alpha(int(alpha))
            author_text.set_alpha(int(alpha))

        message_timer += dt
        if message_timer >= message_display_time and current_message_idx < len(loading_messages):
            if current_message_idx > 0:
                prev_message_text = loading_messages[current_message_idx - 1][0]
                prev_message_y = message_base_y
                prev_message_alpha = 255
            current_message_y = message_base_y + 20
            current_message_idx += 1
            message_timer = 0
            is_paused = False
            if current_message_idx < len(loading_messages):
                current_pause_time = loading_messages[current_message_idx][1]
            print(f"Message {current_message_idx}: {loading_messages[min(current_message_idx, len(loading_messages)-1)][0]}")

        # Pasek ładowania
        target_progress = progress_per_step * (current_message_idx + 1 if current_message_idx < len(loading_messages) else total_steps)
        if current_message_idx < len(loading_messages):
            if not is_paused and loading_progress < target_progress:
                loading_progress = min(target_progress, loading_progress + loading_speed * dt)
            elif loading_progress >= target_progress:
                is_paused = True
                pause_timer = 0
        else:
            if loading_progress < 100:
                loading_progress = min(100, loading_progress + loading_speed * dt)
            if loading_progress >= 100:
                finished_loading = True
                print(f"Progress reached {loading_progress}%, triggering fade out")

        if is_paused:
            pause_timer += dt
            if pause_timer >= current_pause_time:
                is_paused = False

        dot_timer += dt
        if dot_timer >= dot_speed:
            dot_timer = 0
            dot_cycle = (dot_cycle + 1) % 3
        dots = "." * (dot_cycle + 1)

        if prev_message_alpha > 0:
            prev_message_y -= roll_speed * dt
            prev_message_alpha = max(0, prev_message_alpha - fade_out_speed * dt)
        if current_message_idx < len(loading_messages) and current_message_y > message_base_y:
            current_message_y = max(message_base_y, current_message_y - roll_speed * dt)

        message_texts = []
        if prev_message_text and prev_message_alpha > 0:
            prev_text = message_font.render(prev_message_text, True, WHITE)
            prev_text.set_alpha(int(prev_message_alpha))
            prev_dots = message_font.render("...", True, WHITE)
            prev_dots.set_alpha(int(prev_message_alpha))
            prev_text_rect = prev_text.get_rect(center=(message_x, prev_message_y))
            message_texts.append((prev_text, (message_x, prev_message_y)))
            message_texts.append((prev_dots, (prev_text_rect.right + dot_offset, prev_message_y)))

        if current_message_idx < len(loading_messages):
            current_text = message_font.render(loading_messages[current_message_idx][0], True, WHITE)
            current_dots = message_font.render(dots, True, WHITE)
            current_text_rect = current_text.get_rect(center=(message_x, current_message_y))
            message_texts.append((current_text, (message_x, current_message_y)))
            message_texts.append((current_dots, (current_text_rect.right + dot_offset, current_message_y)))

        screen.fill(BLACK)
        screen.blit(quote_text, quote_rect)
        screen.blit(author_text, author_rect)

        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
        filled_width = (bar_width - 4) * (loading_progress / 100)
        pygame.draw.rect(screen, GREEN, (bar_x + 2, bar_y + 2, filled_width, bar_height - 4))

        for text, pos in message_texts:
            screen.blit(text, text.get_rect(center=pos))

        pygame.display.flip()
        clock.tick(60)

        if finished_loading:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            for alpha in range(0, 255, 10):
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                clock.tick(60)
            print("Fade out completed")
            running = False

    print("Loading screen finished, returning True")
    return True

# Główna funkcja symulacji – obsługuje fizykę i renderowanie
def main_simulation():
    global GM, STRONG_FIELD_RADIUS, EVENT_HORIZON_RADIUS, isometric_view, to_remove, stars, simulated_time, selected_star_idx, absorbed_stars, camera_x, camera_y, camera_zoom, elapsed_time, SIMULATION_SPEED, TRAIL_LENGTH, BLACK_HOLE_RADIUS, FALLING_STARS_ENABLED, FALLING_STARS_PERCENTAGE, STAR_GM_FACTOR, RELATIVITY_STRENGTH, RELATIVITY_ENABLED, RELATIVITY_VISUALS_ENABLED, STAR_INTERACTION_ENABLED, COLLISIONS_ENABLED, prediction_length, CRITICAL_HIGHLIGHT_ENABLED, NUM_ORBITING, NUM_CAPTURED, ORBITS_ENABLED, dragging_star
    print("Entering main_simulation")
    try:
        zoom_out_animation(screen, stars)
    except Exception as e:
        print(f"Error in zoom_out_animation: {e}")
        return "exit"

    G = 6.67430e-11
    dragging_slider = None
    star_clicked = None
    clock = pygame.time.Clock()
    to_remove = []
    font = pygame.font.SysFont("monospace", 12)
    running = True
    pause_simulation = False
    show_interface = False
    show_stats = False
    show_experimental = False
    realism_mode = False
    show_orbits = False
    simulated_time = 0
    elapsed_time = 0
    selected_star_idx = 0 if stars else None
    absorbed_stars = 0
    trail_editable_length = TRAIL_LENGTH
    black_hole_radius = BLACK_HOLE_RADIUS
    strong_field_radius = EVENT_HORIZON_RADIUS + 50
    MAX_HIGHLIGHTED_STARS = 5
    critical_stars = []
    tracking_max_star = False
    tracking_star = None
    used_names = set(star.name for star in stars)
    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    copyright_text = font.render("copyright by Magik 2025 Optimized by GROK", True, WHITE)
    COPYRIGHT_POS = (WIDTH // 2 - copyright_text.get_width() // 2, HEIGHT - 20)
    trail_update_interval = 5
    trail_counter = 0
    orbits_text = font.render(f"Orbits: {'On' if ORBITS_ENABLED else 'Off'}", True, WHITE)
    orbits_rect = orbits_text.get_rect(topleft=(10, 10))
    isometric_view = False
    orbit_point_counter = 0

    def set_realism_mode():
        global GM, SIMULATION_SPEED, trail_editable_length, black_hole_radius, FALLING_STARS_PERCENTAGE, STAR_GM_FACTOR, RELATIVITY_STRENGTH, GRAVITY_FALLOFF
        GM = 20000
        SIMULATION_SPEED = 0.5
        trail_editable_length = 100
        black_hole_radius = 5
        FALLING_STARS_PERCENTAGE = 10
        STAR_GM_FACTOR = 0.0005
        RELATIVITY_STRENGTH = 0.0002
        GRAVITY_FALLOFF = 2.0
        sliders["GM"]["value"] = GM
        sliders["Sim Speed"]["value"] = SIMULATION_SPEED
        sliders["Trail Length"]["value"] = trail_editable_length
        sliders["BH Radius"]["value"] = black_hole_radius
        sliders["Fall Chance"]["value"] = FALLING_STARS_PERCENTAGE
        sliders["Star Interaction"]["value"] = STAR_GM_FACTOR
        sliders["Relativity Str"]["value"] = RELATIVITY_STRENGTH

    def distance_to_black_hole(star):
        return math.hypot(star.x - WIDTH / 2, star.y - HEIGHT / 2)

    while running:
        try:
            dt = clock.tick(60) / 1000.0
            elapsed_time += dt
            EVENT_HORIZON_RADIUS = int(math.sqrt(GM) * 0.5)
            global STRONG_FIELD_RADIUS

            sliders = {
                "GM": {"min": 1000, "max": 200000, "value": GM, "rect": None},
                "Sim Speed": {"min": 0.1, "max": 100.0, "value": SIMULATION_SPEED, "rect": None},
                "Trail Length": {"min": 1, "max": 1000, "value": trail_editable_length, "rect": None},
                "BH Radius": {"min": 5, "max": 90, "value": black_hole_radius, "rect": None},
                "Fall Chance": {"min": 0, "max": 100, "value": FALLING_STARS_PERCENTAGE, "rect": None},
                "Star Interaction": {"min": 0.0, "max": 10.0, "value": STAR_GM_FACTOR, "rect": None},
                "Prediction Len": {"min": 10, "max": 500, "value": prediction_length, "rect": None},
                "Relativity Str": {"min": 0.0, "max": 0.1, "value": RELATIVITY_STRENGTH, "rect": None},
                "Disk Radius": {"min": 10, "max": 500, "value": STRONG_FIELD_RADIUS, "rect": None},
            }

            if show_experimental:
                num_sliders = len(sliders)
                exp_box_height = 50 + num_sliders * 40
                exp_box = pygame.Surface((300, exp_box_height))
                exp_box.fill(GRAY)
                exp_box.set_alpha(200)
                exp_rect = exp_box.get_rect(topright=(WIDTH - 10, 380))
                screen.blit(exp_box, exp_rect.topleft)
                for i, (key, slider) in enumerate(sliders.items()):
                    label_y = exp_rect.top + 10 + i * 40
                    label = font.render(
                        f"{key}: {slider['value']:.3f}" if key in ["Sim Speed", "Star Interaction", "Relativity Str"] 
                        else f"{key}: {int(slider['value'])}", True, WHITE)
                    screen.blit(label, (exp_rect.left + 10, label_y))
                    slider_rect = pygame.Rect(exp_rect.left + 10, exp_rect.top + 25 + i * 40, 280, 10)
                    slider["rect"] = slider_rect
                    pygame.draw.rect(screen, LIGHT_GRAY, slider_rect)
                    slider_pos = slider_rect.left + (slider["value"] - slider["min"]) / (slider["max"] - slider["min"]) * slider_rect.width
                    green_rect = pygame.Rect(int(slider_pos) - 5, slider_rect.top - 2, 10, 14)
                    pygame.draw.rect(screen, GREEN, green_rect)

            sim_speed_text = font.render(f"Sim Speed: {SIMULATION_SPEED:.1f}x", True, WHITE)
            trail_text = font.render(f"Trail Length: {trail_editable_length}", True, WHITE)
            stars_text = font.render(f"Stars: {NUM_ORBITING} orb, {NUM_CAPTURED} cap", True, WHITE)
            star_interaction_text = font.render(f"Star Interaction: {'On' if STAR_INTERACTION_ENABLED else 'Off'}", True, RED if STAR_INTERACTION_ENABLED else WHITE)
            pause_text = font.render("Pause/Unpause", True, WHITE)
            restart_text = font.render("Restart", True, WHITE)
            gm_text = font.render(f"GM: {GM}", True, WHITE)
            bh_radius_text = font.render(f"BH Radius: {black_hole_radius}", True, WHITE)
            falling_enabled_text = font.render(f"Falling Stars: {'On' if FALLING_STARS_ENABLED else 'Off'}", True, RED if FALLING_STARS_ENABLED else WHITE)
            falling_percent_text = font.render(f"Fall Chance: {FALLING_STARS_PERCENTAGE}%", True, WHITE)
            critical_highlight_text = font.render(f"Highlight Critical: {'On' if CRITICAL_HIGHLIGHT_ENABLED else 'Off'}", True, RED if CRITICAL_HIGHLIGHT_ENABLED else WHITE)
            relativity_text = font.render(f"Relativity: {'On' if RELATIVITY_ENABLED else 'Off'}", True, RED if RELATIVITY_ENABLED else WHITE)
            relativity_visuals_text = font.render(f"Relativity Visuals: {'On' if RELATIVITY_VISUALS_ENABLED else 'Off'}", True, RED if RELATIVITY_VISUALS_ENABLED else WHITE)
            collisions_text = font.render(f"Collisions: {'On' if COLLISIONS_ENABLED else 'Off'}", True, RED if COLLISIONS_ENABLED else WHITE)
            realism_text = font.render(f"Realism: {'On' if realism_mode else 'Off'}", True, WHITE)
            exit_to_menu_text = font.render("Back to Menu", True, RED)

            pause_rect = pygame.Rect(0, 0, 0, 0)
            restart_rect = pygame.Rect(0, 0, 0, 0)
            gm_rect = pygame.Rect(0, 0, 0, 0)
            bh_radius_rect = pygame.Rect(0, 0, 0, 0)
            falling_enabled_rect = pygame.Rect(0, 0, 0, 0)
            falling_percent_rect = pygame.Rect(0, 0, 0, 0)
            critical_highlight_rect = pygame.Rect(0, 0, 0, 0)
            relativity_rect = pygame.Rect(0, 0, 0, 0)
            relativity_visuals_rect = pygame.Rect(0, 0, 0, 0)
            star_interaction_rect = pygame.Rect(0, 0, 0, 0)
            collisions_rect = pygame.Rect(0, 0, 0, 0)
            realism_rect = pygame.Rect(0, 0, 0, 0)
            exit_to_menu_rect = pygame.Rect(0, 0, 0, 0)

            if show_interface:
                screen.blit(orbits_text, orbits_rect.topleft)
                orbits_color = GREEN if ORBITS_ENABLED else RED
                orbits_text = font.render(f"Orbits: {'On' if ORBITS_ENABLED else 'Off'}", True, orbits_color)
                orbits_rect = orbits_text.get_rect(topleft=(10, next_y_position))
                screen.blit(orbits_text, orbits_rect.topleft)

                star_interaction_rect = star_interaction_text.get_rect(topright=(WIDTH - 10, 70))
                pause_rect = pause_text.get_rect(topright=(WIDTH - 10, 110))
                restart_rect = restart_text.get_rect(topright=(WIDTH - 10, 130))
                gm_rect = gm_text.get_rect(topright=(WIDTH - 10, 150))
                bh_radius_rect = bh_radius_text.get_rect(topright=(WIDTH - 10, 170))
                falling_enabled_rect = falling_enabled_text.get_rect(topright=(WIDTH - 10, 190))
                falling_percent_rect = falling_percent_text.get_rect(topright=(WIDTH - 10, 210))
                critical_highlight_rect = critical_highlight_text.get_rect(topright=(WIDTH - 10, 230))
                relativity_rect = relativity_text.get_rect(topright=(WIDTH - 10, 250))
                relativity_visuals_rect = relativity_visuals_text.get_rect(topright=(WIDTH - 10, 270))
                collisions_rect = collisions_text.get_rect(topright=(WIDTH - 10, 290))
                realism_rect = realism_text.get_rect(topright=(WIDTH - 10, 310))
                exit_to_menu_rect = exit_to_menu_text.get_rect(topright=(WIDTH - 10, 330))

            if not pause_simulation:
                global exited_stars, replace_exited_stars
                exited_stars = 0
                replace_exited_stars = True

                num_steps = max(1, int(dt * (SIMULATION_SPEED * 0.125) / dt_phys))  # Skalowanie o 0.25
                trail_counter += 1
                for _ in range(num_steps):
                    accelerations = []
                    for star in stars:
                        ax, ay, az = 0.0, 0.0, 0.0
                        # Wpływ czarnej dziury
                        dx = WIDTH / 2 - star.x
                        dy = HEIGHT / 2 - star.y
                        r = math.hypot(dx, dy)
                        if r > 0:
                            force = GM / (r ** GRAVITY_FALLOFF)
                            ax += force * dx / r
                            ay += force * dy / r

                        # Wpływ innych gwiazd (N-ciał)
                        if STAR_INTERACTION_ENABLED:
                            for other in stars:
                                if other != star:
                                    dx = other.x - star.x
                                    dy = other.y - star.y
                                    r = math.hypot(dx, dy)
                                    if r > 0:
                                        force = (G * star.mass * other.mass * STAR_GM_FACTOR) / (r ** GRAVITY_FALLOFF)
                                        ax += force * dx / r / star.mass
                                        ay += force * dy / r / star.mass
                        accelerations.append((ax, ay, az))

                    # Aktualizacja pozycji i prędkości
                    for star, (ax, ay, az) in zip(stars, accelerations):
                        star.vx += ax * dt_phys
                        star.vy += ay * dt_phys
                        if hasattr(star, 'vz'):
                            star.vz += az * dt_phys
                            star.z += star.vz * dt_phys
                        star.x += star.vx * dt_phys
                        star.y += star.vy * dt_phys

                        # Losowy impuls dla dynamiki
                        if random.random() < 0.01:
                            impulse = random.uniform(-0.1, 0.1)
                            star.vx += impulse
                            star.vy += impulse

                        if ORBITS_ENABLED and trail_counter % 5 == 0:  # Wracam do co 5 kroków
                            star.trail.append((star.x, star.y))
                            if len(star.trail) > trail_editable_length:
                                star.trail.pop(0)
                            point = (star.x, star.y, star.z) if hasattr(star, 'z') else (star.x, star.y)
                            star.current_orbit_points.append(point)

                            # Logika dla gwiazd orbitujących (na podstawie odległości)
                            if not star.captured:
                                current_distance = math.hypot(star.x - WIDTH / 2, star.y - HEIGHT / 2)
                                if star.previous_distance is not None:
                                    if current_distance < star.previous_distance:
                                        star.is_approaching = True
                                    elif current_distance > star.previous_distance and star.is_approaching:
                                        star.is_approaching = False
                                        star.orbits_completed = getattr(star, 'orbits_completed', 0) + 1
                                        if star.current_orbit_points:
                                            star.last_orbit_points = list(star.current_orbit_points)
                                            star.current_orbit_points = []
                                star.previous_distance = current_distance

                        # Logika dla gwiazd przechwyconych (na podstawie kąta)
                        dx = star.x - WIDTH / 2
                        dy = star.y - HEIGHT / 2
                        current_angle = math.atan2(dy, dx)
                        if star.last_angle is not None:
                            angle_diff = (current_angle - star.last_angle) % (2 * math.pi)
                            if angle_diff > math.pi:
                                angle_diff -= 2 * math.pi
                            elif angle_diff < -math.pi:
                                angle_diff += 2 * math.pi
                            if star.captured:
                                star.total_angle += angle_diff
                                if abs(star.total_angle) >= 2 * math.pi:
                                    star.orbit_count = getattr(star, 'orbit_count', 0) + 1
                                    if star.current_orbit_points:
                                        star.last_orbit_points = list(star.current_orbit_points)
                                        star.current_orbit_points = []
                                    star.total_angle = 0.0
                        star.last_angle = current_angle

                        # Precesja i perturbacje tylko dla orbitujących
                        if not star.captured and STAR_INTERACTION_ENABLED:
                            if random.random() < 0.005:
                                angle_shift = random.uniform(-0.01, 0.01)
                                star.vx += math.cos(angle_shift) * 0.1
                                star.vy += math.sin(angle_shift) * 0.1

                        if realism_mode:
                            if hasattr(star, 'vz'):
                                v_total_km_s = math.sqrt(star.vx**2 + star.vy**2 + star.vz**2) * PX_TO_KM
                            else:
                                v_total_km_s = math.sqrt(star.vx**2 + star.vy**2) * PX_TO_KM
                            if v_total_km_s > C:
                                scale = C / v_total_km_s
                                star.vx *= scale / PX_TO_KM
                                star.vy *= scale / PX_TO_KM
                                if hasattr(star, 'vz'):
                                    star.vz *= scale / PX_TO_KM
                    simulated_time += dt_phys * TIME_SCALE
                if trail_counter >= trail_update_interval:
                    trail_counter = 0

            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    tracking_star = None
                    if event.key == pygame.K_ESCAPE:
                        return "exit"
                    elif event.key == pygame.K_p:
                        pause_simulation = not pause_simulation
                        tracking_max_star = False
                    elif event.key == pygame.K_r:
                        reset_simulation(used_names)
                        critical_stars.clear()
                        tracking_max_star = False
                    elif event.key == pygame.K_l:
                        realism_mode = not realism_mode
                        if realism_mode:
                            set_realism_mode()
                        tracking_max_star = False
                    elif event.key == pygame.K_i:
                        show_interface = not show_interface
                        tracking_max_star = False
                    elif event.key == pygame.K_q:
                        RELATIVITY_ENABLED = not RELATIVITY_ENABLED
                        tracking_max_star = False
                    elif event.key == pygame.K_f:
                        show_stats = not show_stats
                        tracking_max_star = False
                    elif event.key == pygame.K_e:
                        show_experimental = not show_experimental
                        tracking_max_star = False
                    elif event.key == pygame.K_c:
                        COLLISIONS_ENABLED = not COLLISIONS_ENABLED
                        tracking_max_star = False
                    elif event.key == pygame.K_v:
                        isometric_view = not isometric_view
                        tracking_max_star = False
                    elif event.key == pygame.K_KP_PLUS:
                        stars.append(Star(captured=(new_star_type == "captured"), used_names=used_names))
                        if new_star_type == "orbiting":
                            NUM_ORBITING += 1
                        else:
                            NUM_CAPTURED += 1
                        tracking_max_star = False
                    elif event.key == pygame.K_KP_MINUS and NUM_ORBITING > 0:
                        for i, star in enumerate(stars):
                            if not star.captured:
                                if any(s == star for s, _, _ in critical_stars):
                                    critical_stars.remove(next((s, st, t) for s, st, t in critical_stars if s == star))
                                stars.pop(i)
                                NUM_ORBITING -= 1
                                if selected_star_idx is not None and selected_star_idx >= len(stars):
                                    selected_star_idx = len(stars) - 1 if len(stars) > 0 else None
                                break
                        tracking_max_star = False
                    elif event.key == pygame.K_LEFT:
                        SIMULATION_SPEED = max(0.1, SIMULATION_SPEED - 0.1)
                        tracking_max_star = False
                    elif event.key == pygame.K_RIGHT:
                        SIMULATION_SPEED = min(100.0, SIMULATION_SPEED + 0.1)
                        tracking_max_star = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    ui_clicked = False
                    if orbits_rect.collidepoint(mouse_x, mouse_y):
                        ORBITS_ENABLED = not ORBITS_ENABLED
                        ui_clicked = True
                    if show_stats and stars:
                        max_star = max(stars, key=lambda s: s.mass, default=None)
                        orbiting_stars = [star for star in stars if not star.captured]
                        highest_orbit_star = max(orbiting_stars, key=lambda s: s.a, default=None) if orbiting_stars else None
                        lowest_orbit_star = min(orbiting_stars, key=lambda s: s.a, default=None) if orbiting_stars else None
                        stats_box_rect = pygame.Rect(10, HEIGHT // 2 - 150, 300, 300)
                        if stats_box_rect.collidepoint(mouse_x, mouse_y):
                            for i, line in enumerate(stats_lines):
                                if i in [6, 7, 8]:
                                    rect = pygame.Rect(stats_box_rect.left + 10, stats_box_rect.top + 10 + i * 30, font.size(line)[0], font.get_height())
                                    if rect.collidepoint(mouse_x, mouse_y):
                                        if i == 6 and max_star:
                                            selected_star_idx = stars.index(max_star)
                                            for star in stars:
                                                star.selected = (star == max_star)
                                            camera_x = max_star.x
                                            camera_y = max_star.y
                                            clamp_camera()
                                            tracking_star = max_star
                                            ui_clicked = True
                                        elif i == 7 and highest_orbit_star:
                                            selected_star_idx = stars.index(highest_orbit_star)
                                            for star in stars:
                                                star.selected = (star == highest_orbit_star)
                                            tracking_star = highest_orbit_star
                                            ui_clicked = True
                                        elif i == 8 and lowest_orbit_star:
                                            selected_star_idx = stars.index(lowest_orbit_star)
                                            for star in stars:
                                                star.selected = (star == lowest_orbit_star)
                                            tracking_star = lowest_orbit_star
                                            ui_clicked = True
                    if not ui_clicked and show_experimental:
                        for key, slider in sliders.items():
                            if slider["rect"] and slider["rect"].collidepoint(mouse_x, mouse_y):
                                dragging_slider = key
                                ui_clicked = True
                                break
                    if not ui_clicked and show_interface:
                        if pause_rect.collidepoint(mouse_x, mouse_y):
                            pause_simulation = not pause_simulation
                            ui_clicked = True
                        elif restart_rect.collidepoint(mouse_x, mouse_y):
                            reset_simulation(used_names)
                            critical_stars.clear()
                            tracking_max_star = False
                            ui_clicked = True
                        elif realism_rect.collidepoint(mouse_x, mouse_y):
                            realism_mode = not realism_mode
                            if realism_mode:
                                set_realism_mode()
                            ui_clicked = True
                        elif exit_to_menu_rect.collidepoint(mouse_x, mouse_y):
                            fade_out(screen, screen.copy())
                            return "menu"
                        elif falling_enabled_rect.collidepoint(mouse_x, mouse_y):
                            FALLING_STARS_ENABLED = not FALLING_STARS_ENABLED
                            ui_clicked = True
                        elif falling_percent_rect.collidepoint(mouse_x, mouse_y):
                            FALLING_STARS_PERCENTAGE = min(100, FALLING_STARS_PERCENTAGE + 5) if FALLING_STARS_PERCENTAGE < 100 else 0
                            ui_clicked = True
                        elif critical_highlight_rect.collidepoint(mouse_x, mouse_y):
                            CRITICAL_HIGHLIGHT_ENABLED = not CRITICAL_HIGHLIGHT_ENABLED
                            if not CRITICAL_HIGHLIGHT_ENABLED:
                                critical_stars.clear()
                            ui_clicked = True
                        elif relativity_rect.collidepoint(mouse_x, mouse_y):
                            RELATIVITY_ENABLED = not RELATIVITY_ENABLED
                            ui_clicked = True
                        elif relativity_visuals_rect.collidepoint(mouse_x, mouse_y):
                            RELATIVITY_VISUALS_ENABLED = not RELATIVITY_VISUALS_ENABLED
                            ui_clicked = True
                        elif star_interaction_rect.collidepoint(mouse_x, mouse_y):
                            STAR_INTERACTION_ENABLED = not STAR_INTERACTION_ENABLED
                            ui_clicked = True
                        elif collisions_rect.collidepoint(mouse_x, mouse_y):
                            COLLISIONS_ENABLED = not COLLISIONS_ENABLED
                            ui_clicked = True
                        elif selected_star_idx is not None and stars and 0 <= selected_star_idx < len(stars):
                            selected_star = stars[selected_star_idx]
                            if show_orbit_rect.collidepoint(mouse_x, mouse_y):  # Używamy wcześniej ustawionego show_orbit_rect
                                show_orbits = not show_orbits
                                ui_clicked = True
                    if not ui_clicked and stars and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        min_distance = float('inf')
                        for i, star in enumerate(stars):
                            if isometric_view:
                                iso_x = (star.x - camera_x) * camera_zoom + WIDTH // 2 + (star.z * 0.5) * camera_zoom
                                iso_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2 - (star.z * 0.5) * camera_zoom
                                distance = math.hypot(iso_x - mouse_x, iso_y - mouse_y)
                            else:
                                screen_x = (star.x - camera_x) * camera_zoom + WIDTH // 2
                                screen_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2
                                distance = math.hypot(screen_x - mouse_x, screen_y - mouse_y)
                            if distance < 15 and distance < min_distance:
                                min_distance = distance
                                selected_star_idx = i
                                for s in stars:
                                    s.selected = (s == star)
                                ui_clicked = True
                        if not ui_clicked:
                            for star in stars:
                                if not any(s == star for s, _, _ in critical_stars):
                                    star.selected = False
                            tracking_max_star = False
                    elif not ui_clicked and stars and event.button == 3:
                        mouse_x, mouse_y = event.pos
                        for i, star in enumerate(stars):
                            screen_x = (star.x - camera_x) * camera_zoom + WIDTH // 2
                            screen_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2
                            if math.hypot(screen_x - mouse_x, screen_y - mouse_y) < 15:
                                dragging_star = star
                                selected_star_idx = i
                                for s in stars:
                                    s.selected = (s == star)
                                ui_clicked = True
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging_star = None
                    dragging_slider = None
                elif event.type == pygame.MOUSEMOTION:
                    if dragging_star:
                        mouse_x, mouse_y = event.pos
                        dragging_star.x = mouse_x + camera_x - WIDTH // 2
                        dragging_star.y = mouse_y + camera_y - HEIGHT // 2
                        dragging_star.vx = 0
                        dragging_star.vy = 0
                    if dragging_slider is not None:
                        mx, _ = event.pos
                        slider = sliders[dragging_slider]
                        slider["value"] = slider["min"] + (slider["max"] - slider["min"]) * (mx - slider["rect"].left) / slider["rect"].width
                        slider["value"] = max(slider["min"], min(slider["max"], slider["value"]))
                        if dragging_slider == "GM":
                            GM = int(slider["value"])
                            EVENT_HORIZON_RADIUS = int(math.sqrt(GM) * 0.5)
                        elif dragging_slider == "Sim Speed":
                            SIMULATION_SPEED = slider["value"]
                        elif dragging_slider == "Trail Length":
                            trail_editable_length = int(slider["value"])
                            for star in stars:
                                while len(star.trail) > trail_editable_length:
                                    star.trail.pop(0)
                        elif dragging_slider == "BH Radius":
                            black_hole_radius = int(slider["value"])
                        elif dragging_slider == "Fall Chance":
                            FALLING_STARS_PERCENTAGE = int(slider["value"])
                        elif dragging_slider == "Star Interaction":
                            STAR_GM_FACTOR = slider["value"]
                        elif dragging_slider == "Prediction Len":
                            prediction_length = int(slider["value"])
                        elif dragging_slider == "Relativity Str":
                            RELATIVITY_STRENGTH = slider["value"]
                        elif dragging_slider == "Disk Radius":
                            STRONG_FIELD_RADIUS = int(slider["value"])
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        camera_zoom = min(MAX_ZOOM, camera_zoom + 0.05)
                    elif event.y < 0:
                        camera_zoom = max(MIN_ZOOM, camera_zoom - 0.05)

            if not pause_simulation:
                if CRITICAL_HIGHLIGHT_ENABLED:
                    updated_critical_stars = []
                    for star, state, timer in critical_stars:
                        new_state = get_star_state(star)
                        if new_state:
                            star.critical = True
                            updated_critical_stars.append((star, new_state, None))
                        elif state == "exiting" and new_state is None:
                            star.critical = False
                            updated_critical_stars.append((star, "post_exit", 1.0))
                        elif state == "post_exit" and timer > 0:
                            star.critical = False
                            updated_critical_stars.append((star, "post_exit", timer - dt))
                    critical_stars = [(star, state, timer) for star, state, timer in updated_critical_stars if state != "post_exit" or timer > 0]
                    for star in stars:
                        if not any(s == star for s, _, _ in critical_stars):
                            state = get_star_state(star)
                            if state and len(critical_stars) < MAX_HIGHLIGHTED_STARS:
                                star.critical = True
                                critical_stars.append((star, state, None))
                            else:
                                star.critical = False

                if COLLISIONS_ENABLED and STAR_INTERACTION_ENABLED:
                    to_remove = []
                    for i in range(len(stars) - 1):
                        for j in range(i + 1, len(stars)):
                            dx = stars[j].x - stars[i].x
                            dy = stars[j].y - stars[i].y
                            distance = math.hypot(dx, dy)
                            if distance < (stars[i].size + stars[j].size) * 0.5:
                                total_mass = stars[i].mass + stars[j].mass
                                new_vx = (stars[i].vx * stars[i].mass + stars[j].vx * stars[j].mass) / total_mass
                                new_vy = (stars[i].vy * stars[i].mass + stars[j].vy * stars[j].mass) / total_mass
                                stars[i].mass = total_mass
                                stars[i].size = min(15, stars[i].size + stars[j].size * 0.5)
                                stars[i].vx = new_vx
                                stars[i].vy = new_vy
                                to_remove.append(j)
                    for idx in sorted(to_remove, reverse=True):
                        if stars[idx] == tracking_star:
                            tracking_star = None
                        stars.pop(idx)
                        if stars[idx].captured:
                            NUM_CAPTURED -= 1
                        else:
                            NUM_ORBITING -= 1
                    if selected_star_idx is not None and (selected_star_idx >= len(stars) or not stars):
                        selected_star_idx = None

                to_replace = []
                to_remove = []
                for i, star in enumerate(stars):
                    if check_star_bounds(star):
                        to_replace.append((i, star.captured))
                    if FALLING_STARS_ENABLED:
                        fall_prob = star.fall_probability()
                        if fall_prob > 0 and random.uniform(0, 100) < fall_prob:
                            to_remove.append(i)
                            absorbed_stars += 1

                for idx in sorted(to_remove, reverse=True):
                    if stars[idx] == tracking_star:
                        tracking_star = None
                    stars.pop(idx)
                    if stars[idx].captured:
                        NUM_CAPTURED -= 1
                    else:
                        NUM_ORBITING -= 1

                for idx, captured in to_replace:
                    if stars[idx] == tracking_star:
                        tracking_star = None
                    if replace_exited_stars:
                        stars[idx] = Star(captured=captured, used_names=used_names)
                    else:
                        stars.pop(idx)
                        exited_stars += 1

                if selected_star_idx is not None and (selected_star_idx >= len(stars) or not stars):
                    selected_star_idx = None

            if tracking_max_star and stars:
                max_star = max(stars, key=lambda s: s.mass, default=None)
                if max_star:
                    camera_x = max_star.x
                    camera_y = max_star.y
                    clamp_camera()

            keys = pygame.key.get_pressed()
            if not pause_simulation:
                if keys[pygame.K_t]:
                    trail_editable_length = max(1, trail_editable_length - 10 * dt)
                if keys[pygame.K_y]:
                    trail_editable_length = min(1000, trail_editable_length + 10 * dt)
                if keys[pygame.K_h]:
                    GM = max(1000, GM - 1000 * dt)
                if keys[pygame.K_g]:
                    GM = min(100000, GM + 1000 * dt)
                if keys[pygame.K_n]:
                    black_hole_radius = max(5, black_hole_radius - 1 * dt)
                if keys[pygame.K_b]:
                    black_hole_radius = min(20, black_hole_radius + 1 * dt)
                if keys[pygame.K_w] and not tracking_max_star:
                    camera_y -= 10 / camera_zoom
                if keys[pygame.K_s] and not tracking_max_star:
                    camera_y += 10 / camera_zoom
                if keys[pygame.K_a] and not tracking_max_star:
                    camera_x -= 10 / camera_zoom
                if keys[pygame.K_d] and not tracking_max_star:
                    camera_x += 10 / camera_zoom
                clamp_camera()

            if tracking_star:
                camera_x = tracking_star.x
                camera_y = tracking_star.y
                clamp_camera()

            all_stars = stars
            highest_distance_star = max(all_stars, key=lambda s: math.hypot(s.x - WIDTH / 2, s.y - HEIGHT / 2)) if all_stars else None
            lowest_distance_star = min(all_stars, key=lambda s: math.hypot(s.x - WIDTH / 2, s.y - HEIGHT / 2)) if all_stars else None

            screen.fill(BLACK)
            trail_surface.fill((0, 0, 0, 0))

            bh_x = (WIDTH / 2 - camera_x) * camera_zoom + WIDTH // 2
            bh_y = (HEIGHT / 2 - camera_y) * camera_zoom + HEIGHT // 2
            if isometric_view:
                bh_y -= (0 * 0.5) * camera_zoom
            for r in range(int(strong_field_radius * camera_zoom), int(EVENT_HORIZON_RADIUS * camera_zoom), -1):
                alpha = int(50 * (1 - (r / camera_zoom - EVENT_HORIZON_RADIUS) / (strong_field_radius - EVENT_HORIZON_RADIUS)))
                pygame.draw.circle(screen, (alpha, alpha, alpha), (int(bh_x), int(bh_y)), r, 1)
            pygame.draw.circle(screen, DARK_GRAY, (int(bh_x), int(bh_y)), int(EVENT_HORIZON_RADIUS * camera_zoom), 1)
            pygame.draw.circle(screen, RED, (int(bh_x), int(bh_y)), int(black_hole_radius * camera_zoom))

            if not show_interface:
                interface_hint = font.render("To show interface click 'I'", True, WHITE)
                screen.blit(interface_hint, (WIDTH - interface_hint.get_width() - 10, 10))
            else:
                screen.blit(orbits_text, orbits_rect.topleft)

            hovered_star_idx = None
            if stars:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                min_distance = float('inf')
                for i, star in enumerate(stars):
                    if isometric_view:
                        iso_x = (star.x - camera_x) * camera_zoom + WIDTH // 2 + (star.z * 0.5) * camera_zoom
                        iso_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2 - (star.z * 0.5) * camera_zoom
                        distance = math.hypot(iso_x - mouse_x, iso_y - mouse_y)
                    else:
                        screen_x = (star.x - camera_x) * camera_zoom + WIDTH // 2
                        screen_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2
                        distance = math.hypot(screen_x - mouse_x, screen_y - mouse_y)
                    if distance < 15 and distance < min_distance:
                        min_distance = distance
                        hovered_star_idx = i

            for i, star in enumerate(stars):
                if isometric_view:
                    iso_x, iso_y, star_color = star.draw_isometric(screen, camera_x, camera_y, camera_zoom)
                    screen_x, screen_y = iso_x, iso_y
                else:
                    star_color = star.draw(trail_surface, camera_x, camera_y, camera_zoom)
                    screen_x = (star.x - camera_x) * camera_zoom + WIDTH // 2
                    screen_y = (star.y - camera_y) * camera_zoom + HEIGHT // 2
                
                if not isometric_view:
                    pygame.draw.circle(screen, star_color, (int(screen_x), int(screen_y)), int(star.size * camera_zoom))
                
                critical_state = next((state for s, state, _ in critical_stars if s == star), None)
                box_color = WHITE
                if critical_state:
                    if critical_state == "approaching":
                        box_color = GREEN
                    elif critical_state == "inside":
                        box_color = RED
                    elif critical_state == "exiting":
                        box_color = YELLOW
                    elif critical_state == "post_exit":
                        box_color = GREEN
                elif star.selected or i == hovered_star_idx:
                    box_color = WHITE
                
                if critical_state or star.selected or i == hovered_star_idx:
                    pygame.draw.rect(screen, box_color, 
                                    (int(screen_x - star.size * camera_zoom - 5), 
                                     int(screen_y - star.size * camera_zoom - 5), 
                                     int(star.size * 2 * camera_zoom + 10), 
                                     int(star.size * 2 * camera_zoom + 10)), 3)
                    velocity = math.hypot(star.vx, star.vy) * PX_TO_KM / 1e6
                    info_lines = [
                        f"{star.name}",
                        f"S^{star.mass:.1f}",
                        f"{velocity:.1f} km/s"
                    ]
                    for j, line in enumerate(info_lines):
                        info_text = font.render(line, True, box_color)
                        screen.blit(info_text, (int(screen_x - info_text.get_width() // 2), 
                                               int(screen_y - star.size * camera_zoom - 20 - j * 15)))

            screen.blit(trail_surface, (0, 0))

            if show_orbits and selected_star_idx is not None and stars and 0 <= selected_star_idx < len(stars):
                selected_star = stars[selected_star_idx]
                if ORBITS_ENABLED:
                    if hasattr(selected_star, 'last_orbit_points') and selected_star.last_orbit_points:
                        transformed_points = []
                        for point in selected_star.last_orbit_points:
                            if len(point) == 3:  # (x, y, z)
                                x, y, z = point
                            else:  # (x, y)
                                x, y = point
                                z = 0
                            if isometric_view:
                                iso_x = (x - camera_x) * camera_zoom + WIDTH // 2 + (z * 0.5) * camera_zoom
                                iso_y = (y - camera_y) * camera_zoom + HEIGHT // 2 - (z * 0.5) * camera_zoom
                                transformed_points.append((iso_x, iso_y))
                            else:
                                transformed_points.append(((x - camera_x) * camera_zoom + WIDTH // 2, 
                                                          (y - camera_y) * camera_zoom + HEIGHT // 2))
                        if len(transformed_points) > 1:
                            orbit_color = (0, 0, 255) if selected_star.captured else (139, 0, 0)
                            pygame.draw.lines(screen, orbit_color, False, transformed_points, 2)
                    orbit_data, orbit_color = selected_star.draw_orbit(screen, camera_x, camera_y, camera_zoom)
                    if orbit_data is not None:
                        if not selected_star.captured:
                            pygame.draw.lines(screen, orbit_color, False, orbit_data, 2)
                        else:
                            for point in orbit_data[::5]:
                                pygame.draw.circle(screen, orbit_color, (int(point[0]), int(point[1])), 3)

            if show_interface:
                next_y_position = 10
                if selected_star_idx is not None and stars and 0 <= selected_star_idx < len(stars):
                    selected_star = stars[selected_star_idx]
                    if hasattr(selected_star, 'vz'):
                        velocity = math.hypot(selected_star.vx, selected_star.vy, selected_star.vz) * PX_TO_KM / 1e6
                    else:
                        velocity = math.hypot(selected_star.vx, selected_star.vy) * PX_TO_KM / 1e6
                    if hasattr(selected_star, 'z'):
                        distance = math.sqrt((selected_star.x - WIDTH / 2)**2 + (selected_star.y - HEIGHT / 2)**2 + selected_star.z**2) * PX_TO_KM / 1e6
                    else:
                        distance = math.hypot(selected_star.x - WIDTH / 2, selected_star.y - HEIGHT / 2) * PX_TO_KM / 1e6
                    accel = selected_star.compute_acceleration(stars)
                    if len(accel) == 2:
                        ax, ay = accel
                        accel_magnitude = math.hypot(ax, ay) * PX_TO_KM / 1e6
                    else:
                        ax, ay, az = accel
                        accel_magnitude = math.sqrt(ax**2 + ay**2 + az**2) * PX_TO_KM / 1e6
                    closest_dist = float('inf')
                    for other_star in stars:
                        if other_star != selected_star:
                            if hasattr(other_star, 'z'):
                                dist = math.sqrt((selected_star.x - other_star.x)**2 + (selected_star.y - other_star.y)**2 + (selected_star.z - other_star.z)**2) * PX_TO_KM / 1e6
                            else:
                                dist = math.hypot(selected_star.x - other_star.x, selected_star.y - other_star.y) * PX_TO_KM / 1e6
                            closest_dist = min(closest_dist, dist)
                    energy = 0.5 * selected_star.mass * velocity**2
                    angular_momentum = selected_star.mass * velocity * distance
                    if not selected_star.captured:
                        T_sim = 2 * math.pi * math.sqrt(selected_star.a**3 / GM)
                        orbit_time_years = T_sim * TIME_SCALE
                        orbit_display = f"{orbit_time_years:.2f} years"
                    else:
                        orbit_display = f"{selected_star.orbit_times[-1]:.2f} years" if selected_star.orbit_times else "N/A"
                    uplyw_lat = simulated_time
                    years = int(uplyw_lat)
                    months = int((uplyw_lat - years) * 12)
                    stats_left = [
                        f"Star: {selected_star.name} ({'Orbiting' if not selected_star.captured else 'Captured'})",
                        f"Velocity: {velocity:.1f} km/s",
                        f"Accel: {accel_magnitude:.2f} km/s^2",
                        f"Dist to BH: {distance:.1f} M km",
                        f"Closest Obj: {closest_dist:.1f} M km",
                        f"Energy: {energy:.2e} J",
                        f"Ang. Momentum: {angular_momentum:.2e} kg·km²/s",
                        f"Last Orbit: {orbit_display}"
                    ]
                    if selected_star.captured:
                        stats_left.append(f"Orbit Count: {selected_star.orbit_count}")
                    stats_left.append(f"Show Orbit: {'On' if show_orbits else 'Off'}")
                    stats_left.append(f"Orbits Completed: {selected_star.orbits_completed if not selected_star.captured else selected_star.orbit_count}")
                    
                    # Rysowanie i ustawienie rectów
                    for i, line in enumerate(stats_left):
                        color = WHITE if i != len(stats_left) - 2 else (GREEN if show_orbits else RED)  # "Show Orbit" to przedostatnia linia
                        text = font.render(line, True, color)
                        text_rect = text.get_rect(topleft=(10, 10 + i * 15))
                        screen.blit(text, text_rect.topleft)
                        if i == len(stats_left) - 2:  # Rect dla "Show Orbit"
                            show_orbit_rect = text_rect
                        next_y_position = 10 + (i + 1) * 15
                    
                    fall_prob = selected_star.fall_probability()
                    fall_prob_text = font.render(f"Fall Probability: {fall_prob:.1f}%", True, WHITE)
                    screen.blit(fall_prob_text, (10, next_y_position + 30))
                    next_y_position += 45

                orbits_rect = orbits_text.get_rect(topleft=(10, next_y_position))

                simulation_time_text = font.render(f"Czas symulacji: {elapsed_time:.2f} s", True, LIGHT_BLUE)
                uplyw_lat_text = font.render(f"Upływ lat: {years} lat, {months} miesięcy", True, LIGHT_BLUE)
                screen.blit(simulation_time_text, (10, HEIGHT - 75))
                screen.blit(uplyw_lat_text, (10, HEIGHT - 60))
                legend_text = font.render("S^1 = Masa Słońca (1.989e30 kg)", True, WHITE)
                screen.blit(legend_text, (10, HEIGHT - 30))

                screen.blit(sim_speed_text, (WIDTH - sim_speed_text.get_width() - 10, 10))
                screen.blit(trail_text, (WIDTH - trail_text.get_width() - 10, 30))
                screen.blit(stars_text, (WIDTH - stars_text.get_width() - 10, 50))
                screen.blit(star_interaction_text, star_interaction_rect.topleft)
                screen.blit(pause_text, pause_rect.topleft)
                screen.blit(restart_text, restart_rect.topleft)
                screen.blit(gm_text, gm_rect.topleft)
                screen.blit(bh_radius_text, bh_radius_rect.topleft)
                screen.blit(falling_enabled_text, falling_enabled_rect.topleft)
                screen.blit(falling_percent_text, falling_percent_rect.topleft)
                screen.blit(critical_highlight_text, critical_highlight_rect.topleft)
                screen.blit(relativity_text, relativity_rect.topleft)
                screen.blit(relativity_visuals_text, relativity_visuals_rect.topleft)
                screen.blit(collisions_text, collisions_rect.topleft)
                screen.blit(realism_text, realism_rect.topleft)
                screen.blit(exit_to_menu_text, exit_to_menu_rect.topleft)
                screen.blit(copyright_text, COPYRIGHT_POS)

                if pause_rect.collidepoint(mouse_x, mouse_y):
                    pause_text = font.render("Pause/Unpause", True, GREEN)
                    screen.blit(pause_text, pause_rect.topleft)
                    pygame.draw.rect(screen, LIGHT_GRAY, pause_rect, 2)
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    restart_text = font.render("Restart", True, GREEN)
                    screen.blit(restart_text, restart_rect.topleft)
                    pygame.draw.rect(screen, LIGHT_GRAY, restart_rect, 2)
                if gm_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, gm_rect, 2)
                if bh_radius_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, bh_radius_rect, 2)
                if falling_enabled_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, falling_enabled_rect, 2)
                if falling_percent_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, falling_percent_rect, 2)
                if critical_highlight_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, critical_highlight_rect, 2)
                if relativity_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, relativity_rect, 2)
                if relativity_visuals_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, relativity_visuals_rect, 2)
                if star_interaction_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, star_interaction_rect, 2)
                if collisions_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, LIGHT_GRAY, collisions_rect, 2)
                if realism_rect.collidepoint(mouse_x, mouse_y):
                    realism_text = font.render(f"Realism: {'On' if realism_mode else 'Off'}", True, GREEN)
                    screen.blit(realism_text, realism_rect.topleft)
                    pygame.draw.rect(screen, LIGHT_GRAY, realism_rect, 2)
                if exit_to_menu_rect.collidepoint(mouse_x, mouse_y):
                    exit_to_menu_text = font.render("Back to Menu", True, GREEN)
                    screen.blit(exit_to_menu_text, exit_to_menu_rect.topleft)
                    pygame.draw.rect(screen, LIGHT_GRAY, exit_to_menu_rect, 2)

            if show_experimental:
                num_sliders = len(sliders)
                exp_box_height = 50 + num_sliders * 40
                exp_box = pygame.Surface((300, exp_box_height))
                exp_box.fill(GRAY)
                exp_box.set_alpha(200)
                exp_rect = exp_box.get_rect(topright=(WIDTH - 10, 380))
                screen.blit(exp_box, exp_rect.topleft)
                for i, (key, slider) in enumerate(sliders.items()):
                    label_y = exp_rect.top + 10 + i * 40
                    label = font.render(
                        f"{key}: {slider['value']:.3f}" if key in ["Sim Speed", "Star Interaction", "Relativity Str"] 
                        else f"{key}: {int(slider['value'])}", True, WHITE)
                    screen.blit(label, (exp_rect.left + 10, label_y))
                    slider_rect = pygame.Rect(exp_rect.left + 10, exp_rect.top + 25 + i * 40, 280, 10)
                    slider["rect"] = slider_rect
                    pygame.draw.rect(screen, LIGHT_GRAY, slider_rect)
                    slider_pos = slider_rect.left + (slider["value"] - slider["min"]) / (slider["max"] - slider["min"]) * slider_rect.width
                    green_rect = pygame.Rect(int(slider_pos) - 5, slider_rect.top - 2, 10, 14)
                    pygame.draw.rect(screen, GREEN, green_rect)
                if "Disk Radius" in sliders:
                    STRONG_FIELD_RADIUS = int(sliders["Disk Radius"]["value"])

            if show_stats and stars:
                stats_box = pygame.Surface((300, 300))
                stats_box.fill(GRAY)
                stats_box.set_alpha(200)
                total_energy = sum(0.5 * star.mass * (math.hypot(star.vx, star.vy) * PX_TO_KM)**2 for star in stars)
                total_momentum = sum(star.mass * math.hypot(star.vx, star.vy) * math.hypot(star.x - WIDTH / 2, star.y - HEIGHT / 2) * PX_TO_KM for star in stars)
                max_star = max(stars, key=lambda s: s.mass, default=None)
                max_mass = max_star.mass if max_star else 0.0
                max_star_info = f"Max Star: {max_star.name if max_star else 'None'} ({max_mass:.1f})"
                typical_stars = 1000000
                current_stars = len(stars)
                star_percentage = (current_stars / typical_stars) * 100 if typical_stars > 0 else 0
                orbiting_stars = [star for star in stars if not star.captured]
                highest_orbit_star = max(orbiting_stars, key=lambda s: s.a, default=None) if orbiting_stars else None
                lowest_orbit_star = min(orbiting_stars, key=lambda s: s.a, default=None) if orbiting_stars else None
                stats_lines = [
                    f"Absorbed Stars: {absorbed_stars}",
                    f"Total Energy: {total_energy:.2e} J",
                    f"Total Momentum: {total_momentum:.2e} kg·km²/s",
                    f"Active Stars: {current_stars}",
                    f"Typical BH Stars: {typical_stars:,} (~1M)",
                    f"Stars in Sim: {current_stars} ({star_percentage:.1f}%)",
                    max_star_info,
                    f"Highest Orbit: {highest_orbit_star.name if highest_orbit_star else 'None'} ({highest_orbit_star.a if highest_orbit_star else 0:.1f})",
                    f"Lowest Orbit: {lowest_orbit_star.name if lowest_orbit_star else 'None'} ({lowest_orbit_star.a if lowest_orbit_star else 0:.1f})"
                ]
                stats_box_rect = pygame.Rect(10, HEIGHT // 2 - 150, 300, 300)
                replace_text = font.render("Replace Exited: " + ("On" if replace_exited_stars else "Off"), True, WHITE)
                replace_rect = replace_text.get_rect(topleft=(stats_box_rect.left + 10, stats_box_rect.top + 10))
                stats_box.blit(replace_text, replace_rect.topleft)
                orbits_text = font.render("Show Orbits: " + ("On" if ORBITS_ENABLED else "Off"), True, WHITE)
                orbits_rect = orbits_text.get_rect(topleft=(stats_box_rect.left + 10, replace_rect.bottom + 20))
                stats_box.blit(orbits_text, orbits_rect.topleft)
                for i, line in enumerate(stats_lines):
                    text_color = WHITE
                    if i in [6, 7, 8]:
                        clickable_rect = pygame.Rect(stats_box_rect.left + 10, stats_box_rect.top + 10 + i * 30, font.size(line)[0], font.get_height())
                        if clickable_rect.collidepoint(mouse_x, mouse_y):
                            text_color = GREEN
                    text = font.render(line, True, text_color)
                    stats_box.blit(text, (10, 10 + i * 30))
                screen.blit(stats_box, stats_box_rect.topleft)

            pygame.display.flip()

        except Exception as e:
            print(f"Error in main_simulation loop: {e}")
            return "exit"

    return "menu"  # Powrót do menu po zakończeniu pętli

# Resetowanie symulacji – tworzenie nowych gwiazd i zerowanie parametrów
def reset_simulation(used_names):
    global stars, simulated_time, selected_star_idx, absorbed_stars, camera_x, camera_y, camera_zoom, elapsed_time
    used_names.clear()  # Czyszczenie listy użytych nazw
    stars = [Star(captured=False, used_names=used_names) for _ in range(NUM_ORBITING)] + [Star(captured=True, used_names=used_names) for _ in range(NUM_CAPTURED)]  # Tworzenie nowych gwiazd
    simulated_time = 0  # Zerowanie czasu symulowanego
    elapsed_time = 0  # Zerowanie czasu rzeczywistego
    selected_star_idx = 0 if stars else None  # Reset indeksu wybranej gwiazdy
    absorbed_stars = 0  # Zerowanie wchłoniętych gwiazd
    camera_x, camera_y = WIDTH / 2, HEIGHT / 2  # Reset pozycji kamery
    camera_zoom = 1.0  # Reset zoomu kamery

# Zmodyfikowana główna pętla
if __name__ == "__main__":
    while True:
        action, NUM_ORBITING, NUM_CAPTURED = start_menu()  # Uruchomienie menu startowego
        if action == "exit":
            break  # Wyjście z programu
        reset_simulation(set())  # Reset symulacji przed startem
        fade_out(screen, screen.copy())  # Animacja zanikania
        if not loading_screen(screen):  # Wywołanie ekranu ładowania
            break  # Wyjście, jeśli użytkownik zamknie okno podczas ładowania
        action = main_simulation()  # Uruchomienie symulacji
        if action == "exit":
            break  # Wyjście z programu
    pygame.quit()  # Zamknięcie Pygame
    sys.exit()  # Wyjście z programu