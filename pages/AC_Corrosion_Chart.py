import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import math
from modulos import num2station
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

def Graficos_Densidad_AC_custom( VAC1,RHO1, km , i_ac_inferior):
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
    # km=num2station(km)
    plt.title('Voltaje AC vs Tamaño del Holiday para $i_{ac}$='+str(int(i_ac_inferior))+'-'+str(i_ac_100)+' A/$m^2$'+'\n'+str(km), size=12)
    # plt.grid()
    plt.ylim([0.1,1000])
    plt.xlim([0.1,100])
    # plt.grid()
    # plt.tight_layout()
    
    logo_path = "imagen\logo.png" # type: ignore
    logo_img = mpimg.imread(logo_path)
    logo_img_rotated = np.rot90(logo_img)
    imagebox = OffsetImage(logo_img, zoom=0.15, alpha=0.9)
    ab = AnnotationBbox(imagebox, (.81, .17), frameon=False, xycoords='axes fraction', boxcoords="axes fraction", pad=0.1)
    ax.add_artist(ab)      
    
    
    
    plt.show()
    # fig.savefig(f'Plots/Densidad_AC_{km}.png', dpi=300)
    return fig

def AC_Corrosion():
    st.title("Calculo de conductancia específica de recubrimiento")
    # st.write("Welcome to the second page of the Streamlit application!")
    # st.write("Here you can add different components and functionalities tailored to this page.")

    st.header("1.-Datos de entrada")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # resistencia1, d1 = st.number_input("resistencia #1:", format="%.4f"), st.number_input("Distancia #1 [cm]:")
        km=st.number_input("Km [m]:", step=1)
        Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        if Voltaje_AC and km:
            st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.0f} V")
    with c2:
        Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        if Voltaje_AC and km:
            st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.0f} V")
    c1, c2 = st.columns([2, 1])
    # with c1:
    #     if (RESISTIVIDAD_1)>0 and (RESISTIVIDAD_2)>0:
    #         resistividad_avg=round(((RESISTIVIDAD_1)+(RESISTIVIDAD_2))/2,0)
    #         st.markdown(f"\nResistividad promedio: {resistividad_avg:,.2f} Ω-cm",)


if __name__ == "__main__":
    AC_Corrosion()