
def config_ax(ax, xylabels=None, title=None, loc=None):
    """
    Configure appearance of the Matplotlib figure using given axis.
    """

    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.tick_params(color='0.9')

    if xylabels is not None:
        ax.set_xlabel(xylabels[0])
        ax.set_ylabel(xylabels[1])

    if title is not None:
        ax.set_title(title)

    if loc is not None:
        ax.legend(loc=loc)
