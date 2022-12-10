# -*- coding: utf-8 -*-
# importamos las librerías necesarias
import sympy as sp
import numpy as np
import math

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

    def cinematica_dir(self, a, b, c,ret_T=False):

        # Descricao do robo
        # Rotacao Graus |      x      |      y      |     z
        # ---------------------------------------------------------
        #      q1       |    0.000    |   0.000    |     0.000     | junta rotativa base  (Rz)
        #      q2       |    0.000    |   0.000    |     0.000     | junta rotativa elo 1 (Rx)
        #      q3       |    0.000    |   0.000    |     0.000     | junta rotativa elo 2 (Rx)
        # ---------------------------------------------------------
        #      0         |    0       |     0       |     0         | sobra ferramenta

        print('Teta1: {}; Teta2: {}; Teta3: {};'.format(a, b, c))

        # Posicoe de partida servos (graus)
        m1 = 180 #corrigindo valor das coordenadas...
        m2 = 0
        m3 = -135
        m4 = 0
        
        # Mecanismo 4 barras
        # c =  (b - c)
        # c +=b

        # c *=-1
        # b = b * (-1)
        # print(a, b, c)

        q1 = (a+m1)*np.pi/180
        q2 =(b+m2)*np.pi/180      
        q3 = (c+m3)*np.pi/180
        q4 = (b-180+m4)*np.pi/180

        # Comprimento elos
        # x1 = 3.475
        x1 = 5.2
        x2 = 8.18
        x3 = 8.08
        # x3 = 13.58

        # Rotacao base
        Rz = np.matrix([[np.cos(q1), -np.sin(q1), 0, 0],
                        [np.sin(q1), np.cos(q1), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # Comprimento base
        tz = np.matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0  ],
                        [0, 0, 1, x1 ],
                        [0, 0, 0, 1  ]])

        # Rotacao junta 1
        pr = np.matrix([[np.cos(q2), 0, np.sin(q2), 0], 
                    [0, 1, 0, 0],
                    [-np.sin(q2), 0, np.cos(q2), 0],
                    [0, 0, 0, 1]])

        Ry1 = np.linalg.inv(pr)

        # Comprimento elo 1
        tx1 = np.matrix([[1, 0, 0, x2],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # Rotacao junta 2
        Ry2 = np.matrix([[np.cos(q3), 0, np.sin(q3), 0], 
            [0, 1, 0, 0],
            [-np.sin(q3), 0, np.cos(q3), 0],
            [0, 0, 0, 1]])

        Ry3 = np.matrix([[np.cos(q4), 0, np.sin(q4), 0], 
                    [0, 1, 0, 0],
                    [-np.sin(q4), 0, np.cos(q4), 0],
                    [0, 0, 0, 1]])



        # Comprimento elo 2
        # tx2 = np.matrix([[1, 0, 0, 10.68],
        #                 [0, 1, 0, 3.5],
        #                 [0, 0, 1, 2.5],
        #                 [0, 0, 0, 1]])

        tx2 = np.matrix([[1, 0, 0, x3],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

    

        # T = Rz*tz*Ry1*tx1*Ry2*Ry3*tx2
        # T = Rz*tz*Ry1*tx1*Ry2*Ry3*tx2

        z = np.dot(tz, Rz)
        f = np.dot(z,Ry1)
        xone= np.dot(f,tx1)
        yone=np.dot(xone,Ry2)
        zone = np.dot(yone,Ry3)
        T_fim=np.dot(zone,tx2)
        
        T = tz*Rz*Ry1*tx1*Ry2*Ry3*tx2
        # T = sp.simplify(T)

        px = T[0,3]
        py = T[1,3]
        pz = T[2,3]
        print('q1: {}; q2: {}; q3: {} q4: {};'.format(q1*180/np.pi, q2*180/np.pi, q3*180/np.pi,q4*180/np.pi))
        print('px: {}; py: {}; pz: {};'.format(px, py, pz))
        if ret_T == False:
            return px, py, pz
        else:
            return T

    def cinematica_inv(self,method,px,py,pz,T):
        
        alfa = 0
        beta = 0
        gama = 0

        T[0,3] = px
        T[1,3] = py
        T[2,3] = pz
        
        print("T:\n",T)
        if method == "RAG":
            print("[cinematica_inv] method: RAG")
            nx = T[0,0]
            ny = T[1,0]
            nz = T[2,0]
            ox = T[0,1]
            oy = T[1,1]
            ax = T[0,2]
            ay = T[2,2]

            print('nx: {}; ny: {}; nz: {};'.format(nx, ny, nz))
            alfa = math.atan2(ny,nx)*180/math.pi
            alfa1 = alfa + 180
            beta = math.atan2(-nz,(nx*np.cos(alfa*np.pi/180) + ny*np.sin(alfa*np.pi/180)))*180/math.pi
            beta1 = beta + 180
            gama = math.atan2((-ay*np.cos(alfa*np.pi/180) + ax*np.sin(alfa*np.pi/180)),(oy*np.cos(alfa*np.pi/180) - ox*np.sin(alfa*np.pi/180)))*180/math.pi
            gama1 = gama + 180
            # print("Alfa:{}; Alfa1:{}".format(alfa,alfa1))
            # print("Beta:{}; Beta1:{}".format(beta,beta1))
            # print("Gama:{}; Gama1:{}".format(gama-90,gama1))
        elif method == "Euler":
            print("[cinematica_inv] method: Euler")
            nx = T[0,0]
            ny = T[1,0]
            nz = T[2,0]
        elif method == "DH":
            print("[cinematica_inv] method: DH")
            nx = T[0,0]
            ny = T[1,0]
            nz = T[2,0]
        else:
            print("[cinematica_inv] method: INVALID")
            alfa = 90
            beta = 90
            gama = 90

        print('Alfa: {}; Beta: {}; gama: {};'.format(alfa, beta+45, gama-90))
        return alfa, beta+45, gama-90
 


        

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
