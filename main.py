import pygame
import random
import math
import wave


# ============================================================
# CONFIGURATION
# ============================================================

WIDTH = 800
HEIGHT = 800
FPS = 60

BACKGROUND = (2, 4, 3)

STREAM_COUNT = 55

MIN_SPEED = 2.0
MAX_SPEED = 7.0

MIN_LENGTH = 8
MAX_LENGTH = 26

FONT_SIZE = 22

SAMPLE_RATE = 44100


# ============================================================
# COLORS
# ============================================================

HEAD_COLOR = (205, 225, 205)

TRAIL_COLORS = [
    (145, 170, 145),
    (120, 150, 125),
    (95, 125, 100),
    (70, 100, 78),
    (48, 75, 55),
    (30, 55, 38),
]


# ============================================================
# CHARACTER SET
# ============================================================

CHARACTERS = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "!@#$%^&*"
    "+-=<>/"
)


# ============================================================
# INITIALIZE PYGAME
# ============================================================

pygame.init()

pygame.mixer.init(
    frequency=SAMPLE_RATE,
    size=-16,
    channels=1,
    buffer=512
)

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "EIDOLON — Matrix Rain"
)

clock = pygame.time.Clock()


# ============================================================
# FONTS
# ============================================================

font = pygame.font.Font(
    None,
    FONT_SIZE
)

title_font = pygame.font.Font(
    None,
    64
)

countdown_font = pygame.font.Font(
    None,
    150
)

instruction_font = pygame.font.Font(
    None,
    36
)


# ============================================================
# PROCEDURAL SOUND GENERATOR
# ============================================================

def create_tone(
    filename,
    start_frequency,
    end_frequency,
    duration,
    volume
):

    sample_count = int(
        SAMPLE_RATE * duration
    )

    with wave.open(
        filename,
        "w"
    ) as sound_file:

        sound_file.setnchannels(1)
        sound_file.setsampwidth(2)
        sound_file.setframerate(
            SAMPLE_RATE
        )

        audio_data = bytearray()

        for i in range(sample_count):

            progress = (
                i / sample_count
            )

            frequency = (
                start_frequency
                + (
                    end_frequency
                    - start_frequency
                )
                * progress
            )

            time = (
                i / SAMPLE_RATE
            )

            # Main tone
            sine = math.sin(
                2
                * math.pi
                * frequency
                * time
            )

            # Small harmonic
            harmonic = (
                0.25
                * math.sin(
                    2
                    * math.pi
                    * frequency
                    * 2
                    * time
                )
            )

            # Fade out
            envelope = (
                1 - progress
            )

            value = int(
                (
                    sine
                    + harmonic
                )
                * envelope
                * volume
            )

            audio_data += int(
                value
            ).to_bytes(
                2,
                byteorder="little",
                signed=True
            )

        sound_file.writeframes(
            audio_data
        )


# ============================================================
# CINEMATIC SCI-FI MUSIC GENERATOR
# ============================================================

