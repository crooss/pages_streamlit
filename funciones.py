def texto(texto):
    return texto.upper()

import math
import shutil
import os
import tempfile
from pathlib import Path
import utm
import matplotlib.ticker as mtick
import matplotlib.image as mpimg


def radianes_a_horas(radianes):
        radianes = radianes % (2 * math.pi) # Normalizar los radianes para estar en el rango de 0 a 2π
        horas = (radianes / (2 * math.pi)) * 12 # Convertir radianes a horas   
        horas_completas = int(horas) # Extraer las horas completas
        minutos = (horas - horas_completas) * 60 # Convertir el resto a minutos
        minutos_completos = int(round(minutos,2))
        segundos = (minutos - minutos_completos) * 60 # Convertir el resto a segundos
        segundos_completos = int(round(segundos,0))
        return horas_completas, minutos_completos, segundos_completos

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
matplotlib.use('agg')

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
        ax.set_theta_direction(-1) # type: ignore
        ax.set_theta_offset(np.pi / 2) # type: ignore
        ax.set_yticklabels([])
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        ax.set_ylim(0,ax.get_rmax()) # type: ignore
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
                        ha=label.get_ha(), va=label.get_va()) # type: ignore
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
        tick = [ax.get_rmax(),ax.get_rmax()*0.86] # type: ignore
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
        logo = plt.imread(r"images/logo solo circulo CPI Nuevo2.png")
        imagebox = OffsetImage(logo, zoom=0.6)
        ab = AnnotationBbox(imagebox, (-.05,1.11), frameon=False, xycoords='axes fraction')
        ax.add_artist(ab)
        ax.fill_between(np.linspace(0, 2 * np.pi, 100), 6, 7, color='lightgray', alpha=1, zorder=-2)
        plt.gcf().canvas.draw()
        plt.savefig('images/fig.png')  # Save the figure as an image
        plt.close()
        print('Figure saved')
        return 'images/fig.png'

def grafica_conductancia(valor, seleccion_tuberia):
    fig, ax = plt.subplots(figsize=(1, 6))
    # Determine the color based on the value
    if seleccion_tuberia=='Tuberías largas con pocas ramificaciones':
        if valor <= 100:
            bar_color = 'green'
        elif valor <= 500:
            bar_color = 'limegreen'
        elif valor <= 1000:
            bar_color = 'yellow'
        elif valor <= 40000:
            bar_color = 'red'   
        else:
            bar_color = 'gray'
    elif seleccion_tuberia=='Distribución de Gas o Agua, con muchas ramificaciones':
        if valor <= 500:
            bar_color = 'green'
        elif valor <= 1000:
            bar_color = 'limegreen'
        elif valor <= 5000:
            bar_color = 'yellow'
        elif valor <= 40000:
            bar_color = 'red'   
        else:
            bar_color = 'gray'

    ax.bar(1, valor, color=bar_color, width=1)
    print(ax.get_xlim())
    minimo_x, maximo_x=ax.get_xlim()
    ax.set_xlim(minimo_x, maximo_x)
    
    if seleccion_tuberia=='Tuberías largas con pocas ramificaciones':
        for each in [100,500,1000,40000]:
            ax.hlines(y=each, xmin=minimo_x, xmax=maximo_x, colors='black', linestyles='-')
        if valor<200000:
            ax.set_ylim(5, 200000)
            additional_yticks = [40000, 500]
        else:
            ax.set_ylim(5, 1000000)
            additional_yticks = [200000,40000, 500]
    elif seleccion_tuberia=='Distribución de Gas o Agua, con muchas ramificaciones':
        for each in [500,1000,5000,40000]:
            ax.hlines(y=each, xmin=minimo_x, xmax=maximo_x, colors='black', linestyles='-')
        if valor<200000:
            ax.set_ylim(5, 200000)
            additional_yticks = [40000, 5000,500]
        else:
            ax.set_ylim(5, 1000000)
            additional_yticks = [200000,40000,5000, 500]    
    ax.set_yscale('log')
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore
    # Crear el mapa de colores
    cmap = ListedColormap(['green', 'limegreen', 'yellow', 'red', 'gray'])
    norm_bins = np.array([0, 1, 2, 3, 4,5])
    norm = matplotlib.colors.BoundaryNorm(norm_bins, cmap.N) # type: ignore
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ticks=[0.5, 1.5, 2.5, 3.5, 4.5], ax=ax, fraction=0.2, pad=0.5)
    
    cbar.ax.set_yticklabels(['Excelente', 'Bueno', 'Regular', 'Pobre', 'Sin Recubrimiento'])
    cbar.ax.set_aspect('auto')

    ax.set_ylabel('Conductancia a 1,000 Ω-cm [μS/m$^2$]')
    ax.get_xaxis().set_visible(False)
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore
    ax.text(2.5, .05, f'Conductancia [μS/m$^2$]:\n{valor:,.0f} μS/m$^2$', ha='left', va='bottom', fontsize=8, color='black', transform=ax.transAxes)
    ax.text(10, .5, 'Table 2.6 CP 4–Cathodic Protection Specialist Course Manual', ha='center', va='center', transform=ax.transAxes, fontsize=8, color='gray', rotation=90)
    ax.set_ylim(1, 1000000)
    plt.savefig('images/barras_CP4.png', dpi=300, bbox_inches='tight')
    return 'images/barras_CP4.png'
 
