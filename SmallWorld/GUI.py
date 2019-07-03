#!/usr/bin/env python
# coding: utf-8

from IPython.display import display
import ipywidgets as widgets

################################################################################################################
################################################################################################################
X_number_Text = widgets.BoundedIntText(
                    value=100,
                    min=1,
                    max=100,
                    step=1,
                    description='init X',
                    readout=True,
                    readout_format='d',
                    disabled=False)

sizex_Text = widgets.BoundedIntText(
                    value=100,
                    min=5,
                    max=200,
                    step=5,
                    description='size x',
                    readout=True,
                    readout_format='d',
                    disabled=False)

sizey_Text = widgets.BoundedIntText(
                    value=100,
                    min=5,
                    max=200,
                    step=5,
                    description='size y',
                    readout=True,
                    readout_format='d',
                    disabled=False)

nlinks_Text = widgets.BoundedIntText(
                    value=100,
                    min=0,
                    max=200,
                    step=1,
                    description='n links',
                    readout=True,
                    tooltips = "number of links in the network",
                    readout_format='d',
                    disabled=False)


distribution_button = widgets.Dropdown(
                            options=['Gauss', 'Laplace'],
                            description='Distribution:',
                            value = 'Laplace',
                            readout = True,
                            readout_format = 's',
                            disabled= False )


concentration_slide_bar = widgets.FloatSlider(   
                            min=0,
                            max=0.5,
                            step=0.01,
                            value=0.15,
                            description='c:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            tooltips = "cytotoxic cells concentration",
                            readout=True,
                            readout_format='.2f')

scale_slide_bar = widgets.FloatSlider(   
                            min=0,
                            max=5,
                            step=0.1,
                            value= 1.3,
                            description='scale:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.2f')


k1_slide_bar = widgets.FloatSlider(   
                            min=0.005,
                            max=1,
                            step=0.001,
                            value=1,
                            description='k1:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.3f')

k2_slide_bar = widgets.FloatSlider(   
                            min=0.005,
                            max=1,
                            step=0.001,
                            value=1,
                            description='k2:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.3f')

lambd_slide_bar = widgets.FloatSlider(   
                            min=0.01,
                            max=1,
                            step=0.01,
                            value=0.3,
                            description='\u03BB:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.4f')

beta_slide_bar = widgets.FloatSlider(   
                            min=0,
                            max=0.01 ,
                            step=0.0001,
                            value=0.0,
                            description='\u03B2:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.4f')

n_Text = widgets.BoundedIntText(
                    value=1000,
                    min=1,
                    max=20000,
                    step=1,
                    description='n',
                    tooltips = 'number of iterations',
                    readout=True,
                    readout_format='d',
                    disabled=False)

k_Text = widgets.BoundedIntText(
                    value=20,
                    min=1,
                    max=1000,
                    step=1,
                    button_style = 'info',
                    description='k',
                    tooltips = 'number of sample networks',
                    readout=True,
                    readout_format='d',
                    disabled=False)

limit_Text = widgets.BoundedIntText(
                    value=60,
                    min=0,
                    max=100,
                    step=5,
                    button_style = 'info',
                    description='limit',
                    readout=True,
                    readout_format='d',
                    disabled=False)


sampling_Buttons = widgets.Dropdown(
            options=['Dense', 'Regular', 'Sparse'],
            value = 'Sparse',
            description='sampling:',
            disabled=False,
            width = 10,
            tooltips=['[0,2,4,6,8]','[0,3,6,9]', '[0,5,10,15,20]'],
)
################################################################################################################
################################################################################################################

html1 = widgets.HTML(
    value = '<p style="padding-left: 40px;">Legend:</p><ul> \
            <li style="list-style-type: none;"> <ul> \
            <li><strong>init X</strong> - initial number of tumor cells</li> \
            <li><strong>n links&nbsp;</strong> - number of links in the network</li> \
            <li><strong>size x, size y </strong>-&nbsp;<span class="tlid-translation translation" lang="en">\
            <span class="" title="">network size</span></span></li> \
            </ul></li></ul>'
)


html2 = widgets.HTML(
    value = '<p style="padding-left: 40px;">Legend:</p> <ul> <li style="list-style-type: none;"> \
             <ul><li><strong><span class="tlid-translation translation" lang="en"><span class="" title="">distribution </span></span>\
             </strong>- d<span class="tlid-translation translation" lang="en"><span class="" title="">istribution of cancer cells ound the central poin</span></span></li> \
            <li><strong>scale</strong> - standard deviation of the d<span class="tlid-translation translation" lang="en"><span class="" \title="">istribution</span></span></li> \
            <li><strong>c</strong> -cytotoxic cells concentration</li> \
            </ul></li></ul>'
)


html4 = widgets.HTML(
    value = '<p style="padding-left: 40px;">Legend:</p><ul> \
            <li style="list-style-type: none;"><ul> \
            <li><strong>n</strong> - number of iterations</li>\
            <li><strong>k</strong> - number of sample networks</li>\
            <li><strong>sampling</strong> - <span class="tlid-translation translation" lang="en"><span class="" title="">sampling frequency</span></span></li> \
            </ul></li></ul>'
)

################################################################################################################
################################################################################################################

date_Picker = widgets.DatePicker(description='date',disabled=False, readout=True)

author_Text = widgets.Text(
                    value='no one',
                    description='author:',
                    readout=True,
                    readout_format='s',
                    disabled=False)

savefile_Text = widgets.Text(
                    value='samplefile.csv',
                    description='file name:',
                    readout=True,
                    readout_format='s',
                    disabled=False)

savefile_max_Text = widgets.Text(
                    value='samplefile_max.csv',
                    description='file name:',
                    readout=True,
                    readout_format='s',
                    disabled=False)

################################################################################################################
################################################################################################################

start_Button = widgets.ToggleButton(
    continuous_update=True,
    value=False,
    description='START',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    icon='check',
    readout=True,
    readout_format='b',
)
################################################################################################################
################################################################################################################

body1 = widgets.VBox([ X_number_Text, nlinks_Text, sizex_Text, sizey_Text])
body2 = widgets.VBox([ distribution_button, scale_slide_bar, concentration_slide_bar] )
body4 = widgets.VBox([ n_Text, k_Text, limit_Text, sampling_Buttons])

tab3 = widgets.VBox([ k1_slide_bar, k2_slide_bar, lambd_slide_bar, beta_slide_bar] )
tab5 = widgets.VBox([ author_Text, date_Picker, savefile_Text, savefile_max_Text])
 
tab1 = widgets.HBox([ body1, html1])
tab2 = widgets.HBox([ body2, html2])
tab4 = widgets.HBox([ body4, html4])

children = [tab1, tab2, tab3, tab4, tab5]
GUI = widgets.Tab()
GUI.children = children

GUI.set_title(0, 'Geometry of the net')
GUI.set_title(1, 'Network settings')
GUI.set_title(2, 'Parameters')     
GUI.set_title(3, 'Simulation settings') 
GUI.set_title(4, 'Author') 