import matplotlib.pyplot as plt
import numpy as np
import qsogen as qg

from matplotlib.widgets import Button, Slider, CheckButtons
from matplotlib.collections import LineCollection



def qsomodel(z,M_i,ebv):
    sed = qg.Quasar_sed(z,LogL3000=None,M_i=M_i,ebv=ebv)
    return sed.wavred, sed.flux/np.max(sed.flux)



def get_filters(name,bands,colors,visible=True):
    lines = []
    text = {}
    for key in bands:
        filt = np.loadtxt('./filters/'+name+'_'+key+'.filter')
        lines.append(filt)
        text[key] = (np.max(filt[:,0])-np.min(filt[:,0]))/2.0+np.min(filt[:,0])
    
    lc = LineCollection(lines,colors=colors,alpha=0.4,visible=visible,label=name,facecolor=colors)
    
    return lc,text

init_z = 4.0
init_Mi = -28
init_ebv = 0.
#init_Mi = -28

lam, f = qsomodel(init_z,init_Mi,init_ebv)

fig, ax = plt.subplots(figsize=[8,5])
line, = ax.plot(lam, f, zorder=10,color='black',lw=2)
ax.set_xlabel('Wavelength ($\AA$)')
ax.set_ylabel('$\\nu ~f_\\nu$ (arbitary)')

#############################################################



b_HSC,t_HSC = get_filters('HSC',['g','r','i','z','Y'],colors='royalblue')
ax.add_collection(b_HSC)

HSCtxt = []
for key in t_HSC:
    _ = ax.text(t_HSC[key],0.02,key,visible=True,color='blue',alpha=0.5,horizontalalignment='center')
    HSCtxt.append(_)

b_DECam,t_DECam = get_filters('DECam',['g','r','i','z','Y'],colors='teal',visible=False)
ax.add_collection(b_DECam)

DECamtxt = []
for key in t_DECam:
    _ = ax.text(t_DECam[key],0.02,key,visible=False,color='teal',alpha=0.5,horizontalalignment='center')
    DECamtxt.append(_)

b_VISTA,t_VISTA = get_filters('VISTA',['Y','J','H','Ks'],colors='darkred')
ax.add_collection(b_VISTA)

VISTAtxt = []
for key in t_VISTA:
    _ = ax.text(t_VISTA[key],0.02,key,visible=True,color='darkred',alpha=0.5,horizontalalignment='center')
    VISTAtxt.append(_)

b_WISE,t_WISE = get_filters('WISE',['W1','W2'],colors='black')
ax.add_collection(b_WISE)

WISEtxt = []
for key in t_WISE:
    _ = ax.text(t_WISE[key],0.02,key,visible=True,color='black',alpha=0.5,horizontalalignment='center')
    WISEtxt.append(_)

text_by_label = {'HSC': HSCtxt,
                 'DECam': DECamtxt,
                 'VISTA': VISTAtxt,
                 'WISE': WISEtxt,
                 }


lines_by_label = {l.get_label(): l for l in [b_HSC,b_DECam,b_VISTA,b_WISE]}
line_colors = [l.get_color() for l in lines_by_label.values()]






############################################################
ax.set_xscale('log')
#ax.set_yscale('log')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(right=0.8, bottom=0.25)

# Make a horizontal slider to control the frequency.
axz = fig.add_axes([0.15, 0.1, 0.65, 0.03])
z_slider = Slider(
    ax=axz,
    label='Redshift (z)',
    valmin=0.0,
    valmax=10.0,
    valstep=0.05,
    valinit=init_z,
)



# register the update function with each slider

#amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
# Make a horizontal slider to control the frequency.
axMi = fig.add_axes([0.15, 0.05, 0.65, 0.03])
Mi_slider = Slider(
    ax=axMi,
    label='M$_i$',
    valmin=-30.,
    valmax=-16.,
    valstep=0.1,
    valinit=init_Mi,
)

axebv = fig.add_axes([0.15, 0.01, 0.65, 0.03])
ebv_slider = Slider(
    ax=axebv,
    label='ebv$',
    valmin=-0.5,
    valmax=0.5,
    valstep=0.01,
    valinit=init_ebv,
)



# The function to be called anytime a slider's value changes
def update(val):
    lam, f = lam, f = qsomodel(z_slider.val,Mi_slider.val,ebv_slider.val)
    line.set_ydata(f)
    line.set_xdata(lam)
    #line.set_xdata()
    fig.canvas.draw_idle()
    
    
z_slider.on_changed(update)
Mi_slider.on_changed(update)
ebv_slider.on_changed(update)



#############
#filter buttons




rax = plt.axes([0.85,0.4,0.1,0.3])
check = CheckButtons(
    ax=rax,
    labels=lines_by_label.keys(),
    actives=[l.get_visible() for l in lines_by_label.values()],
    label_props={'color': line_colors,'alpha':[0.9]*len(lines_by_label)},
    frame_props={'edgecolor': line_colors},
    check_props={'facecolor': line_colors},
)


def callback(label):
    ln = lines_by_label[label]
    #print(ln.get_visible())
    ln.set_visible(not ln.get_visible())
    ln.figure.canvas.draw_idle()
    
    for b in text_by_label[label]:
        b.set_visible(ln.get_visible())
    
    
    
    
check.on_clicked(callback)


#plt.isinteractive()
plt.show()
ax.set_xlim(3500.,60000.)
ax.set_ylim(0.)
#plt.close()
#fig.tight_layout()

ax.set_ylim(0.)

plt.show()
