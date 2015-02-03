__author__ = 'andrew.willis'

#SYNOPTIC LAUNCHER

import maya.cmds as cmds
import os, imp
try:
    import MNCA_projectid
    PROJECTvar= MNCA_projectid.PROJECTIDcls().id()
except:
    PROJECTvar=''
    pass

#License Parsing
import licenseParsing
licenseParsing.licParse()

class synopticLauncherLocalCLS:
    def __init__(self):
        global SCRIPTlis, PROJECTtxt
        if cmds.window('synopticLauncherLocal',exists=True):
            cmds.deleteUI('synopticLauncherLocal',wnd=True)

        win = cmds.window(t='Local Synoptic Launcher',s=False,w=150)
        cmds.renameUI(win, 'synopticLauncherLocal')
        cmas=cmds.columnLayout(adj=True,w=150)

        SCRIPTlis=cmds.textScrollList(w=150,h=200,dcc=self.RUNSYNfn)
        cmds.popupMenu(p=SCRIPTlis)
        cmds.menuItem(l='Run Synoptic',c=self.RUNSYNfn)
        cmds.menuItem(l='Delete Synoptic',c=self.DELETEfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Refresh',c=self.REFRESHfn)

        cmds.separator()

        cmds.showWindow()

        self.REFRESHfn()
        return

    def DELETEfn(self,*args):
        global SCRIPTlis, PROJECTtxt
        REPvar=cmds.confirmDialog(icn='question',\
                               t='Delete',\
                               m='Are you sure you want to delete this synoptic?',\
                               button=['Yes','No'])
        if REPvar=='No':
            cmds.error('error : cancelled by user')

        SELvar=cmds.textScrollList(SCRIPTlis,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No item selected from list.',\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        else:
            SELvar=SELvar[0]
        os.remove('D:/synopticLocalLibrary/'+SELvar+'.pyc')
        self.REFRESHfn()
        return

    def RUNSYNfn(self,*args):
        global SCRIPTlis, PROJECTtxt

        SELvar=cmds.textScrollList(SCRIPTlis,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No item selected from list.',\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        else:
            SELvar=SELvar[0]
        try:
            imp.load_compiled(SELvar,'D:/synopticLocalLibrary/'+SELvar+'.pyc')
        except Exception as e:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='Error running synoptic script\n'+str(e),\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        return

    def REFRESHfn(self,*args):
        global SCRIPTlis, PROJECTtxt

        if os.path.isdir('D:/synopticLocalLibrary')==False:
            os.makedirs('D:/synopticLocalLibrary')

        SYNlis=os.listdir('D:/synopticLocalLibrary')

        cmds.textScrollList(SCRIPTlis,e=True,ra=True)

        for chk in SYNlis:
            cmds.textScrollList(SCRIPTlis,e=True,a=chk.replace('.pyc',''))
        return


synopticLauncherLocalCLS()