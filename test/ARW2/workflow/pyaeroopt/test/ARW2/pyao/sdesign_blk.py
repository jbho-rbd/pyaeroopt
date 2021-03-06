from pyaeroopt.interface.sdesign import SdesignInputBlock


## This file defines the files that need to be changed in order to move the problem
## to a new design point.  An outline of the file is as follows:
##      1. Sdesign  file definition
##      2. Material file definition

################################################################################
###############        Sdesign Input File Generation        ####################
################################################################################

#  The following code generates an sdesign input file given a design variable
#  vector p

outstruct = SdesignInputBlock('SDOUTPUT',
                              ['varmode', 'position', 0])

outfluid = SdesignInputBlock('SDOUTPUT',
                             ['varmode', 'fluidposition', 0])

define = SdesignInputBlock('DEFINE',
                           ['# define a box surrounding the wing'],
                           ['x1', 220.0],
                           ['x2', 320.0],
                           ['#'],
                           ['z1', 45.0],
                           ['z2', 65.0],
                           ['#'],
                           ['y1', 7.0],
                           ['y2', 43.0],
                           ['y3', 81.0],
                           ['y4', 125.0],
                           ['#'],
                           ['# define convenient constants'],
                           ['L', 'y4-y1'],
                           ['L1', 'y3-y1'],
                           ['L2', 'y2-y1'],
                           ['#'],
                           ['R1', 'L1/L'],
                           ['R2', 'L2/L'],
                           ['#'],
                           ['chord', '0.5*(x2-x1)'],
                           ['chord1', '0.5*(x2-x1)*R1'],
                           ['chord2', '0.5*(x2-x1)*R2'],
                           ['mchord', '-0.5*(x2-x1)'],
                           ['mchord1', '-0.5*(x2-x1)*R1'],
                           ['mchord2', '-0.5*(x2-x1)*R2'],
                           ['#'],
                           ['B', '100'],
                           ['B1', '100*R1/2'],
                           ['B2', '100*R2/3'],
                           ['B05', '0.05*B'],
                           ['B105', '0.05*B1'],
                           ['B205', '0.05*B2'])

nodes = SdesignInputBlock('NODES',
                          ['1', ' x1', 'y1', 'z1'],
                          ['2', ' x2', 'y1', 'z1'],
                          ['3', ' x2', 'y1', 'z2'],
                          ['4', ' x1', 'y1', 'z2'],
                          ['#'],
                          ['5', ' x1', 'y2', 'z1'],
                          ['6', ' x2', 'y2', 'z1'],
                          ['7', ' x2', 'y2', 'z2'],
                          ['8', ' x1', 'y2', 'z2'],
                          ['#'],
                          ['9', ' x1', 'y3', 'z1'],
                          ['10', 'x2', 'y3', 'z1'],
                          ['11', 'x2', 'y3', 'z2'],
                          ['12', 'x1', 'y3', 'z2'],
                          ['#'],
                          ['13', 'x1', 'y4', 'z1'],
                          ['14', 'x2', 'y4', 'z1'],
                          ['15', 'x2', 'y4', 'z2'],
                          ['16', 'x1', 'y4', 'z2'])

edges = SdesignInputBlock('EDGES',
                          ['# define the edges of the design volume'],
                          ['1', ' linear', '2', '1  2'],
                          ['2', ' linear', '2', '2  3'],
                          ['3', ' linear', '2', '3  4'],
                          ['4', ' linear', '2', '4  1'],
                          ['#'],
                          ['5', ' cubic', ' 4', '1  5  9  13'],
                          ['6', ' cubic', ' 4', '2  6  10 14'],
                          ['7', ' cubic', ' 4', '3  7  11 15'],
                          ['8', ' cubic', ' 4', '4  8  12 16'],
                          ['#'],
                          ['9', ' linear', '2', '13 14'],
                          ['10', 'linear', '2', '14 15'],
                          ['11', 'linear', '2', '15 16'],
                          ['12', 'linear', '2', '16 13'])

