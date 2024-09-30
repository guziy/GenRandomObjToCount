import random

import matplotlib.axes
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from random import choices
from matplotlib.markers import MarkerStyle
from pathlib import Path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



def get_random_icon_path():
    icons_dir = Path(__file__).parent / "icons"
    icons = list(icons_dir.iterdir())
    icon_idx = random.choice(range(len(icons)))

    return icons[icon_idx], icon_idx


def get_random_image(fig_dpi=100):
    icon_pth, idx = get_random_icon_path()
    return OffsetImage(
        plt.imread(icon_pth, format="png"), zoom=72 / fig_dpi), idx


def main():
    n_plots = 20
    fig_dpi = 100

    empty = ["|", "None", None, "nothing", "none", "", " ", "_"]
    # markers = list(m for m in MarkerStyle.markers.keys() if m not in empty)
    n_rows = set([i for i in range(8, 22) if i % 10 != 0])
    n_cols = set([i for i in range(8, 22) if i % 10 != 0])

    img_dir = Path("plots")
    img_dir.mkdir(exist_ok=True)

    used = set()

    for _ in range(n_plots):
        fig = plt.figure(figsize=(18, 20), dpi=fig_dpi)

        r = random.choice(list(n_rows))
        c = random.choice(list(n_cols))

        dims = (r, c)
        while dims in used:
            r = random.choice(list(n_rows))
            c = random.choice(list(n_cols))

        used.add(dims)

        # mi = choices(m_indices, k=1)[0]
        # print(f"selected marker: {markers[mi]}")

        ax = fig.gca()
        assert isinstance(ax, matplotlib.axes.Axes)
        icon, icon_idx = get_random_image(fig_dpi=fig_dpi)

        x2d, y2d = np.meshgrid(range(c), range(r))

        ax.scatter(x2d, y2d, c="none")

        for x in range(c):
            for y in range(r):
                icon.image.axes = ax
                ab = AnnotationBbox(icon, (x, y),
                                    frameon=False,
                                    pad=0.0)
                ax.add_artist(ab)


        # ax.set_title(f"{r}x{c}x{mi}")
        # ax.scatter(x, y, marker=markers[mi], s=900)


        ax.set_axis_off()

        instructions = """
            Approximation: ________;  Réponse: ________
            
            Indice: arranger en groupes de dix, le nombre de ces 
            groupes vous donne le nombre de groupes (dizaines). 
            Calculez l'approximation en utilisant 
            seulement le nombre de dizaines.
        """

        ax.annotate(instructions,
                    xy=(0, 0),
                    va="top",
                    ha="left",
                    xycoords=ax.transAxes, fontsize=30)

        img = img_dir / Path(f"{r}x{c}_{icon_idx}.pdf")
        fig.savefig(img, bbox_inches="tight")
        plt.close(fig)


if __name__ == '__main__':
    main()
