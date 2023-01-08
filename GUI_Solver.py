
import numpy as np
import pyqtgraph as pg

from scipy import linalg
from PyQt6.QtWidgets import QLabel
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtWidgets import QComboBox, QMainWindow, QApplication, QWidget, QVBoxLayout

WIDTH = 1000
HIGHT = 700
DISPLAY_HEIGHT = 500
BUTTON_SIZE = 40
START_POINT = "0"
A = {}
Points = {0: [0, 0]}
j = 0
j_elem = 0
a = int(0)
Forces = {}
constrains = {}
New_point = {0: [0, 0]}
B = {}
Elem_points = {0: [0, 0, 0, 0]}



class AnotherWindow_1(QMainWindow):

    def __init__(self, j):
        super().__init__()

        self.combobox = {}
        self.combobox_label = {}

        box = []
        for i in range(j + 1):
            i = str(i)
            box.extend(['' + i])
        layout = QGridLayout()


        for i in range(j + 1):
            self.combobox_label[box[i]] = QLabel('Point ' + box[i] + ' (' + str(Points[i]) + ')')
            self.combobox[box[i]] = QComboBox()
            self.combobox[box[i]].addItems(['Free', 'Full fix', 'Fix Y', 'Fix X'])
            layout.addWidget(self.combobox[box[i]], i + 1, 2)
            layout.addWidget(self.combobox_label[box[i]], i + 1, 1)

        self.gene = QPushButton("Generate")
        layout.addWidget(self.gene, 0, 1)
        self.gene.clicked.connect(self.constr)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


    def constr(self):

        box = []
        for i in range(j + 1):
            i = str(i)
            box.extend(['' + i])
        licz = 0
        for i in range(j+1):
            box_keys = self.combobox.get(box[i]).currentIndex()
            if box_keys == 0:
                constrains[licz] = 0
                constrains[licz+1] = 0
            elif box_keys == 1:
                constrains[licz] = 1
                constrains[licz+1] = 1

            elif box_keys == 2:
                constrains[licz] = 0
                constrains[licz+1] = 1

            elif box_keys == 3:
                constrains[licz] = 1
                constrains[licz+1] = 0
            licz = licz+2
        constrain = constrains.copy()
        print('Constrains added')




class AnotherWindow(QWidget):

    def __init__(self, j):
        super().__init__()

        self.buttonMap = {}
        self.buttonMap1 = {}
        self.buttonMap2 = {}
        buttonsLayout = QGridLayout()
        keyBoard = []
        for i in range(j + 1):
            i = str(i)
            keyBoard.extend(['' + i])

        for row, key in enumerate(keyBoard):
            self.buttonMap[key] = QLabel('Point ' + key + ' (' + str(Points[row]) + ')')
            # self.buttonMap[key].setFixedSize(2*BUTTON_SIZE, BUTTON_SIZE)
            buttonsLayout.addWidget(self.buttonMap[key], row, 1)
        self.setLayout(buttonsLayout)

        keys = []
        for i in range(2 * (j + 1)):
            i = str(i)
            keys.extend(['' + i])

        z = 0
        for row, key in enumerate(keyBoard):
            for col in range(2):
                self.buttonMap1[keys[z]] = QLineEdit('0')
                buttonsLayout.addWidget(self.buttonMap1[keys[z]], row, col + 2)
                z = int(z)
                z = z + 1
            self.setLayout(buttonsLayout)

        self.gen = QPushButton("Generate")
        buttonsLayout.addWidget(self.gen, row + 1, 3)

        self.gen.clicked.connect(self.power)

    def power(self):
        for i in range(2 * (j + 1)):
            i = str(i)
            Forces[i] = self.buttonMap1[i].text()

        print('Forces added')


class PyCalcWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()

        self.w = None
        self.wind_2 = None  # No external window yet.
        self.setWindowTitle("Solver")
        self.setFixedSize(WIDTH, HIGHT)  # Tu można zmienić wymiary Okna
        self.generalLayout = QVBoxLayout()  # Ogólny sposób wyświeltania rzeczy
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)  # Coś z centralnym widgeten
        self.setCentralWidget(centralWidget)
        self._createDisplay()  # Tutaj wywołanie funkcji odpowiedzielnej za Wyświetlacz// u mnie plot?
        self._createButtons()  # Tutaj wywołanie przycisków

    # FUNKCJE DLA KLASY MAINWINDOW

    def _createButtons(self):
        self.point_1_x = QLineEdit()
        self.point_1_x.setText(START_POINT)
        self.point_1_x.setReadOnly(True)

        self.point_1_y = QLineEdit()
        self.point_1_y.setText(START_POINT)
        self.point_1_y.setReadOnly(True)

        self.point_2_x = QLineEdit()
        self.point_2_y = QLineEdit()

        self.but_generate = QPushButton("Generete")

        self.but_generate.clicked.connect(self.func)
        self.but_generate.clicked.connect(self.licznik)

        self.but_solve = QPushButton("Solve")
        self.but_solve.clicked.connect(self.solver)

        self.but_accept = QPushButton("Add Forces")
        self.but_accept.clicked.connect(self.show_new_window)

        self.but_constrain = QPushButton("Add Constrains")
        self.but_constrain.clicked.connect(self.show_new_window_2)

        # Ustawienie punktów pod wykresem
        buttonsLayout = QGridLayout()
        buttonsLayout.addWidget(self.point_1_x, 0, 1)
        buttonsLayout.addWidget(self.point_1_y, 0, 2)
        buttonsLayout.addWidget(self.but_solve, 0, 3)
        buttonsLayout.addWidget(self.point_2_x, 1, 1)
        buttonsLayout.addWidget(self.point_2_y, 1, 2)
        buttonsLayout.addWidget(self.but_generate, 1, 3)
        buttonsLayout.addWidget(self.but_accept, 2, 3)
        buttonsLayout.addWidget(self.but_constrain, 3, 3)
        self.generalLayout.addLayout(buttonsLayout)

    def _createDisplay(self):
        self.display = pg.PlotWidget()  # QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # Tonie wiem co robi XDDDD
        self.generalLayout.addWidget(self.display)
        self.display.setBackground('w')

    def licznik(self):

        global j
        global Points
        global New_point
        global j_elem

        j = j + 1
        j_elem = j_elem+1

        Elem_points[j_elem] = B.copy()
        print(Elem_points)
        Points[j] = self.func()
        print(j_elem)

        for i in range(j_elem):  # To avoid to much points
            if Elem_points[j_elem] == Elem_points[i]:
                print("Repet elem")
                del Elem_points[j_elem]
                j_elem = j_elem - 1
                break
            else:
                print("New elem")



        for i in range(j):  # To avoid to much points
            if Points[j] == Points[i]:
                print("Repet")
                del Points[j]
                j = j - 1
                break
            else:
                print("New point")

    def func(self):
        global B
        x_1 = float(self.point_1_x.text())
        x_2 = float(self.point_1_y.text())
        x_3 = float(self.point_2_x.text())
        x_4 = float(self.point_2_y.text())
        pen = pg.mkPen(color=(255, 0, 0), width=5)
        self.display.plot([x_1, x_3], [x_2, x_4], pen=pen)
        #pen = pg.mkPen(color=(1, 0, 0), width=5)
        #self.display.plot([x_3, x_3+0.001], [x_4, x_4+0.001], pen=pen)
        B = [x_1, x_2, x_3, x_4]
        x_1 = (self.point_1_x.setText("" + str(x_3)))
        x_2 = (self.point_1_y.setText("" + str(x_4)))
        A = [x_3, x_4]


        return A

    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow(j)
        self.w.show()

    def show_new_window_2(self, checked):
        if self.wind_2 is None:
            self.wind_2 = AnotherWindow_1(j)
        self.wind_2.show()

    def solver(self):

        A = 0.01 ** 2  # m^2
        E = 205 * (10 ** 9)  # Pa
        global j
        forc = []
        for i in range(2*(j + 1)):
            i = str(i)
            forc.extend(['' + i])
        pts_array=np.zeros((len(Points), 2))
        force_array = np.zeros((len(Forces), 1))
        elem_array = np.zeros((len(Elem_points)-1, 4))
        const_array=np.zeros((len(constrains), 1))


        for i in range(j + 1):
            pts_array[i, 0:2] = np.array(Points[i])

        for i in range(2*(j+1)):
            force_array[i, 0] = np.array(Forces[forc[i]])
            const_array[i, 0] = np.array(constrains[i])

        del Elem_points[0]
        print(elem_array)
        print(Elem_points)
        print(Elem_points[1])
        print(elem_array[0, 0:4])


        for i in range(len(Elem_points)):
            ii=i+1
            print(ii)
            elem_array[i, 0:4]=np.array(Elem_points[ii])
        print(elem_array)

        # Calculation length of elements, sin() and cos()
        raw_ele = len(elem_array)  # Number of raws in elemenst array

        leng = np.zeros((raw_ele, 1))
        s = np.zeros((raw_ele, 1))
        c = np.zeros((raw_ele, 1))
        for i in range(raw_ele):
            leng[i, 0] = np.sqrt(
                (elem_array[i, 2] - elem_array[i, 0]) ** 2 + (elem_array[i, 3] - elem_array[i, 1]) ** 2)
            s[i] = (elem_array[i, 3] - elem_array[i, 1]) / leng[i, 0]
            c[i] = (elem_array[i, 2] - elem_array[i, 0]) / leng[i, 0]

        # Calculation DC matrix
        DC = {}
        for i in range(raw_ele):
            DC[i] = np.array([[c[i, 0], s[i, 0], 0, 0],
                              [-s[i, 0], c[i, 0], 0, 0],
                              [0, 0, c[i, 0], s[i, 0]],
                              [0, 0, -s[i, 0], c[i, 0]]])

        # Definition of K Matrix
        K = np.zeros((4, 4))
        K[0, 0] = 1
        K[0, 2] = -1
        K[2, 0] = -1
        K[2, 2] = 1
        Kp = {}
        Ko = {}
        for i in range(raw_ele):
            Kp[i] = np.array((A * E / leng[i, 0]) * K)
            Ko[i] = np.array(DC[i].conj().transpose() @ Kp[i] @ DC[i])

        # print(Ko[1])
        # Elements numbering
        raw_pts = len(pts_array)
        v1 = np.zeros((len(elem_array), 1))
        v2 = np.zeros((len(elem_array), 1))
        # v1 = {}
        # v2 = {}
        for w in range(raw_pts):
            for j in range(raw_pts):
                for i in range(raw_ele):
                    if elem_array[i, 0] == pts_array[w, 0] and elem_array[i, 1] == pts_array[w, 1] \
                            and elem_array[i, 2] == pts_array[j, 0] and elem_array[i, 3] == pts_array[j, 1]:

                        v1[i, 0] = w
                        v2[i, 0] = j
                        break
                    else:
                        continue
        # Building a stiffness matrix
        p = 3
        ppp1 = v1
        ppp2 = v2
        u1 = v1
        u2 = v2

        ## Przejście z numeru punktu na numer w kolumnie macierzy sztywności
        u1 = u1 * 2
        u2 = u2 * 2

        # Stworzenie macierzy sztywności dla każdego elementu
        KKK = {}
        for i in range(raw_ele):
            KK = np.zeros((2*raw_pts, 2*raw_pts))
            s = Ko[i]
            a = s[0:2, 0:2]
            b = s[0:2, 2:4]

            m1 = int(u1[i, 0])
            m2 = int(u1[i, 0]) + 2
            m3 = int(u2[i, 0])
            m4 = int(u2[i, 0]) + 2


            KK[m1:m2, m1:m2] = a
            KK[m3:m4, m3:m4] = a
            KK[m1:m2, m3:m4] = b
            KK[m3:m4, m1:m2] = b
            KKK[i] = KK

        K_szt = np.zeros((2*raw_pts, 2*raw_pts))
        for i in range(raw_ele):
            K_szt = K_szt + KKK[i]
        # print(K_szt)
        # Podmiana odpowiednich kolumn i wierszy na współrzędne utwierdzeia
        print(const_array)
        for i in range(len(const_array)):  #range(raw_ele):
            if const_array[i, 0] == 0:
                continue
            else:
                x = np.zeros((1, 2*raw_pts))
                x[0, i] = 1
                K_szt[i, :] = x
                x = x.conj().transpose()
                K_szt[:, i] = x[:, 0]
        print(K_szt)
        print(force_array)
        # Policzenie przemieszczeń punków
        ui = linalg.inv(K_szt) @ force_array
        # skalowanie przemieszczeń
        ui = ui * 100
        # print(ui)
        # wyciągnięcie przemieszczeń i zapisaie ich w dwóch zmiennych x1 oraz y1
        x1 = {}
        y1 = {}
        for i in range(len(pts_array)):
            x1[i, 0] = ui[i * 2, 0]
            y1[i, 0] = ui[i * 2 + 1, 0]

        # dodanie przemieszczeń do punktów aby móc narysować wykres
        pi = np.zeros((5, 2))
        for i in range(len(pts_array)):
            pi[i, 0] = pts_array[i, 0] + x1[i, 0]
            pi[i, 1] = pts_array[i, 1] + y1[i, 0]

        # poukłądanie przemiszczonych punktów w takiej konwencji jak macierz
        # elementów wczytaną z txt
        ele = np.zeros((len(elem_array), 4))

        for i in range(len(elem_array)):
            ele[i, 0:2] = pi[int(v1[i, 0]), :].copy()
            ele[i, 2:4] = pi[int(v2[i, 0]), :].copy()

        for i in range(len(elem_array)):
            pen = pg.mkPen(color=(1, 0, 0), width=5)
            self.display.plot([ele[i, 0], ele[i, 2]], [ele[i, 1], ele[i, 3]], pen=pen)

def main():
    """PyCalc's main function."""
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    sys.exit(pycalcApp.exec())


if __name__ == "__main__":
    main()