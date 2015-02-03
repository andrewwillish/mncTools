#FRAME COUNTER KILLER
#Andrew Willis 2013 [MNC]

import maya.cmds as cmds
import os, sys, getpass, datetime, socket

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()

if cmds.window('MNCAFramekiller',exists=True):
    cmds.deleteUI('MNCAFramekiller',wnd=True)

#Existance check
if cmds.objExists('shotMaster')==False:
    cmds.confirmDialog( icon='warning',title='Message', message='No shotMaster within the maya scene!', button=['Ok'] ,defaultButton='Ok' )
    cmds.error('NO SHOT MASTER WITHIN THE MAYA SCENE!')

try:
    PRJSRSvar=cmds.getAttr('sceneInfo.projName',asString=True)
    PRJCDEvar=cmds.getAttr('sceneInfo.projCode',asString=True)
    PRJEPSvar=cmds.getAttr('sceneInfo.episodeName',asString=True)
    PRJSEQvar=cmds.getAttr('sceneInfo.sequenceName',asString=True)
except:
    cmds.confirmDialog( icon='warning',title='Message', message='No shotMaster within the maya scene!', button=['Ok'] ,defaultButton='Ok' )
    cmds.error('error: no shot master within the scene')

class FRAMEMURDERERcls:
    def __init__(self):
        global CAMSEARCHvar,CAMtxtscr
        win = cmds.window(t='MNCA Frame Killer',s=False)
        cmds.renameUI(win, 'MNCAFramekiller')
        cmas=cmds.columnLayout(adj=True)
        f1=cmds.frameLayout(l='Camera Listing',w=200)
        CAMtxtscr=cmds.textScrollList()
        CAMSEARCHvar= cmds.ls('shotMaster',dag=True)
        cmds.textScrollList(CAMtxtscr,e=True,ra=True)
        for chk in CAMSEARCHvar:
            if chk.find('cam_master')>=0:
                cmds.textScrollList(CAMtxtscr,e=True,a=chk)
        cmds.columnLayout(adj=True,p=cmas)
        cmds.separator()
        cmds.button(l='KILL FRAME COUNT',bgc=[1.0,0.643835616566,0.0],c=self.KILLCAMCOUNTfn)
        cmds.button(l='ACTIVATE FRAME COUNT',bgc=[0.0,1.0,0.0],c=self.ACTIVATEFRAMECOUNTfn)
        cmds.button(l='REFRESH',c=self.REFRESHfn)
        cmds.showWindow()        
        return

    def KILLCAMCOUNTfn(self,*args):
        global CAMSEARCHvar,CAMtxtscr
        SELECTEDCAMvar=cmds.textScrollList(CAMtxtscr,q=True,si=True)
        if SELECTEDCAMvar==None:
            cmds.confirmDialog( icon='warning',title='Message', message='No camera from list selected!', button=['Ok'] ,defaultButton='Ok' )
            cmds.error('PROCEEDINGS ERROR: NO CAMERA FROM LIST SELECTED!') 
        SELECTEDCAMvar=SELECTEDCAMvar[0]
        IDNUMvar=SELECTEDCAMvar.replace('cam_master','')
        try:
            cmds.delete('cameraex'+IDNUMvar)
            cmds.delete('cameraex2'+IDNUMvar)
        except:
            cmds.confirmDialog( icon='warning',title='Message', message='Annotation object not found!', button=['Ok'] ,defaultButton='Ok' )
            cmds.error('PROCEEDINGS ERROR: ANNOTATION OBJECT NOT FOUND! ANCIENT CASE!')        
        cmds.confirmDialog( icon='information',title='Message', message='Camera frame count annotation deleted!', button=['Ok'] ,defaultButton='Ok' )
        return
    
    #Activate Frame Count Proceedings
    def ACTIVATEFRAMECOUNTfn(self,*args):
        global CAMSEARCHvar,CAMtxtscr
        SELECTEDCAMvar=cmds.textScrollList(CAMtxtscr,q=True,si=True)
        if SELECTEDCAMvar==None:
            cmds.confirmDialog( icon='warning',title='Message', message='No camera from list selected!', button=['Ok'] ,defaultButton='Ok' )
            cmds.error('PROCEEDINGS ERROR: NO CAMERA FROM LIST SELECTED!') 
        SELECTEDCAMvar=SELECTEDCAMvar[0]
        IDNUMvar=SELECTEDCAMvar.replace('cam_master','')
        cmds.expression(n='cameraex'+str(IDNUMvar),o='anFramecount'+str(IDNUMvar),s='float $f=frame; setAttr -type "string" "anFramecount'+str(IDNUMvar)+'.text" ("Frame: "+$f);')
        cmds.expression(n='cameraex2'+str(IDNUMvar),o='anShotInformation'+str(IDNUMvar),s='string $p=`getAttr sceneInfo.Key`; setAttr -type\
             "string" "anShotInformation.text" ("Scene: "+"'+PRJCDEvar+'_'+PRJEPSvar+'_'+PRJSEQvar+'_'+'SH_"+$p);')
        
        cmds.confirmDialog( icon='information',title='Message', message='Camera frame count activated!', button=['Ok'] ,defaultButton='Ok' )
        return
    
    #Refresh
    def REFRESHfn(self,*args):
        import MNCA_laytframekiller
        reload(MNCA_laytframekiller)
        return
    
    
#WRITING LOG
USERNAMEvar=getpass.getuser()
COMPNAMEvar=socket.gethostname()
DATE=datetime.datetime.now()
TARGETvar='MNCA_laytframekiller'
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
    
FRAMEMURDERERcls()
