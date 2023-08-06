# figures other than from PIR book

import numpy as np
# from numpy import roll
import scipy.stats as ss
from scipy.fft import rfft, irfft # , fftshift, ifftshift, fft, ifft
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib as mpl
from .. import build
from .. constants import FIG_H, FIG_W


def adjusting_layer_losses():
    """
    Figure to illustrate the process of adjusting layer losses.
    TODO: Add reference

    """
    f, ax = plt.subplots(1, 1, figsize=(FIG_H, FIG_W), constrained_layout=True)
    fz = ss.lognorm(.4)
    xs = np.linspace(0, fz.isf(1e-3), 1001, endpoint=False)
    F = fz.cdf(xs)
    ax.plot(F, xs)
    a1 = 1.5
    a0 = 1
    ax.axhline(a1, c='k', lw=.25)
    ax.axhline(a0, c='k', lw=.25)
    p0 = fz.cdf(a0)
    p1 = fz.cdf(a1)
    ax.plot([p0, p0], [0, a0], c='k', lw=.25)
    ax.plot([p1, p1], [0, a1], c='k', lw=.25)
    ax.set_xticks([0, p0, p1, 1])
    ax.set_xticklabels(['0', '$F(a_{i-1})$', '$F(a_{i})$', ''])
    ax.set_yticks([0, a0, a1, 3.5])
    ax.set_yticklabels(['0', '$a_{i-1}$', '$a_{i}$', ''])
    ax.text((p0+p1)/2, a0/2, '$f_i$', ha='center', va='center')
    ax.text((1+p1)/2, 1.25, '$e_i$', ha='center', va='center')
    xx = [.8]
    yy = [1.15]
    ll = ['$m_i$']
    ho = -0.2
    vo = 0.55
    ax.set(xlabel='Nonexceedance probability\n$F(x)$', ylabel='Outcome $x$',
           ylim=[0, 3.5], xlim=[-0.05, 1.05],
           title='Lee diagram\n$x$ vs $F(x)$')
    for x, y, l in zip(xx, yy, ll):
        ax.annotate(text=l,
                    xy=(x, y),
                    xytext=(x + ho, y + vo),
                    arrowprops={'arrowstyle': '->', 'linewidth': .5}
                    )
    return f


def savings_charge():
    """
    Figure to illustrate the insurance savings and expense(charge).

    """
    f, ax = plt.subplots(1, 1, figsize=(FIG_H, FIG_W), constrained_layout=True)
    fz = ss.lognorm(.4)
    xs = np.linspace(0, fz.isf(1e-3), 1001, endpoint=False)
    F = fz.cdf(xs)
    ax.plot(F, xs, lw=3)
    a1 = 1.25  # height of line
    ax.axhline(a1, c='C7', lw=1.5)
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_yticks([0, a1, 3.5])
    ax.set_yticklabels(['0', '$r$', ''])
    ax.set(xlabel='Nonexceedance probability', ylabel='Scaled outcome',
           ylim=[0, 3.5], xlim=[0, 1],
           title='Insurance savings and expense')

    xx = [.9, .25]
    yy = [1.05 * a1, .8* a1]
    ll = ['Insurance\ncharge, $\\phi(r)$',
         'Insurance\nsavings, $\\psi(r)$']
    hos = [-0.1, 0.25]
    vos = [1.2, .65]
    ax.text(.5, a1 * .4, '$E[X\\wedge l]$', ha='center', va='center')
    for x, y, l, ho, vo in zip(xx, yy, ll, hos, vos):
        ax.annotate(text=l,
                    xy=(x, y),
                    xytext=(x + ho, y + vo),
                    ha='right',
                    va='bottom',
                    arrowprops={'arrowstyle': '->', 'linewidth': .5}
                    )
    return f


