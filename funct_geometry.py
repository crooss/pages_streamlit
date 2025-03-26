import matplotlib.pyplot as plt
import math

def calcular_WA(w,t):
    if t < 10:
        return w/10
    else:
        return w/t



def Plot_geometry(df, optionW, optionL, optiont):
    df['ESPESOR [mm]']=df['ESPESOR [in]']*25.4
    df['WA'] = df.apply(lambda row: calcular_WA(row[optionW], row[optiont]), axis=1)
    df['LA'] = df.apply(lambda row: calcular_WA(row[optionL], row[optiont]), axis=1)
        
    fig, ax = plt.subplots(figsize=(6, 6))
    
    ax.scatter(df['LA'],df['WA'],s=3,color='black', marker='o',zorder=5, alpha=.5)

    maximo=max(df['LA'].max(),df['WA'].max())
    maximo=math.ceil(maximo / 10) * 10
    
    ax.set_xlim(0,10)
    ax.set_ylim(0,10)
    # Colorear áreas de calidad
    transparencia=.5
    ax.fill([0, 1, 1, 0,],  [0, 0, 1, 1,], 'lightblue', alpha=transparencia, label='Pin-hole')
    ax.fill([1, 2, 6, 3, 3, 1], [1, 1, 3, 3, 6, 2], 'gray', alpha=transparencia,label='Pitting')
    ax.fill([0,1,1,0], [1,1,10,10], 'red', alpha=transparencia,label='Circumferential slotting')
    ax.fill([1,3,3,1,1], [2,6,10,10,2], 'plum', alpha=transparencia,label='Circumferential grooving')
    ax.fill([1,10,10,1], [0,0,1,1], 'orange', alpha=transparencia, label='Axial slotting')
    ax.fill([2,10,10,6,2], [1,1,3,3,1], 'salmon', alpha=transparencia,label='Axial grooving')
    ax.fill([3,10,10,3], [3,3,10,10], 'limegreen', alpha=transparencia,label='General')
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ax.set_xlabel('L/A')
    ax.set_ylabel('W/A')
    ax.set_title('Anomaly dimension class')
    ax.text(1.56, .5, 'Pipeline Operators Forum POF \nSpecifications and requirements for in-line inspection of pipelines \nFigure 2.2', ha='center', va='center', transform=ax.transAxes, fontsize=8, color='gray', rotation=90)
    plt.text(1, -.1, 'If t < 10 mm then A = 10 mm \nIf t ≥ 10 mm then A = t', ha='right', va='center', transform=ax.transAxes, fontsize=8, color='gray', rotation=0)
    
    
    plt.savefig('images/Plot_geometry.png', dpi=300, bbox_inches='tight')
    return 'images/Plot_geometry.png'
    plt.show()