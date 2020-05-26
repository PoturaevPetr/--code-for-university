import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from impedance.plotting import plot_nyquist
from impedance.plotting import plot_bode
from impedance.circuits import CustomCircuit
from sklearn.metrics import r2_score
DAT=[]
while True:
    n = float(input("Потенциал ",))
    if n==000:
        break
    if n!= 0:
        # READ EXPERIM ENT
        data = np.genfromtxt('Impedance -' + str(n) + '.z', skip_header=123, delimiter='')
        data = data[:52]
        frequencies = data[:, 0]
        Z = data[:, 4] + 1j * data[:, 5]
        frequencies = frequencies[np.imag(Z) < 0]
        Z = Z[np.imag(Z) < 0]
        ############## FIG. B
        circuitB = 'R0-p(E, R1-p(C1,R2,W1))'
        initial_guessB = [1, 1, 1, 1000, 1, 100, 1, 1]
        circuitB = CustomCircuit(circuitB, initial_guess=initial_guessB)
        circuitB.fit(frequencies, Z)
        circuitB.parameters_
        print("Схема Б", circuitB)
        P = [-1 * n, m.log10(circuitB.parameters_[3]), m.log10(circuitB.parameters_[4]), m.log10(circuitB.parameters_[5])]
        # ФИТТИНГ
        Z_fitB = circuitB.predict(frequencies)
        # Погрешность
        res_meas_real = (Z - circuitB.predict(frequencies)).real / np.abs(Z)
        res_meas_imag = (Z - circuitB.predict(frequencies)).imag / np.abs(Z)
        # ploting
        plt.figure(figsize=(6, 6))
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222)
        ax3 = plt.subplot(223)
        ax4 = plt.subplot(224)
        #GRAFS
        plot_bode(axes=(ax1, ax2), f=frequencies, Z= Z, fmt='o')
        plot_bode(axes=(ax1, ax2), f=frequencies, Z=Z_fitB)
        plot_nyquist(ax3, frequencies, Z, fmt='o')
        plot_nyquist(ax3, frequencies, Z_fitB)
        #ERROR
        ax4.plot(frequencies, res_meas_real, '-', label=r'$\Delta_{\mathrm{Real}}$')
        ax4.plot(frequencies, res_meas_imag, '-', label=r'$\Delta_{\mathrm{Imag}}$')
        ax4.set_title('Measurement Model Error', fontsize=12)
        ax4.tick_params(axis='both', which='major', labelsize=12)
        ax4.set_ylabel('$\Delta$ $(\%)$', fontsize=10)
        ax4.set_xlabel('$f$ [Hz]', fontsize=10)
        ax4.set_xscale('log')
        ax4.set_ylim(-.1, .1)
        ax4.legend(loc=1, fontsize=10, ncol=2)
        vals = ax4.get_yticks()
        ax4.set_yticklabels(['{:.0%}'.format(x) for x in vals])
        plt.tight_layout()
        plt.show()
        # VRITE
        p = input('Записать значения ')
    #для вывода
        if p == '+':
            DAT.append(P)
            dat=pd.DataFrame(DAT)
            dat.columns = ['E','R1','C1','R2']
            E=dat['E']
            R1=dat['R1']
            C2=dat['C1']
            R2=dat['R2']
            print(dat)
        if p == '0':
            continue
        if p == '-':
            print(dat)
            break
par=input('Построить зависимости Х от Е? ')
#trend
z_R1 = np.polyfit(E, R1, 1)
y_R1 = np.poly1d(z_R1)(E)
#
z_C1 = np.polyfit(E, C2, 1)
y_C1 = np.poly1d(z_C2)(E)
#
z_R2 = np.polyfit(E, R2, 1)
y_R2 = np.poly1d(z_R2)(E)
if par=='+':
    plt.figure();
    # plotting trend and parameters
    #R1
    dat.plot(x=0, y=1, ax=plt.subplot(221))
    plt.plot(E, y_R1, "r--", lw=1)
    text = f"$y={z_R1[0]:0.4f}\;x{z_R1[1]:+0.4f}$\n$R^2 = {r2_score(dat['R1'], y_R1):0.3f}$"
    plt.gca().text(0.05, 0.8, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
    #C1
    dat.plot(x=0, y=2, ax=plt.subplot(222))
    plt.plot(E, y_C1, "r--", lw=1)
    text = f"$y={z_C1[0]:0.4f}\;x{z_C1[1]:+0.4f}$\n$R^2 = {r2_score(dat['C1'], y_C1):0.3f}$"
    plt.gca().text(0.05, 0.8, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
    #R2
    dat.plot(x=0, y=3, ax=plt.subplot(223))
    plt.plot(E, y_R2, "r--", lw=1)
    text = f"$y={z_R2[0]:0.4f}\;x{z_R2[1]:+0.4f}$\n$R^2 = {r2_score(dat['R2'], y_R2):0.3f}$"
    plt.gca().text(0.05, 0.8, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
    plt.show()