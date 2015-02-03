#camera generator
#Andrew Willis 2014

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()
#License Parsing==========================================================================================

import maya.cmds as cmds
import getpass, asiist

#get project name and project code from asiist
for chk in asiist.getEnvi():
    if chk[0] == 'projName': PRJ_NAME = chk[1]
    if chk[0] == 'projCode': PRJ_CODE = chk[1]
    if chk[0] == 'resWidth': PRJ_RESWIDTH = chk[1]
    if chk[0] == 'resHeight': PRJ_RESHEIGHT = chk[1]
    if chk[0] == 'fulcrumWidth': FULC_WIDTH = chk[1]
    if chk[0] == 'fulcrumHeight': FULC_HEIGHT = chk[1]
    if chk[0] == 'saveWidth': SAVE_WIDTH = chk[1]
    if chk[0] == 'saveHeight': SAVE_HEIGHT = chk[1]
    if chk[0] == 'saveActionWidth': SAVE_ACTWIDTH = chk[1]
    if chk[0] == 'saveActionHeight': SAVE_ACTHEIGHT = chk[1]

#Preliminary Scene Data
try:
    SCN_EPS = cmds.getAttr('sceneInfo.episodeName',asString=True)
    SCN_SEQ = cmds.getAttr('sceneInfo.sequenceName',asString=True)
except:
    cmds.confirmDialog( icon='warning',title='Message', message='No shotMaster within the maya scene!', button=['Ok'] ,defaultButton='Ok' )
    cmds.error('error: no shot master within the scene')

