__author__ = 'andrew.willis'

import maya.cmds as cmds

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()

class GENERATEANIMTEMPcls:
    def __init__(self):
        if cmds.objExists('ANIM_TEMP')==True:
            REPvar=cmds.confirmDialog(icn='question', title='Exists', message='ANIM_TEMP exists within scene file would you like to delete it?', button=['Delete','Replace','Cancel'])
            if REPvar=='Cancel':
                cmds.error('error: cancelled by user')
            elif REPvar=='Replace':
                try:
                    self.DELETETEMPfn()
                    self.CREATETEMPfn()
                except Exception as e:
                    raise StandardError, str(e)
            elif REPvar=='Delete':
                try:
                    self.DELETETEMPfn()
                except Exception as e:
                    raise  StandardError, str(e)
        else:
            try:
                self.CREATETEMPfn()
            except Exception as e:
                raise StandardError, str(e)
        return

    def DELETETEMPfn(self, *args):
        cmds.editRenderLayerGlobals(crl='defaultRenderLayer')
        cmds.delete('ANIM_TEMP')
        return

    def CREATETEMPfn(self, *args):
        if cmds.objExists('shotMaster')==False:
            cmds.confirmDialog(icn='warning', title='Error', message='There is no shotMaster within scene file!', \
                               button=['Ok'])
            cmds.error('error: cancelled by user')

        #Create render layer
        cmds.createRenderLayer(n='ANIM_TEMP', noRecurse=True)

        #Import Transform object [Char and Props]
        cmds.select('char','props',hi=True)
        TEMPlis=cmds.ls(sl=True)

        cmds.select(cl=True)
        for chk in TEMPlis:
            cmds.select(chk)
            if cmds.ls(sl=True,showType=True)[1]=='transform':
                cmds.editRenderLayerMembers('ANIM_TEMP',chk,nr=True)
        #Import Transform object [Char and Props]

        #Import Transform [Sets]
        cmds.select('sets',hi=True)
        TEMPlis=cmds.ls(sl=True)

        cmds.select(cl=True)
        for chk in TEMPlis:
            cmds.select(chk)
            if cmds.ls(sl=True,showType=True)[1]=='transform':
                cmds.editRenderLayerMembers('ANIM_TEMP',chk,nr=True)
                cmds.editRenderLayerGlobals(crl='ANIM_TEMP')
                cmds.hyperShade(assign='lambert1')
        #Import Transform [Sets]

        cmds.select(cl=True)
        cmds.confirmDialog(icn='information', title='Done', message='ANIM_TEMP has been created.', button=['Ok'])
        return

GENERATEANIMTEMPcls()