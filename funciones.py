def texto(texto):
    return texto.upper()

import math
def radianes_a_horas(radianes):
        radianes = radianes % (2 * math.pi) # Normalizar los radianes para estar en el rango de 0 a 2π
        horas = (radianes / (2 * math.pi)) * 12 # Convertir radianes a horas   
        horas_completas = int(horas) # Extraer las horas completas
        minutos = (horas - horas_completas) * 60 # Convertir el resto a minutos
        minutos_completos = int(minutos)
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
plt.rcParams['font.family'] = 'calibri'
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
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    # Crear el mapa de colores
    cmap = ListedColormap(['green', 'limegreen', 'yellow', 'red', 'gray'])
    norm_bins = np.array([0, 1, 2, 3, 4,5])
    norm = matplotlib.colors.BoundaryNorm(norm_bins, cmap.N)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ticks=[0.5, 1.5, 2.5, 3.5, 4.5], ax=ax, fraction=0.2, pad=0.5)
    
    cbar.ax.set_yticklabels(['Excelente', 'Bueno', 'Regular', 'Pobre', 'Sin Recubrimiento'])
    cbar.ax.set_aspect('auto')

    ax.set_ylabel('Conductancia a 1,000 Ω-cm [μS/m$^2$]')
    ax.get_xaxis().set_visible(False)
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
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
    ax.fill_between(x, 0, y, where=(y >= 0) & (y <= 100), facecolor='green', alpha=transparencia, label='Excelente', zorder=1)
    ax.fill_betweenx(y, 0, x, where=(y >= 0) & (y <= 100), facecolor='green', alpha=transparencia, zorder=1)

    ax.fill_between(x, 0, y, where=(y >= 100-.1) & (y <= 500), facecolor='limegreen', alpha=transparencia, label='Buena', zorder=0)    
    ax.fill_betweenx(y, 0, x, where=(y >= 100-.1) & (y <= 500), facecolor='limegreen', alpha=transparencia, zorder=0)    
    
    ax.fill_between(x, 0, y, where=(y >= 500) & (y <= 1000), facecolor='yellow', alpha=transparencia, label='Regular')    
    ax.fill_betweenx(y, 0, x, where=(y >= 500) & (y <= 1000), facecolor='yellow', alpha=transparencia)    

    ax.fill_between(x, 0, y, where=(y >= 1000) & (y <= 40000), facecolor='red', alpha=transparencia, label='Pobre')
    ax.fill_betweenx(y, 0, x, where=(y >= 1000) & (y <= 40000), facecolor='red', alpha=transparencia)
    
    ax.fill_between(x, 0, y, where=(y >= 40000), facecolor='gray', alpha=transparencia, label='Bare')
    ax.fill_betweenx(y, 0, x, where=(y >= 40000) & (y <= 1000000), facecolor='gray', alpha=transparencia)

    x_value = x[np.where(y >= valor_conductancia)[0][0]]
    ax.scatter(x_value, valor_conductancia, color='black', zorder=5)  # Coordenadas del punto
    # Anotación de un punto específico con recuadro de fondo blanco
    ax.annotate(f'{valor_conductancia:,.0f} μS/m²\n{x_value:.3f}% bare\n{100-x_value:.3f}% coated', xy=(x_value, valor_conductancia), xytext=(7, 1000),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),
                fontsize=8)

    ax.set_xlabel('% de Área Desnuda')
    ax.set_ylabel('Conductancia @1,000 Ω-cm [μS/m$^2$]')
    ax.set_title('Gráfico de Conductancia @1,000 Ω-cm')

    # Escalas logarítmicas
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim(.0001,100)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}%'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        # Agregar etiquetas adicionales en el eje y
    additional_yticks = [ 40000, 500]
    ax.set_yticks(list(ax.get_yticks()) + additional_yticks)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
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
    ax.annotate(f'{valor_conductancia:,.0f} μS/m²\n{x_value:.3f}% bare\n{100-x_value:.3f}% coated', xy=(x_value, valor_conductancia), xytext=(7, 1000),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),
                fontsize=8)

    ax.set_xlabel('% de Área Desnuda')
    ax.set_ylabel('Conductancia @1,000 Ω-cm [μS/m$^2$]')
    ax.set_title('Gráfico de Conductancia @1,000 Ω-cm')

    # Escalas logarítmicas
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim(.0001,100)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}%'))
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