def create_ambient_music(filename):

    duration = 24.0

    total_samples = int(
        SAMPLE_RATE * duration
    )

    audio_data = bytearray()

    # Original dark sci-fi chord progression
    chords = [
        [55.0, 82.41, 110.0],
        [49.0, 73.42, 98.0],
        [58.27, 87.31, 116.54],
        [43.65, 65.41, 87.31],
    ]

    for i in range(total_samples):

        time = i / SAMPLE_RATE

        # ----------------------------------------------------
        # CHORD
        # ----------------------------------------------------

        chord_index = int(
            time / 6
        ) % len(chords)

        chord = chords[
            chord_index
        ]

        drone = 0.0

        for frequency in chord:

            drone += math.sin(
                2
                * math.pi
                * frequency
                * time
            )

        drone /= len(chord)


        # ----------------------------------------------------
        # SLOW SUB-BASS PULSE
        # ----------------------------------------------------

        pulse_frequency = 1.2

        pulse = (
            math.sin(
                2
                * math.pi
                * pulse_frequency
                * time
            )
            + 1
        ) / 2

        pulse *= 0.5


        # ----------------------------------------------------
        # ATMOSPHERIC HIGH TONES
        # ----------------------------------------------------

        atmosphere = (
            math.sin(
                2
                * math.pi
                * 220
                * time
            )
            * 0.025
        )

        atmosphere += (
            math.sin(
                2
                * math.pi
                * 277.18
                * time
            )
            * 0.018
        )


        # ----------------------------------------------------
        # SLOW ATMOSPHERIC MOVEMENT
        # ----------------------------------------------------

        movement = (
            math.sin(
                2
                * math.pi
                * 0.07
                * time
            )
            * 0.5
            + 0.5
        )


        # ----------------------------------------------------
        # MIX
        # ----------------------------------------------------

        sample = (
            drone * 0.28
            + drone * pulse * 0.18
            + atmosphere * movement
        )

        # Master volume
        sample *= 0.20


        # ----------------------------------------------------
        # CONVERT TO 16-BIT AUDIO
        # ----------------------------------------------------

        value = int(
            sample * 32767
        )

        value = max(
            -32767,
            min(
                32767,
                value
            )
        )

        audio_data += int(
            value
        ).to_bytes(
            2,
            byteorder="little",
            signed=True
        )


    # --------------------------------------------------------
    # WRITE WAV
    # --------------------------------------------------------

    with wave.open(
        filename,
        "w"
    ) as sound_file:

        sound_file.setnchannels(1)
        sound_file.setsampwidth(2)
        sound_file.setframerate(
            SAMPLE_RATE
        )

        sound_file.writeframes(
            audio_data
        )


# ============================================================
# CREATE AUDIO
# ============================================================

create_tone(
    "countdown.wav",
    500,
    350,
    0.14,
    6500
)

create_tone(
    "start.wav",
    300,
    900,
    0.25,
    7000
)

create_tone(
    "surge.wav",
    160,
    420,
    0.18,
    4500
)

create_ambient_music(
    "matrix_music.wav"
)


# ============================================================
# LOAD AUDIO
# ============================================================

countdown_sound = pygame.mixer.Sound(
    "countdown.wav"
)

start_sound = pygame.mixer.Sound(
    "start.wav"
)

surge_sound = pygame.mixer.Sound(
    "surge.wav"
)

matrix_music = pygame.mixer.Sound(
    "matrix_music.wav"
)


countdown_sound.set_volume(
    0.35
)

start_sound.set_volume(
    0.40
)

surge_sound.set_volume(
    0.18
)

matrix_music.set_volume(
    0.35
)


# ============================================================
# MATRIX STREAM
# ============================================================

class MatrixStream:

    def __init__(self):

        self.reset(
            initial=True
        )


    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self,
        initial=False
    ):

        self.x = random.randint(
            0,
            WIDTH - FONT_SIZE
        )

        if initial:

            self.y = random.uniform(
                -HEIGHT,
                HEIGHT
            )

        else:

            self.y = random.uniform(
                -400,
                -50
            )

        self.speed = random.uniform(
            MIN_SPEED,
            MAX_SPEED
        )

        self.length = random.randint(
            MIN_LENGTH,
            MAX_LENGTH
        )

        self.characters = [
            random.choice(
                CHARACTERS
            )
            for _ in range(
                self.length
            )
        ]

        self.change_timer = 0

        self.change_interval = random.randint(
            3,
            10
        )

        # A small percentage of streams
        # are naturally faster.

        self.surge = (
            random.random()
            < 0.12
        )

        if self.surge:

            self.speed *= random.uniform(
                1.4,
                2.0
            )


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        self.y += self.speed

        # Character mutation
        self.change_timer += 1

        if (
            self.change_timer
            >= self.change_interval
        ):

            self.change_timer = 0

            self.change_interval = (
                random.randint(
                    3,
                    10
                )
            )

            changes = random.randint(
                1,
                3
            )

            for _ in range(changes):

                index = random.randint(
                    0,
                    self.length - 1
                )

                self.characters[index] = (
                    random.choice(
                        CHARACTERS
                    )
                )

        # Reset when off-screen

        if (
            self.y
            - self.length * FONT_SIZE
            > HEIGHT
        ):

            self.reset()


    # ========================================================
    # DRAW
    # ========================================================

    def draw(
        self,
        surface
    ):

        for index, character in enumerate(
            self.characters
        ):

            character_y = (
                self.y
                - index * FONT_SIZE
            )

            if (
                character_y
                < -FONT_SIZE
                or character_y
                > HEIGHT
            ):

                continue

            if index == 0:

                color = HEAD_COLOR

            else:

                color_index = min(
                    index - 1,
                    len(TRAIL_COLORS) - 1
                )

                color = TRAIL_COLORS[
                    color_index
                ]

            rendered_character = (
                font.render(
                    character,
                    True,
                    color
                )
            )

            surface.blit(
                rendered_character,
                (
                    self.x,
                    character_y
                )
            )


