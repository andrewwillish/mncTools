__author__ = 'andrew.willis'

#SYNOPTIC GENERATOR
#Andrew Willis [2014]

import xml.etree.cElementTree as ET
import imp
import os
import asiist

import maya.cmds as cmds

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
WIN_ROOT = os.environ['ProgramFiles'][:2]+'/'

#get project name and project code from asiist
for chk in asiist.getEnvi():
    if chk[0] == 'projName': PRJ_NAME = chk[1]
    if chk[0] == 'projCode': PRJ_CODE = chk[1]

PROJECTvar = PRJ_NAME

#parse license
import licenseParsing
licenseParsing.licParse()

#Declare file data
SYNOPTICSIZEXvar=''
SYNOPTICSIZEYvar=''
SYNOPTICNAMEvar=''
SYNOPTICCOLORvar=[0.5,0.5,0.5]
COMPONENTSlis=[]

class synopticGeneratorCLS:
    def __init__(self):
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld, SELECTIONLISTtxtscr

        if cmds.window('synopticGenerator',exists=True):cmds.deleteUI('synopticGenerator',wnd=True)
        if cmds.window('currentSynoptic',exists=True):cmds.deleteUI('currentSynoptic',wnd=True)

        win = cmds.window(t='Synoptic Generator',menuBar=True,s=False,w=205,h=750,tbm=False)
        cmds.renameUI(win, 'synopticGenerator')
        cmds.menu(l='File')
        cmds.menuItem(l='New Synoptic',c=self.NEWSYNfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Save Synoptic XML ...',c=self.SAVEINSTRUCTIONfn)
        cmds.menuItem(l='Open Synoptic XML ...',c=self.OPENINSTRUCTIONfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Close Current Synoptic',c=self.CLOSECURRENTSYNfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Compile Synoptic',c=self.COMPILESYNOPTICfn)
        cmds.menuItem(l='Compile Synoptic to Local',c=self.COMPILELOCALfn)
        cmds.menuItem(l='Compile Synoptic to Server',c=self.COMPILESHARESYNOPTICfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Exit',c=self.EXITfn)

        cmds.menu(l='Synoptic')
        cmds.menuItem(l='Change Synoptic Window Size',c=self.CHANGESYNWINSIZEfn)
        cmds.menuItem(l='Change Synoptic Window Color',c=self.CHANGESYNWINCOLORfn)

        cmds.menu(l='Help')
        cmds.menuItem(l='About',c=self.ABOUTfn)

        cmas=cmds.columnLayout(adj=True,w=200)

        f0=cmds.frameLayout(l='Component Library',p=cmas,w=200)
        cmds.columnLayout(adj=True)
        COMPONENTLIBtxtscr=cmds.textScrollList(sc=self.POPULATECONTROLfn)
        cmds.separator()

        cmds.rowColumnLayout()
        cmds.rowColumnLayout(nc=3, columnWidth=[(1, 99),(2,2), (3, 99)], p=cmas)
        cmds.button(l='ADD COMPONENT',h=20, bgc=[0.328767123313,0.684931506747,0.0],c=self.ADDCOMPONENTfn)
        cmds.text(l='')
        cmds.button(l='DEL COMPONENT',bgc=[1,0,0],h=20,c=self.DELETECOMPONENTfn)

        f1=cmds.frameLayout(l='Component Control',p=cmas)
        f11=cmds.columnLayout(adj=True)

        cmds.text(l='  Component Name & Caption',bgc=[1,1,1],al='left', fn='boldLabelFont',p=f11)
        cmds.separator()
        cmds.text(l='Name:',al='left')
        COMPNAMEtxtfld=cmds.textField(cc=self.CHANGECOMPNAMEfn)
        cmds.text(l='Caption:',al='left')
        COMPCAPTIONtxtfld=cmds.textField(cc=self.CHANGECOMPNCAPTIONfn)

        cmds.text(l='',p=f11,h=4)

        cmds.text(l='  Component Position',bgc=[1,1,1],al='left', fn='boldLabelFont',p=f11)
        cmds.separator()
        cmds.rowColumnLayout(nc=4, columnWidth=[(1, 20),(2,78), (3, 20),(4,78)], p=f11)
        cmds.text(l='X: ')
        COMPXLOCtxtfld=cmds.textField(cc=self.CHANGECOMPPOSfn)
        cmds.text(l='Y: ')
        COMPYLOCtxtfld=cmds.textField(cc=self.CHANGECOMPPOSfn)

        cmds.rowColumnLayout(nc=5, columnWidth=[(1, 40),(2,40), (3, 35),(4,40),(5,40)], p=f11)
        cmds.button(l="LEFT",c=lambda*args:self.CHANGECOMPPOSINCfn(0))
        cmds.button(l="RIGHT",c=lambda*args:self.CHANGECOMPPOSINCfn(1))
        COMPINCREMENTtxtfld=cmds.textField(tx='1')
        cmds.button(l="UP",c=lambda*args:self.CHANGECOMPPOSINCfn(2))
        cmds.button(l="DOWN",c=lambda*args:self.CHANGECOMPPOSINCfn(3))

        cmds.text(l='',p=f11,h=4)

        cmds.text(l='  Component Size',bgc=[1,1,1],al='left', fn='boldLabelFont',p=f11)
        cmds.separator(p=f11)
        cmds.rowColumnLayout(nc=4, columnWidth=[(1, 20),(2,78), (3, 20),(4,78)], p=f11)
        cmds.text(l='X: ')
        COMPXSIZEtxtfld=cmds.textField(cc=self.CHANGECOMPSIZEfn)
        cmds.text(l='Y: ')
        COMPYSIZEtxtfld=cmds.textField(cc=self.CHANGECOMPSIZEfn)

        cmds.text(l='',p=f11,h=4)

        cmds.text(l='  Component Color',bgc=[1,1,1],al='left', fn='boldLabelFont',p=f11)
        cmds.separator(p=f11)
        cmds.rowColumnLayout(nc=2, columnWidth=[(1, 20),(2,175)], p=f11)
        cmds.text(l='R: ')
        COMPCOLORRfltsld=cmds.floatSlider(min=0,max=1,v=0,dc=self.CHANGECOMPCOLORSLIDERfn)
        cmds.text(l='G: ')
        COMPCOLORGfltsld=cmds.floatSlider(min=0,max=1,dc=self.CHANGECOMPCOLORSLIDERfn)
        cmds.text(l='B: ')
        COMPCOLORBfltsld=cmds.floatSlider(min=0,max=1,dc=self.CHANGECOMPCOLORSLIDERfn)
        cmds.separator(p=f11)
        cmds.rowColumnLayout(nc=6, columnWidth=[(1, 20),(2,45), (3, 20),(4,45),(5,20),(6,45)], p=f11)
        cmds.text(l='R:')
        COMPCOLORRtxtfld=cmds.textField(cc=self.CHANGECOMPCOLORfn)
        cmds.text(l='G:')
        COMPCOLORGtxtfld=cmds.textField(cc=self.CHANGECOMPCOLORfn)
        cmds.text(l='B:')
        COMPCOLORBtxtfld=cmds.textField(cc=self.CHANGECOMPCOLORfn)

        cmds.text(l='',p=f11,h=4)

        cmds.text(l='  Component Selection',bgc=[1,1,1],al='left', fn='boldLabelFont',p=f11)
        cmds.separator(p=f11)
        cmds.button(l='SET COMPONENT SELECTION SET',h=40,p=f11,bgc=[1.0,0.643835616566,0.0],\
                    c=self.COMPSETSELECTIONfn)
        cmds.separator(p=f11)
        cmds.text(l='Selection List:',p=f11,al='left')
        SELECTIONLISTtxtscr=cmds.textScrollList(p=f11,h=100,en=False)
        cmds.showWindow()
        return

    def ABOUTfn(self,*args):
        cmds.confirmDialog(t='About',m='SYNOPTIC GENERATOR\n\nCreated by Andrew Willis [2014]',button=['Ok'])
        return

    def COMPILELOCALfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        if not os.path.isdir(WIN_ROOT+'/synopticLocalLibrary'):
            os.makedirs(WIN_ROOT+'/synopticLocalLibrary')

        WRITEvar=self.COMPILEINSTRUCTIONfn()

        if os.path.isfile(WIN_ROOT+'/synopticLocalLibrary/'+SYNOPTICNAMEvar+'.pyc'):
            REPvar=cmds.confirmDialog(icn='warning',t='Existing File',\
                                      m='There is an existing synoptic with the same name. Would you like to replace it?',\
                                      button=['Yes','No'])
            if REPvar=='No':
                cmds.error('error : operation cancelled by user')

        OPvar=open(WIN_ROOT+'/synopticLocalLibrary/'+SYNOPTICNAMEvar+'.py','w')
        OPvar.write(WRITEvar)
        OPvar.close()

        imp.load_source(SYNOPTICNAMEvar+'Synoptic',WIN_ROOT+'/synopticLocalLibrary/'+SYNOPTICNAMEvar+'.py')

        os.remove(WIN_ROOT+'/synopticLocalLibrary/'+SYNOPTICNAMEvar+'.py')
        cmds.confirmDialog(icn='information',\
                           t='Compile Done',\
                           m='Synoptic successfully compiled.',\
                           button=['Ok'])
        return

    def COMPILESHARESYNOPTICfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        if not cmds.window('currentSynoptic',exists=True):
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        if PROJECTvar=='':
            cmds.confirmDialog(icn='warning',\
                               t='Sharing Error',\
                               m='Unable to share synoptic outside server service.',\
                               button=['Ok'])
            cmds.error('error : unable to share synoptic')

        REPvar=cmds.confirmDialog(icon='question',\
                                  t='Share Synoptic',\
                                  m='This will share current synoptic to server for project '+PROJECTvar+'.',\
                                  button=['Ok','Cancel'])
        if REPvar == 'Cancel':
            cmds.error('error : cancelled by user')

        if not os.path.isdir(SCRIPT_ROOT+'/synopticLibrary/'+PROJECTvar): os.makedirs(SCRIPT_ROOT+'/synopticLibrary/'+PROJECTvar)

        WRITEvar=self.COMPILEINSTRUCTIONfn()

        if not os.path.isfile(SCRIPT_ROOT+'/TECH/synopticLibrary/'+PROJECTvar+'/'+SYNOPTICNAMEvar+'.pyc'):
            REPvar=cmds.confirmDialog(icn='warning',t='Existing File',\
                                      m='There is an existing synoptic with the same name. Would you like to replace it?',\
                                      button=['Yes','No'])
            if REPvar=='No':
                cmds.error('error : operation cancelled by user')

        OPvar=open(SCRIPT_ROOT+'/TECH/synopticLibrary/'+PROJECTvar+'/'+SYNOPTICNAMEvar+'.py','w')
        OPvar.write(WRITEvar)
        OPvar.close()

        imp.load_source(SYNOPTICNAMEvar+'Synoptic',SCRIPT_ROOT+'/TECH/synopticLibrary/'+PROJECTvar+'/'+SYNOPTICNAMEvar+'.py')

        os.remove(SCRIPT_ROOT+'/TECH/synopticLibrary/'+PROJECTvar+'/'+SYNOPTICNAMEvar+'.py')
        cmds.confirmDialog(icn='information',\
                           t='Compile Done',\
                           m='Synoptic successfully shared to server.',\
                           button=['Ok'])

        #UNSAVED MARKER============================================================
        if not SYNOPTICNAMEvar.endswith('*'):
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================
        return

    def COMPILESYNOPTICfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        if not cmds.window('currentSynoptic',exists=True):
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        #Get compiling file path
        FILESPATHvar=cmds.fileDialog2(cap='Select Target Directory',fm=3)
        if FILESPATHvar<>None:
            FILESPATHvar=FILESPATHvar[0]

            WRITEvar=self.COMPILEINSTRUCTIONfn()

            OPvar=open(FILESPATHvar+'/'+SYNOPTICNAMEvar+'.py','w')
            OPvar.write(WRITEvar)
            OPvar.close()

            imp.load_source(SYNOPTICNAMEvar+'Synoptic',FILESPATHvar+'/'+SYNOPTICNAMEvar+'.py')

            os.remove(FILESPATHvar+'/'+SYNOPTICNAMEvar+'.py')
            cmds.confirmDialog(icn='information',\
                               t='Compile Done',\
                               m='Synoptic successfully compiled.',\
                               button=['Ok'])

        return

    def COMPILEINSTRUCTIONfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        #Write temp file
        WRITEvar=\
"""import maya.cmds as cmds

#License Parsing==========================================================================================
import maya.mel as mel
LICERRORvar=0
try:
    LICREADvar=mel.eval('mncalic')
    if LICREADvar<>'Valid License File':
        LICERRORvar=1
except:
    cmds.confirmDialog(icn='warning',t='Missing License',m='Cannot locate MNCA Tools license!', button=['Ok'])
    cmds.error('Missing License')
if LICERRORvar==1:
    cmds.confirmDialog(icn='warning',t='Expired License',m='Your license has expired!', button=['Ok'])
    cmds.error('Expired License')
#License Parsing==========================================================================================


class """+str(SYNOPTICNAMEvar)+"""CLS:
    def __init__(self):
        global namespaceBTN, namespaceTXT
        if cmds.window('"""+str(SYNOPTICNAMEvar)+"""SYN',exists=True):
            cmds.deleteUI('"""+str(SYNOPTICNAMEvar)+"""SYN',wnd=True)

        cmds.window('"""+str(SYNOPTICNAMEvar)+"""SYN',t='"""+str(SYNOPTICNAMEvar)+""" Synoptic',s=False,w="""+str(SYNOPTICSIZEXvar)+""",h="""+str(int(SYNOPTICSIZEYvar)+40)+""")
        form=cmds.formLayout()
        cmds.text(l='',w="""+str(SYNOPTICSIZEXvar)+""",h="""+str(SYNOPTICSIZEYvar)+""",bgc="""+str(SYNOPTICCOLORvar)+""")

"""

        for chk in COMPONENTSlis:
            WRITEvar=WRITEvar+\
"""
        cmds.button('"""+str(chk[0])+"""',l='"""+str(chk[1])+"""',w="""+str(chk[4])+""",h="""+str(chk[5])+""",bgc="""+str(chk[6])+""",c=lambda*args:self.SELECTIONfn("""+str(chk[7])+"""))"""
            WRITEvar=WRITEvar+\
"""
        cmds.formLayout(form,e=True,attachForm=[('"""+str(chk[0])+"""','top',"""+str(chk[3])+"""),('"""+str(chk[0])+"""','left',"""+str(chk[2])+""")])"""
        WRITEvar=WRITEvar+\
"""

        namespaceBTN=cmds.button('nameSpaceButton',l='SET NAMESPACE',h=20,bgc=[1.0,0.643835616566,0.0],w="""+str(SYNOPTICSIZEXvar)+""",c=self.SETNAMESPACEfn)
        cmds.formLayout(form,e=True,attachForm=[('nameSpaceButton','top',"""+str(SYNOPTICSIZEYvar)+"""),('nameSpaceButton','left',0)])
        namespaceTXT=cmds.text('textNameSpace',l='<n/a>',h=20,w="""+str(SYNOPTICSIZEXvar)+""",fn='boldLabelFont')
        cmds.formLayout(form,e=True,attachForm=[('textNameSpace','top',"""+str(SYNOPTICSIZEYvar+20)+"""),('textNameSpace','left',0)])

        cmds.showWindow()
        return

    def SELECTIONfn(self,SELECTIONlis):
        global namespaceBTN, namespaceTXT
        MODvar=cmds.getModifiers()

        namespaceVar=cmds.text(namespaceTXT,q=True,l=True)
        if namespaceVar=='<n/a>':
            namespaceVar=''
        else:
            namespaceVar=namespaceVar+':'

        TEMPlis=[]
        for chk in SELECTIONlis:
            TEMPlis.append(namespaceVar+chk)

        if MODvar==0:
            cmds.select(TEMPlis)
        elif MODvar==1:
            cmds.select(TEMPlis,add=True)
        return

    def SETNAMESPACEfn(self,*args):
        global namespaceBTN, namespaceTXT
        SELvar=cmds.ls(sl=True)
        if SELvar==[]:
            cmds.confirmDialog(icn='warning',t='Error',m='No object selected!',button=['Ok'])
            cmds.error('error : no object selected')
        SELvar=SELvar[0]
        cmds.text(namespaceTXT,e=True,l=SELvar[:SELvar.find(':')])
        return

"""+str(SYNOPTICNAMEvar)+"""CLS()
"""
        return WRITEvar

    def OPENINSTRUCTIONfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        #Unsave shield
        if SYNOPTICNAMEvar.endswith('*')==True:
            REPvar=cmds.confirmDialog(icn='question',\
                                      t='Save Synoptic',\
                                      m='There is an unsaved synoptic in the workspace. Would you like to save it?',\
                                      button=["Save","Don't save","Cancel"])
            if REPvar=='Cancel':
                cmds.error('error : cancelled by user')
            elif REPvar=='Save':
                self.SAVEINSTRUCTIONfn()

        #Get file path
        FILEPATHvar=cmds.fileDialog(m=0,t='Open Synoptic',dm='*.xml')
        if FILEPATHvar=='':
            cmds.error('error : cancelled by user')

        #Parse file path
        tree=ET.parse(FILEPATHvar)
        root=tree.getroot()

        #Get synopticData
        SYNOPTICSIZEXvar=int(root[0][0].text)
        SYNOPTICSIZEYvar=int(root[0][1].text)

        TEMPlis=[]
        TEMPlis.append(float(root[0][2].get('R')))
        TEMPlis.append(float(root[0][2].get('G')))
        TEMPlis.append(float(root[0][2].get('B')))
        SYNOPTICCOLORvar=TEMPlis

        SYNOPTICNAMEvar=FILEPATHvar[FILEPATHvar.rfind('/')+1:FILEPATHvar.rfind('.x')]

        #Get componentData
        COMPONENTSlis=[]

        for chk in root[1]:
            TEMPlis=[]
            #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
            TEMPlis.append(chk.tag)
            TEMPlis.append(chk.get('compCaption'))
            TEMPlis.append(chk.get('compXLoc'))
            TEMPlis.append(chk.get('compYLoc'))
            TEMPlis.append(chk.get('compXSize'))
            TEMPlis.append(chk.get('compYSize'))
            COLORTEMPlis=chk.get('compColor').split(',')
            DUMPlis=[]
            for chz in COLORTEMPlis:
                DUMPlis.append(float(chz))
            TEMPlis.append(DUMPlis)
            TEMPlis.append(chk.get('compSelList').split(','))
            COMPONENTSlis.append(TEMPlis)

        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
        for chk in COMPONENTSlis:
            cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

        cmds.textField(COMPNAMEtxtfld,e=True,tx='')
        cmds.textField(COMPCAPTIONtxtfld,e=True,tx='')
        cmds.textField(COMPXLOCtxtfld,e=True,tx='')
        cmds.textField(COMPYLOCtxtfld,e=True,tx='')
        cmds.textField(COMPXSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPYSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORRtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORGtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORBtxtfld,e=True,tx='')

        cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(0.0))
        cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)

        #Build synoptic again
        self.BUILDSYNOPTICWINfn()
        return

    def SAVEINSTRUCTIONfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        #IMPLEMENT XML STYLE FOR SAVING SYNOPTIC INSTRUCTION SET

        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        #Get save file path
        FILEPATHvar=cmds.fileDialog(m=1,t='Save Synoptic',dm='*.xml')

        #Save procedure
        root=ET.Element("root")

        #Saving basic synopticData
        synopticData=ET.SubElement(root,'synopticData')

        synXVar=ET.SubElement(synopticData,'synXVar')
        synXVar.text=str(SYNOPTICSIZEXvar)
        synYVar=ET.SubElement(synopticData,'synYVar')
        synYVar.text=str(SYNOPTICSIZEYvar)
        synColorVar=ET.SubElement(synopticData,'synColorLis')
        synColorVar.set('R',str(SYNOPTICCOLORvar[0]))
        synColorVar.set('G',str(SYNOPTICCOLORvar[1]))
        synColorVar.set('B',str(SYNOPTICCOLORvar[2]))

        #Saving component data
        componentData=ET.SubElement(root,'componentData')

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        for chk in COMPONENTSlis:
            TEMPvar=ET.SubElement(componentData,str(chk[0]))
            TEMPvar.set('compName',str(chk[0]))
            TEMPvar.set('compCaption',str(chk[1]))
            TEMPvar.set('compXLoc',str(chk[2]))
            TEMPvar.set('compYLoc',str(chk[3]))
            TEMPvar.set('compXSize',str(chk[4]))
            TEMPvar.set('compYSize',str(chk[5]))

            TEMPlis=[]
            for chr in chk[6]:
                TEMPlis.append(str(chr))
            TEMPvar.set('compColor',str(','.join(TEMPlis)))

            TEMPlis=[]
            for chr in chk[7]:
                TEMPlis.append(str(chr))
            TEMPvar.set('compSelList',str(','.join(TEMPlis)))

        tree=ET.ElementTree(root)
        tree.write(FILEPATHvar)

        SYNOPTICNAMEvar=FILEPATHvar[FILEPATHvar.rfind('/')+1:FILEPATHvar.rfind('.x')]

        #Build synoptic again
        self.BUILDSYNOPTICWINfn()
        return

    def COMPSETSELECTIONfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        SELlis=cmds.ls(sl=True)
        TEMPlis=[]

        for chk in SELlis:
            if chk.find(':')<>-1:
                TEMPlis.append(chk[chk.find(':')+1:])
            else:
                TEMPlis.append(chk)

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][7]=TEMPlis
            cnt+=1

        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=SELvar)

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        self.POPULATECONTROLfn()
        return

    def CHANGECOMPCOLORSLIDERfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        Rvar=cmds.floatSlider(COMPCOLORRfltsld,q=True,v=True)
        Gvar=cmds.floatSlider(COMPCOLORGfltsld,q=True,v=True)
        Bvar=cmds.floatSlider(COMPCOLORBfltsld,q=True,v=True)

        cmds.textField(COMPCOLORRtxtfld,e=True,tx=str(Rvar))
        cmds.textField(COMPCOLORGtxtfld,e=True,tx=str(Gvar))
        cmds.textField(COMPCOLORBtxtfld,e=True,tx=str(Bvar))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        self.CHANGECOMPCOLORfn()
        return

    def CHANGECOMPCOLORfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================
        COLORAlis=[]
        Rvar=cmds.textField(COMPCOLORRtxtfld,q=True,tx=True)
        Gvar=cmds.textField(COMPCOLORGtxtfld,q=True,tx=True)
        Bvar=cmds.textField(COMPCOLORBtxtfld,q=True,tx=True)

        COLORAlis.append(float(Rvar))
        COLORAlis.append(float(Gvar))
        COLORAlis.append(float(Bvar))

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][6]=COLORAlis
            cnt+=1

        #Build synoptic again
        cmds.button(str(FILElis[0]),e=True,bgc=COLORAlis)

        cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(Rvar))
        cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(Gvar))
        cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(Bvar))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=SELvar)
        return

    def CHANGECOMPSIZEfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        XSIZEvar=cmds.textField(COMPXSIZEtxtfld,q=True,tx=True)
        YSIZEvar=cmds.textField(COMPYSIZEtxtfld,q=True,tx=True)

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][4]=XSIZEvar
                COMPONENTSlis[cnt][5]=YSIZEvar
            cnt+=1

        #Build synoptic again
        cmds.button(FILElis[0],e=True,w=int(XSIZEvar),h=int(YSIZEvar))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=SELvar)
        return

    def CHANGECOMPPOSINCfn(self,DIRvar):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        INCval=cmds.textField(COMPINCREMENTtxtfld,q=True,tx=True)

        if INCval=='':
            cmds.confirmDialog(icn='warning',\
                               title='Error',\
                               message='X position or Y position can not be empty!',\
                               button=['Ok'])
            cmds.error('error : X or Y position is empty')

        if INCval.isdigit()==False:
            cmds.confirmDialog(icn='warning',\
                               title='Error',\
                               message='X position or Y position is not number',\
                               button=['Ok'])
            cmds.error('error : X or Y position is not number')

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        #DIRvar 0=LEFT, 1=RIGHT, 2=UP, 3=DOWN
        if DIRvar==0:
            CURRENTvar=cmds.textField(COMPXLOCtxtfld,q=True,tx=True)
            WRITEvar=int(CURRENTvar)-int(INCval)
            if WRITEvar<=0:
                WRITEvar=0
            cmds.textField(COMPXLOCtxtfld,e=True,tx=str(WRITEvar))
        elif DIRvar==1:
            CURRENTvar=cmds.textField(COMPXLOCtxtfld,q=True,tx=True)
            WRITEvar=(int(CURRENTvar)+int(INCval))
            if WRITEvar>=int(SYNOPTICSIZEXvar)-int(FILElis[4]):
                WRITEvar=int(SYNOPTICSIZEXvar)-int(FILElis[4])
            cmds.textField(COMPXLOCtxtfld,e=True,tx=str(WRITEvar))
        elif DIRvar==2:
            CURRENTvar=cmds.textField(COMPYLOCtxtfld,q=True,tx=True)
            WRITEvar=int(CURRENTvar)-int(INCval)
            if WRITEvar<=0:
                WRITEvar=0
            cmds.textField(COMPYLOCtxtfld,e=True,tx=str(WRITEvar))
        elif DIRvar==3:
            CURRENTvar=cmds.textField(COMPYLOCtxtfld,q=True,tx=True)
            WRITEvar=int(CURRENTvar)+int(INCval)
            if WRITEvar>=int(SYNOPTICSIZEYvar)-int(FILElis[5]):
                WRITEvar=int(SYNOPTICSIZEYvar)-int(FILElis[5])
            cmds.textField(COMPYLOCtxtfld,e=True,tx=str(WRITEvar))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        self.CHANGECOMPPOSfn()
        return

    def CHANGECOMPPOSfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        XPOSvar=cmds.textField(COMPXLOCtxtfld,q=True,tx=True)
        YPOSvar=cmds.textField(COMPYLOCtxtfld,q=True,tx=True)

        if XPOSvar=='' or YPOSvar=='':
            cmds.confirmDialog(icn='warning',\
                               title='Error',\
                               message='X position or Y position can not be empty!',\
                               button=['Ok'])
            cmds.error('error : X or Y position is empty')

        if XPOSvar.isdigit()==False or YPOSvar.isdigit()==False:
            cmds.confirmDialog(icn='warning',\
                               title='Error',\
                               message='X position or Y position is not number',\
                               button=['Ok'])
            cmds.error('error : X or Y position is not number')

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][2]=XPOSvar
                COMPONENTSlis[cnt][3]=YPOSvar
            cnt+=1

        #Build synoptic again
        cmds.formLayout('currentSynopticFL',e=True,attachForm=[(str(FILElis[0]),'top',int(YPOSvar)),(str(FILElis[0]),'left',int(XPOSvar))])

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=SELvar)
        return

    def CHANGECOMPNCAPTIONfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        NEWNAMEvar=str(cmds.textField(COMPCAPTIONtxtfld,q=True,tx=True))

        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][1]=NEWNAMEvar
            cnt+=1

        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
        for chk in COMPONENTSlis:
            cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

        #Build synoptic again
        cmds.button(str(FILElis[0]),e=True,l=str(NEWNAMEvar))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================
        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=SELvar)
        return

    def CHANGECOMPNAMEfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        NEWNAMEvar=str(cmds.textField(COMPNAMEtxtfld,q=True,tx=True))

        for chk in COMPONENTSlis:
            if chk[0]==NEWNAMEvar:
                cmds.confirmDialog(icn='warning',\
                                   title='Error',\
                                   message='There is another component with the nema '+NEWNAMEvar+'.',\
                                   button=['Ok'])
                cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
                for chk in COMPONENTSlis:
                    cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

                cmds.textField(COMPNAMEtxtfld,e=True,tx='')
                cmds.textField(COMPCAPTIONtxtfld,e=True,tx='')
                cmds.textField(COMPXLOCtxtfld,e=True,tx='')
                cmds.textField(COMPYLOCtxtfld,e=True,tx='')
                cmds.textField(COMPXSIZEtxtfld,e=True,tx='')
                cmds.textField(COMPYSIZEtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORRtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORGtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORBtxtfld,e=True,tx='')

                cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(0.0))
                cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(0.0))
                cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(0.0))
                cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)
                cmds.error('error : identical component name')

        cnt=0
        for chk in COMPONENTSlis:
            if chk==FILElis:
                COMPONENTSlis[cnt][0]=NEWNAMEvar
            cnt+=1

        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
        for chk in COMPONENTSlis:
            cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

        #Re-select
        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,si=NEWNAMEvar)

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        #Build synoptic again
        self.BUILDSYNOPTICWINfn()
        return

    def DELETECOMPONENTfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld,NAMESPACEtxtfld

        #Selection check==============================================================
        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No component selected from library.',\
                               button=['Ok'])
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Selection check==============================================================

        REPvar=cmds.confirmDialog(icn='question',\
                                  t='Delete Component',\
                                  m='Are you sure you want to delete '+FILElis[0]+'?',\
                                  button=['Yes','No'])
        if REPvar=='No':
            cmds.error('error : cancelled by user')

        COMPONENTSlis.remove(FILElis)

        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
        for chk in COMPONENTSlis:
            cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

        cmds.textField(COMPNAMEtxtfld,e=True,tx='')
        cmds.textField(COMPCAPTIONtxtfld,e=True,tx='')
        cmds.textField(COMPXLOCtxtfld,e=True,tx='')
        cmds.textField(COMPYLOCtxtfld,e=True,tx='')
        cmds.textField(COMPXSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPYSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORRtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORGtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORBtxtfld,e=True,tx='')

        cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(0.0))

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)
        cmds.deleteUI(FILElis[0],control=True)
        return

    def POPULATECONTROLfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, SELECTIONLISTtxtscr

        SELvar=cmds.textScrollList(COMPONENTLIBtxtscr,q=True,si=True)
        if SELvar==[]:
            cmds.error('error : no component selected')
        SELvar=SELvar[0]

        for chk in COMPONENTSlis:
            if chk[0]==SELvar:
                FILElis=chk

        if FILElis==[]:
            cmds.error('error : unable to find matched selection in memory')
        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
        cmds.textField(COMPNAMEtxtfld,e=True,tx=FILElis[0])
        cmds.textField(COMPCAPTIONtxtfld,e=True,tx=FILElis[1])
        cmds.textField(COMPXLOCtxtfld,e=True,tx=FILElis[2])
        cmds.textField(COMPYLOCtxtfld,e=True,tx=FILElis[3])
        cmds.textField(COMPXSIZEtxtfld,e=True,tx=FILElis[4])
        cmds.textField(COMPYSIZEtxtfld,e=True,tx=FILElis[5])
        cmds.textField(COMPCOLORRtxtfld,e=True,tx=FILElis[6][0])
        cmds.textField(COMPCOLORGtxtfld,e=True,tx=FILElis[6][1])
        cmds.textField(COMPCOLORBtxtfld,e=True,tx=FILElis[6][2])

        cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(FILElis[6][0]))
        cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(FILElis[6][1]))
        cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(FILElis[6][2]))

        cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)
        for chk in FILElis[7]:
            cmds.textScrollList(SELECTIONLISTtxtscr,e=True,a=chk)

        #CONTINUE WRITING CODE FOR POPULATING COMPONENT CONTROL BASED ON COMPONENT LIBRARY
        return

    def ADDCOMPONENTfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr

        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]

        REPvar=cmds.promptDialog(t='Add Component', m='Please enter component name',button=['Ok','Cancel'])
        if REPvar=='Cancel':
            cmds.error('error : cancelled by user')

        NAMEvar=cmds.promptDialog(q=True,text=True)
        if NAMEvar=='':
            cmds.confirmDialog(icn='warning',t='Empty String',message='Component name can not be empty.', button=['Ok'])
            cmds.error('error : component name can not be empty')
        CAPTIONvar=NAMEvar
        XLOCvar=0
        YLOCvar=0
        XSIZEvar=20
        YSIZEvar=20
        COLORlis=[0.7,0.7,0.7]
        SELECTIONlis=[]

        for chk in COMPONENTSlis:
            if chk[0]==NAMEvar:
                cmds.confirmDialog(icn='warning',t='Duplicate',message='Component name already exist.', button=['Ok'])
                cmds.error('error : component name exist')

        TEMPlis=[]
        TEMPlis.append(NAMEvar)
        TEMPlis.append(CAPTIONvar)
        TEMPlis.append(XLOCvar)
        TEMPlis.append(YLOCvar)
        TEMPlis.append(XSIZEvar)
        TEMPlis.append(YSIZEvar)
        TEMPlis.append(COLORlis)
        TEMPlis.append(SELECTIONlis)

        COMPONENTSlis.append(TEMPlis)

        cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
        for chk in COMPONENTSlis:
            cmds.textScrollList(COMPONENTLIBtxtscr,e=True,a=chk[0])

        cmds.textField(COMPNAMEtxtfld,e=True,tx='')
        cmds.textField(COMPCAPTIONtxtfld,e=True,tx='')
        cmds.textField(COMPXLOCtxtfld,e=True,tx='')
        cmds.textField(COMPYLOCtxtfld,e=True,tx='')
        cmds.textField(COMPXSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPYSIZEtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORRtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORGtxtfld,e=True,tx='')
        cmds.textField(COMPCOLORBtxtfld,e=True,tx='')

        cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(0.0))
        cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(0.0))

        cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================
        #Build synoptic again
        cmds.button(str(TEMPlis[0]),l=str(TEMPlis[1]),w=int(TEMPlis[4]),h=int(TEMPlis[5]),bgc=TEMPlis[6],en=False)
        return

    def CLOSECURRENTSYNfn(self,*args):
        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')
        else:
            REPvar=cmds.confirmDialog(icn='question',t='Close',message='Close current synoptic?', button=['Yes','No'])
            if REPvar=='Yes':
                reload (synopticGenerator)
            else:
                cmds.error('error : cancelled by user')
        return

    def EXITfn(self,*args):
        if cmds.window('currentSynoptic',exists=True):
            TITLEvar=cmds.window('currentSynoptic',q=True,t=True)
            if TITLEvar.endswith('*')==True:
                REPvar=cmds.confirmDialog(icn='question',\
                                   t='Save Synoptic',\
                                   message='There is an unsaved synoptic. Would you like to save it?',\
                                   button=['Yes','No'])
                if REPvar=='Yes':
                    self.SAVEINSTRUCTIONfn()
            cmds.deleteUI('currentSynoptic',wnd=True)

        cmds.deleteUI('synopticGenerator',wnd=True)
        return

    def CHANGESYNWINSIZEfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis



        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================

        cmds.layoutDialog(title='Change Size',ui=self.SETSYNWINfn)
        return

    def CHANGESYNWINCOLORfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis



        if cmds.window('currentSynoptic',exists=True)==False:
            cmds.confirmDialog(icn='warning',\
                               t='Warning',\
                               message='There is no active synoptic in the workspace.',\
                               button=['Ok'])
            cmds.error('error : no active synoptic in the workspace')

        #UNSAVED MARKER============================================================
        if SYNOPTICNAMEvar.endswith('*')==False:
            SYNOPTICNAMEvar=SYNOPTICNAMEvar+'*'
        #UNSAVED MARKER============================================================
        cmds.layoutDialog(title='Change Color',ui=self.SETSYNCOLORfn)
        return

    #SYNOPTIC BUILDING==================================================================================================
    #===================================================================================================================
    def BUILDSYNOPTICWINfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        if cmds.window('currentSynoptic',exists=True):
            cmds.deleteUI('currentSynoptic',wnd=True)

        #Build window
        cmds.window('currentSynoptic',\
                    t=SYNOPTICNAMEvar,\
                    mw=False,\
                    mnb=False,\
                    mxb=False,\
                    w=SYNOPTICSIZEXvar,\
                    h=SYNOPTICSIZEYvar,\
                    s=False,\
                    tbm=False)
        #cmas=cmds.columnLayout(adj=True)

        #Build component
        form=cmds.formLayout('currentSynopticFL')
        cmds.text(l='',w=SYNOPTICSIZEXvar,h=SYNOPTICSIZEYvar,bgc=SYNOPTICCOLORvar)
        for chk in COMPONENTSlis:
            #Parse component
            #Component data listing [<name>,<caption>,<xloc>,<yloc>,<xsize>,<ysize>,<color list>,<selection list>]
            cmds.button(str(chk[0]),l=str(chk[1]),w=int(chk[4]),h=int(chk[5]),bgc=chk[6],\
                        c=lambda*args:self.COMPSELECTACTIONfn(str(chk[0])),en=False)

            cmds.formLayout(form,e=True,attachForm=[(str(chk[0]),'top',int(chk[3])),(str(chk[0]),'left',int(chk[2]))])
        #Build component

        cmds.showWindow()
        #Build window
        return
    #===================================================================================================================
    #SYNOPTIC BUILDING==================================================================================================

    def SETSYNWINPROCfn(self,XVALvar, YVALvar):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        if XVALvar.isdigit()==True and YVALvar.isdigit()==True:
            SYNOPTICSIZEXvar=int(XVALvar)
            SYNOPTICSIZEYvar=int(YVALvar)
            SYNOPTICNAMEvar='Untitled Synoptic*'
            self.BUILDSYNOPTICWINfn()
            cmds.layoutDialog(dismiss='CONTINUE')
        else:
            SYNOPTICSIZEXvar=''
            SYNOPTICSIZEYvar=''
            cmds.confirmDialog(icn='warning',\
                               t='Invalid Data',\
                               m='Invalid size data entered.',\
                               button=['Ok'])
            cmds.layoutDialog(dismiss='CONTINUE')
            cmds.error('error : invalid size value')

        return

    def NEWSYNfn(self,*args):
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        if cmds.window('currentSynoptic',exists=True):
            REPvar=cmds.confirmDialog(icn='warning',\
                                      title='Current Synoptic Open',\
                                      message='There is a synoptic still open in the workspace.',\
                                      button=['Clear Synoptic','Cancel'])
            if REPvar=='Clear Synoptic':
                cmds.deleteUI('currentSynoptic',wnd=True)
                SYNOPTICSIZEXvar=''
                SYNOPTICSIZEYvar=''
                SYNOPTICNAMEvar=''
                SYNOPTICCOLORvar=[0.5,0.5,0.5]
                COMPONENTSlis=[]

                cmds.textScrollList(COMPONENTLIBtxtscr,e=True,ra=True)
                cmds.textField(COMPNAMEtxtfld,e=True,tx='')
                cmds.textField(COMPCAPTIONtxtfld,e=True,tx='')
                cmds.textField(COMPXLOCtxtfld,e=True,tx='')
                cmds.textField(COMPYLOCtxtfld,e=True,tx='')
                cmds.textField(COMPXSIZEtxtfld,e=True,tx='')
                cmds.textField(COMPYSIZEtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORRtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORGtxtfld,e=True,tx='')
                cmds.textField(COMPCOLORBtxtfld,e=True,tx='')

                cmds.floatSlider(COMPCOLORRfltsld,e=True,v=float(0.0))
                cmds.floatSlider(COMPCOLORGfltsld,e=True,v=float(0.0))
                cmds.floatSlider(COMPCOLORBfltsld,e=True,v=float(0.0))

                cmds.textScrollList(SELECTIONLISTtxtscr,e=True,ra=True)
            else:
                cmds.error('error : cancelled by user')
        REPvar=cmds.layoutDialog(title='New Synoptic',ui=self.SETSYNWINfn)
        return

    def SETSYNWINfn(self,*args):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        global COMPONENTLIBtxtscr,COMPNAMEtxtfld,COMPCAPTIONtxtfld,COMPXLOCtxtfld,COMPYLOCtxtfld,COMPINCREMENTtxtfld,\
        COMPXSIZEtxtfld,COMPYSIZEtxtfld,COMPCOLORRfltsld,COMPCOLORGfltsld,COMPCOLORBfltsld,COMPCOLORRtxtfld,\
        COMPCOLORGtxtfld,COMPCOLORBtxtfld, NAMESPACEtxtfld

        c1=cmds.columnLayout(adj=True,w=200)
        cmds.text(l='')
        cmds.text(l='  Set synoptic window size.',w=200,al='left')
        cmds.text(l='')
        cmds.rowColumnLayout(nc=4, columnWidth=[(1, 20),(2,75),(3,20),(4,75)])
        cmds.text(l='X: ',fn='boldLabelFont')

        if cmds.window('currentSynoptic',exists=True):
            XVALvar=cmds.textField(tx=str(SYNOPTICSIZEXvar))
        else:
            XVALvar=cmds.textField(tx='200')
        cmds.text(l='Y: ',fn='boldLabelFont')

        if cmds.window('currentSynoptic',exists=True):
            YVALvar=cmds.textField(tx=str(SYNOPTICSIZEYvar))
        else:
            YVALvar=cmds.textField(tx='400')

        cmds.text(l='',p=c1)
        cmds.separator(p=c1)
        cmds.button(l='CONTINUE',p=c1,h=30,bgc=[1.0,0.643835616566,0.0],\
                    c=lambda*args:self.SETSYNWINPROCfn(cmds.textField(XVALvar,q=True,tx=True),cmds.textField(YVALvar,q=True,tx=True)))
        return

    def SETSYNCOLORPROCfn(self,Rvar,Gvar,Bvar):
        global SYNOPTICSIZEXvar, SYNOPTICSIZEYvar, SYNOPTICNAMEvar, SYNOPTICCOLORvar, COMPONENTSlis
        COLORlis=[]
        COLORlis.append(Rvar)
        COLORlis.append(Gvar)
        COLORlis.append(Bvar)
        SYNOPTICCOLORvar= COLORlis
        cmds.layoutDialog(dismiss='CONTINUE')
        self.BUILDSYNOPTICWINfn()
        return

    def SETSYNCOLORUPDATEfn(self,Rvar,Gvar,Bvar):
        global TESTCOLORSYNtxt
        COLORlis=[]
        COLORlis.append(Rvar)
        COLORlis.append(Gvar)
        COLORlis.append(Bvar)
        cmds.text(TESTCOLORSYNtxt,e=True,bgc=COLORlis)
        return

    def SETSYNCOLORfn(self,*args):
        global TESTCOLORSYNtxt
        c1=cmds.columnLayout(adj=True,w=200)
        cmds.text(l='')
        cmds.text(l='  Set synoptic window background color.',w=200,al='left')
        cmds.text(l='')
        cmds.rowColumnLayout(nc=2, columnWidth=[(1, 20),(2,178)],p=c1)

        cmds.text(l='R: ',fn='boldLabelFont')
        Rfs=cmds.floatSlider(min=0.0,max=1.0,dc=lambda*args:self.SETSYNCOLORUPDATEfn(cmds.floatSlider(Rfs,q=True,v=True),\
                                                          cmds.floatSlider(Gfs,q=True,v=True),\
                                                          cmds.floatSlider(Bfs,q=True,v=True)))
        cmds.text(l='G: ',fn='boldLabelFont')
        Gfs=cmds.floatSlider(min=0.0,max=1.0,dc=lambda*args:self.SETSYNCOLORUPDATEfn(cmds.floatSlider(Rfs,q=True,v=True),\
                                                          cmds.floatSlider(Gfs,q=True,v=True),\
                                                          cmds.floatSlider(Bfs,q=True,v=True)))
        cmds.text(l='B: ',fn='boldLabelFont')
        Bfs=cmds.floatSlider(min=0.0,max=1.0,dc=lambda*args:self.SETSYNCOLORUPDATEfn(cmds.floatSlider(Rfs,q=True,v=True),\
                                                          cmds.floatSlider(Gfs,q=True,v=True),\
                                                          cmds.floatSlider(Bfs,q=True,v=True)))

        cmds.separator(p=c1)
        TESTCOLORSYNtxt=cmds.text(l='', h=20,p=c1)
        cmds.separator(p=c1)
        cmds.button(l='CONTINUE',p=c1,h=30,bgc=[1.0,0.643835616566,0.0],\
                    c=lambda*args: self.SETSYNCOLORPROCfn(cmds.floatSlider(Rfs,q=True,v=True),\
                                                          cmds.floatSlider(Gfs,q=True,v=True),\
                                                          cmds.floatSlider(Bfs,q=True,v=True)))
        return
synopticGeneratorCLS()

#DETERMINE THE PROBLEM WITH PASSING VALUE FROM LAYOUT DIALOG