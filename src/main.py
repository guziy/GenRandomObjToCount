

import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from random import choices
from matplotlib.markers import MarkerStyle


def main():
    n_plots = 5

    markers = list(MarkerStyle.markers.keys())

    n_rows = list(range(11, 21))
    m_indices = list(range(len(markers)))

    max_n_obj = 150
    min_n_obj = 90
    n_obj = range(min_n_obj, max_n_obj)

    img_dir = Path("plots")
    img_dir.mkdir(exist_ok=True)

    for _ in range(n_plots):
        fig = plt.figure(figsize=(18, 20), dpi=100)

        r = choices(n_rows, k=1)[0]
        n = choices(n_obj, k=1)[0]
        c = n // r

        mi = choices(m_indices, k=1)[0]

        y, x = np.meshgrid(range(r), range(c))

        ax = fig.gca()
        # ax.set_title(f"{r}x{c}x{mi}")

        ax.scatter(x, y, marker=markers[mi], s=300)

        ax.set_axis_off()

        instructions = """
            Approximation: ________;  Réponse: ________
            
            Indice: arranger en groupes de dix, le nombre des 
            ces groupes vous donne le nombre de dizaines. 
            Calculez l'approximations en utilisant seulement le nombre de dizaines
        """

        ax.annotate(instructions,
                    xy=(0, 0),
                    va="top",
                    ha="left",
                    xycoords=ax.transAxes, fontsize='xx-large')

        img = img_dir / Path(f"{r}x{c}x{mi}.pdf")
        fig.savefig(img)
        plt.close(fig)




if __name__ == '__main__':
    main()