#NULL GENERATOR [ANIM SERVICE]
#Andrew Willis [MNCA]

import maya.cmds as cmds

#license Parsing
import licenseParsing
licenseParsing.licParse()


class NULGENcls:
    def __init__(self):
        global ALIGROTtchkbx
        if cmds.window('mncToolsAnimNullGenerator', exists=True):cmds.deleteUI('mncToolsAnimNullGenerator', wnd=True)

        win = cmds.window(t='Null Generator',s=False,w=200)
        cmds.renameUI(win, 'mncToolsAnimNullGenerator')
        cmas=cmds.columnLayout(adj=True)    
        ALIGROTtchkbx=cmds.checkBox(l='Align Rotation',v=True,w=160)  
        cmds.separator()
        cmds.button(l='ATTACH NULL',c=self.NULLGENfn,h=20,bgc=[1.0,0.643835616566,0.0])
        cmds.showWindow()
        return
    
    def NULLGENfn(self,*args):
        global ALIGROTtchkbx
        OBJSELvar = cmds.ls(sl=True)
        if OBJSELvar == []:
            cmds.confirmDialog(icon='warning',t='Error',m='No object selected!',button=['Ok'])
            cmds.error('NO OBJECT SELECTED')
        elif len(OBJSELvar) > 1:
            cmds.confirmDialog(icon='warning',t='Error',m='More than one object selected!',button=['Ok'])
            cmds.error('MORE THAN ONE OBJECT SELECTED')
        
        TARGETTRANSvar = cmds.xform(OBJSELvar[0],q=True,piv=True,ws=True)
        TARGETROTATvar = cmds.xform(OBJSELvar[0],q=True,ro=True,ws=True)
        
        CURVEvar = cmds.curve(d=True,p=[(1,-1,1),(1,-1,-1),(-1,-1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1),(1,1,1), (1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1),(-1,1,1),(-1,-1,1)])
        
        cmds.move(TARGETTRANSvar[0], TARGETTRANSvar[1], TARGETTRANSvar[2], CURVEvar)
        
        if cmds.checkBox(ALIGROTtchkbx, q=True, v=True): cmds.rotate(TARGETROTATvar[0], TARGETROTATvar[1], TARGETROTATvar[2], CURVEvar)
        return

NULGENcls()