patch = SdesignInputBlock('PATCH',
                          ['# 2D patches enclosing the volume'],
                          ['1', 'coons', 'quad4  ', '0', '0', '1  2  3  4'],
                          ['2', 'coons', 'quad4  ', '0', '0', '9  10 11 12'],
                          ['3', 'coons', 'quad8p4', '0', '0', '5  4  8  12'],
                          ['4', 'coons', 'quad8p4', '0', '0', '5  1  6  9'],
                          ['5', 'coons', 'quad8p4', '0', '0', '6  2  7  10'],
                          ['6', 'coons', 'quad8p4', '0', '0', '8  3  7  11'])

volume = SdesignInputBlock('VOLUME',
                           ['# define a volume composed of the patches'],
                           ['1', 'coons', 'brick8 ', '1 1 1', '1  2  3  4  5  6'])

dsgvar = SdesignInputBlock('DSGVAR',
                           ['# the x, y, z components of the control nodes that are design variables'],
                           ['1', ' 0 0 0'],
                           ['2', ' 0 0 0'],
                           ['3', ' 0 0 0'],
                           ['4', ' 0 0 0'],
                           ['#'],
                           ['5', ' 3 0 6'],
                           ['6', ' 3 0 9'],
                           ['7', ' 3 0 9'],
                           ['8', ' 3 0 6'],
                           ['#'],
                           ['9', ' 2 0 5'],
                           ['10', '2 0 8'],
                           ['11', '2 0 8'],
                           ['12', '2 0 5'],
                           ['#'],
                           ['13', '1 0 4'],
                           ['14', '1 0 7'],
                           ['15', '1 0 7'],
                           ['16', '1 0 4'])


def absvar(p):
    """ Generates the ABSVAR input block based on the current parameter
    vector p.
    """
    block = SdesignInputBlock('ABSVAR',
                              ['# Define the abstract variables'],
                              ['# SONE  : sweep'],
                              ['# STWO  : twist'],
                              ['# STHREE: dihedral'],
                              ['1', p[0], '1.0', '-0.1 ', '0.2'],
                              ['2', p[1], '1.0', '-0.1 ', '0.1'],
                              ['3', p[2], '1.0', '-0.05', '0.15'])
    return block

link = SdesignInputBlock('LINK',
                         ['# connect the abstract variables to the design variables'],
                         ['1', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[1] ^ 1.0 }\n'+
                          '          L * OPR[1]\n'+
                          '      }\n'],
                         ['2', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[1] ^ 1.0 }\n'+
                          '          L1 * OPR[1]\n'+
                          '      }\n'],
                         ['3', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[1] ^ 1.0 }\n'+
                          '          L2 * OPR[1]\n'+
                          '      }\n'],
                         ['4', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          chord * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B * VAR[3] ^ 1.0 + B05\n'+
                          '      }\n'],
                         ['5', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          chord1 * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B1 * VAR[3] ^ 1.0 + B105\n'+
                          '      }\n'],
                         ['6', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          chord2 * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B2 * VAR[3] ^ 1.0 + B205\n'+
                          '      }\n'],
                         ['7', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          mchord * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B * VAR[3] ^ 1.0 + B05\n'+
                          '      }\n'],
                         ['8', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          mchord1 * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B1 * VAR[3] ^ 1.0 + B105\n'+
                          '      }\n'],
                         ['9', 'SUM { DEF_OPR[1] = TAN { 1.0 * VAR[2] ^ 1.0 }\n'+
                          '          mchord2 * OPR[1] ^ 1.0 + 0.0\n'+
                          '          B2 * VAR[3] ^ 1.0 + B205\n'+
                          '      }'])

femeshstruct = SdesignInputBlock('FEMESH',
                                 'ARW2.fenodes')

femeshfluid = SdesignInputBlock('FEMESH',
                                'skin.fluid.fenodes')


