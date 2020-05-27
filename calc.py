import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
class MainApp(App):
    def build(self):
        a_layout=BoxLayout(orientation="vertical",
                           size_hint=(1, 1),
                           padding=20)
        a_layout.add_widget(Label(text="Download",
                                  size_hint=(1, 0.1)))
        b_layout = BoxLayout(size_hint=(1, 0.1))
        self.solution = TextInput(text="",
                                  size_hint=(0.8, 1))
        b_layout.add_widget(self.solution)
        b_layout.add_widget(Button(text='Ok',
                                   size_hint=(0.2, 1),
                                   on_press=self.download))
        a_layout.add_widget(b_layout)
        self.output = TextInput(text="",
                                size_hint=(1, 0.3))
        a_layout.add_widget(self.output)
        a_layout.add_widget(Label(text="Ploting",
                                  size_hint=(1,0.1)))
        c_layout=BoxLayout(size_hint=(1,0.1))
        c_layout.add_widget(Button(text="Plot E-I",
                                   on_press=self.Plot_E_I))
        c_layout.add_widget(Button(text="Plot lg(i)-E",
                                   on_press=self.Plot_lg_i_E))
        self.potetial=TextInput()
        c_layout.add_widget(self.potetial)
        c_layout.add_widget(Button(text="Plot linear section",
                                   on_press=self.Plot_linear_section))
        a_layout.add_widget(c_layout)
        i_layout=BoxLayout(size_hint=(1,0.3))
        self.image1=Image(source="",
                          size_hint=(0.333,1),
                          pos_hint={'center_x':.5, 'center_y':.5})
        self.image2 = Image(source="",
                            size_hint=(0.333, 1),
                            pos_hint={'center_x':.5, 'center_y':.5})
        self.image3 = Image(source="",
                            size_hint=(0.333, 1),
                            pos_hint={'center_x':.5, 'center_y':.5})
        i_layout.add_widget(self.image1)
        i_layout.add_widget(self.image2)
        i_layout.add_widget(self.image3)
        a_layout.add_widget(Button(text="Tafel equation parameters",
                                   size_hint=(1,0.1),
                                   on_press=self.Tafel_equation_parameters))
        self.parameters=TextInput(size_hint=(1,0.1))
        a_layout.add_widget(self.parameters)
        #a_layout.add_widget(i_layout)
        return a_layout
    def download(self, instence):
        text = self.solution.text
        self.data = np.genfromtxt(r''+text+'.txt', skip_header=7, delimiter='')
        self.output.text=str(self.data)
        return
    def Plot_E_I(self,instence):
        n = 0
        for i in self.data[:, 2]:
            if i > 0 or i == 0: n += 1
            if i < 0: break
        E = [i / 1000 for i in self.data[n:, 1]]
        i = [i / 1000000 for i in self.data[n:, 2]]
        ###
        plt.figure(figsize=(5, 5))
        ax1 = plt.subplot()
        ax1.plot(E, i)
        plt.xlabel('E, B')
        plt.ylabel('i, A')
        plt.show()
        return
    def Plot_lg_i_E(self,instence):
        n = 0
        for i in self.data[:, 2]:
            if i > 0 or i == 0: n += 1
            if i < 0: break
        E = [i / 1000 for i in self.data[n:, 1]]
        i = [i / 1000000 for i in self.data[n:, 2]]
        ###
        plt.figure(figsize=(5, 5))
        ax2 = plt.subplot()
        lgi = []
        for j in i:
            lgi.append(np.log10(-1 * j))
        ax2.plot(lgi, E)
        plt.xlabel('lg(i)')
        plt.ylabel('E, B')
        plt.show()
        return
    def Plot_linear_section(self,instence):
        pt= str(self.potetial.text)
        n = 0
        for i in self.data[:, 1]:
            if i > int(pt):
                n += 1
            if i < int(pt):
                break
        i1 = [i / 1000000 for i in self.data[n:, 2]]
        lgi1 = []
        for j in i1:
            lgi1.append(np.log10(-1 * j))
        E1 = [-1 * i / 1000 for i in self.data[n:, 1]]
        z_1 = np.polyfit(lgi1, E1, 1)
        y_2 = np.poly1d(z_1)(lgi1)
        plt.figure(figsize=(5, 5))
        ax3 = plt.subplot()
        ax3.plot(lgi1, E1)
        plt.xlabel('lg(i)')
        plt.ylabel('-E, B')
        ax3.plot(lgi1, y_2, "r--", lw=1)
        text = f"$y={z_1[0]:0.4f}\;x{z_1[1]:+0.4f}$\n$R^2 = {r2_score(E1, y_2):0.3f}$"
        plt.gca().text(0.05, 0.8, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
        self.p=[('a='),z_1[1],'\n', ('b='), z_1[0],'\n','Exchange current:', (10**(-1*z_1[1]/z_1[0])),'\n', 'transfer constant:', (2.3*8.314*298/(96495*z_1[0])) ]
        #self.p=[('a', 'b', 'Exchange_current', 'transfer_constant'),(z_1[1], z_1[0], (10**(-1*z_1[1]/z_1[0])),(2.3*8.314*298/(96495*z_1[0])))]
        plt.show()
    def Tafel_equation_parameters(self, instence):
        self.parameters.text=str(self.p)
        return
if __name__ == "__main__":
    app = MainApp()
    app.run()