def tuberias_largas(valor_conductancia):
    x = np.linspace(0.0001, 180, 1000000)  # % de Área Desnuda
    y = np.power(10, 4.03856 + 0.90785 * np.log10(x))

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Dibujar línea principal
    ax.plot(x, y, color='black')

    # Colorear áreas de calidad
    transparencia=1
    ax.fill_between(x, 0, y, where=(y >= 0) & (y <= 100), facecolor='green', alpha=transparencia, label='Excelente', zorder=1) # type: ignore
    ax.fill_betweenx(y, 0, x, where=(y >= 0) & (y <= 100), facecolor='green', alpha=transparencia, zorder=1) # type: ignore

    ax.fill_between(x, 0, y, where=(y >= 100-.1) & (y <= 500), facecolor='limegreen', alpha=transparencia, label='Buena', zorder=0)     # type: ignore
    ax.fill_betweenx(y, 0, x, where=(y >= 100-.1) & (y <= 500), facecolor='limegreen', alpha=transparencia, zorder=0)     # type: ignore
    
    ax.fill_between(x, 0, y, where=(y >= 500) & (y <= 1000), facecolor='yellow', alpha=transparencia, label='Regular')     # type: ignore
    ax.fill_betweenx(y, 0, x, where=(y >= 500) & (y <= 1000), facecolor='yellow', alpha=transparencia)     # type: ignore

    ax.fill_between(x, 0, y, where=(y >= 1000) & (y <= 40000), facecolor='red', alpha=transparencia, label='Pobre') # type: ignore
    ax.fill_betweenx(y, 0, x, where=(y >= 1000) & (y <= 40000), facecolor='red', alpha=transparencia) # type: ignore
    
    ax.fill_between(x, 0, y, where=(y >= 40000), facecolor='gray', alpha=transparencia, label='Bare') # type: ignore
    ax.fill_betweenx(y, 0, x, where=(y >= 40000) & (y <= 1000000), facecolor='gray', alpha=transparencia) # type: ignore

    x_value = x[np.where(y >= valor_conductancia)[0][0]]
    ax.scatter(x_value, valor_conductancia, color='black', zorder=5)  # Coordenadas del punto
    # Anotación de un punto específico con recuadro de fondo blanco
    ax.annotate(f'{valor_conductancia:,.0f} μS/m²\n{x_value:.3f}% bare\n{100-x_value:.3f}% coated', 
            xy=(x_value, valor_conductancia),  # type: ignore
            # arrowprops=dict(facecolor='black', arrowstyle='->'),
            xytext=(7, 70),
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),
            fontsize=8)

    ax.set_xlabel('% de Área Desnuda')
    ax.set_ylabel('Conductancia @1,000 Ω-cm [μS/m$^2$]')
    ax.set_title('Gráfico de Conductancia @1,000 Ω-cm')

    # Escalas logarítmicas
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim(.0001,100)
    
    def ty(num):
        num=round(num*10,5)
        if  num % 2==0:
            return f'{num/10:.0f}%'
        else:
            return f'{num/10:.3f}%'
        
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, ti: ty(x))) # type: ignore
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore
        # Agregar etiquetas adicionales en el eje y
    additional_yticks = [ 40000, 500]
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore
    ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='black')
    ax.legend(loc='best')
    ax.set_ylim(1,1000000)

    ax.text(1.05, .5, 'CP 3–Cathodic Protection Technologist COURSE MANUAL Figure 4-6', ha='center', va='center', transform=ax.transAxes, fontsize=9, color='gray', rotation=90)
    plt.savefig('images/tuberias_largas.png', dpi=300, bbox_inches='tight')
    # plt.show()