################################################################################
##############         Material File Generation                   ##############
################################################################################

# The following code generates a material file given a 3-element vector of
# material parameters, p = [material_var_1, material_var_2, material_var_3]

initThicknessDict = dict([('129', 0.1114),
                          ('130', 0.1095),
                          ('131', 0.0695),
                          ('132', 0.0875),
                          ('133', 0.0514),
                          ('135', 0.0491),
                          ('140', 0.0468),
                          ('141', 0.0479),
                          ('142', 0.0536),
                          ('143', 0.0477),
                          ('144', 0.0400),
                          ('153', 0.1387),
                          ('154', 0.08267),
                          ('155', 0.07408),
                          ('156', 0.06399),
                          ('157', 0.1100),
                          ('158', 0.0600),
                          ('159', 0.0571),
                          ('160', 0.0583),
                          ('161', 0.0581),
                          ('162', 0.0500),
                          ('163', 0.0400),
                          ('191', 0.2500),
                          ('255', 0.0500)])

groupDict = dict([('129', 1),
                  ('130', 1),
                  ('131', 2),
                  ('132', 2),
                  ('133', 2),
                  ('135', 2),
                  ('140', 2),
                  ('141', 2),
                  ('142', 2),
                  ('143', 2),
                  ('144', 2),
                  ('153', 1),
                  ('154', 1),
                  ('155', 1),
                  ('156', 1),
                  ('157', 3),
                  ('158', 3),
                  ('159', 1),
                  ('160', 1),
                  ('161', 1),
                  ('162', 1),
                  ('163', 3),
                  ('191', 1),
                  ('255', 3)])

