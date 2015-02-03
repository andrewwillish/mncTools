#SET CREATOR
#Andrew Willis MNCA [2013]

import maya.cmds as cmds
import os, random, socket, getpass, datetime

#License Parsing
import licenseParsing
licenseParsing.licParse()

#Sequence Shield=====
if cmds.objExists('shot_master')==True:
    cmds.confirmDialog(icn='warning',t='Error',m='Unable to work with sequence file!', button=['Ok'])
    cmds.error('UNABLE TO WORK WITH SEQUENCE FILE')
#Sequence Shield=====

if cmds.window('MNCA_assetsetscreator', exists=True):
    cmds.deleteUI('MNCA_assetsetscreator', wnd=True)

class ASSETSETSCREATORcls:
    def __init__(self):
        global SETLISTtxtscr
        cmds.window('MNCA_assetsetscreator',t='MNCA Sets Manager',s=False,h=300)
        cmas=cmds.columnLayout(adj=True)  
        
        f1=cmds.frameLayout(l='Sets List',w=250)
        cmds.columnLayout(adj=True)
        SETLISTtxtscr=cmds.textScrollList(h=400)
        
        TEMPlis=cmds.ls(type='objectSet')
        SETlis=[]
        for chk in TEMPlis:
            if chk.startswith('g_')==True:
                SETlis.append(chk)
        cmds.textScrollList(SETLISTtxtscr,e=True, a=SETlis)
        
        cmds.separator(p=cmas)
        cmds.button(l='REFRESH' ,p=cmas, c=self.REFRESHfn)
        cmds.showWindow()    
        
        cmds.popupMenu(p=SETLISTtxtscr)  
        cmds.menuItem(l='Add Selected Object to Sets',c=self.ADDSELECTEDOBJfn)
        cmds.menuItem(l='Remove Selected Object from Sets',c=self.REMOVESELECTEOBJfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Select Object in Sets',c=self.SELECTOBJINSETfn)
        cmds.menuItem(l='Empty Sets',c=self.EMPTYSETSfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Add New Sets',c=self.ADDNEWSETfn)        
        cmds.menuItem(l='Rename Selected Sets',c=self.RENAMELISTfn)
        cmds.menuItem(l='Remove Selected Sets',c=self.REMOVESELECTEDSETSfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Create Standard Sets [color, ao, bg, sky]',c=self.CREATESTANDARDfn)
        cmds.menuItem(divider=True)
        return
    
    def REMOVESELECTEDSETSfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED') 
        
        REPvar=cmds.confirmDialog(icn='question', t='Proceed',m='Are you sure you want to delete '+SELECTEDSETvar+' sets?', button=['Ok','Cancel'])
        if REPvar=='Cancel':
            cmds.error('CANCELLED BY USER')
            
        cmds.delete(SELECTEDSETvar)
        self.REFRESHLISTfn()
        return
    
    def RENAMELISTfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED')       
            
        RESULTvar=cmds.promptDialog(t='New Set Name', m='Enter new set name: ', button=['Ok', 'Cancel'], cancelButton='Cancel', dismissString='Cancel', defaultButton='Ok')
        if RESULTvar=='Ok':
            NEWSETNAMEvar=cmds.promptDialog(q=True,text=True)
        
        if NEWSETNAMEvar==SELECTEDSETvar:
            cmds.confirmDialog(icn='warning',t='Error',m='Unable to rename same sets name!', button=['Ok'])
            cmds.error('INVALID NEW SETS NAME')
        
        cmds.sets(cp=SELECTEDSETvar,n='g_'+NEWSETNAMEvar)  
        cmds.delete(SELECTEDSETvar)
        self.REFRESHLISTfn()
        return
    
    def REFRESHLISTfn(self,*args):
        global SETLISTtxtscr
        cmds.textScrollList(SETLISTtxtscr,e=True,ra=True)
        TEMPlis=cmds.ls(type='objectSet')
        SETlis=[]
        for chk in TEMPlis:
            if chk.startswith('g_')==True:
                SETlis.append(chk)
        cmds.textScrollList(SETLISTtxtscr,e=True, a=SETlis)
        return
    
    def ADDNEWSETfn(self,*args):
        global SETLISTtxtscr
        RESULTvar=cmds.promptDialog(t='New Set Name', m='Enter new set name: ', button=['Ok', 'Cancel'], cancelButton='Cancel', dismissString='Cancel', defaultButton='Ok')
        if RESULTvar=='Ok':
            NEWSETNAMEvar=cmds.promptDialog(q=True,text=True)
        
        cmds.sets(em=True,n='g_'+NEWSETNAMEvar)
        self.REFRESHLISTfn()
        return
    
    def EMPTYSETSfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED')
        
        REPvar=cmds.confirmDialog(icn='question', t='Proceed',m='Are you sure you want to empty '+SELECTEDSETvar+' sets?', button=['Ok','Cancel'])
        if REPvar=='Cancel':
            cmds.error('CANCELLED BY USER')
        cmds.select(SELECTEDSETvar)
        cmds.sets(rm=SELECTEDSETvar)
        cmds.select(cl=True)
        return
    
    def SELECTOBJINSETfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED')
        
        cmds.select(SELECTEDSETvar)
        return
    
    def REMOVESELECTEOBJfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED')
        
        if cmds.ls(sl=True)==[]:
            cmds.confirmDialog(icn='warning',t='Error',m='No object selected!', button=['Ok'])
            cmds.error('NO OBJECT SELECTED')
        else:
            SELlis=cmds.ls(sl=True)  
        
        for chk in SELlis:
            cmds.sets(chk, rm=SELECTEDSETvar)      
        return
    
    def ADDSELECTEDOBJfn(self,*args):
        global SETLISTtxtscr
        try:
            SELECTEDSETvar=cmds.textScrollList(SETLISTtxtscr,q=True, si=True)[0]
        except:
            cmds.confirmDialog(icn='warning',t='Error',m='Select set to be added to!', button=['Ok'])
            cmds.error('SET TARGET IS NOT SELECTED')
        
        if cmds.ls(sl=True)==[]:
            cmds.confirmDialog(icn='warning',t='Error',m='No object selected!', button=['Ok'])
            cmds.error('NO OBJECT SELECTED')
        else:
            SELlis=cmds.ls(sl=True)
        
        cmds.sets(SELlis,e=True, fe=SELECTEDSETvar)
        return
    
    def CREATESTANDARDfn(self,*args):
        if cmds.objExists('g_color')==False:
            cmds.sets(em=True,n='g_color')
        if cmds.objExists('g_ao')==False:
            cmds.sets(em=True,n='g_ao')
        if cmds.objExists('g_bg')==False:
            cmds.sets(em=True,n='g_bg')
        if cmds.objExists('g_sky')==False:
            cmds.sets(em=True,n='g_sky')      
        cmds.confirmDialog(icn='information',t='Done',m='Standard Sets created!', button=['Ok'])
        self.REFRESHLISTfn()                 
        return
    
    def REFRESHfn(self,*args):
        import MNCA_assetsetscreator
        reload (MNCA_assetsetscreator)
        return

ASSETSETSCREATORcls()