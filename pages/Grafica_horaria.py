import streamlit as st
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import math
matplotlib.use('agg')
# plt.rcParams['font.family'] = 'Century Gothic'

def Grafica_horaria():
    st.title("Welcome to Page 1")
    st.write("This is the first page of the Streamlit application.")
    
    # Example of an interactive widget
    nombre=st.text_input("Nombre de la anomalia", value="#1")
    
    
    angulo_inicio=st.number_input("Angulo inicial", min_value=0.0, max_value=360.0, format="%.2f")
    angulo_final=st.number_input("Angulo final",min_value=0.0, max_value=360.0, format="%.2f")
    PM=st.number_input("PM")/100
    

    # if name:
    #     st.write(f"Hello, {name}!")

    def radianes_a_horas(radianes):
        radianes = radianes % (2 * math.pi) # Normalizar los radianes para estar en el rango de 0 a 2π
        horas = (radianes / (2 * math.pi)) * 12 # Convertir radianes a horas   
        horas_completas = int(horas) # Extraer las horas completas
        minutos = (horas - horas_completas) * 60 # Convertir el resto a minutos
        minutos_completos = int(minutos)
        segundos = (minutos - minutos_completos) * 60 # Convertir el resto a segundos
        segundos_completos = int(round(segundos,0))
        return horas_completas, minutos_completos, segundos_completos

    def graficar(angulo_inicio,angulo_final,nombre,PM):
        nombre=nombre.upper()
        if angulo_final-angulo_inicio<0:
            angulo_inicio=-360+angulo_inicio
        angulo=((angulo_final)+(angulo_inicio))/2
        # Centro del defecho en grados (ejemplo: 45*np.pi/180)
        theta= angulo * np.pi/180
        width = np.pi*(angulo_final-angulo_inicio)/180
        radii = .5
        # fig, ax = plt.subplot(111, polar=True)
        fig,ax=plt.figure(figsize=(6,6)), plt.subplot(111, polar=True) 
        bars = ax.bar(theta, radii, width=width, bottom=6.5, color='red')
        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_yticklabels([])
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        ax.set_ylim(0,ax.get_rmax())
        ax.tick_params(axis='x', which='major', pad=7)
        ax.axhline(y=6, color='black', linestyle='-', linewidth=3)
        ax.axhline(y=7, color='black', linestyle='-', linewidth=3)
        ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
        ax.set_xticklabels(['12:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30'])
        plt.gcf().canvas.draw()
        angles = np.linspace(0,2*np.pi,len(ax.get_xticklabels())+1)
        angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
        angles = np.rad2deg(angles)
        labels = []
        for label, angle in zip(ax.get_xticklabels(), angles):
            angle=float(label.get_text().split(':')[0])*360/12+float(label.get_text().split(':')[1])*(360/(12*60))
            # print(label.get_text(),angle )
            x,y = label.get_position()
            lab = ax.text(x,y, label.get_text(), transform=label.get_transform(),
                        ha=label.get_ha(), va=label.get_va())
            if angle<180 or angle==360:
                lab.set_rotation(90-angle)
            else:
                lab.set_rotation(-90-angle)
            labels.append(lab)
        ax.set_xticklabels([])
        ax.set_title(f'Anomalía: {nombre}', va='bottom', pad=35)
        ax.plot([0, theta - width / 2], [0, 6.5], color='gray', linestyle='--', linewidth=.5)
        ax.plot([0, theta + width / 2], [0, 6.5], color='gray', linestyle='--', linewidth=.5)
        horas_ini_f=radianes_a_horas(theta - width / 2)
        horas_fin_f=radianes_a_horas(theta + width / 2)
        A='Horario inicial: {:02}:{:02}:{:02}'.format(horas_ini_f[0], horas_ini_f[1], horas_ini_f[2])
        B='Horario final  : {:02}:{:02}:{:02}'.format(horas_fin_f[0], horas_fin_f[1], horas_fin_f[2])
        ax.text(1.1, -0.05,
                f'{A}\n{B}',
                transform=ax.transAxes, 
                ha='right', 
                va='bottom', 
                fontsize=7, 
                color='blue')
        ax.text(.1, -0.05,
            'Corrosión y Protección',
            transform=ax.transAxes, 
            ha='right', 
            va='bottom', 
            fontsize=7, 
            color='blue')
        ax.text(0, 0, f'{round(width * 180 / np.pi, 2)}°', ha='center', va='center', fontsize=10, color='black')
        tick = [ax.get_rmax(),ax.get_rmax()*0.86]
        for t  in np.deg2rad(np.arange(0,360,15)):
            ax.plot([t,t], tick, lw=0.72, color="black")
            
        if angulo<=180:
            rotation =270-round(angulo,2)+180
            pos_y=6-1.6
        else:
            rotation =-90-round(angulo,2)
            pos_y=6-.3
        # Finally add the labels
        ax.text(
            x=theta, 
            y=pos_y, 
            s=f'{PM:.2%}', 
            ha="left", 
            va='center', 
            rotation=rotation, 
            rotation_mode="anchor") 
        logo = plt.imread(r"C:\Users\croos\OneDrive\Escritorio\Logos\Logo Corrosion 2019\logo solo circulo CPI Nuevo2.png")
        imagebox = OffsetImage(logo, zoom=0.6)
        ab = AnnotationBbox(imagebox, (-.05,1.11), frameon=False, xycoords='axes fraction')
        ax.add_artist(ab)
        ax.fill_between(np.linspace(0, 2 * np.pi, 100), 6, 7, color='lightgray', alpha=1, zorder=-2)
        plt.gcf().canvas.draw()
        plt.savefig('images\\fig.png')  # Save the figure as an image
        plt.close()
        print('Figure saved')
        return 'images/fig.png'
    
    if angulo_final and nombre and PM:
        graficar(angulo_inicio,angulo_final,nombre,PM)
    
        # Display the saved figure in Streamlit
        st.image('images/fig.png', caption='Generated Plot', use_container_width=True)
    
    # Example of a chart
    # st.line_chart([1, 2, 3, 4, 5])

if __name__ == "__main__":
    Grafica_horaria()