# -*- coding: utf-8 -*-
# importamos las librerías necesarias
import sympy as sp
import numpy as np

class MatrixRob():

    def __init__(self):
        return

    def symTfromDH(self,theta, d, a, alpha):

        # theta y alpha en radianes
        # d y a en metros
        Rz = sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0, 0],
                    [sp.sin(theta), sp.cos(theta), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        tz = sp.Matrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, d],
                    [0, 0, 0, 1]])
        ta = sp.Matrix([[1, 0, 0, a],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        Rx = sp.Matrix([[1, 0, 0, 0],
                    [0, sp.cos(alpha), -sp.sin(alpha), 0],
                    [0, sp.sin(alpha), sp.cos(alpha), 0],
                    [0, 0, 0, 1]])
        T = Rz*tz*ta*Rx
        return T

    def cinematica_dir(self, a, b, c):

        # Descricao do robo
        # Rotacao Graus |      x      |      y      |     z
        # ---------------------------------------------------------
        #      q1       |    0.000    |   0.000    |     0.000     | junta rotativa base  (Rz)
        #      q2       |    0.000    |   0.000    |     0.000     | junta rotativa elo 1 (Rx)
        #      q3       |    0.000    |   0.000    |     0.000     | junta rotativa elo 2 (Rx)
        # ---------------------------------------------------------
        #      0         |    0       |     0       |     0         | sobra ferramenta

        # Posicoe de partida servos (graus)
        m1 = 0
        m2 = 0
        m3 = 0

        # Mecanismo 4 barras
        # c = b - c

        # print(a, b, c)

        q1 = (a+m1)*np.pi/180
        q2 = (b+m2)*np.pi/180      
        q3 = (c+m3)*np.pi/180

        # Comprimento elos
        # x1 = 3.475
        x1 = 5
        x2 = 8.18
        x3 = 8.08

        # Rotacao base
        Rz = np.matrix([[np.cos(q1), -np.sin(q1), 0, 0],
                        [np.sin(q1), np.cos(q1), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # Comprimento base
        tz = np.matrix([[1, 0, 0, 2.5],
                        [0, 1, 0, -1.75],
                        [0, 0, 1, x1],
                        [0, 0, 0, 1]])

        # Rotacao junta 1
        Ry1 = np.matrix([[np.cos(q2), 0, np.sin(q2), 0], 
                    [0, 1, 0, 0],
                    [-np.sin(q2), 0, np.cos(q2), 0],
                    [0, 0, 0, 1]])

        Ry1 = np.linalg.inv(Ry1)

        # Comprimento elo 1
        tx1 = np.matrix([[1, 0, 0, (-1)*x2],
                        [0, 1, 0, 1.75],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # Rotacao junta 2
        Ry2 = np.matrix([[np.cos(q3), 0, -np.sin(q3), 0], 
                    [0, 1, 0, 0],
                    [np.sin(q3), 0, np.cos(q3), 0],
                    [0, 0, 0, 1]])

        # Comprimento elo 2
        tx2 = np.matrix([[1, 0, 0, 10.68],
                        [0, 1, 0, 3.5],
                        [0, 0, 1, 2.5],
                        [0, 0, 0, 1]])

        # T = Rz*tz*Ry1*tx1*Ry2*tx2
        T = Rz*tz*Ry1*tx1*Ry2*tx2

        # T = sp.simplify(T)

        px = T[0,3]
        py = T[1,3]
        pz = T[2,3]
        print('px: {}; py: {}; pz: {};'.format(px, py, pz))
        return px, py, pz


        

    # def prepara_modelo(self):
            
    #     q1 = sp.symbols('q1')
    #     T01 = symTfromDH(180*((sp.pi)/180), 0.300, 0.400, q1)
    #     # T01

    #     q2 = sp.symbols('q2')
    #     T12 = symTfromDH(q2, -0.05, 0.400, 180*((sp.pi)/180))
    #     # T12

    #     q3 = sp.symbols('q3')
    #     T23 = symTfromDH(q3, -0.05, 0.400, 180*((sp.pi)/180))
    #     # T23

    #     T3e = symTfromDH(0, -0.05, 0, 0)
    #     # T4e

    #     T0e = T01*T12*T23*T3e
    #     # T0e

    #     # verificar simplificacao
    #     T = sp.simplify(T0e)
    #     print('Matriz de transformacao simplificada')
    #     # T[3]
    #     # T[7]
    #     # T[11]
    #     return T

    # def Obter_angulos(self,u,x, y, z, T):
    #     # Definimos un punto de destino
    #     # x = 0.01
    #     # y = 0.1
    #     # z = 0.01
    #     print('Condenadas: ({}, {}, {})'.format(x, y, z))

    #     # preparamos las ecuaciones transformando las expresiones
    #     # de la forma <expresion = valor> a la forma <expresion - valor> = 0
    #     print('As equacoes:')
    #     eq1 = T[3] - x
    #     print('I: {}'.format(eq1))

    #     eq2 = T[7] - y
    #     print('II: {}'.format(eq2))

    #     eq3 = T[11] - z
    #     print('III: {}'.format(eq3))

    #     # enviamos los ángulos a las articulaciones
    #     try:
    #         q1 = sp.symbols('q1')
    #         q2 = sp.symbols('q2')
    #         q3 = sp.symbols('q3')
    #         q = sp.nsolve((eq1, eq2, eq3), (q1, q2, q3), (1, 1, 1))
    #         print('Angulos de entrada')
            
    #     except:
    #         print('Solucao nao encontrada')
    #         q = [0, 0, 0]

    #     return q

    # def obter_cordenadas(self,q1, q2, q3):

    #     T01 = symTfromDH(180*((sp.pi)/180), 0.300, 0.400, q1)
    #     T12 = symTfromDH(q2, -0.05, 0.400, 180*((sp.pi)/180))
    #     T23 = symTfromDH(q3, -0.05, 0.400, 180*((sp.pi)/180))
    #     T3e = symTfromDH(0, -0.05, 0, 0)
    #     T0e = T01*T12*T23*T3e
    #     # print('x:{}, y:{}, z:{}'.format(T0e[3], T0e[7], T0e[11]))
    #     return T0e
    def teste(self):
        print("entrou nesta função")


    def inicia(self, tipo, form, s, v, g):
                    
        T = self.prepara_modelo()
        print(T)

        operacao = tipo # 'inversa' | 'direta'

        if operacao == 0: #'inversa'
            u = form
            x = s
            y = v
            z = g
            q = self.Obter_angulos(u,x, y, z, T)
            print(q)

        if operacao == 1: #'direta'
            q1 = s
            q2 = v
            q3 = g
            T0e = self.obter_cordenadas(q1, q2, q3)
            print('x:{}, y:{}, z:{}'.format(T0e[3], T0e[7], T0e[11]))

        # y verificamos la posición del actuador
        #...CoppeiaSim
