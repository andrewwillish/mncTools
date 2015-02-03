__author__ = 'andrew.willis'

import maya.cmds as cmds
import os, asiist, getpass
import xml.etree.cElementTree as ET

#get project name and project code from asiist
for chk in asiist.getEnvi():
    if chk[0] == 'projName': PRJ_NAME = chk[1]
    if chk[0] == 'projCode': PRJ_CODE = chk[1]

#get current project
currentProject = PRJ_NAME

#CURRENT_USER
CURRENT_USER = str(getpass.getuser())
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
WIN_ROOT = os.environ['ProgramFiles'][:2]+'/'

#determine root location assetRoot and sequenceRoot
if not os.path.isfile(SCRIPT_ROOT+'/xml/root.xml'): raise StandardError, 'root.xml not exists'
root = (ET.parse(SCRIPT_ROOT+'/xml/root.xml')).getroot()
ASSET_ROOT = root[0].text
SEQUENCE_ROOT = root[1].text
ECF_ROOT = root[2].text
SOUND_ROOT = root[3].text


class assetImporterCls:
    def __init__(self):
        if cmds.window('assetImporter', exists=True): cmds.deleteUI('assetImporter', wnd=True)

        cmds.window('assetImporter',t='Asset Importer', s=False)
        cmas=cmds.columnLayout(adj=True)

        crow=cmds.rowColumnLayout(nc=3,cw=[(1,150),(2,150),(3,150)],p=cmas)

        c1=cmds.frameLayout(l='Char',p=crow)
        cmds.columnLayout(adj=True,p=c1)
        cmds.textField('charSearch',cc=self.populateTable)
        cmds.textScrollList('charTextScroll',dcc=lambda*args:self.importAsset(source='char'))

        c2=cmds.frameLayout(l='Props',p=crow)
        cmds.columnLayout(adj=True,p=c2)
        cmds.textField('propsSearch',cc=self.populateTable)
        cmds.textScrollList('propsTextScroll',dcc=lambda*args:self.importAsset(source='props'))

        c3=cmds.frameLayout(l='Sets',p=crow)
        cmds.columnLayout(adj=True,p=c3)
        cmds.textField('setsSearch',cc=self.populateTable)
        cmds.textScrollList('setsTextScroll',dcc=lambda*args:self.importAsset(source='sets'))

        cmds.text(l='Note: Double click on asset name to import selected asset',p=cmas)
        cmds.separator(p=cmas)
        cmds.button(l='REFRESH',p=cmas,bgc=[1.0,0.643835616566,0.0],c=self.refresh)

        cmds.showWindow()

        self.refresh()
        return

    def populateTable(self,*args):
        #get all file list in server
        allCharLis=os.listdir(ASSET_ROOT+'/'+currentProject+'/char')
        allPropsLis=os.listdir(ASSET_ROOT+'/'+currentProject+'/props')
        allSetsLis=os.listdir(ASSET_ROOT+'/'+currentProject+'/sets')

        #get filter keyword
        charSearch=cmds.textField('charSearch',q=True,tx=True)
        propSearch=cmds.textField('propsSearch',q=True,tx=True)
        setSearch=cmds.textField('setsSearch',q=True,tx=True)

        #filtration process
        tempLis=[]
        if charSearch!='':
            for chk in allCharLis: tempLis.append(chk) if chk.find(charSearch)!=-1 else None
            allCharLis=tempLis
        tempLis=[]
        if propSearch!='':
            for chk in allPropsLis: tempLis.append(chk) if chk.find(propSearch)!=-1 else None
            allPropsLis=tempLis
        tempLis=[]
        if setSearch!='':
            for chk in allSetsLis: tempLis.append(chk) if chk.find(setSearch)!=-1 else None
            allSetsLis=tempLis

        #populate table
        cmds.textScrollList('charTextScroll',e=True,ra=True)
        cmds.textScrollList('propsTextScroll',e=True,ra=True)
        cmds.textScrollList('setsTextScroll',e=True,ra=True)
        for chk in allCharLis:cmds.textScrollList('charTextScroll',e=True,a=chk)
        for chk in allPropsLis:cmds.textScrollList('propsTextScroll',e=True,a=chk)
        for chk in allSetsLis:cmds.textScrollList('setsTextScroll',e=True,a=chk)
        return

    def refresh(self,*args):
        self.populateTable()
        return

    def importAsset(self,source=None):
        if source is None: cmds.confirmDialog(icn='warning',t='Error',message='No source specified', btn=['OK']);\
        raise StandardError, 'error: no source specified'

        #check if temporer namespace exist
        for chk in cmds.ls():
            if chk.find('temporer')!=-1:
                try:
                    cmds.delete(chk)
                except:
                    pass

        #determine path
        if source=='char':
            asset=cmds.textScrollList('charTextScroll',q=True,si=True)[0]
        elif source=='props':
            asset=cmds.textScrollList('propsTextScroll',q=True,si=True)[0]
        elif source=='sets':
            asset=cmds.textScrollList('setsTextScroll',q=True,si=True)[0]
        path=ASSET_ROOT+'/'+currentProject+'/'+source+'/'+asset

        #determine if there is any RENDER version or not
        repVar=cmds.confirmDialog(icn='question',t='Select sub-version', \
                                  m='Select sub-version.',\
                                  button=['NORMAL','RENDER','CANCEL'])
        if repVar=='RENDER':
            if os.path.isdir(path+'/RENDER'):
                for chk in os.listdir(path+'/RENDER'):
                    if chk.endswith('.ma'):
                        importPath=path+'/RENDER/'+chk
            else:
                cmds.confirmDialog(icn='warning', t='Error',m='There is no RENDER version for this asset.',\
                                   button=['OK'])
                raise StandardError,'error : there is no render version for this asset'
        elif repVar=='NORMAL':
            for chk in os.listdir(path):
                if chk.endswith('.ma'):
                    importPath=path+'/'+chk
        else:
            raise StandardError,'error : cancelled by user'

        #create standard group
        if cmds.objExists('all')==False:
            cmds.group(n='all',em=True)
            cmds.group(n='geo',em=True,p='all')
            cmds.group(n='rig',em=True,p='all')

        #file reference process
        #note: we reference the asset first to get the unique namespace implemented
        reffFile= cmds.file(importPath,r=True,mnc=False,namespace=asset)

        geoNode='';rigNode='';allNode='';stateCtrlNode=''
        gColorNode='';gAoNode='';gBgNode='';gSkyNode='';gTransNode=''
        for chk in cmds.referenceQuery(reffFile,nodes=True):
            #get geo group
            if chk.endswith(':geo'):geoNode=chk
            #get rig group
            if chk.endswith(':rig'):rigNode=chk
            #get all group
            if chk.endswith(':all'):allNode=chk
            #get All group
            if chk.endswith(':All'):allNode=chk
            #get stateCtrl group
            if chk.endswith(':stateCtrl'):stateCtrlNode=chk

            #get :g_color node
            if chk.endswith(':g_color'):gColorNode=chk
            #get :g_ao node
            if chk.endswith(':g_ao'):gAoNode=chk
            #get :g_bg node
            if chk.endswith(':g_bg'):gBgNode=chk
            #get :g_sky node
            if chk.endswith(':g_sky'):gSkyNode=chk
            #get :g_trans node
            if chk.endswith(':g_trans'):gTransNode=chk

        #import asset reference
        cmds.file(reffFile,ir=True)

        #find and delete geo, rig, stateCtrl, and all
        if geoNode!='':cmds.parent(geoNode,'geo')
        if rigNode!='':cmds.parent(rigNode,'rig')
        if allNode!='':cmds.delete(allNode)

        #parse objectSet recorded
        cmds.select(cl=True)
        if gColorNode!='':
            if cmds.objExists('g_color')==False: cmds.sets(n='g_color')
            cmds.select(gColorNode)
            cmds.sets(cmds.ls(sl=True),include='g_color')
            cmds.delete(gColorNode)

        cmds.select(cl=True)
        if gAoNode!='':
            if cmds.objExists('g_ao')==False: cmds.sets(n='g_ao')
            cmds.select(gAoNode)
            cmds.sets(cmds.ls(sl=True),include='g_ao')
            cmds.delete(gAoNode)

        cmds.select(cl=True)
        if gBgNode!='':
            if cmds.objExists('g_bg')==False: cmds.sets(n='g_bg')
            cmds.select(gBgNode)
            cmds.sets(cmds.ls(sl=True),include='g_bg')
            cmds.delete(gBgNode)

        cmds.select(cl=True)
        if gSkyNode!='':
            if cmds.objExists('g_sky')==False: cmds.sets(n='g_sky')
            cmds.select(gSkyNode)
            cmds.sets(cmds.ls(sl=True),include='g_sky')
            cmds.delete(gSkyNode)

        cmds.select(cl=True)
        if gTransNode!='':
            if cmds.objExists('g_trans')==False: cmds.sets(n='g_trans')
            cmds.select(gTransNode)
            cmds.sets(cmds.ls(sl=True),include='g_trans')
            cmds.delete(gTransNode)

        #re-parse stateCtrl
        if cmds.objExists('smoothCtrl')==False:
            cmds.group(em=True,n='smoothCtrl')
            cmds.group(em=True,n='extraCtrl')
            cmds.group('smoothCtrl','extraCtrl',n='stateCtrl')

            try:
                cmds.parent('stateCtrl','All')
            except:
                cmds.parent('stateCtrl','all')
            cmds.select('smoothCtrl')
            cmds.addAttr(ln='smoothState',k=True,at='enum',en='ON:OFF')
            cmds.addAttr(ln='smoothLevel',k=True,at='enum',en='0:1:2')

            cmds.setAttr('stateCtrl.translateX',k=False)
            cmds.setAttr('stateCtrl.translateY',k=False)
            cmds.setAttr('stateCtrl.translateZ',k=False)
            cmds.setAttr('stateCtrl.rotateX',k=False)
            cmds.setAttr('stateCtrl.rotateY',k=False)
            cmds.setAttr('stateCtrl.rotateZ',k=False)
            cmds.setAttr('stateCtrl.scaleX',k=False)
            cmds.setAttr('stateCtrl.scaleY',k=False)
            cmds.setAttr('stateCtrl.scaleZ',k=False)
            cmds.setAttr('stateCtrl.visibility',k=False)

            cmds.setAttr('smoothCtrl.translateX',k=False)
            cmds.setAttr('smoothCtrl.translateY',k=False)
            cmds.setAttr('smoothCtrl.translateZ',k=False)
            cmds.setAttr('smoothCtrl.rotateX',k=False)
            cmds.setAttr('smoothCtrl.rotateY',k=False)
            cmds.setAttr('smoothCtrl.rotateZ',k=False)
            cmds.setAttr('smoothCtrl.scaleX',k=False)
            cmds.setAttr('smoothCtrl.scaleY',k=False)
            cmds.setAttr('smoothCtrl.scaleZ',k=False)
            cmds.setAttr('smoothCtrl.visibility',k=False)

            cmds.setAttr('extraCtrl.translateX',k=False)
            cmds.setAttr('extraCtrl.translateY',k=False)
            cmds.setAttr('extraCtrl.translateZ',k=False)
            cmds.setAttr('extraCtrl.rotateX',k=False)
            cmds.setAttr('extraCtrl.rotateY',k=False)
            cmds.setAttr('extraCtrl.rotateZ',k=False)
            cmds.setAttr('extraCtrl.scaleX',k=False)
            cmds.setAttr('extraCtrl.scaleY',k=False)
            cmds.setAttr('extraCtrl.scaleZ',k=False)
            cmds.setAttr('extraCtrl.visibility',k=False)

        #Apply polySmooth
        smooth = cmds.ls(type='polySmoothFace')
        for obj in smooth :
            if cmds.isConnected( 'smoothCtrl.smoothState', obj + '.nodeState' ) == 0 :
                cmds.connectAttr( 'smoothCtrl.smoothState', obj + '.nodeState', f=True )
            else :
                print obj + " has connection"
            if cmds.isConnected( 'smoothCtrl.smoothLevel', obj + '.divisions' ) == 0 :
                cmds.connectAttr( 'smoothCtrl.smoothLevel', obj + '.divisions', f=True )
            else :
                print obj + " has connection"

        cmds.setAttr('smoothCtrl.smoothState',1)

        #sentinel check
        if not cmds.objExists(asset+':sentinel'):
            cmds.file(new=True, f=True)
            cmds.confirmDialog(icn='warning', t='Sentinel Check', m='Illegal file insertion.', button=['OK'])
        else:
            cmds.confirmDialog(icn='information',t='Done',m='Asset insertion done.',button=['OK'])
        return
assetImporterCls()