# import pywebio
from pywebio.session import run_js

# put_button("ReUpload_images",onclick=lambda: run_js('window.location.reload()'))
import pywebio
from pywebio.input import *
from pywebio.output import *
import math
from sympy import *
pywebio.config(title='RC-DESIGNER', description="abhi korde's RCC designer", theme='yeti', js_code=None, js_file=[], css_style=None, css_file=[])

def main():
    put_button("HOME",onclick=lambda: run_js('window.location.reload()'))
    put_image('https://www.pngmart.com/files/22/Civil-Engineering-PNG-Image.png', width='90')
    # put_button("BACK",onclick=lambda: run_js('window.history.go(-1)'))


    # put_button(label='Home', onclick=run_js('window.location.reload()'))
    operation = radio('choose what to design', options=['Column Design', 'Footing Design', 'Staircase design (Dog-legged)', 'Beam Design (Simply supported)'], required='must')
    if operation == 'Column Design':


        put_text('COLUMN DESIGN')
        HH = input_group('column calculation', [
            input('Unsupported Length of the Column in m: ', name='L', type=FLOAT, required='must'),
            input('Axial load on Column in kN: ', name='P', type=FLOAT, required='must'),
            select('Grade of concrete used in N/mm²: ',[None,20, 25, 30, 35, 40, 45, 50, 55, 60, 65], name='fck', type=FLOAT, required='must'),
            select('Grade of steel used in N/mm²: ',[None, 415,500], name='fy', type=FLOAT, required='must')])
        Pu_requred = 1.5*HH['P']
        # Approximate dimenion of column
        D = HH['L']*(1000/12)
        put_text()
        put_text('                                   𝐃 𝐄 𝐒 𝐈 𝐆 𝐍    𝐒 𝐔 𝐌 𝐌 𝐀 𝐑 𝐘 :')
        put_text('------------------------------------------------------------------------------------------------------------------')
        put_text('➨ Size shall be provoided between', D, 'mm and 400 mm')
        # D = int(input('Size of square column provoided ( recomended- 350mm): '))
        In = input_group('Column calculation', [
            input('Size of square column provoided ( recomended- 350mm): ', name='D', type=FLOAT, required='must'),
            input('Diameter of bars to be provoided (recomended 20 mm): ', name='bar', type=FLOAT, required='must')])
        # put_text('Provoided column size ', D)
        # Load carrying capacity
        Asc = 0.015*D**2
        Ac = (D**2)-Asc
        Pu = (0.4*HH['fck']*Ac)+(0.67*HH['fy']*Asc)
        Pu = Pu/1000
        # Longitudinal steel
        put_text('➨ Area of Steel required (mm²)',Asc )
        # bar = int(input('Diameter of bars to be provoided (recomended 20 mm): '))
        B = 0.7854*(In['bar']**2)
        no_of_bar = Asc/B
        if no_of_bar%1 != 0:
            no_of_bar = int(no_of_bar)
            no_of_bar = no_of_bar+1
        # Transverse ties
        Bt = 0.25*In['bar']
        if Bt<=6:
            Bt = 6
        elif 6<Bt<9:
            Bt = 8
        elif Bt > 8:
            Bt = 10
        # pitch of lateral ties 
        a = D
        b = 16*In['bar']
        c = 300
        if  a<b and a<c:
            S=a
        elif b<a and b<c:
            S=b
        elif c<a and c<b:
            S=c
        put_text('➨ Size of column',D,'X',D,'mm')
        put_text('➨ Provoide', no_of_bar,'bars of', In['bar'],'mm dia')
        put_text('➨ Transeverse ties: ','provoide lateral ties of', Bt,'mm dia at a pitch of', S,'mm')
        put_text('➨ load carrying capacity of column is', Pu, 'kN')
    elif operation == 'Footing Design':
        put_text('FOOTING DESIGN')
        HH = input_group('Footing calculations', [
            input('Shorter side of the column in mm: ', name='b', type=FLOAT, required='must'),
            input('Longer side of the column in mm: ', name='D', type=FLOAT, required='must'),
            select('Grade of concrete used in N/mm²: ',[None,20, 25, 30, 35, 40, 45, 50, 55, 60, 65], name='fck', type=FLOAT, required='must'),
            select('Grade of steel used in N/mm²: ',[None, 415,500], name='fy', type=FLOAT, required='must'),
            input('SBC of soil in kN/m²', name='SBC', type=FLOAT, required='must'),
            input('Load on column in kN: ', name='p', type=FLOAT, required='must')
        ])
        wf = 1.1*HH['p']*1.5
        # wu = 1.5*wf
        # Area of footing
        Af = (wf/1.5)/HH['SBC']
        # Size of footing
        L = math.sqrt(Af/(HH['b']/HH['D']))
        B = (HH['b']/HH['D'])*L
        L = int(L)
        L = L+1
        B = int(B)
        B = B+1
        # AF PROVOIDED
        Af = L*B
        # upward soil pressure
        P = 1.5*HH['p']/Af
        # depth of footing for bending moment
        D = HH['D']/1000
        b = HH['b']/1000
        # Bending moment in x direction
        Mx = (P*B*(L-D)*(L-D))/8
        # Bending moment in y direction
        My = (P*L*(B-b)*(B-b))/8
        # Maximum bending moment
        if Mx >= My:
            Mmax = Mx
        if Mx <My:
            Mmax = My
        #  calculation of depth d
        d1 = math.sqrt((Mmax*10**6)/(138*HH['fck']))
        # Check for depth in one way shear(beam shear)
        Tv = 250*(math.sqrt(HH['fck']))
        x = symbols('x')
        eq = Eq(P*B*(((L-D)/2)-x),Tv*B*x)
        sol = solve(eq,x)
        d2 = sol[0]
        d2 = d2*1000
        # check for depth in 2 way shear
        y = symbols('y')
        bo  = 2*((D+y)+(b+y))
        eq2 = Eq(P*(Af-(D+y)*(b+y)),Tv*bo*y)
        sol2 = solve(eq2,y)
        d3 = sol2[1]
        d3 = d3*1000
        # Determining the required depth
        put_text()
        put_text('                                   𝐃 𝐄 𝐒 𝐈 𝐆 𝐍    𝐒 𝐔 𝐌 𝐌 𝐀 𝐑 𝐘:')
        put_text('------------------------------------------------------------------------------------------------------------------')
        if d1>d2 and d1>d3:
            put_text('➨ Required Depth for footing is ', d1)
        if d2>d1 and d2>d3:
            put_text('➨ Required Depth for footing is ', d2)
        if d3>d1 and d3>d2:
            put_text('➨ Required Depth for footing is ', d3)
        d_provoided= int(input('Enter the depth to be provoided in mm: '))
        put_text('➨ Provoided depth of footing is ',d_provoided,'mm' )
        c = int(input('Enter the cover to be provoided in mm (recomended-50): '))
        bar = int(input('Enter the bar diameter to be provoided in mm (recomended-20): '))
        overall_depth = d_provoided + c + bar/2
        put_text('➨ Over-all depth provoded for footing is', overall_depth)
        # Reinforcement Details:
        # in long direction:
        b = b*1000
        Astx = (0.5*HH['fck']*1000*d_provoided/HH['fy'])*(1-sqrt(1-((4.6*Mx*10**6)/(HH['fck']*1000*d_provoided**2))))
        Asty = (0.5*HH['fck']*1000*d_provoided/HH['fy'])*(1-sqrt(1-((4.6*My*10**6)/(HH['fck']*1000*d_provoided**2))))
        Area_of_bar = (3.142/4)*(bar**2)
        Nx = Astx/Area_of_bar
        # put_text(Nx)
        if Nx%1!=0.0:
            Nx = int(Nx)
            Nx = Nx+1
            # put_text('no of bars', Nx)
            Astx = Area_of_bar*Nx
        else:
            Nx = int(Nx)
            # put_text('no of bars', Nx)
            Astx = Area_of_bar*Nx
        # spacing:
        Spacingx = (L*1000)/Nx
        # in short direction:
        Ny = Asty/Area_of_bar
        if Ny%1!=0.0:
            Ny = int(Ny)
            Ny = Ny+1
            # put_text('no of bars', Ny)
            Asty = Area_of_bar*Ny
        else:
            Ny = int(Ny)
            # put_text('no of bars', Ny)
            Asty = Area_of_bar*Ny
        # spacing:
        Spacingy = (B*1000)/Ny
        put_text('➨  Sorter lenth of footing in m:', B)
        put_text('➨  Longer lenth of footing in m:', L)
        put_text('➨  Provoide', bar , 'mm bars with c/c spacing of', Spacingx , 'mm for longer side of footing.')
        put_text('➨  Provoide', bar , 'mm bars with c/c spacing of', Spacingy , 'mm for shorter side of footing.')
    elif operation=='Staircase design (Dog-legged)' or operation=='Beam Design (Simply supported)':
        put_text(' Staircase design (Dog-legged), Beam Design (Simply supported) are not available now')
        popup('This will available soon!!!.')
        toast('SORRY!!!!')
    Z = select('Do you want to calculate again?',['YES','NO'])
    if Z=='YES':
        k=lambda: run_js('window.location.reload()')
        k()
main()