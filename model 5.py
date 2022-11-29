import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from scipy import stats
from scipy.integrate import quad
from scipy.special import rel_entr


# probability dist. function 1
def pdf1(m, s, x):
    return stats.norm(m, s).pdf(x)


# probability dist. function 2
def pdf2(m2, s2, x):
    return stats.norm(m2, s2).pdf(x)


def KL(m, s, x, m2, s2):
    return pdf1(m, s, x) * np.log(pdf1(m, s, x) / pdf2(m2, s2, x))

# time
x = np.linspace(-25, 25, 1000)

# initial parameters
init_m = 2
init_s = 3
init_m2 = 2
init_s2 = 3

# plots to be manipulated
fig, ax = plt.subplots()
line, = ax.plot(x, pdf1(x, init_m, init_s), color='royalblue', lw=2)
line2, = ax.plot(x, pdf2(x, init_m2, init_s2), color='crimson', lw=2)
plt.title('KL(Blue||Red) = 0')
ax.grid(True)
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.set_xlim(0, 10)
ax.set_ylim(0, 0.25)
# ax.set_xlabel('Distance')
# ax.set_ylabel('Probability')
# ax.set_facecolor('light gray')



# adjusting the room
fig.subplots_adjust(left=0.25, bottom=0.25)

# sliders for Std Deviation
axstd = fig.add_axes([0.25, 0.1, 0.65, 0.03])
std_slider = Slider(
    ax=axstd, color='royalblue', label='Std Dev Blue', valmin=0, valmax=10, valinit=init_s)

axstd2 = fig.add_axes([0.25, 0.15, 0.65, 0.03])
std_slider2 = Slider(
    ax=axstd2, color='crimson', label='Std Dev Red', valmin=0, valmax=10, valinit=init_s2)

# sliders for Mean
axmean = fig.add_axes([0.08, 0.25, 0.0225, 0.63])
mean_slider = Slider(
    ax=axmean, color='royalblue', label="Expected", valmin=0, valmax=5, valinit=init_m, orientation="vertical")

axmean2 = fig.add_axes([0.13, 0.25, 0.0225, 0.63])
mean_slider2 = Slider(
    ax=axmean2, color='crimson', label="Val", valmin=0, valmax=5, valinit=init_m2, orientation="vertical")


# the slider function
def update(val):
    line.set_ydata(pdf1(x, mean_slider.val, std_slider.val))
    line2.set_ydata(pdf1(x, mean_slider2.val, std_slider2.val))
    ax.set_title('KL(Blue||Red) = %1.3f nats' % sum(rel_entr(stats.norm(mean_slider.val, std_slider.val).pdf(x),
                                                   stats.norm(mean_slider2.val, std_slider2.val).pdf(x))),
                 fontsize='15')

    fig.canvas.draw_idle()


# register the update function with each slider
std_slider.on_changed(update)
std_slider2.on_changed(update)
mean_slider.on_changed(update)
mean_slider2.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color="lightgray", hovercolor='0.975')


def reset(event):
    std_slider.reset()
    std_slider2.reset()
    mean_slider2.reset()
    mean_slider.reset()


button.on_clicked(reset)

plt.show()
