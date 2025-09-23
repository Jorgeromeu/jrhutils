from typing import List

import matplotlib.pyplot as plt
from PIL import Image


def display_ims_grid(
    images: List[List[Image.Image]],
    scale=2.5,
    col_titles=None,
    row_titles=None,
    title=None,
    show=True,
    vmin=None,
    vmax=None,
):
    images = images.copy()

    # shape
    n_rows = len(images)
    n_cols = len(images[0])

    if row_titles is not None:
        assert len(row_titles) == n_rows

    if col_titles is not None:
        assert len(col_titles) == n_cols

    # make figure
    fig, axs = plt.subplots(
        n_rows, n_cols, figsize=(n_cols * scale, n_rows * scale), squeeze=False
    )

    for row_i in range(n_rows):
        for col_i in range(n_cols):
            ax = axs[row_i, col_i]
            ax.imshow(images[row_i][col_i], vmin=vmin, vmax=vmax)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)

            if row_i == 0 and col_titles is not None:
                ax.set_title(col_titles[col_i])

            if col_i == 0 and row_titles is not None:
                ax.set_ylabel(row_titles[row_i])

    if title is not None:
        fig.suptitle(title)

    plt.tight_layout()

    if show:
        plt.show()
    else:
        return fig, axs


def display_ims(
    images: List[Image.Image],
    scale=3,
    titles=None,
    title=None,
    show=True,
    vmin=None,
    vmax=None,
):
    result = display_ims_grid(
        [images],
        scale,
        col_titles=titles,
        row_titles=None,
        title=title,
        show=show,
        vmin=vmin,
        vmax=vmax,
    )

    if not show:
        fig, axs = result
        return fig, axs[0]

    return result


def max_divisor(n):
    if n <= 1:
        return None  # No proper divisor for 1 or less
    for i in range(n // 2, 0, -1):
        if n % i == 0:
            return i


def reshape_lst_to_rect(lst: List, divisor=None):
    if divisor is None:
        divisor = max_divisor(len(lst))

    chunked = [lst[i : i + divisor] for i in range(0, len(lst), divisor)]
    return chunked