class layCamGenCls:
    def __init__(self):
        if cmds.window('layCamGen', exists=True): cmds.deleteUI('layCamGen', window=True)
        win = cmds.window(t='Camera Generator', s=False, w=200)
        cmds.renameUI(win, 'layCamGen')
        cmas = cmds.columnLayout(adj=True)

        f0 = cmds.frameLayout(l='Primary Camera Creator',w=200,p=cmas)
        cmds.button(l='CREATE', bgc=[1.0, 0.643835616566, 0.0], h=30, c=self.generateCamera)

        f3 = cmds.frameLayout(l='Primary Camera Synoptic', w=200, p=cmas)
        cmds.columnLayout(adj=True)
        cmds.button(l='SELECT POS', c=lambda*args:self.selectNode(1))
        cmds.button(l='SELECT TILT', c=lambda*args:self.selectNode(2))
        cmds.button(l='SELECT SETTING', c=lambda*args:self.selectNode(3))
        cmds.button(l='DELETE', bgc=[1, 0, 0], c=self.deleteCamera)
        cmds.showWindow()
        return

    def deleteCamera(self, *args):
        try:
            cmds.delete('camMaster')
            if cmds.objExists('cameraex'):cmds.delete('cameraex')
            if cmds.objExists('cameraex2'):cmds.delete('cameraex2')
        except:
            cmds.confirmDialog(icn='warning', title='Error', message='There is no camMaster group in scene file', \
                               button=['Ok'])
            cmds.error('error: there is no camMaster in scene file')

        import mncToolsLayCameraGenerator
        reload(mncToolsLayCameraGenerator)
        return

    def selectNode(self, mode):
        try:
            if mode == 1:
                cmds.select('CAMPOS')
            elif mode == 2:
                cmds.select('CAMTILT')
            else:
                cmds.select('CAMSET')
        except:
            cmds.confirmDialog(icn='warning', title='Error', message='There is no camMaster group in scene file', \
                               button=['Ok'])
            cmds.error('error: there is no camMaster in scene file')
        return

    def generateCamera(self, *args):
        if not cmds.objExists('shotMaster'):
            cmds.confirmDialog(icn='warning', title='Error', message='There is no shotMaster group in scene file', \
                               button=['Ok'])
            cmds.error('error: no shot master within the scene')
        if cmds.objExists('camMaster'):
            cmds.confirmDialog(icn='warning', title='Error', message='There is already a camMaster group in scene file', \
                               button=['Ok'])
            cmds.error('error: no shot master within the scene')

        #CREATE CAMERA==============================================================================================
        genCamera = cmds.camera(dfg=False, dr=True, ncp=1, dsa=True, dst=False, ff='horizontal',\
                                hfa=1.68, vfa=0.945, fs=5.6, fl=50, sa=144)
        genCamera = genCamera[0]
        cmds.rename(genCamera, 'shotCAM')
        #CREATE CAMERA==============================================================================================

        #CREATE ANNOTATION==========================================================================================
        cmds.annotate('shotCAM', p=(0.800, 0.511, -2.514))
        cmds.setAttr('annotationShape1.displayArrow', 0, l=True)
        cmds.setAttr('annotation1.translateX',k=False,l=True)
        cmds.setAttr('annotation1.translateY',k=False,l=True)
        cmds.setAttr('annotation1.translateZ',k=False,l=True)
        cmds.setAttr('annotation1.rotateX',k=False,l=True)
        cmds.setAttr('annotation1.rotateY',k=False,l=True)
        cmds.setAttr('annotation1.rotateZ',k=False,l=True)
        cmds.setAttr('annotation1.scaleX',k=False,l=True)
        cmds.setAttr('annotation1.scaleY',k=False,l=True)
        cmds.setAttr('annotation1.scaleZ',k=False,l=True)
        cmds.setAttr('annotationShape1.overrideEnabled',1)
        cmds.setAttr('annotationShape1.overrideColor',7)

        cmds.annotate('shotCAM',p=(-0.892,0.511,-2.514))
        cmds.setAttr('annotationShape2.displayArrow',0,l=True)
        cmds.setAttr('annotation2.translateX',k=False,l=True)
        cmds.setAttr('annotation2.translateY',k=False,l=True)
        cmds.setAttr('annotation2.translateZ',k=False,l=True)
        cmds.setAttr('annotation2.rotateX',k=False,l=True)
        cmds.setAttr('annotation2.rotateY',k=False,l=True)
        cmds.setAttr('annotation2.rotateZ',k=False,l=True)
        cmds.setAttr('annotation2.scaleX',k=False,l=True)
        cmds.setAttr('annotation2.scaleY',k=False,l=True)
        cmds.setAttr('annotation2.scaleZ',k=False,l=True)
        cmds.setAttr('annotationShape2.overrideEnabled',1)
        cmds.setAttr('annotationShape2.overrideColor',7)

        cmds.annotate('shotCAM',p=(0.000,0.511,-2.514))
        cmds.setAttr('annotationShape3.displayArrow',0,l=True)
        cmds.setAttr('annotation3.translateX',k=False,l=True)
        cmds.setAttr('annotation3.translateY',k=False,l=True)
        cmds.setAttr('annotation3.translateZ',k=False,l=True)
        cmds.setAttr('annotation3.rotateX',k=False,l=True)
        cmds.setAttr('annotation3.rotateY',k=False,l=True)
        cmds.setAttr('annotation3.rotateZ',k=False,l=True)
        cmds.setAttr('annotation3.scaleX',k=False,l=True)
        cmds.setAttr('annotation3.scaleY',k=False,l=True)
        cmds.setAttr('annotation3.scaleZ',k=False,l=True)
        cmds.setAttr('annotationShape3.overrideEnabled',1)
        cmds.setAttr('annotationShape3.overrideColor',7)

        cmds.setAttr('shotCAM.translateX',l=True)
        cmds.setAttr('shotCAM.translateY',l=True)
        cmds.setAttr('shotCAM.translateZ',l=True)
        cmds.setAttr('shotCAM.rotateX',l=True)
        cmds.setAttr('shotCAM.rotateY',l=True)
        cmds.setAttr('shotCAM.rotateZ',l=True)
        cmds.setAttr('shotCAM.scaleX',l=True)
        cmds.setAttr('shotCAM.scaleY',l=True)
        cmds.setAttr('shotCAM.scaleZ',l=True)
        cmds.setAttr('shotCAM.visibility',l=True)
        cmds.group('shotCAM','annotation1','annotation2','annotation3',n='CAMGRP')
        cmds.setAttr('CAMGRP.translateX',k=False,l=True)
        cmds.setAttr('CAMGRP.translateY',k=False,l=True)
        cmds.setAttr('CAMGRP.translateZ',k=False,l=True)
        cmds.setAttr('CAMGRP.rotateX',k=False,l=True)
        cmds.setAttr('CAMGRP.rotateY',k=False,l=True)
        cmds.setAttr('CAMGRP.rotateZ',k=False,l=True)
        cmds.setAttr('CAMGRP.scaleX',k=False,l=True)
        cmds.setAttr('CAMGRP.scaleY',k=False,l=True)
        cmds.setAttr('CAMGRP.scaleZ',k=False,l=True)
        cmds.setAttr('CAMGRP.visibility',k=False,l=True)
        cmds.group('CAMGRP',n='CAMTILT')
        cmds.setAttr('CAMTILT.scaleX',k=False,l=True)
        cmds.setAttr('CAMTILT.scaleY',k=False,l=True)
        cmds.setAttr('CAMTILT.scaleZ',k=False,l=True)
        cmds.setAttr('CAMTILT.visibility',k=False,l=True)
        cmds.group('CAMTILT',n='CAMPOS')
        cmds.setAttr('CAMPOS.scaleX',k=False,l=True)
        cmds.setAttr('CAMPOS.scaleY',k=False,l=True)
        cmds.setAttr('CAMPOS.scaleZ',k=False,l=True)
        cmds.setAttr('CAMPOS.visibility',k=False,l=True)
        cmds.group('CAMPOS',n='camMaster')
        cmds.setAttr('camMaster.translateX',k=False,l=True)
        cmds.setAttr('camMaster.translateY',k=False,l=True)
        cmds.setAttr('camMaster.translateZ',k=False,l=True)
        cmds.setAttr('camMaster.rotateX',k=False,l=True)
        cmds.setAttr('camMaster.rotateY',k=False,l=True)
        cmds.setAttr('camMaster.rotateZ',k=False,l=True)
        cmds.setAttr('camMaster.scaleX',k=False,l=True)
        cmds.setAttr('camMaster.scaleY',k=False,l=True)
        cmds.setAttr('camMaster.scaleZ',k=False,l=True)
        cmds.rename('annotation1','anShotInformation')
        cmds.rename('annotation2','anFramecount')
        cmds.rename('annotation3','anArtistName')
        cmds.expression(n='cameraex',o='anFramecount',s='float $f=frame; setAttr -type "string"\
         "anFramecount.text" ("Frame: "+$f);')
        cmds.expression(n='cameraex2',o='anShotInformation',s='string $p=`getAttr sceneInfo.key`; setAttr -type\
         "string" "anShotInformation.text" ("Scene: "+"'+PRJ_CODE+'_'+SCN_EPS+'_'+SCN_SEQ+'_'+'SH_"+$p);')
        cmds.setAttr('anArtistName.text','Artist: '+str(getpass.getuser()),typ='string')

        #cmds.expression(n='cameraex3',o='hud_grp',s='float $g=`getAttr CAMSET.FOV_alg_35`/50;\
        #setAttr "hud_grp.scaleZ" $g;', ae=True)

        cmds.group('anShotInformation','anFramecount','anArtistName',n='hud_grp')
        cmds.move(0,0,0,'hud_grp.scalePivot')
        #Change str(getpass.getuser()) to str(asmas.getuser())

        cmds.setAttr('anShotInformation.scaleX',k=True,l=False)
        cmds.setAttr('anShotInformation.scaleY',k=True,l=False)
        cmds.setAttr('anShotInformation.scaleZ',k=True,l=False)
        cmds.setAttr('anFramecount.scaleX',k=True,l=False)
        cmds.setAttr('anFramecount.scaleY',k=True,l=False)
        cmds.setAttr('anFramecount.scaleZ',k=True,l=False)
        cmds.setAttr('anArtistName.scaleX',k=True,l=False)
        cmds.setAttr('anArtistName.scaleY',k=True,l=False)
        cmds.setAttr('anArtistName.scaleZ',k=True,l=False)

        #CREATE ANNOTATION==========================================================================================

        #CREATE FULCRUM=============================================================================================
        fulcrumHeight = float(FULC_HEIGHT)
        fulcrumWidth = float(FULC_WIDTH)

        c1=cmds.curve(d=1, p=[(0, 0, 0), \
                              #top right
                              (fulcrumWidth/2,fulcrumHeight/2, -115.744), \
                              #top left
                              ((fulcrumWidth/2)*-1,fulcrumHeight/2,-115.744), \
                              #central
                              (0,0, 0), \
                              #bottom right
                              (fulcrumWidth/2,(fulcrumHeight/2)*-1, -115.744), \
                              #bottom left
                              ((fulcrumWidth/2)*-1,(fulcrumHeight/2)*-1,-115.744), \
                              #central
                              (0,0, 0), \
                              #bottom left
                              ((fulcrumWidth/2)*-1,(fulcrumHeight/2)*-1,-115.744), \
                              #top left
                              ((fulcrumWidth/2)*-1,fulcrumHeight/2, -115.744),  \
                              #top right
                              (fulcrumWidth/2,fulcrumHeight/2, -115.744), \
                              #bottom right
                              (fulcrumWidth/2,(fulcrumHeight/2)*-1, -115.744)],\
                      k=[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] )
        cmds.rename(c1, 'fulcrum')

        BASECOORDTRANSvar = cmds.xform('shotCAM',q=True,t=True,ws=True)
        cmds.group(em=True,n='fulcrum_grp')
        cmds.move(BASECOORDTRANSvar[0],BASECOORDTRANSvar[1],BASECOORDTRANSvar[2],'fulcrum_grp')

        cmds.parent('fulcrum','fulcrum_grp')
        cmds.parent('fulcrum_grp','CAMGRP')
        cmds.color( 'fulcrum', ud=1 )

        cmds.setAttr('fulcrum_grp.translateX',k=False,l=True)
        cmds.setAttr('fulcrum_grp.translateY',k=False,l=True)
        cmds.setAttr('fulcrum_grp.translateZ',k=False,l=True)
        cmds.setAttr('fulcrum_grp.rotateX',k=False,l=True)
        cmds.setAttr('fulcrum_grp.rotateY',k=False,l=True)
        cmds.setAttr('fulcrum_grp.rotateZ',k=False,l=True)
        cmds.setAttr('fulcrum_grp.visibility',k=False,l=True)

        cmds.setAttr('fulcrum.translateX',k=False,l=True)
        cmds.setAttr('fulcrum.translateY',k=False,l=True)
        cmds.setAttr('fulcrum.translateZ',k=False,l=True)
        cmds.setAttr('fulcrum.rotateX',k=False,l=True)
        cmds.setAttr('fulcrum.rotateY',k=False,l=True)
        cmds.setAttr('fulcrum.rotateZ',k=False,l=True)

        cmds.move(0,0,0,'fulcrum_grp.scalePivot')
        #CREATE FULCRUM=============================================================================================

        #CREATE 4:3 ACTION AND TITLE SAFE===========================================================================
        cmds.polyPlane(n='save', sx=1, sy=1, w=float(SAVE_WIDTH), h=float(SAVE_HEIGHT),ax=[0,0,1])
        cmds.polyPlane(n='saveaction', sx=1, sy=1, w=float(SAVE_ACTWIDTH), h=float(SAVE_ACTHEIGHT),ax=[0,0,1])
        cmds.move(-2.493,'save',r=True,z=True)
        cmds.move(-2.493,'saveaction',r=True,z=True)

        cmds.group(em=True,n='save_grp')
        cmds.move(BASECOORDTRANSvar[0], BASECOORDTRANSvar[1], BASECOORDTRANSvar[2], 'save_grp')

        cmds.parent('save','save_grp')
        cmds.parent('saveaction','save_grp')
        cmds.parent('save_grp','CAMGRP')
        cmds.color( 'save', ud=1 )
        cmds.color( 'saveaction', ud=1 )
        cmds.setAttr('save.template',1)
        cmds.setAttr('saveaction.template',1)

        cmds.setAttr('saveaction.translateX',k=False,l=True)
        cmds.setAttr('saveaction.translateY',k=False,l=True)
        cmds.setAttr('saveaction.translateZ',k=False,l=True)
        cmds.setAttr('saveaction.rotateX',k=False,l=True)
        cmds.setAttr('saveaction.rotateY',k=False,l=True)
        cmds.setAttr('saveaction.rotateZ',k=False,l=True)
        cmds.setAttr('saveaction.visibility',1)
        cmds.setAttr('saveaction.visibility',k=False,l=True)

        cmds.setAttr('save.translateX',k=False,l=True)
        cmds.setAttr('save.translateY',k=False,l=True)
        cmds.setAttr('save.translateZ',k=False,l=True)
        cmds.setAttr('save.rotateX',k=False,l=True)
        cmds.setAttr('save.rotateY',k=False,l=True)
        cmds.setAttr('save.rotateZ',k=False,l=True)
        cmds.setAttr('save.visibility',1)
        cmds.setAttr('save.visibility',k=False,l=True)

        cmds.setAttr('save_grp.translateX',k=False,l=True)
        cmds.setAttr('save_grp.translateY',k=False,l=True)
        cmds.setAttr('save_grp.translateZ',k=False,l=True)
        cmds.setAttr('save_grp.rotateX',k=False,l=True)
        cmds.setAttr('save_grp.rotateY',k=False,l=True)
        cmds.setAttr('save_grp.rotateZ',k=False,l=True)
        cmds.setAttr('save_grp.visibility',k=False,l=True)

        cmds.setAttr('hud_grp.translateX',k=False,l=True)
        cmds.setAttr('hud_grp.translateY',k=False,l=True)
        cmds.setAttr('hud_grp.translateZ',k=False,l=True)
        cmds.setAttr('hud_grp.rotateX',k=False,l=True)
        cmds.setAttr('hud_grp.rotateY',k=False,l=True)
        cmds.setAttr('hud_grp.rotateZ',k=False,l=True)
        cmds.setAttr('hud_grp.visibility',k=False,l=True)
        #CREATE 4:3 ACTION AND TITLE SAFE===========================================================================

        #CAM SETTING================================================================================================
        cmds.group(em=True,n='CAMSET')
        cmds.parent('CAMSET','CAMGRP')

        cmds.setAttr('CAMSET.translateX',k=False,l=True)
        cmds.setAttr('CAMSET.translateY',k=False,l=True)
        cmds.setAttr('CAMSET.translateZ',k=False,l=True)
        cmds.setAttr('CAMSET.rotateX',k=False,l=True)
        cmds.setAttr('CAMSET.rotateY',k=False,l=True)
        cmds.setAttr('CAMSET.rotateZ',k=False,l=True)
        cmds.setAttr('CAMSET.scaleX',k=False,l=True)
        cmds.setAttr('CAMSET.scaleY',k=False,l=True)
        cmds.setAttr('CAMSET.scaleZ',k=False,l=True)
        cmds.setAttr('CAMSET.visibility',k=False,l=True)

        #Custom Attribute
        cmds.addAttr( 'CAMSET',ln='Fulcrum_Size', defaultValue=1.0,min=1,k=True )
        cmds.addAttr( 'CAMSET',ln='Fulcrum_Visibility', defaultValue=1.0,min=0,max=1,k=True )
        cmds.addAttr( 'CAMSET',ln='FOV_alg_35', defaultValue=35,k=True )
        cmds.addAttr( 'CAMSET',ln='Far_Clip', defaultValue=100000.0,k=True )
        cmds.addAttr( 'CAMSET',ln='Near_Clip', defaultValue=1.0,k=True )
        cmds.addAttr( 'CAMSET',ln='_________________',attributeType='enum',en='__________',k=True,w=True )
        cmds.setAttr('CAMSET._________________',lock=True)
        cmds.addAttr( 'CAMSET',ln='Frame_Counter',attributeType='enum',en='Off:On',k=True )
        cmds.addAttr( 'CAMSET',ln='Artist_Name',attributeType='enum',en='Off:On',k=True )
        cmds.addAttr( 'CAMSET',ln='File_Name',attributeType='enum',en='Off:On',k=True )

        #Connection
        cmds.connectAttr('CAMSET.Fulcrum_Size','fulcrum.scaleX')
        cmds.connectAttr('CAMSET.Fulcrum_Size','fulcrum.scaleY')
        cmds.connectAttr('CAMSET.Fulcrum_Size','fulcrum.scaleZ')

        cmds.connectAttr('CAMSET.Fulcrum_Visibility','fulcrum.visibility')

        cmds.connectAttr('CAMSET.Frame_Counter','anFramecount.visibility')
        cmds.connectAttr('CAMSET.File_Name','anShotInformation.visibility')
        cmds.connectAttr('CAMSET.Artist_Name','anArtistName.visibility')

        cmds.connectAttr('CAMSET.Far_Clip','shotCAMShape.farClipPlane')
        cmds.connectAttr('CAMSET.Near_Clip','shotCAMShape.nearClipPlane')

        cmds.connectAttr('CAMSET.FOV_alg_35','shotCAMShape.focalLength')
        cmds.setAttr('CAMSET.FOV_alg_35',50)

        cmds.setAttr('CAMSET.Frame_Counter',1)
        cmds.setAttr('CAMSET.Artist_Name',1)
        cmds.setAttr('CAMSET.File_Name',1)

        MULTIDIVvar=cmds.createNode('multiplyDivide',n='cammultiply')
        cmds.setAttr(MULTIDIVvar+'.operation',2)
        cmds.setAttr(MULTIDIVvar+'.input2X',50)
        cmds.connectAttr('CAMSET.FOV_alg_35',MULTIDIVvar+'.input1X')
        cmds.connectAttr(MULTIDIVvar+'.outputX','hud_grp.scaleZ')
        cmds.connectAttr(MULTIDIVvar+'.outputX','fulcrum_grp.scaleZ')
        cmds.connectAttr(MULTIDIVvar+'.outputX','save_grp.scaleZ')
        #CAM SETTING================================================================================================

        #NEAR CLIP GROUP============================================================================================
        cmds.group(em=True,n='nearclip_grp',p='CAMGRP')
        cmds.parent('hud_grp','nearclip_grp')
        cmds.parent('save_grp','nearclip_grp')
        cmds.parent('fulcrum_grp','nearclip_grp')

        cmds.connectAttr('CAMSET.Near_Clip','nearclip_grp.scaleX')
        cmds.connectAttr('CAMSET.Near_Clip','nearclip_grp.scaleY')
        cmds.connectAttr('CAMSET.Near_Clip','nearclip_grp.scaleZ')

        #NEAR CLIP GROUP============================================================================================

        #CELAN-UP===================================================================================================
        cmds.move(0,0,0,'CAMPOS.scalePivot')
        cmds.move(0,0,0,'CAMPOS.rotatePivot')

        cmds.move(0,0,0,'CAMTILT.scalePivot')
        cmds.move(0,0,0,'CAMTILT.rotatePivot')

        cmds.setAttr('shotCAM.translateX',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.translateY',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.translateZ',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.rotateX',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.rotateY',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.rotateZ',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.scaleX',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.scaleY',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.scaleZ',e=True,l=True,k=False)
        cmds.setAttr('shotCAM.visibility',e=True,l=True,k=False)

        cmds.setAttr('hud_grp.scaleX',e=True,l=True,k=False)
        cmds.setAttr('hud_grp.scaleY',e=True,l=True,k=False)
        cmds.setAttr('hud_grp.scaleZ',e=True,l=True,k=False)

        cmds.setAttr('fulcrum_grp.scaleX',e=True,l=True,k=False)
        cmds.setAttr('fulcrum_grp.scaleY',e=True,l=True,k=False)
        cmds.setAttr('fulcrum_grp.scaleZ',e=True,l=True,k=False)

        cmds.setAttr('save_grp.scaleX',e=True,l=True,k=False)
        cmds.setAttr('save_grp.scaleY',e=True,l=True,k=False)
        cmds.setAttr('save_grp.scaleZ',e=True,l=True,k=False)
        #CELAN-UP===================================================================================================

        #Parenting
        cmds.parent('camMaster','shotMaster')

        cmds.select(cl=True)

        import mncToolsLayCameraGenerator
        reload(mncToolsLayCameraGenerator)
        return

layCamGenCls()