def mixing_convergence(freq_cv, sev_cv, bs=1/64):
    """
    Illustrate convergence of mixed distributions to the mixing distribution.

    """

    # make the two dataframes of distributions
    a = build('agg M '
              '1 claims '
              f'sev gamma 1 cv {sev_cv} '
              f'mixed gamma {freq_cv} ', log2=16, bs=bs, approximation='exact')
    dfnb = a.density_df[['p']].rename(columns={'p': 1})
    assert np.abs(a.est_m / a.agg_m - 1) < 1e-3
    # print("1", a.agg_m, a.est_m, a.est_m / a.agg_m - 1)

    for freq in [2, 5, 10, 20, 50, 100, 200]:
        a = build('agg M '
                  f'{freq} claims '
                  f'sev gamma 1 cv {sev_cv} '
                  f'mixed gamma {freq_cv} ', log2=16, bs=bs, approximation='exact')
        dfnb[freq] = a.density_df[['p']]
        assert np.abs(a.est_m / a.agg_m - 1) < 1e-3
        # print(freq, a.agg_m, a.est_m, a.est_m / a.agg_m - 1)

    a = build('agg M '
              '1 claims '
              f'sev gamma 1 cv {sev_cv} '
              'poisson ', log2=16, bs=bs, approximation='exact')
    dfp = a.density_df[['p']].rename(columns={'p': 1})
    assert np.abs(a.est_m / a.agg_m - 1) < 1e-3
    # print("1", a.agg_m, a.est_m, a.est_m / a.agg_m - 1)

    for freq in [2, 5, 10, 20, 50, 100, 200]:
        a = build('agg M '
                  f'{freq} claims '
                  f'sev gamma 1 cv {sev_cv} '
                  'poisson ', log2=16, bs=bs, approximation='exact')
        dfp[freq] = a.density_df[['p']]
        assert np.abs(a.est_m / a.agg_m - 1) < 1e-3
        # print(freq, a.agg_m, a.est_m, a.est_m / a.agg_m - 1)

    # plotting
    fig, axs = plt.subplots(2, 2, figsize=(
        2 * FIG_W, 2 * FIG_H), constrained_layout=True)
    axi = iter(axs.flat)

    for lbl, df in zip(['Poisson distribution', 'Mixed frequency distribution'], [dfp, dfnb]):
        ax0 = next(axi)
        ax1 = next(axi)
        for c in df:
            ax0.plot(df.index/c, c*df[c],       lw=1, label=str(c))
            ax1.plot(df.index/c, df[c].cumsum(), lw=1, label=str(c))

        if ax0 is axs.flat[0]:
            ax0.legend()
        ax0.set(ylim=[0, 1e-1], xlim=[-0.25, 5])
        ax1.set(ylim=[-0.05, 1.05], xlim=[-0.25, 5])

        ax0.set(ylabel='Density', xlabel='Normalized loss', title=lbl)
        ax1.set(ylabel='Distribution', xlabel='Normalized loss', title=lbl)

    # add convergence to mixing
    alpha = freq_cv**-2
    fz = ss.gamma(alpha, scale=1/alpha)
    ps = np.linspace(0, 5, 501)
    ax = axs.flat[-1]
    ax.plot(ps, fz.cdf(ps), lw=2, alpha=.5, c='k', label='Mixing')
    ax.legend(loc='lower right')


def power_variance_family():
    """
    Graph to illustrate the power variance exponential family distributions.

    Reference: Jørgensen, Bent. 1997. The theory of dispersion models. CRC Press.
    """
    alpha = np.linspace(-2, 2, 101)
    p = (alpha-2) / (alpha-1)
    alphabar = -(alpha+1)
    f, ax = plt.subplots(figsize=(FIG_W * 2, FIG_W * 2))
    ax.plot(alphabar, p, lw=3)
    ax.set(ylim=[-5,10])
    # ax.grid(lw=.25, c='b', alpha=.5)
    ax.axhline(1, c='k', lw=1)
    ax.axhline(0, c='k', lw=1)
    ax.axvline(-2, c='k', lw=.5)
    ax.axvline(-3/2, c='k', lw=0.5, ls='--')
    ax.axhline(3, c='k', lw=0.5, ls='--')
    ax.axhline(2, c='r', lw=1)
    ax.axvline(-1, c='r', lw=1)
    ax.set(xlabel='$\\bar\\alpha=-(\\alpha+1)$, base jump density is $x^{\\bar\\alpha}$',
           ylabel='Variance power function $p$, $V(\\mu)=\\phi\\mu^p$')
    ax.yaxis.set_major_locator(ticker.FixedLocator(np.arange(-4,10)))

    def ql(x, y, t, dot=True, rhs=None):
        ax.text(x + .05, y+0.2, t)
        if dot:
            ax.plot(x,y, 'rd', ms=5)
        else:
            if rhs is None:
                rhs = x + 1
            ax.plot([x, rhs], [y, y], lw=3)

    ql(-3, 0, 'Normal')
    ql(-3, 6, 'Stable', False)
    ql(-2, 9, 'Cauchy')
    ql(-2, -2, 'Pos Stable', False)
    ql(-1.5, 3, 'Stab 3/2\nIG')
    ql(-1, 2, 'Gamma')
    ql(1, 1, 'Poisson')
    ql(-1, -2, 'Tweedie', False, 1)
    ax.set(title='Power Variance Exponential Family Distributions');