def materialfile(p):
    """Write the modified material vector for a given design point, p.

    Parameters:
    -------------
    p: 1D array of floats
        structural thickness parameters that specify the change in thickness of
        1) the main wing spar,
        2) the secondary wing spars, and
        3) the ribs
    """
    filestring = ("MATERIAL\n"
    "1 .780 .103E8 0.3205 .26139E-3 1.2 1.2 0.0 .0 .0 .0 .0 0.1625E-1 0.402E-2 0.6394\n"
    "2 .3386 .103E8 .3205 .26139E-3 1.2 1.2 0.0 .0 .0 .0 .0 .3413E-2 0.846E-3 0.15954\n"
    "3 .13850 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3546E-3 .88E-4 .2914E-1\n"
    "4 .12770 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2908E-3 .722E-4 .2568E-1\n"
    "5 .11720 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2611E-3 .585E-4 .225E-1\n"
    "6 .10710 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1882E-3 .468E-4 .196E-1\n"
    "7 .09353 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1412E-3 .3515E-4 .1538E-1\n"
    "8 .07717 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .96569E-4 .2405E-4 .1044E-1\n"
    "9 .06588 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .6678E-4 .1662E-4 .7937E-2\n"
    "10 .05874 .103E8 .3205 .26139E-3 1.2 1.2 0 0 0 .0 0 .47424E-4 .11181E-4 .7076E-2\n"
    "11 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9697E-5 .6649E-2\n"
    "12 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9697E-5 .6648E-2\n"
    "13 .06572 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9697E-5 .6648E-2\n"
    "14 .12580 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .90559E-3 .1205E-3 .1516E-1\n"
    "15 .07264 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9705E-5 .6644E-2\n"
    "16 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9705E-5 .6644E-2\n"
    "17 .78000 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1625E-1 .4054E-2 .6341\n"
    "18 .33860 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3413E-2 .8503E-3 .15882\n"
    "19 .13850 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3546E-3 .8809E-4 .2912E-1\n"
    "20 .12770 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2908E-3 .7204E-4 .2574E-1\n"
    "21 .11720 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2611E-3 .5807E-4 .2265E-1\n"
    "22 .10710 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1882E-3 .4618E-4 .1987E-1\n"
    "23 .09353 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1412E-3 .3446E-4 .1568E-1\n"
    "24 .07717 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .96569E-4 .2348E-4 .1069E-1\n"
    "25 .06588 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .6678E-4 .1625E-4 .8122E-2\n"
    "26 .05874 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .47424E-4 .1154E-4 .724E-2\n"
    "27 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9477E-5 .6804E-2\n"
    "28 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9481E-5 .68E-2\n"
    "29 .06633 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9487E-5 .6796E-2\n"
    "30 .13160 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .13458E-2 .1343E-3 .162E-1\n"
    "31 .07455 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9499E-5 .6787E-2\n"
    "32 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9499E-5 .6787E-2\n"
    "33 .11040 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .13248E-3 .3312E-4 .3115E-1\n"
    "34 .09180 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1102E-3 .2754E-4 .1791E-1\n"
    "35 .08760 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .10512E-3 .2628E-4 .1556E-1\n"
    "36 .08100 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .97201E-4 .243E-4 .12302E-4\n"
    "37 3.33800 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .99841 .3185 .27081E1\n"
    "38 .0500 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1455E-3 .41667E-4 .10417E-2\n"
    "39 .03000 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .33264E-4 .9E-5 .625E-3\n"
    "40 .04965 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .5958E-4 .149E-4 .2833E-2\n"
    "43 .04314 .103E8 .3205 .26139E-3 1.2 1.2 0 0 0 .0 0 .51769E-4 .1294E-4 .18585E-2\n"
    "44 .03930 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .47159E-4 .1179E-4 .1405E-4\n"
    "45 .03930 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .13258E-2 .1179E-4 .1405E-4\n"
    "46 .17600 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2006E-2 .5867E-3 .1136E-1\n"
    "47 .50880 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .43419E-2 .10854E-2 .4287\n"
    "48 .24660 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .13258E-2 .3314E-3 .8836E-1\n"
    "49 .13850 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3546E-3 .8864E-4 .2894E-1\n"
    "50 .12770 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2907E-3 .7268E-4 .2551E-1\n"
    "51 .11720 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2357E-3 .5892E-4 .2238E-1\n"
    "52 .10720 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1886E-3 .4714E-4 .1952E-1\n"
    "53 .09360 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1415E-3 .3537E-4 .1532E-1\n"
    "54 .07730 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .97041E-4 .2426E-4 .1042E-1\n"
    "55 .06600 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .67139E-4 .1678E-4 .792E-2\n"
    "56 .05880 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .47588E-4 .119E-4 .7056E-2\n"
    "57 .05520 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3893E-4 .9734E-5 .6624E-2\n"
    "63 .11040 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1325E-3 .3312E-4 .3115E-1\n"
    "65 .08760 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1051E-3 .2628E-4 .1556E-1\n"
    "66 .08100 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .97201E-4 .243E-4 .123E-4\n"
    "67 3.74500 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1154E1 .3573 .3823E1\n"
    "68 .04000 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1124E-3 .375E-4 .5333E-3\n"
    "69 .02760 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .3312E-4 .828E-5 .4867E-3\n"
    "70 .16800 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .1902E-2 .56E-3 .9878E-2\n"
    "71 .12616 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .354E-4 .1525E-1 .89E-5\n"
    "72 1.27500 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .1929 .2194 .5932E-1\n"
    "73 .78508 .3E+10 .3000 0. 1.0 0 .0 0 .0 0 .0 .981748E-1 .49087E-1 .49087E-1\n"
    "74 2.29500 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .3831 .14269E1 .1107\n"
    "75 .13530 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .2301E-3 .2292E-3 .3053E-1\n"
    "76 .11080 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .1633E-3 .8986E-4 .229E-1\n"
    "77 .11460 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .17E-3 .8952E-4 .2354E-1\n"
    "78 .08100 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .7873E-4 .1968E-4 .1519E-1\n"
    "79 .10410 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .1182E-3 .1238E-3 .2365E-1\n"
    "81 .11260 .103E8 .2050 .30021E-3 1.0 1.0 0 .0 0 .0 0 .1658E-3 .1053E-3 .2374E-1\n"
    "82 .12150 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .1816E-3 .1307E-3 .2608E-1\n"
    "84 .10060 .103E8 .3205 .30021E-3 1.0 1.0 0 .0 0 .0 0 .1154E-3 .8231E-4 .2157E-1\n"
    "85 .04500 .103E8 .3205 .26139E-3 1.0 1.0 0 .0 0 .0 0 .54E-4 .135E-4 .2109E-2\n"
    "86 .17200 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .4299E-3 .424E-1 .1433E-3\n"
    "87 .12535 .3E8 .3000 0. 1.0 0 .0 0 .0 0 .0 .25132E-2 .12566E-2 .12566E-2\n"
    "88 4.69000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .70002E1 .65 .666E1\n"
    "89 6.80000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .1E2 .164E1 .907E1\n"
    "90 5.36000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .45E1 .88 .736E1\n"
    "91 78.53951 .3E8 .3000 0. 1.0 0 .0 0 .0 0 .0 0 .49087E3 .49087E3\n"
    "92 100.0 .3E8 .3000 0. 0 .0 0 .0 0 .0 0 .623E1 .151E1 .151E1\n"
    "93 78.53951 .3E+10 .3000 0. 1.0 0 .0 0 .0 0 .0 .98175E3 .49087E3 .49087E3\n"
    "94 0 .103E8 .3205 .12852E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "95 0 .103E8 .3205 .13401E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "96 0 .103E8 .3205 .19107E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "98 0 .103E8 .3205 .17536E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "99 0 .103E8 .3205 .18284E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "100 0 .103E8 .3205 .15505E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "102 0 .103E8 .3205 .21977E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "103 0 .103E8 .3205 .21108E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "104 0 .103E8 .3205 .16861E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "106 0 .103E8 .3205 .21146E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "107 0 .103E8 .3205 .2205E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "108 0 .103E8 .3205 .17578E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "110 0 .103E8 .3205 .1934E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "111 0 .103E8 .3205 .20166E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "112 0 .103E8 .3205 .15352E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "114 0 .103E8 .3205 .16633E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "115 0 .103E8 .3205 .17342E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "116 0 .103E8 .3205 .13204E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "117 0 .103E8 .3205 .14832E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "118 0 .103E8 .3205 .15461E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "119 0 .103E8 .3205 .1177E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "121 0 .103E8 .3205 .13023E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "122 0 .103E8 .3205 .13577E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "123 0 .103E8 .3205 .89053E-4 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "124 0 .103E8 .3205 .89053E-5 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "127 0 .103E8 .3205 .89053E-5 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "129 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['129'] + p[groupDict['129']-1]) +
    "130 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['130'] + p[groupDict['130']-1]) +
    "131 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['131'] + p[groupDict['131']-1]) +
    "132 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['132'] + p[groupDict['132']-1]) +
    "133 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['133'] + p[groupDict['133']-1]) +
    "135 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['135'] + p[groupDict['135']-1]) +
    "140 0 .348E7 .4000 .17704E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['140'] + p[groupDict['140']-1]) +
    "141 0 .103E8 .3205 .64803E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['141'] + p[groupDict['141']-1]) +
    "142 0 .103E8 .3205 .64803E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['142'] + p[groupDict['142']-1]) +
    "143 0 .103E8 .3205 .64803E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['143'] + p[groupDict['143']-1]) +
    "144 0 .103E8 .3205 .64803E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['144'] + p[groupDict['144']-1]) +
    "145 0 .348E7 .4000 .17704E-3 0 .0 .07300 0 .0 0 .0 0 .0 .0\n"
    "146 0 .348E7 .4000 .17704E-3 0 .0 .06840 0 .0 0 .0 0 .0 .0\n"
    "147 0 .348E7 .4000 .17704E-3 0 .0 .06120 0 .0 0 .0 0 .0 .0\n"
    "148 0 .348E7 .4000 .17704E-3 0 .0 .05040 0 .0 0 .0 0 .0 .0\n"
    "149 0 .348E7 .4000 .17704E-3 0 .0 .04320 0 .0 0 .0 0 .0 .0\n"
    "150 0 .348E7 .4000 .17704E-3 0 .0 .03600 0 .0 0 .0 0 .0 .0\n"
    "151 0 .348E7 .4000 .17704E-3 0 .0 .06600 0 .0 0 .0 0 .0 .0\n"
    "152 0 .348E7 .4000 .17704E-3 0 .0 .05767 0 .0 0 .0 0 .0 .0\n"
    "153 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['153'] + p[groupDict['153']-1]) +
    "154 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['154'] + p[groupDict['154']-1]) +
    "155 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['155'] + p[groupDict['155']-1]) +
    "156 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['156'] + p[groupDict['156']-1]) +
    "157 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['157'] + p[groupDict['157']-1]) +
    "158 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['158'] + p[groupDict['158']-1]) +
    "159 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['159'] + p[groupDict['159']-1]) +
    "160 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['160'] + p[groupDict['160']-1]) +
    "161 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['161'] + p[groupDict['161']-1]) +
    "162 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['162'] + p[groupDict['162']-1]) +
    "163 0 .103E8 .3205 .26139E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['163'] + p[groupDict['163']-1]) +
    "190 0 .103E2 .3205 .17704E-3 0 .0 .25000 0 .0 0 .0 0 .0 .0\n"
    "191 0 .2E7 .3000 .10999E-3 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['191'] + p[groupDict['191']-1]) +
    "195 0 .15E8 .3205 0. 0 .0 .25000 0 .0 0 .0 0 .0 .0\n"
    "199 .12000 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "200 .05880 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "201 .14880 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "203 .03920 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "204 .06000 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "205 .03000 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "209 .05000 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "212 .15900 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "213 .12960 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "214 .03100 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "215 .07334 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "216 .04500 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "217 .05000 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "218 .03000 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "219 .04432 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "220 .02700 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "221 .03566 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "222 .03938 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "223 .01700 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "224 .03858 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "226 .04612 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "227 .03160 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "228 .01580 .348E7 .4000 .17704E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "229 .09820 .103E8 .3205 .99896E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "230 .06760 .103E8 .3205 .99896E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "231 .05820 .103E8 .3205 .99896E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "232 1.55500 .103E8 .3205 .26139E-3 0 .0 0 .0 0 .0 0 .0 0 .0\n"
    "235 .02700 .103E8 .3205 .26139E-3 1.2 1.2 0 .0 0 .0 0 .2955E-4 .81E-5 .4556E-3\n"
    "240 3.50000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .25E1 .46 .229E1\n"
    "241 2.00000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .63998 .26 .42\n"
    "244 4.50000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .45E1 .7 .406E1\n"
    "245 3.30000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .26E1 .33 .247E1\n"
    "246 1.00000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .15 .32E-1 .21\n"
    "248 1.60000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .3 .13 .34\n"
    "249 6.00000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .1E2 .219E1 .589E1\n"
    "250 4.18000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .45E1 .72 .406E1\n"
    "251 5.76000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .55E1 .188E1 .559E1\n"
    "253 6.00000 .15E8 .3205 0. 1.2 1.2 0 .0 0 .0 0 .45E1 .113E1 .8E1\n"
    "255 0 .103E8 .3205 .101 0 .0 {:.12f} 0 .0 0 .0 0 .0 .0\n".format(initThicknessDict['255'] + p[groupDict['255']-1]) +
    "436 0 .103E8 .3205 .89053E-5 0 .0 0 .0 0 .0 0 .0 0 .0\n")
    return filestring