def tuberias_distribucion(valor_conductancia):
    x = np.linspace(0.0001, 180, 1000000)  # % de Área Desnuda
    y = np.power(10, 4.03856 + 0.90785 * np.log10(x))

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Dibujar línea principal
    ax.plot(x, y, color='black')

    # Colorear áreas de calidad
    transparencia=1
    ax.fill_between(x, 0, y, where=(y >= 0) & (y <= 500), facecolor='green', alpha=transparencia, label='Excelente', zorder=1)
    ax.fill_betweenx(y, 0, x, where=(y >= 0) & (y <= 500), facecolor='green', alpha=transparencia, zorder=1)

    ax.fill_between(x, 0, y, where=(y >= 500-.1) & (y <= 1000), facecolor='limegreen', alpha=transparencia, label='Buena', zorder=0)    
    ax.fill_betweenx(y, 0, x, where=(y >= 500-.1) & (y <= 1000), facecolor='limegreen', alpha=transparencia, zorder=0)    
    
    ax.fill_between(x, 0, y, where=(y >= 1000) & (y <= 5000), facecolor='yellow', alpha=transparencia, label='Regular')    
    ax.fill_betweenx(y, 0, x, where=(y >= 1000) & (y <= 5000), facecolor='yellow', alpha=transparencia)    

    ax.fill_between(x, 0, y, where=(y >= 5000) & (y <= 40000), facecolor='red', alpha=transparencia, label='Pobre')
    ax.fill_betweenx(y, 0, x, where=(y >= 5000) & (y <= 40000), facecolor='red', alpha=transparencia)
    
    ax.fill_between(x, 0, y, where=(y >= 40000), facecolor='gray', alpha=transparencia, label='Bare')
    ax.fill_betweenx(y, 0, x, where=(y >= 40000) & (y <= 1000000), facecolor='gray', alpha=transparencia)

    x_value = x[np.where(y >= valor_conductancia)[0][0]]
    ax.scatter(x_value, valor_conductancia, color='black', zorder=5)  # Coordenadas del punto
    # Anotación de un punto específico con recuadro de fondo blanco
    ax.annotate(f'{valor_conductancia:,.0f} μS/m²\n{x_value:.3f}% bare\n{100-x_value:.3f}% coated', 
            xy=(x_value, valor_conductancia), 
            # arrowprops=dict(facecolor='black', arrowstyle='->'),
            xytext=(7, 70),
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),
            fontsize=8)

    ax.set_xlabel('% de Área Desnuda')
    ax.set_ylabel('Conductancia @1,000 Ω-cm [μS/m$^2$]')
    ax.set_title('Gráfico de Conductancia @1,000 Ω-cm')

    # Escalas logarítmicas
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim(.0001,100)
    def ty(num):
        num=round(num*10,5)
        if  num % 2==0:
            return f'{num/10:.0f}%'
        else:
            return f'{num/10:.3f}%'
        
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, ti: ty(x)))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        # Agregar etiquetas adicionales en el eje y
    additional_yticks = [ 40000, 5000,500]
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='black')
    ax.legend(loc='best')
    ax.set_ylim(1,1000000)

    ax.text(1.05, .5, 'CP 3–Cathodic Protection Technologist COURSE MANUAL Figure 4-6', ha='center', va='center', transform=ax.transAxes, fontsize=9, color='gray', rotation=90)
    plt.savefig('images/tuberias_distribucion.png', dpi=300, bbox_inches='tight')
    return 'images/tuberias_distribucion.png'
    # plt.show()

