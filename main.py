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

BACKGROUND = (3, 5, 4)

STREAM_COUNT = 42

MIN_SPEED = 2.0
MAX_SPEED = 6.0

MIN_LENGTH = 8
MAX_LENGTH = 24

FONT_SIZE = 22

SAMPLE_RATE = 44100


# ============================================================
# COLORS
# ============================================================

# Muted Matrix-style colors.
# No vibrant neon colors.

HEAD_COLOR = (185, 205, 185)

TRAIL_COLORS = [
    (120, 145, 125),
    (100, 125, 105),
    (80, 105, 85),
    (60, 85, 65),
    (45, 65, 50),
]


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
# CHARACTER SET
# ============================================================

CHARACTERS = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "!@#$%^&*"
    "+-=<>/"
)


# ============================================================
# SOUND GENERATION
# ============================================================

def create_sound(
    filename,
    frequency,
    duration=0.12,
    volume=5000
):

    samples = int(
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

        for i in range(samples):

            time = i / SAMPLE_RATE

            wave_value = math.sin(
                2
                * math.pi
                * frequency
                * time
            )

            envelope = (
                1
                - (i / samples)
            )

            value = int(
                wave_value
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


# Create countdown sound
create_sound(
    "countdown.wav",
    440,
    0.15,
    6500
)

# Create subtle rain sound
create_sound(
    "rain.wav",
    180,
    0.08,
    2500
)


countdown_sound = pygame.mixer.Sound(
    "countdown.wav"
)

rain_sound = pygame.mixer.Sound(
    "rain.wav"
)

countdown_sound.set_volume(
    0.30
)

rain_sound.set_volume(
    0.10
)


# ============================================================
# MATRIX STREAM
# ============================================================

class MatrixStream:

    def __init__(self):

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        self.x = random.randint(
            0,
            WIDTH - FONT_SIZE
        )

        self.y = random.uniform(
            -HEIGHT,
            0
        )

        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        self.speed = random.uniform(
            MIN_SPEED,
            MAX_SPEED
        )

        # ----------------------------------------------------
        # LENGTH
        # ----------------------------------------------------

        self.length = random.randint(
            MIN_LENGTH,
            MAX_LENGTH
        )

        # ----------------------------------------------------
        # CHARACTERS
        # ----------------------------------------------------

        self.characters = [
            random.choice(
                CHARACTERS
            )
            for _ in range(
                self.length
            )
        ]

        # ----------------------------------------------------
        # CHARACTER CHANGE TIMER
        # ----------------------------------------------------

        self.change_timer = 0

        self.change_interval = random.randint(
            4,
            12
        )


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        # Move stream downward
        self.y += self.speed

        # Occasionally change characters
        self.change_timer += 1

        if (
            self.change_timer
            >= self.change_interval
        ):

            self.change_timer = 0

            self.change_interval = random.randint(
                4,
                12
            )

            # Randomly replace a character
            index = random.randint(
                0,
                self.length - 1
            )

            self.characters[index] = (
                random.choice(
                    CHARACTERS
                )
            )

        # Reset when the entire stream
        # leaves the screen
        if (
            self.y
            - self.length * FONT_SIZE
            > HEIGHT
        ):

            self.reset()


    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.x = random.randint(
            0,
            WIDTH - FONT_SIZE
        )

        self.y = random.uniform(
            -300,
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


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        for index, character in enumerate(
            self.characters
        ):

            character_y = (
                self.y
                - index * FONT_SIZE
            )

            # Don't draw characters
            # outside the screen
            if (
                character_y < -FONT_SIZE
                or character_y > HEIGHT
            ):
                continue

            # First character is brightest
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

            rendered_character = font.render(
                character,
                True,
                color
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
        (190, 205, 190),
        HEIGHT // 2 - 50
    )

    draw_centered_text(
        "PRESS SPACE TO START",
        instruction_font,
        (105, 125, 110),
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
                (190, 205, 190),
                HEIGHT // 2
            )

            pygame.display.flip()

            clock.tick(FPS)


    # --------------------------------------------------------
    # GO
    # --------------------------------------------------------

    screen.fill(
        BACKGROUND
    )

    draw_centered_text(
        "GO",
        countdown_font,
        (190, 205, 190),
        HEIGHT // 2
    )

    pygame.display.flip()

    pygame.time.delay(
        350
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
# START MATRIX
# ============================================================

if running:

    create_streams()


# ============================================================
# MAIN LOOP
# ============================================================

sound_timer = 0


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
    # UPDATE
    # --------------------------------------------------------

    for stream in streams:

        stream.update()


    # --------------------------------------------------------
    # SUBTLE SOUND
    # --------------------------------------------------------

    sound_timer += 1

    if sound_timer >= 45:

        rain_sound.play()

        sound_timer = 0


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

    clock.tick(FPS)


# ============================================================
# CLEANUP
# ============================================================

pygame.quit()