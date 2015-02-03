#MNCA Node search

import maya.cmds as cmds

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()

if cmds.window('MNCA_nodesearch', exists=True):cmds.deleteUI('MNCA_nodesearch', wnd=True)

class NODESEARCHcls:
    def __init__(self):
        global RESTtxtscr, TEXTvar
        win = cmds.window(t='Node Search',s=False)
        cmds.renameUI(win, 'MNCA_nodesearch')
        cmas=cmds.columnLayout(adj=True)          
        
        f1=cmds.frameLayout(l='Search Keyword',p=cmas,w=250)
        cmds.columnLayout(adj=True)
        TEXTvar=cmds.textField(cc=self.SEARCHfn)
        
        f2=cmds.frameLayout(l='Search Result', p=cmas)
        cmds.columnLayout(adj=True)
        RESTtxtscr=cmds.textScrollList(h=200,ams=True,dcc=self.SELECTfn)
        
        cmds.showWindow()
        return
    
    def SELECTfn(self,*args):
        global RESTtxtscr, TEXTvar
        TEMPlis=cmds.textScrollList(RESTtxtscr,q=True,si=True)
        cmds.select(TEMPlis)
        return
    
    def SEARCHfn(self,*args):
        global RESTtxtscr, TEXTvar
        if str(cmds.textField(TEXTvar,q=True,tx=True))<>'':
            TEMPlis=[]
            for chk in cmds.ls():
                if chk.find(str(cmds.textField(TEXTvar,q=True,tx=True)))<>-1:
                    TEMPlis.append(chk)
            
            cmds.textScrollList(RESTtxtscr,e=True,ra=True)
            for chk in TEMPlis:
                cmds.textScrollList(RESTtxtscr,e=True,a=chk)
            
            if TEMPlis==[]:
                cmds.confirmDialog(icn='information',title='No Node Find', message='There is no node matching the keyword!')
        else:
            cmds.textScrollList(RESTtxtscr,e=True,ra=True)
        return

NODESEARCHcls()