def tuberias_TM0102(valor):
    fig, ax = plt.subplots(figsize=(1, 6))
    # Determine the color based on the value
    if valor <= 100:
        bar_color = 'green'
    elif valor <= 500:
        bar_color = 'limegreen'
    elif valor <= 2000:
        bar_color = 'yellow'
    elif valor <= 1000000:
        bar_color = 'red'   

    ax.bar(1, valor, color=bar_color, width=1)
    # print(ax.get_xlim())
    minimo_x, maximo_x=ax.get_xlim()
    ax.set_xlim(minimo_x, maximo_x)
    
    ax.set_yscale('log')
    
    if valor<200000:
        ax.set_ylim(5, 200000)
        additional_yticks = [2000,500]
    else:
        ax.set_ylim(5, 1000000)
        additional_yticks = [2000,500]
    
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore

    # Crear el mapa de colores
    cmap = ListedColormap(['green', 'limegreen', 'yellow', 'red'])
    norm_bins = np.array([0, 1, 2, 3, 4])
    norm = matplotlib.colors.BoundaryNorm(norm_bins, cmap.N) # type: ignore
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ticks=[0.5, 1.5, 2.5, 3.5], ax=ax, fraction=0.2, pad=0.5)
    cbar.ax.set_yticklabels(['Excellent', 'Good', 'Fair', 'Poor'])
    cbar.ax.set_aspect('auto')
    ax.set_ylabel('Conductancia a 1,000 Ω-cm [μS/m$^2$]')
    ax.get_xaxis().set_visible(False)
    for each in [100,500,2000]:
        ax.hlines(y=each, xmin=minimo_x, xmax=maximo_x, colors='black', linestyles='-')
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    if valor<100000:
        ax.set_ylim(5, 1000000)
        additional_yticks = [2000,500]
    else:
        ax.set_ylim(5, 10000000)
        additional_yticks = [2000,500]  
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # type: ignore
    ax.text(2.5, .05, f'Conductancia [μS/m$^2$]:\n{valor:,.0f} μS/m$^2$', ha='left', va='bottom', fontsize=8, color='black', transform=ax.transAxes)
    ax.text(8.5, .5, 'NACE TM0102-2023\nMeasurement of Protective Coating Electrical Conductance on Underground Pipelines\nTable 5 Table of Specific Coating Conductance vs Coating Quality for 1,000 Ω-cm Soil', ha='center', va='center', transform=ax.transAxes, fontsize=8, color='gray', rotation=90)
    plt.savefig('images/barras_TM0102.png', dpi=300, bbox_inches='tight')
    # plt.show()
    return 'images/barras_TM0102.png'
   
#%%
from scipy.interpolate import RegularGridInterpolator # type: ignore
from matplotlib.ticker import MultipleLocator, FuncFormatter # type: ignore
import numpy as np # type: ignore
def mpy_UGLIH(rho,ph):
    if rho>0 and ph>0:
        # Definición de la tabla de valores rho y ph
        rho_values = np.array([10,100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 10000,1000000])  # Valores de rho
        ph_values = np.array([3, 4, 5, 6, 6.5, 7, 7.0001, 7.5, 8, 8.5, 9, 9.5,14])  # Valores de ph

        if rho<10:
            rho=10
        elif rho>1000000:
            rho=1000000
            
        if ph<3:
            ph=3
        elif ph>14:
            return "El ph no puede ser mayor a 14"
        
        # Matriz de valores de la tabla
        data = np.array([
            [22.598, 22.008, 21.535, 20.906, 18.150, 12.795, 32.244, 27.283, 27.283, 27.283, 27.283, 27.283, 27.283],
            [22.598, 22.008, 21.535, 20.906, 18.150, 12.795, 32.244, 27.283, 27.283, 27.283, 27.283, 27.283, 27.283],
            [22.598, 22.008, 21.142, 20.000, 13.268, 10.315, 22.717, 22.323, 22.323, 22.323, 22.323, 22.323, 22.323],
            [22.598, 22.008, 20.984, 18.386, 11.417, 8.898, 18.110, 16.614, 16.614, 16.614, 16.614, 16.614, 16.614],
            [22.598, 22.008, 20.669, 16.575, 10.315, 7.874, 15.472, 13.504, 13.504, 13.504, 13.504, 13.504, 13.504],
            [22.598, 21.575, 19.252, 14.528, 9.213, 7.087, 12.520, 9.567, 9.606, 9.449, 9.449, 9.449, 9.449],
            [21.969, 18.583, 14.843, 12.441, 7.559, 4.882, 5.315, 4.921, 4.630, 4.630, 4.630, 4.630, 4.630],
            [15.276, 13.465, 11.850, 9.449, 5.512, 3.528, 4.685, 3.752, 3.469, 3.394, 3.386, 3.366, 3.366],
            [13.740, 12.087, 10.197, 8.031, 4.213, 2.528, 3.724, 3.075, 2.606, 2.406, 2.299, 2.252, 2.252],
            [12.598, 10.669, 9.213, 7.008, 3.134, 1.394, 2.953, 1.906, 0.835, 0.039, 0.039, 0.039, 0.039],
            [11.929, 10.039, 8.622, 6.142, 2.650, 0.815, 2.606, 1.394, 0.206, 0.039, 0.039, 0.039, 0.039],
            [11.102, 9.370, 7.874, 5.315, 2.217, 0.013, 2.079, 0.380, 0.039, 0.039, 0.039, 0.039, 0.039],
            [11.102, 9.370, 7.874, 5.315, 2.217, 0.013, 2.079, 0.380, 0.039, 0.039, 0.039, 0.039, 0.039]
        ])
        
        # Crear el interpolador
        interpolador = RegularGridInterpolator((rho_values, ph_values), data)

        # Interpolación
        valor_interpolado = interpolador((rho, ph))
        return round(valor_interpolado+0,3)


