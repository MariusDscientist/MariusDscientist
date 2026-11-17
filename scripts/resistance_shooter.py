"""Run gh-space-shooter with a Star Wars theme.

gh-space-shooter has no theming options, so this patches its render context
(colors) and the ship drawing before handing control to its normal CLI.
Takes exactly the same arguments as the `gh-space-shooter` command.

SIDE=light (default): Resistance X-wing, red bolts, First Order fleet in steel blue.
SIDE=dark:            TIE fighter, green bolts, Resistance fleet in burning reds.
"""

import os

from gh_space_shooter import cli
from gh_space_shooter.game.drawables.ship import Ship
from gh_space_shooter.game.render_context import RenderContext

SHIP_ROW = 10  # gh_space_shooter.constants.SHIP_POSITION_Y

# ---------------------------------------------------------------- light side
HULL = (236, 238, 242)      # X-wing white
STRIPE = (232, 96, 28)      # Resistance orange
ENGINE = (255, 120, 60)
CANOPY = (40, 48, 64)


def light_context() -> RenderContext:
    return RenderContext(
        cell_size=12,
        cell_spacing=3,
        padding=40,
        background_color=(3, 4, 10),
        grid_color=(16, 20, 30),
        enemy_colors={1: (40, 66, 96), 2: (58, 104, 150), 3: (84, 150, 205), 4: (150, 205, 245)},
        ship_color=HULL,
        bullet_color=(255, 48, 48),  # red X-wing bolts
    )


def draw_xwing(self, draw, context: RenderContext) -> None:
    """Top-down X-wing: long nose, S-foils with orange stripes, wingtip cannons."""
    x, y = context.get_cell_position(self.x, SHIP_ROW)
    cx = x + context.cell_size / 2
    top, h = y - 4, context.cell_size + 6

    for side in (-1, 1):
        root_x = cx + side * 2
        tip_x = cx + side * 11
        draw.polygon(
            [(root_x, top + h * 0.55), (tip_x, top + h * 0.62),
             (tip_x, top + h * 0.80), (root_x, top + h * 0.85)],
            fill=HULL,
        )
        draw.line([(cx + side * 5, top + h * 0.60), (cx + side * 9, top + h * 0.64)], fill=STRIPE, width=2)
        draw.line([(tip_x, top + h * 0.20), (tip_x, top + h * 0.80)], fill=HULL, width=1)
        draw.point((tip_x, top + h * 0.18), fill=(255, 48, 48))

    draw.polygon(
        [(cx, top), (cx - 1.5, top + h * 0.35), (cx - 2.5, top + h),
         (cx + 2.5, top + h), (cx + 1.5, top + h * 0.35)],
        fill=HULL,
    )
    draw.line([(cx, top + h * 0.12), (cx, top + h * 0.30)], fill=STRIPE, width=1)
    draw.ellipse([cx - 1.5, top + h * 0.45, cx + 1.5, top + h * 0.60], fill=CANOPY)

    for side in (-1, 1):
        ex = cx + side * 3.5
        draw.rectangle([ex - 1, top + h * 0.80, ex + 1, top + h], fill=(150, 156, 168))
        draw.point((ex, top + h + 1), fill=ENGINE)


# ----------------------------------------------------------------- dark side
TIE_PANEL = (58, 62, 70)
TIE_FRAME = (150, 156, 168)
TIE_POD = (120, 126, 138)
TIE_WINDOW = (20, 22, 28)


def dark_context() -> RenderContext:
    return RenderContext(
        cell_size=12,
        cell_spacing=3,
        padding=40,
        background_color=(6, 2, 3),
        grid_color=(28, 10, 12),
        enemy_colors={1: (90, 14, 18), 2: (150, 24, 30), 3: (215, 40, 40), 4: (255, 110, 90)},
        ship_color=TIE_FRAME,
        bullet_color=(70, 255, 90),  # green TIE bolts
    )


def draw_tie(self, draw, context: RenderContext) -> None:
    """TIE fighter seen from behind: two hexagonal wing panels and a ball cockpit."""
    x, y = context.get_cell_position(self.x, SHIP_ROW)
    cx = x + context.cell_size / 2
    cy = y + context.cell_size / 2

    for side in (-1, 1):
        wx = cx + side * 9
        hexagon = [(wx, cy - 11), (wx + 3, cy - 6), (wx + 3, cy + 6),
                   (wx, cy + 11), (wx - 3, cy + 6), (wx - 3, cy - 6)]
        draw.polygon(hexagon, fill=TIE_PANEL, outline=TIE_FRAME)
        draw.line([(wx, cy - 10), (wx, cy + 10)], fill=TIE_FRAME, width=1)
        draw.line([(cx + side * 3, cy), (wx, cy)], fill=TIE_FRAME, width=2)  # pylon

    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=TIE_POD)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=TIE_WINDOW)


if os.environ.get("SIDE", "light") == "dark":
    RenderContext.darkmode = staticmethod(dark_context)
    Ship.draw = draw_tie
else:
    RenderContext.darkmode = staticmethod(light_context)
    Ship.draw = draw_xwing

if __name__ == "__main__":
    cli.app()
