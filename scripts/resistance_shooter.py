"""Run gh-space-shooter with a Resistance X-wing theme.

gh-space-shooter has no theming options, so this patches its render context
(colors) and the ship drawing before handing control to its normal CLI.
Takes exactly the same arguments as the `gh-space-shooter` command.
"""

from gh_space_shooter import cli
from gh_space_shooter.game.drawables.ship import Ship
from gh_space_shooter.game.render_context import RenderContext

HULL = (236, 238, 242)      # X-wing white
STRIPE = (232, 96, 28)      # Resistance orange
ENGINE = (255, 120, 60)     # engine glow
CANOPY = (40, 48, 64)


def resistance() -> RenderContext:
    return RenderContext(
        cell_size=12,
        cell_spacing=3,
        padding=40,
        background_color=(3, 4, 10),
        grid_color=(16, 20, 30),
        # First Order fleet: cold steel blues, brighter = more contributions
        enemy_colors={1: (40, 66, 96), 2: (58, 104, 150), 3: (84, 150, 205), 4: (150, 205, 245)},
        ship_color=HULL,
        bullet_color=(255, 48, 48),  # red X-wing laser bolts
    )


def draw_xwing(self, draw, context: RenderContext) -> None:
    """Top-down X-wing: long nose, four S-foil wings with orange stripes."""
    x, y = context.get_cell_position(self.x, 10)  # SHIP_POSITION_Y
    cx = x + context.cell_size / 2
    top, h = y - 4, context.cell_size + 6

    # S-foils (wings), slightly swept, with laser cannons on the tips
    for side in (-1, 1):
        root_x = cx + side * 2
        tip_x = cx + side * 11
        draw.polygon(
            [(root_x, top + h * 0.55), (tip_x, top + h * 0.62),
             (tip_x, top + h * 0.80), (root_x, top + h * 0.85)],
            fill=HULL,
        )
        draw.line([(cx + side * 5, top + h * 0.60), (cx + side * 9, top + h * 0.64)], fill=STRIPE, width=2)
        draw.line([(tip_x, top + h * 0.20), (tip_x, top + h * 0.80)], fill=HULL, width=1)  # cannon
        draw.point((tip_x, top + h * 0.18), fill=(255, 48, 48))

    # Fuselage and nose
    draw.polygon(
        [(cx, top), (cx - 1.5, top + h * 0.35), (cx - 2.5, top + h),
         (cx + 2.5, top + h), (cx + 1.5, top + h * 0.35)],
        fill=HULL,
    )
    draw.line([(cx, top + h * 0.12), (cx, top + h * 0.30)], fill=STRIPE, width=1)
    draw.ellipse([cx - 1.5, top + h * 0.45, cx + 1.5, top + h * 0.60], fill=CANOPY)

    # Engines
    for side in (-1, 1):
        ex = cx + side * 3.5
        draw.rectangle([ex - 1, top + h * 0.80, ex + 1, top + h], fill=(150, 156, 168))
        draw.point((ex, top + h + 1), fill=ENGINE)


RenderContext.darkmode = staticmethod(resistance)
Ship.draw = draw_xwing

if __name__ == "__main__":
    cli.app()