# print(radianes_a_horas(2.103121749))


#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator # type: ignore
from matplotlib.ticker import MultipleLocator, FuncFormatter # type: ignore
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter)
import math
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import OptimizeWarning
warnings.filterwarnings("ignore", category=OptimizeWarning)

def Modelado_mitigación_UHLIG(rho, ph, pot_off):
    ph if ph != 7 else ph+.00001  # Asegurar que el pH no sea menor a 3
    if ph>14.0:
        print("El pH no puede ser mayor a 14")
        return 
    # mpy_uhlig = mpy_UGLIH(rho, ph)  # Cálculo de mpy según UHLIG
    mpy_uhlig = mpy_UGLIH(rho, ph)  if mpy_UGLIH(rho, ph)>1.5 else 1.5 # type: ignore # limitar a 1.5, evitar error
    x=np.linspace(10,50000,100)
    y=np.linspace(3,14)
    x,y=np.meshgrid(x,y)

    Z = np.zeros_like(x)

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            Z[i, j] = mpy_UGLIH(x[i, j], y[i, j])

    fig, ax = plt.subplots(1,2,figsize=(12,4),gridspec_kw={"width_ratios": [2, 2]})
    fig.subplots_adjust( wspace=0.3, hspace=0.1)
    
    grafico=ax[0].contourf(x,y,Z,cmap='rainbow',levels= 20)
    ax[0].scatter(rho, ph, zorder=5, color='black', s=30, label=f"mpy: {mpy_uhlig:.2f} mpy")
    # puntos=axes.scatter(6200,5, zorder=5,color='black',s=6)
    ax[0].yaxis.set_major_locator(MultipleLocator(1))
    ax[0].xaxis.set_major_locator(MultipleLocator(1000))
    ax[0].set_xticks(ax[0].get_xticks(), ax[0].get_xticklabels(), rotation=90, ha='center',size=8)
    ax[0].set_yticks(ax[0].get_yticks(), ax[0].get_yticklabels(), ha='center',size=9)
    lim_supx= math.ceil(rho)*1.1 if rho>= 9900 else 10000
    ax[0].set(ylim=(3,14), xlim=(0,lim_supx),ylabel='pH', xlabel='Resistividad')
    ax[0].get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    ax[0].set_title(f"Predicción de mpy Unmitigated", fontsize=12)
    ax[0].legend(fontsize=8)    
    cbar = plt.colorbar(grafico,ticks=np.arange(0, 34,2))
    cbar.set_label('mpy')
    ax[0].grid(True, color='black')

