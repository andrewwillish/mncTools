__author__ = 'andrew.willis'

#import module
import maya.cmds as cmds

class subdivManager:
    def __init__(self):
        if cmds.window('subdivManager', exists=True):cmds.deleteUI('subdivManager', wnd=True)

        win = cmds.window(t='Subdiv Approx Mgr', s=False, w=200)
        cmds.renameUI(win, 'subdivManager')

        cmds.columnLayout('cmas', adj=True)
        cmds.textScrollList('samListTextScroll', w=200, h=250)

        cmds.separator(p='cmas')
        cmds.button(l='REFRESH', bgc=[1.0,0.643835616566,0.0], p='cmas', c=self.populateSubdv)

        cmds.showWindow()

        #popper
        cmds.popupMenu(p='samListTextScroll')
        cmds.menuItem(l='New Subdiv Approx', c=self.addNewSubDiv)
        cmds.menuItem(l='Delete Subdiv Approx', c=self.deleteSubDv)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Add Selected Object', c=self.assignToSubdiv)
        cmds.menuItem(l='Remove Selected Object', c=self.removeFromSubdiv)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Assigned Object', c=self.selectSubdiv)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Subdiv Node', c=self.editSubdiv)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Rename Subdiv Node', c=self.rename)

        self.populateSubdv()
        return

    def editSubdiv(self, *args):
        subdivSel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        if subdivSel is not None:
            subdivSel = subdivSel[0]
            cmds.select(subdivSel)
        return

    def removeFromSubdiv(self, *args):
        subdivSel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        objSel = cmds.ls(sl=True)
        if subdivSel is not None:
            subdivSel = subdivSel[0]
            if objSel != []:
                for obj in objSel:
                    shapes = None
                    history = cmds.listHistory(obj)
                    for parse in history:
                        if cmds.objectType(parse) == 'mesh':shapes = parse
                    if shapes is not None:
                        try:
                            cmds.disconnectAttr(subdivSel+'.message', shapes+'.miSubdivApprox')
                        except Exception as e:
                            cmds.confirmDialog(icn='warning', t='Subdiv Approx Mgr', m=str(e), button=['OK'])
                            cmds.error(str(e))
        return

    def selectSubdiv(self, *args):
        subdivSel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        if subdivSel is not None:
            subdivSel = subdivSel[0]
            selItem = []
            if cmds.listConnections(subdivSel) is not None:
                for item in cmds.listConnections(subdivSel):
                    if not cmds.objectType(item) == 'mentalrayItemsList':
                        selItem.append(item)
                cmds.select(selItem)
        return

    def assignToSubdiv(self, *args):
        subdivSel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        objSel = cmds.ls(sl=True)
        if subdivSel is not None:
            subdivSel = subdivSel[0]
            if objSel != []:
                for obj in objSel:
                    shapes = None
                    history = cmds.listHistory(obj)
                    for parse in history:
                        if cmds.objectType(parse) == 'mesh':shapes = parse
                    if shapes is not None:
                        cmds.select(shapes)
                        try:
                            cmds.addAttr(shapes,at='message', longName='miSubdivApprox')
                        except Exception as e:
                            pass
                        cmds.connectAttr(subdivSel+'.message', shapes+'.miSubdivApprox')
        return

    def rename(self, *args):
        sel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        if sel is not None:
            sel = sel[0]
            newName = cmds.promptDialog(t='Subdiv Approx Mgr', m='Enter new Subdivision Approx name',\
                                        button=['OK', 'CANCEL'])
            if newName == 'OK':
                new = cmds.promptDialog(q=True, text=True)
                cmds.rename(sel, new)
        self.populateSubdv()
        return

    def deleteSubDv(self, *args):
        sel = cmds.textScrollList('samListTextScroll', q=True, si=True)
        if sel is not None:
            sel = sel[0]
            repVar = cmds.confirmDialog(icn='question', t='Subdiv Approx Mgr', m='Delete '+sel+'?',\
                                        button=['OK', 'CANCEL'])
            if repVar == 'OK': cmds.delete(sel)
        self.populateSubdv()
        return

    def addNewSubDiv(self, *args):
        newName = cmds.promptDialog(t='Subdiv Approx Mgr', m='Enter new Subdivision Approx name', tx='mrSubdivApprox', \
                                    button=['OK', 'CANCEL'])
        if newName == 'OK':
            new = cmds.promptDialog(q=True, text=True)
            tempNode = cmds.createNode('mentalraySubdivApprox', n=new)
            cmds.setAttr(tempNode+'.nSubdivisions', 1)
        self.populateSubdv()
        return

    def populateSubdv(self, *args):
        cmds.textScrollList('samListTextScroll', e=True, ra=True)
        for chk in cmds.ls(type='mentalraySubdivApprox'):
            cmds.textScrollList('samListTextScroll', e=True, a=chk)
        return

subdivManager()