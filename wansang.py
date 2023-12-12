from scipy.io.wavfile import read
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from os import listdir
import random
# from playsound import playsound
import vlc

KeepGoing = True
anotherGraphOrNot = False
oneGraphY_Lt, oneGraphX_Lt = [], []

def drawGridFun():
    wavNp = read("./data/0_a.wav")
    wavNp = np.array(wavNp[1], dtype=float)
    xSeri = [x for x in range(len(wavNp))]
    global oneGraphX_Lt, oneGraphY_Lt
    wavLt = listdir("./data")
    wavLt = [x for x in wavLt if ".wav" in x]
    oneGraphX_Lt = xSeri.copy()

    random.shuffle(wavLt)

    f, axes = plt.subplots(8, 5, figsize=(10, 9))
    plt.subplots_adjust(hspace=0.33)

    axLt, wavPathLt, yLtLt = [], [], []
    ix, iy = 0, 0
    for ii, cWav in enumerate(wavLt[0:40]):
        # if ii == 5: break
        wavPath = 'data/' + cWav
        wavPathLt.append(wavPath)
        # print(wavPath)

        wavNp = read(wavPath)
        wavNp = np.array(wavNp[1], dtype=float)
        yLtLt.append(wavNp)

        cAx = axes[ix, iy]
        axLt.append(cAx)

        wavG = sns.lineplot(x=xSeri, y=wavNp, ax=cAx, color="black")
        wavG.set_ylim(-3000, 3000)
        wavG.set_title(cWav, fontsize=10)

        iy += 1
        if iy == 5:
            ix += 1
            iy = 0

    def onclick_select(event):
        print("I am clicked~~~~~~~~~", event.inaxes)
        singleOrDouble = 's'
        for ii in range(len(axLt)) :
            if event.inaxes == axLt[ii]:
                if event.dblclick:
                    singleOrDouble = 'd'
                    # print("double click~~~~~~~~~~")
                    global KeepGoing, anotherGraphOrNot, oneGraphY_Lt
                    KeepGoing = False 
                    plt.close()
                    # global anotherGraphOrNot
                    oneGraphY_Lt = yLtLt[ii].copy()
                    anotherGraphOrNot = True
                elif singleOrDouble != 'd':     
                    print("~~~~~~~~~~ single click")
                    if axLt[ii].get_facecolor()[0] == 1:
                        axLt[ii].set_facecolor('green')
                        axLt[ii].set_alpha(0)
                    else:
                        axLt[ii].set_facecolor('red')
                        axLt[ii].set_alpha(0)
                    plt.draw()

                    media = vlc.MediaPlayer(wavPathLt[ii])
                    media.play()             

    f.canvas.mpl_connect("button_press_event",onclick_select)

    def ButtonFun(val):
        plt.close()

    buttonAxes = plt.axes([0.81, 0.000001, 0.1, 0.075])
    buttonUpdate = Button(buttonAxes, 'Next Set',color="yellow")
    buttonUpdate.on_clicked(ButtonFun)

    plt.tight_layout()
    plt.show()


def anotherGraphFun():
    # Define initial parameters
    init_amplitude = 5
    init_frequency = 3

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    # line, = ax.plot(t, f(t, init_amplitude, init_frequency), lw=2)
    line, = ax.plot(oneGraphX_Lt, oneGraphY_Lt, lw=2)
    ax.set_xlabel('Time [s]')

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.25)

    # # Make a vertically oriented slider to control the amplitude
    axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
    amp_slider = Slider(
        ax=axamp, label="Amplitude", valmin=0, valmax=10,
        valinit=init_amplitude, orientation="vertical" )

    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata([x*amp_slider.val for x in oneGraphY_Lt])

        fig.canvas.draw_idle()

    # register the update function with each slider
    amp_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, '<- back', hovercolor='0.975')

    def reset(event):
        global KeepGoing, anotherGraphOrNot
        KeepGoing = True
        anotherGraphOrNot = False
        plt.close()
        KeepGoing = True
        anotherGraphOrNot = False
    button.on_clicked(reset)

    plt.show()

while(KeepGoing):
    drawGridFun()
    if anotherGraphOrNot:
        anotherGraphFun()