# ============================================================
# CREATE STREAMS
# ============================================================

streams = []


def create_streams():

    streams.clear()

    for _ in range(
        STREAM_COUNT
    ):

        streams.append(
            MatrixStream()
        )


# ============================================================
# CENTERED TEXT
# ============================================================

def draw_centered_text(
    text,
    selected_font,
    color,
    y
):

    rendered_text = (
        selected_font.render(
            text,
            True,
            color
        )
    )

    rect = (
        rendered_text.get_rect(
            center=(
                WIDTH // 2,
                y
            )
        )
    )

    screen.blit(
        rendered_text,
        rect
    )


# ============================================================
# START SCREEN
# ============================================================

def draw_start_screen():

    screen.fill(
        BACKGROUND
    )

    draw_centered_text(
        "MATRIX RAIN",
        title_font,
        (190, 215, 190),
        HEIGHT // 2 - 55
    )

    draw_centered_text(
        "PRESS SPACE TO START",
        instruction_font,
        (100, 130, 105),
        HEIGHT // 2 + 30
    )

    pygame.display.flip()


# ============================================================
# COUNTDOWN
# ============================================================

def countdown():

    for number in [3, 2, 1]:

        start_time = (
            pygame.time.get_ticks()
        )

        countdown_sound.play()

        while (
            pygame.time.get_ticks()
            - start_time
            < 1000
        ):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    return False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        return False


            screen.fill(
                BACKGROUND
            )

            draw_centered_text(
                str(number),
                countdown_font,
                (190, 215, 190),
                HEIGHT // 2
            )

            pygame.display.flip()

            clock.tick(
                FPS
            )


    # --------------------------------------------------------
    # GO
    # --------------------------------------------------------

    screen.fill(
        BACKGROUND
    )

    draw_centered_text(
        "GO",
        countdown_font,
        (205, 230, 205),
        HEIGHT // 2
    )

    pygame.display.flip()

    start_sound.play()

    # Start cinematic music
    matrix_music.play(
        loops=-1
    )

    pygame.time.delay(
        400
    )

    return True


# ============================================================
# START SCREEN
# ============================================================

running = True

waiting_to_start = True


while (
    running
    and waiting_to_start
):

    draw_start_screen()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            elif event.key == pygame.K_SPACE:

                waiting_to_start = False


# ============================================================
# COUNTDOWN
# ============================================================

if running:

    running = countdown()


# ============================================================
# START SIMULATION
# ============================================================

if running:

    create_streams()


# ============================================================
# MAIN LOOP
# ============================================================

surge_timer = random.randint(
    300,
    600
)


while running:

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False


    # --------------------------------------------------------
    # UPDATE STREAMS
    # --------------------------------------------------------

    for stream in streams:

        stream.update()


    # --------------------------------------------------------
    # RANDOM SPEED SURGE
    # --------------------------------------------------------

    surge_timer -= 1

    if surge_timer <= 0:

        surge_sound.play()

        selected_streams = random.sample(
            streams,
            min(
                8,
                len(streams)
            )
        )

        for stream in selected_streams:

            stream.speed *= random.uniform(
                1.3,
                1.8
            )

        surge_timer = random.randint(
            360,
            700
        )


    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    screen.fill(
        BACKGROUND
    )

    for stream in streams:

        stream.draw(
            screen
        )


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    pygame.display.flip()

    clock.tick(
        FPS
    )


# ============================================================
# CLEANUP
# ============================================================

matrix_music.stop()

pygame.quit()