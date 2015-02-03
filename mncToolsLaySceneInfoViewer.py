#MNCA SCENE INFO VIEWER
#Andrew Willis 2013 [MNCA]

import maya.cmds as cmds
import os
import shutil

#License Parsing
import licenseParsing
licenseParsing.licParse()

if cmds.window('mncToolsLaySceneInfoViewer', exists=True):cmds.deleteUI('mncToolsLaySceneInfoViewer', wnd=True)

#Check Existance
if not cmds.objExists('shotMaster'):
    cmds.confirmDialog( icon='warning',title='Message', message='No shot_master within the maya scene!', button=['Ok'] ,defaultButton='Ok' )
    cmds.error('NO SHOT MASTER WITHIN THE MAYA SCENE!')
    
SHOTDURATIONlis=[]
SHOTNAMElis=[]
#Preliminary Scene Data
PRJSRSvar = cmds.getAttr('sceneInfo.projName',asString=True)
PRJCDEvar = cmds.getAttr('sceneInfo.projCode',asString=True)
PRJEPSvar = cmds.getAttr('sceneInfo.episodeName',asString=True)
PRJSEQvar = cmds.getAttr('sceneInfo.sequenceName',asString=True)
SHOTLISTATTRvar = cmds.listAttr('sceneInfo')
for chk in SHOTLISTATTRvar:
    if chk.find('SH') >= 0:
        TEMPvar=cmds.getAttr('sceneInfo.'+chk,asString=True)
        SHOTNAMElis.append(chk)
        SHOTDURATIONlis.append(TEMPvar)    

class SCENEINFOVIEWER:
    def __init__(self):
        win = cmds.window(t='Scene Information',s=False,w=200,h=300)
        cmds.renameUI(win, 'mncToolsLaySceneInfoViewer')
        cmas=cmds.columnLayout(adj=True)
        f1=cmds.frameLayout(l='Sequence Credential',w=200)
        fc1=cmds.columnLayout(adj=True,p=f1)
        cmds.rowColumnLayout(nc=2,columnWidth=[(1, 80), (2, 120)],p=fc1)
        cmds.text(l='Series: ')
        cmds.text(l=PRJSRSvar,fn= "boldLabelFont")
        cmds.text(l='Episode: ')
        cmds.text(l=PRJEPSvar,fn= "boldLabelFont")
        cmds.text(l='Sequence: ')
        cmds.text(l=PRJSEQvar,fn= "boldLabelFont")
        
        f2=cmds.frameLayout(l='Shot Listing',w=200,p=cmas)
        cmds.rowColumnLayout(nc=2,columnWidth=[(1, 80), (2, 120)],p=f2)
        cmds.text(l='Shot',fn='boldLabelFont')
        cmds.text(l='Duration',fn='boldLabelFont')
        fc2=cmds.scrollLayout(horizontalScrollBarThickness=10, p=f2, h=200)
        cmds.rowColumnLayout(nc=2,columnWidth=[(1, 80), (2, 100)],p=fc2)
        cmds.columnLayout(adj=True,p=fc2)
        cmds.separator()
        cmds.rowColumnLayout(nc=2,columnWidth=[(1, 80), (2, 100)],p=fc2)
        cmds.separator()
        cmds.separator()
        cnt=0
        LENSHOTLISvar=len(SHOTNAMElis)
        while cnt<LENSHOTLISvar:
            cmds.text(l=SHOTNAMElis[cnt])
            cmds.text(l=SHOTDURATIONlis[cnt])
            cmds.separator()
            cmds.separator()
            cnt+=1
        cmds.showWindow()        
        return

#DEVELOPMENT NOTE: continue with the conversion for scene info viewer

    def REFRESHfn(self,*args):
        import mncToolsLaySceneInfoViewer
        reload (mncToolsLaySceneInfoViewer)
        return

SCENEINFOVIEWER()