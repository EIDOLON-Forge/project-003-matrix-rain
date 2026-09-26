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
            harmonic = 0.25 * math.sin(
                2
                * math.pi
                * frequency
                * 2
                * time
            )

            # Short fade
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
# CREATE SOUNDS
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
    "tick.wav",
    180,
    110,
    0.055,
    3500
)

create_tone(
    "surge.wav",
    160,
    420,
    0.18,
    4500
)


# ============================================================
# LOAD SOUNDS
# ============================================================

countdown_sound = pygame.mixer.Sound(
    "countdown.wav"
)

start_sound = pygame.mixer.Sound(
    "start.wav"
)

tick_sound = pygame.mixer.Sound(
    "tick.wav"
)

surge_sound = pygame.mixer.Sound(
    "surge.wav"
)


countdown_sound.set_volume(0.35)
start_sound.set_volume(0.40)
tick_sound.set_volume(0.08)
surge_sound.set_volume(0.18)


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

        # Different streams mutate
        # at different rates.

        self.change_timer = 0

        self.change_interval = random.randint(
            3,
            10
        )

        # Some streams become temporary
        # speed bursts.

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

            # Change multiple characters
            # occasionally.

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

        # Reset when stream leaves screen

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

            # Bright head
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
# STREAM COLLECTION
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

sound_timer = 0

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
    # ADDICTIVE TICK SOUND
    # --------------------------------------------------------

    sound_timer += 1

    if sound_timer >= 24:

        tick_sound.play()

        sound_timer = 0


    # --------------------------------------------------------
    # RANDOM SURGE
    # --------------------------------------------------------

    surge_timer -= 1

    if surge_timer <= 0:

        surge_sound.play()

        # Temporarily accelerate
        # several streams.

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

pygame.quit()