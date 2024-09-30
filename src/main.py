import random

import matplotlib.axes
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from random import choices
from matplotlib.markers import MarkerStyle
from pathlib import Path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import itertools as itt



def get_random_icon_path():
    icons_dir = Path(__file__).parent / "icons"
    icons = list(icons_dir.iterdir())
    icon_idx = random.choice(range(len(icons)))

    return icons[icon_idx], icon_idx


def get_random_image(fig_dpi=100):
    icon_pth, idx = get_random_icon_path()
    return OffsetImage(
        plt.imread(icon_pth, format="png"), zoom=72 / fig_dpi), idx


def get_sample_params(min_len=8, max_len=22, n_obj_min=61, n_obj_max=100, n_plots=10):
    """
    generate kind of random sample params (nrows, ncols_max, n_objects)
    :param max_len: max num of rows/cols
    :param min_len: min num of rows/cols
    :param n_obj_min:
    :param n_obj_max:
    :param n_plots:
    :return:
    """
    rng = range(min_len, max_len + 1)
    n_rows = [i for i in rng if i % 10 != 0]
    n_cols_max = [i for i in rng if i % 10 != 0]
    n_obj = range(n_obj_min, n_obj_max + 1)
    triples = set()

    for r in n_rows:
        for c_max in n_cols_max[::-1]:
            n = random.choice(n_obj)
            triples.add((r, c_max, n))
            if len(triples) > n_plots:
                return triples
    return triples


def main():
    n_plots = 40
    fig_dpi = 100
    img_dir = Path("plots")
    triples = get_sample_params(n_plots=n_plots)
    for t in triples:
        print(t)

    for params in triples:
        fig = plt.figure(figsize=(18, 20), dpi=fig_dpi)

        r, c_max, n = params

        ax = fig.gca()
        assert isinstance(ax, matplotlib.axes.Axes)
        icon, icon_idx = get_random_image(fig_dpi=fig_dpi)

        x2d, y2d = np.meshgrid(range(c_max), range(r))

        ax.scatter(x2d, y2d, c="none")

        for count, (y, x) in enumerate(itt.product(reversed(range(r)), range(c_max))):
            icon.image.axes = ax
            ab = AnnotationBbox(icon, (x, y),
                                frameon=False,
                                pad=0.0)
            ax.add_artist(ab)
            if count >= n - 1:
                break

        ax.set_axis_off()

        instructions = """
            Approximation: ________;  Réponse: ________
            
            Indice: arranger en groupes de dix, le nombre de ces 
            groupes vous donne le nombre de dizaines. 
            Le nombre de dizaines vous donne l'approximation.
        """

        ax.annotate(instructions,
                    xy=(0, 0),
                    va="top",
                    ha="left",
                    xycoords=ax.transAxes, fontsize=30)

        img = img_dir / Path(f"{r}x{c_max}_{n}_{icon_idx}.pdf")
        fig.savefig(img, bbox_inches="tight")
        plt.close(fig)


if __name__ == '__main__':
    main()
