#CONTROLLER LIBRARY

import maya.cmds as cmds
import os
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import getpass, datetime, socket

#License Parsing
import licenseParsing
licenseParsing.licParse()

#Determining root path
rootPathVar = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

CACHEsrvr='X:/TECH/controllerlib/'

class CONTROLLERLIBcls:
    def __init__(self):
        global NEWNAMEtxtfld, CONTROLLERtxtscr, CACHEsrvr,IMAGEimg, SCRSHTPANELvar, SCRSHTPANEL2var
        if cmds.window('mncRigLibrary', exists=True):cmds.deleteUI('mncRigLibrary', wnd=True)
        cmds.window('mncRigLibrary',t='Controller Library',s=False)
        cmas=cmds.columnLayout(adj=True)
        tabs=cmds.tabLayout()
        
        child1=cmds.columnLayout(adj=True)
        f1=cmds.frameLayout(l='Export Controller',p=child1,w=300)
        cmds.columnLayout(adj=True)   
        cmds.text(l='Controller New Name: ')
        NEWNAMEtxtfld=cmds.textField()
        cmds.separator()
        cmds.text(l='Screen Shot Frame:')
        cmds.paneLayout(w=300,h=300)
        SCRSHTPANELvar=cmds.modelPanel(cam='persp',mbv=False)
        cmds.columnLayout(adj=True,p=child1)
        cmds.separator()
        cmds.text(l='')
        cmds.separator()
        cmds.button(l='REGISTER CONTROLLER' ,h=40, bgc=[1.0,0.643835616566,0.0],c=self.REGISTERfn)
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        child2=cmds.columnLayout(adj=True)
        f2=cmds.frameLayout(l='Import Update Controller',p=child2)
        cmds.columnLayout(adj=True)
        cmds.text(l='Select Controller: ')
        cmds.button(l='<<CONTROLLER PREVIEW>>',h=20, bgc=[1.0,0.643835616566,0.0],c=self.PREVIEWfn)
        CONTROLLERtxtscr=cmds.textScrollList(h=100)
        cmds.button(l='IMPORT CONTROLLER' , bgc=[1.0,0.643835616566,0.0],c=self.IMPORTCONTROLLERfn)
        cmds.separator()
        cmds.text(l='Screen Shot Frame: ')        
        cmds.paneLayout(w=300,h=300)
        SCRSHTPANEL2var=cmds.modelPanel(cam='persp',mbv=False)   
        cmds.button(l='UPDATE CONTROLLER' , bgc=[1.0,0.643835616566,0.0],c=self.UPDATECONTROLLERfn)
        
        cmds.separator(p=cmas)
        cmds.button(l='REFRESH',c=self.REFRESHfn,p=cmas)
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'REGISTER CONTROLLER'), (child2, 'IMPORT CONTROLLER')) )
        cmds.showWindow()
        
        CTRLlis=os.listdir(CACHEsrvr+'library/')
        for chk in CTRLlis:
            if chk.endswith('.png')==False:
                cmds.textScrollList(CONTROLLERtxtscr,e=True,append=chk[:-3])
        return
    
    def REFRESHfn(self,*args):
        import MNCA_rigcontroller
        reload(MNCA_rigcontroller)
        return
    
    def PREVIEWfn(self,*args):
        global CACHEsrvr
        IMGvar=cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)
        if IMGvar==None:
            cmds.confirmDialog(icon='warning',title='Message',message='No controller selected!', button=['Ok'])
        
        if cmds.window('SCR', exists=True):
            cmds.deleteUI('SCR', wnd=True)   
        
        if os.path.isfile(CACHEsrvr+'library/ctrlimg_'+IMGvar[0][8:]+'.png')==False:
            cmds.confirmDialog(icon='warning',title='Message',message='Image file is not available!', button=['Ok'])
            cmds.error('IMAGE FILE IS NOT AVAILABLE')
            
        cmds.window('SCR',s=False)
        cmds.columnLayout(adj=True)
        cmds.image(image=CACHEsrvr+'library/ctrlimg_'+IMGvar[0][8:]+'.png')
        cmds.showWindow()
        return
    
    def REGISTERfn(self,*args):
        global NEWNAMEtxtfld, CONTROLLERtxtscr, CACHEsrvr, IMAGEimg, SCRSHTPANELvar, SCRSHTPANEL2var
        if cmds.textField(NEWNAMEtxtfld,q=True,tx=True)=='':
            cmds.confirmDialog(icon='warning',title='Message',message='Controller new name is empty!', button=['Ok'])
            cmds.error('TEXTFIELD EMPTY')
        else:
            if os.path.isfile(CACHEsrvr+'/library/'+'ctrllib_'+cmds.textField(NEWNAMEtxtfld,q=True,tx=True)+'.ma')==True:
                REPLYvar=cmds.confirmDialog(icon='question', title='Message',message='Identical name found. Overwrite?', button=['Yes','No'])
                if REPLYvar=='Yes':
                    cmds.select(cl=True)
                    cmds.setFocus(SCRSHTPANELvar)
                    MODELPANELvar=apiUI.M3dView.active3dView()
                    IMAGEvar=api.MImage()
                    MODELPANELvar.readColorBuffer(IMAGEvar, True)
                    IMAGEvar.writeToFile(CACHEsrvr+'/library/'+'ctrlimg_'+cmds.textField(NEWNAMEtxtfld,q=True,tx=True)+'.png','png')
                    
                    cmds.file(rename=CACHEsrvr+'/library/'+'ctrllib_'+cmds.textField(NEWNAMEtxtfld,q=True,tx=True)+'.ma')
                    cmds.file( save=True, type='mayaAscii' )
                else:
                    cmds.error('CANCELLED BY USER')
            else:      
                cmds.select(cl=True)
                cmds.setFocus(SCRSHTPANELvar)
                MODELPANELvar=apiUI.M3dView.active3dView()
                IMAGEvar=api.MImage()
                MODELPANELvar.readColorBuffer(IMAGEvar, True)
                IMAGEvar.writeToFile(CACHEsrvr+'/library/'+'ctrlimg_'+cmds.textField(NEWNAMEtxtfld,q=True,tx=True)+'.png','png')                
                
                cmds.file(rename=CACHEsrvr+'/library/'+'ctrllib_'+cmds.textField(NEWNAMEtxtfld,q=True,tx=True)+'.ma')
                cmds.file( save=True, type='mayaAscii' )      
                          
        cmds.textField(NEWNAMEtxtfld,e=True,tx='')
        
        cmds.file(new=True,f=True)
        import MNCA_rigcontroller
        reload(MNCA_rigcontroller)
        return
    
    def IMPORTCONTROLLERfn(self,*args):
        global NEWNAMEtxtfld, CONTROLLERtxtscr, CACHEsrvr, IMAGEimg
        if cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)==None:
            cmds.confirmDialog(icon='warning',title='Message',message='Controller not selected', button=['Ok'])
            cmds.error('NO CONTROLLER SELECTED')
        cmds.file(CACHEsrvr+'library/'+cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)[0]+'.ma',i=True)
        return
    
    def UPDATECONTROLLERfn(self,*args):
        global NEWNAMEtxtfld, CONTROLLERtxtscr, CACHEsrvr, IMAGEimg, SCRSHTPANEL2var
        if cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)==None:
            cmds.confirmDialog(icon='warning',title='Message',message='Controller not selected', button=['Ok'])
            cmds.error('NO CONTROLLER SELECTED')  
            
        REPLYvar=cmds.confirmDialog(icon='question', title='Message',message='This will overwrite the selected file. Proceed?', button=['Yes','No'])    
        if REPLYvar=='Yes':
            cmds.select(cl=True)
            cmds.setFocus(SCRSHTPANEL2var)
            MODELPANELvar=apiUI.M3dView.active3dView()
            IMAGEvar=api.MImage()
            MODELPANELvar.readColorBuffer(IMAGEvar, True)            
            IMAGEvar.writeToFile(CACHEsrvr+'/library/'+'ctrlimg_'+cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)[0][8:]+'.png','png')
            
            cmds.file(rename=CACHEsrvr+'library/'+cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)[0]+'.ma')
            cmds.file( save=True, type='mayaAscii' )  
            
            if os.path.isdir('C:/workspace/library/')==False:
                os.mkdir('C:/workspace/library/')
            TIMEvar=cmds.date(f='YYYYYYMMDDhhmmss')  
            cmds.file(rename='C:/workspace/library/'+cmds.textScrollList(CONTROLLERtxtscr,q=True,si=True)[0]+'_'+TIMEvar+'.ma')
            cmds.file( save=True, type='mayaAscii' )  
        else:
            cmds.error('CANCELLED BY USER')
        return