# Ajuste de curva logarítmica para mpy Unmitigated
    x_data = np.array([mpy_uhlig, 1])
    y_data = np.array([-0.5, -0.85])
    # Función con asíntota en x=0.1
    def log_asymptotic(x, A, B):
        return A * np.log(x - 0.1) + B
    # Ajuste de parámetros
    params, _ = curve_fit(log_asymptotic, x_data, y_data)
    A, B = params
    x = np.linspace(.1+.01, mpy_uhlig, 500)  # type: ignore # evitar x=0.1 por la singularidad
    y = log_asymptotic(x, A, B)
    mpy_predict=x[np.where(y>=pot_off)[0][0]]

    etiqueta=f'y = {A:.3f}  ln(x - 0.1) - {-1*B:.3f}' if B<0 else f'y = {A:.3f}  ln(x - 0.1) + {B:.3f}'
    curva_plot=ax[1].plot(x, y, label=etiqueta)
    ax[1].invert_yaxis()
    puntos_ajuste=ax[1].scatter(x_data, y_data, color='maroon', zorder=5, s=12,label="Puntos de ajuste")
    punto_predict=ax[1].scatter(mpy_predict, pot_off, color='blue', zorder=5, label=f"Predicción mpy = {mpy_predict:.2f} mpy \n $\\rho$ = {rho:,} $\u03A9$ cm \n pH = {ph:.1f} \n Potencial off= {pot_off:.3f} V")
    ax[1].vlines(mpy_predict, -.4, pot_off, color='blue', linestyle='--', lw=1, label=f"mpy predicción {mpy_predict:.2f} mpy")
    ax[1].hlines(pot_off, 0, mpy_predict, color='blue', linestyle='--', lw=1)
    asintota=ax[1].axvline(0.1, color='gray', linestyle='--', lw=1, label="Asíntota en $x = 0.1$ mpy")
    Linea_pot_nat=ax[1].axhline(-.500, color='maroon', linestyle='--', lw=1,label='Pot Natural')
    Linea_criterio=ax[1].axhline(-.850, color='red', linestyle='--', lw=1,label='Criterio -0.850 V')
    ax[1].set_xlabel("mpy")
    ax[1].set_ylabel("Potencial (V)")
    ax[1].set_yticks(np.arange(-2, np.max(y)+0.1, 0.1))
    # ax[1].set_xticks(np.arange(0, math.ceil(mpy_uhlig*1.1),1), rotation=90)
    # ax[1].xaxis.set_major_locator(ticker.MaxNLocator(20,integer=True))
    ax[1].xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax[1].set_xticks(ax[1].get_xticks(), ax[1].get_xticklabels(), rotation=90)
    
    ax[1].xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax[1].yaxis.set_minor_locator(ticker.MultipleLocator(.05))
    # .set_major_formatter(FormatStrFormatter('%.3f'))

    ax[1].set_title(f"Curva de predicción con $\\rho$={rho:,} $\u03A9$ cm y pH={ph:.1f} a un pot_off:{pot_off:.3f} V", fontsize=8)
    leyenda1=ax[1].legend(handles=[ puntos_ajuste, Linea_criterio,Linea_pot_nat, asintota], loc='upper right',fontsize=6)
    ax[1].add_artist(leyenda1)

    leyenda2=ax[1].legend(handles=[punto_predict], loc='upper left', fontsize=8)
    ax[1].add_artist(leyenda2)

    leyenda3=ax[1].legend(handles=curva_plot, loc='lower right', fontsize=6)
    ax[1].add_artist(leyenda3)


    ax[1].set_xlim(0,mpy_uhlig*1.1) # type: ignore
    ax[1].set_ylim(-.4,-1.6)
    ax[1].grid(True)
    # fig.tight_layout()
    return fig

def df_to_shp(df, lat_col='Latitud', lon_col='Longitud', EPSG_code=None, shape_name='output_shapefile'):
    import utm
    from shapely.geometry import Point
    import geopandas as gpd
    import streamlit as st
    
    warnings.filterwarnings("ignore")
        
    if lat_col!= 'Latitud' or lon_col != 'Longitud':
        # zona=utm.from_latlon(df['Latitud'][0], df['Longitud'][0])[2]
        # epsg_code =EPSG_code if EPSG_code else f'EPSG:{32600+zona}'  # UTM zona correspondiente
        
            # Listas para almacenar las coordenadas UTM
        lon = []
        lat = []
        # Calcular UTM para cada fila
        x,y,zone,letter=utm.from_latlon(df['Latitud'][0], df['Longitud'][0]) # type: ignore

        for idx, row in df.iterrows(): # type: ignore
            try:
                latitude, longitude = utm.to_latlon(easting=row[lon_col],northing=row[lat_col], zone_number=zone, northern=True) # type: ignore
                lat.append(latitude)
                lon.append(longitude)
            except Exception as e:
                print(f"Error en fila {idx}: {e}")
                lat.append(None)
                lon.append(None)

        df['longitude'] = lon
        df['latitude'] = lat
         
        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=EPSG_code)
        

    else:
        epsg_code = EPSG_code if EPSG_code else 'EPSG:4326'  # Coordenadas geográficas (latitud/longitud)
        # Create a GeoDataFrame
        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=epsg_code)
        gdf['latitude'] = gdf[lat_col]
        gdf['longitude'] = gdf[lon_col]

    # Save the GeoDataFrame as a Shapefile
    shapefile_path = f'images/{shape_name}.shp.zip'
    archivo_shp=gdf.to_file(shapefile_path, driver='ESRI Shapefile')    

    print(f'Shapefile saved to {shapefile_path}')
    
    return shapefile_path, gdf

def A_cm2(VAC1,RHO1):
    d_metros=8*VAC1/(100*(RHO1/100)*(math.pi))
    d_cm=d_metros*100
    A=math.pi*(d_cm/2)*(d_cm/2)
    return A

def A_cm2_20_30(VAC1,RHO1, i_ac_inferior):
    d_metros=8*VAC1/(i_ac_inferior*(RHO1/100)*(math.pi))
    d_cm=d_metros*100
    A=math.pi*(d_cm/2)*(d_cm/2)
    return A