#WRITING LOG
USERNAMEvar=getpass.getuser()
COMPNAMEvar=socket.gethostname()
DATE=datetime.datetime.now()
TARGETvar='MNCA_rigcontroller'
LOGvar=str(DATE.hour)+':'+str(DATE.minute)+':'+str(DATE.second)+'\t'+'START'+'\t'+USERNAMEvar+'\t'+COMPNAMEvar+'\t'+TARGETvar+'\r\n'
if os.path.isfile('X:/TECH/log/MNCA/'+str(DATE.year)+'.'+str(DATE.month)+'.'+str(DATE.day)+'.txt')==False:
    OPENLOGvar=open('X:/TECH/log/MNCA/'+str(DATE.year)+'.'+str(DATE.month)+'.'+str(DATE.day)+'.txt','w')
    OPENLOGvar.write(LOGvar)
    OPENLOGvar.close()
else:
    OPENLOGvar=open('X:/TECH/log/MNCA/'+str(DATE.year)+'.'+str(DATE.month)+'.'+str(DATE.day)+'.txt','r')
    CONTAINERlis=OPENLOGvar.read()
    OPENLOGvar.close()
    OPENLOGvar=open('X:/TECH/log/MNCA/'+str(DATE.year)+'.'+str(DATE.month)+'.'+str(DATE.day)+'.txt','w')
    OPENLOGvar.write(CONTAINERlis+LOGvar)
    OPENLOGvar.close()  

CONTROLLERLIBcls()