def num2station(cadnum, decimales=0):
    if cadnum==0:
        cadtxt='0+000'
        return cadtxt
    if decimales==0:
        cadtxt=f'{int(cadnum // 1000)}+{int(cadnum % 1000):03d}'
        return cadtxt
    if 0<cadnum<10:
        cadnumk = int(cadnum // 1000)
        cadnumu = cadnum % 1000
        cadtxt=f'{cadnumk}+00{cadnumu:03.{decimales}f}'
        return cadtxt
    elif 10<=cadnum<100:
        cadnumk = int(cadnum // 1000)
        cadnumu = cadnum % 1000
        cadtxt=f'{cadnumk}+0{cadnumu:03.{decimales}f}'
        return cadtxt
    else:
        cadnumk = int(cadnum // 1000)
        cadnumu = cadnum % 1000
        cadtxt=f'{cadnumk}+{cadnumu:03.{decimales}f}'
        return cadtxt

def Graficos_Densidad_AC_custom( VAC1,RHO1, km , i_ac_inferior=20):
    if not np.isfinite(VAC1) or not np.isfinite(RHO1) or float(VAC1) <= 0 or float(RHO1) <= 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'Datos no válidos para VAC/RHO', ha='center', va='center')
        ax.set_axis_off()
        return 'Datos no válidos para VAC/RHO', fig

    def V_ac(i_ac, rho_ohm_cm, diam_cm):
        V_ac=(i_ac*rho_ohm_cm*math.pi*diam_cm/10000)*(1/8)
        return V_ac
    
    def Acm2_to_dcm(area):
        diam_cm = 2 * (area / math.pi) ** 0.5
        diam_m = diam_cm / 100
        return diam_cm

    i_ac_100=100

    T_cm2=np.linspace(0.1,100,num=10000)
    Vect_VAC_20_30=V_ac(i_ac_inferior, RHO1, Acm2_to_dcm(T_cm2))
    Vect_VAC_100=V_ac(i_ac_100, RHO1, Acm2_to_dcm(T_cm2))
    
    fig,ax =plt.subplots()
    angulo=16
    
    L2030=ax.plot(T_cm2,Vect_VAC_20_30,linestyle='-',c='blue', zorder=2)
    texto=f'{RHO1:,.0f} $\\Omega$-cm para '+r'$i_{ac}$='+f'{i_ac_inferior} A/$m^2$' # type: ignore
    plt.annotate(texto, xy=(T_cm2[-1], Vect_VAC_20_30[-1]), xytext=(-3, 17), rotation=angulo, textcoords="offset points", ha="right", va="top", color='blue')

    L100=ax.plot(T_cm2,Vect_VAC_100,linestyle='-',c='blue', zorder=2)
    texto=f'{RHO1:,.0f} $\\Omega$-cm para '+r'$i_{ac}$='+f'{i_ac_100} A/$m^2$' # type: ignore
    plt.annotate(texto, xy=(T_cm2[-1], Vect_VAC_100[-1]), xytext=(-3, 17), rotation=angulo, textcoords="offset points", ha="right", va="top", color='blue')

    #===================================fill between=========================================
    tranparencia=0.7
    T_cm2__v2=np.linspace(0.1,1,num=10000)
    
    ax.fill_between([0.1,1], 1000      , color='lime', interpolate=True, zorder=1, edgecolor='lime')
    ax.fill_between([0.1,1.01], 15   ,1000, color='red' , interpolate=True, zorder=1, edgecolor='red')
    
    ax.fill_between(T_cm2, Vect_VAC_100  , 1000        , where=Vect_VAC_100>=V_ac(i_ac_100, RHO1, Acm2_to_dcm(1)) , color='red'   , interpolate=True, zorder=0, edgecolor='red')
    ax.fill_between(T_cm2, Vect_VAC_20_30, Vect_VAC_100, where=Vect_VAC_100>=V_ac(i_ac_100, RHO1, Acm2_to_dcm(1)) , color='orange', interpolate=True, zorder=0, edgecolor='orange')
    ax.fill_between(T_cm2, Vect_VAC_20_30  ,             where=Vect_VAC_100>=V_ac(i_ac_100, RHO1, Acm2_to_dcm(1)) , color='lime'  , interpolate=True, zorder=0, edgecolor='lime')
    #===================================fill between=========================================


    # ax.scatter(1,VAC1,c='blue', zorder=2)
    horizontal=[0.1, 1,A_cm2(VAC1,RHO1),A_cm2_20_30(VAC1,RHO1, i_ac_inferior),100]
    horizontar_ordenada=sorted(horizontal)
    ax.plot(horizontar_ordenada,[VAC1,VAC1,VAC1,VAC1,VAC1],linestyle='--', color='black',linewidth=1, marker='o', markersize=4, zorder=2, alpha=0.7)
    # ax.plot([1  , 1],[0.1 ,VAC1],linestyle='--', color='blue',linewidth=1)
    
    ax.text(.15 ,150,'VAC={:.3f} V'.format(VAC1),ha='left', va='bottom', color='blue',size=9)

    d_cm=2*math.sqrt(1/math.pi)
    d_m=d_cm/100
    densidad=8*VAC1/((RHO1/100)*math.pi*d_m)
    ax.text(.15 ,100,r'Densidad $i_{ac}$ a 1 $cm^2$='+f'{densidad:.2f} A/$m^2$',ha='left', va='center', color='blue',size=9)

    xs=A_cm2(VAC1,RHO1)
    xs20_30=A_cm2_20_30(VAC1,RHO1, i_ac_inferior)
    # print(f'{xs20:.4f}, {xs:.4f}')
    alto_barra=0.15

    
    TT=np.linspace(0.1,1,num=10000)
    if i_ac_100 > densidad >i_ac_inferior:
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2<=xs, color='red', interpolate=True, zorder=1, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2>=xs, color='orange', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2>=xs20_30, color='limegreen', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2<=1, color='limegreen', interpolate=True, zorder=1, edgecolor='black') # type: ignore
    elif densidad < i_ac_inferior:
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2<=xs, color='red', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2<=xs20_30, color='orange', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2>=xs20_30, color='limegreen', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2<=1, color='limegreen', interpolate=True, zorder=1, edgecolor='black') # type: ignore
    elif densidad > i_ac_100:
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2<=xs, color='red', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2>=xs, color='orange', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where=T_cm2>=xs20_30, color='limegreen', interpolate=True, zorder=0, edgecolor='black')
        ax.fill_between(T_cm2, y1=alto_barra, where= T_cm2<=1, color='limegreen', interpolate=True, zorder=1, edgecolor='black') # type: ignore

    ax.text(1,alto_barra+.02,f'1.0 $cm^2$',ha='center', va='bottom', color='blue',size=6, zorder=3, rotation=90)
    if xs20_30>0.1 and xs20_30<100:
        ax.text(xs20_30,alto_barra+.02,f'{round(xs20_30,2)} $cm^2$',ha='center', va='bottom', color='blue',size=6, zorder=3, rotation=90)
    if xs>0.1 and xs<100:
        ax.text(xs     ,alto_barra+.02,f'{round(xs,2)} $cm^2$'     ,ha='center', va='bottom', color='blue',size=6, zorder=3, rotation=90)

    ax.set_yscale('log')
    ax.set_xscale('log')

    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:.0f}"))
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:.0f}"))
    ax.xaxis.set_minor_formatter(mtick.StrMethodFormatter("{x:.1f}"))

    ax.tick_params(axis='x', which='major', labelsize=8, rotation=90)
    ax.tick_params(axis='x', which='minor', labelsize=5, rotation=90)
    ax.tick_params(axis='y', which='minor', labelsize=5)

    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(10)

    ax.axhline(y=15, linestyle='--', color='maroon',linewidth=1, label='Limite seguro')
    ax.text(.12 ,17,'Voltaje Seguro para el Personal 15 V',ha='left', va='bottom', color='black',size=7)

    plt.xlabel('Superficie del Holiday ($cm^2$)')
    plt.ylabel('Voltaje AC (Volts)')
    print(km)
    km=num2station(km)
    plt.title('Voltaje AC vs Tamaño del Holiday para $i_{ac}$='+str(int(i_ac_inferior))+'-'+str(i_ac_100)+' A/$m^2$'+'\n'+str(km), size=12)
    # plt.grid()
    plt.ylim([0.1,1000])
    plt.xlim([0.1,100])
    # plt.grid()
    # plt.tight_layout()
    
    logo_path = "images\logo.png" # type: ignore
    logo_img = mpimg.imread(logo_path)
    logo_img_rotated = np.rot90(logo_img)
    imagebox = OffsetImage(logo_img, zoom=0.15, alpha=0.9)
    ab = AnnotationBbox(imagebox, (.81, .17), frameon=False, xycoords='axes fraction', boxcoords="axes fraction", pad=0.1)
    ax.add_artist(ab)      
    
    # plt.show()
    plt.savefig('images/AC_Corrosion.png', dpi=300, bbox_inches='tight')
    # fig.savefig(f'Plots/Densidad_AC_{km}.png', dpi=300)
    return 'images/AC_Corrosion.png'

