__author__ = 'andrew.willis'

#Shot Setup - MNC Version
#Andrew Willis 2014

#License Parsing
import licenseParsing
licenseParsing.licParse()

import maya.cmds as cmds
import asiist, os, getpass
import xml.etree.cElementTree as ET
import mncRegCore

#cutom error declaration
class registrarError(Exception):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return repr(self.text)

#check shotMaster existence
if not cmds.objExists('shotMaster'):
    cmds.confirmDialog(icn='warning', t='Error', m='shotMaster not exists.', button=['OK'])
    cmds.error('error : shotMaster not exists')

#CURRENT_USER
CURRENT_USER = str(getpass.getuser())
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
WIN_ROOT = os.environ['ProgramFiles'][:2]+'/'

#get project name and project code from asiist
for chk in asiist.getEnvi():
    if chk[0] == 'projName': PRJ_NAME = chk[1]
    if chk[0] == 'projCode': PRJ_CODE = chk[1]

#determine root location assetRoot and sequenceRoot
if not os.path.isfile(SCRIPT_ROOT+'/xml/root.xml'): raise registrarError, 'root.xml not exists'
root = (ET.parse(SCRIPT_ROOT+'/xml/root.xml')).getroot()
ASSET_ROOT = root[0].text
SEQUENCE_ROOT = root[1].text
ECF_ROOT = root[2].text
SOUND_ROOT = root[3].text

#read assetType.xml data
try:
    tree = ET.parse(SCRIPT_ROOT+'/xml/assetType.xml')
    root = tree.getroot()
    ASSET_TYPES = []
    for chk in root:
        ASSET_TYPES.append({'tag':str(chk.tag), 'desc':str(chk.text)})
except Exception as e:
    cmds.confirmDialog(icn='warning', t='error', m=str(e), button=['OK'])
    raise registrarError, 'failed to fetch assetType.xml'

class shotBuilderCls:
    def __init__(self):
        if cmds.window('veShotBuilder', exists=True):cmds.deleteUI('veShotBuilder',wnd=True)

        win = cmds.window(t='Shot Builder - ['+PRJ_NAME+']', s=False)
        cmds.renameUI(win, 'veShotBuilder')
        cmas = cmds.rowColumnLayout(nc=2)

        left = cmds.columnLayout(adj=True,p=cmas)
        f1 = cmds.frameLayout(l='Asset Open',p=left)
        cmds.columnLayout(adj=True)
        cmds.optionMenu('assetType',w=150, cc=self.populate)
        cmds.menuItem(l='')
        for chk in ASSET_TYPES:
            cmds.menuItem(l=chk['tag'])
        cmds.text(l='Search Asset :', fn='boldLabelFont', al='left')
        cmds.textField('assetSearch', cc=self.populate)

        f2 = cmds.frameLayout(l='Asset Content' ,p=left)
        cmds.columnLayout(adj=True)
        cmds.textScrollList('assetContent', w=150, h=150, sc=self.populateInformation)

        right=cmds.columnLayout(adj=True,p=cmas)
        f3=cmds.frameLayout(l='Asset Information', p=right)
        pf3=cmds.columnLayout(adj=True)
        f3split=cmds.rowColumnLayout(nc=2, p=pf3)
        cmds.columnLayout(adj=True, p=f3split)
        cmds.picture('preview', image=SCRIPT_ROOT+'/NA.png', w=150,h=150)
        cmds.columnLayout(adj=True, p=f3split)
        cmds.text(l='Asset Name :', fn='boldLabelFont', al='left')
        cmds.textField('assetName', en=False)
        cmds.text(l='Asset Description :',fn='boldLabelFont', al='left')
        cmds.scrollField('assetDesc', h=70, en=False, ww=True)
        cmds.text(l='Asset Path :', fn='boldLabelFont', al='left')
        cmds.textField('assetPath', en=False)

        cmds.separator(p=pf3)
        cmds.button(l='REFERENCE ASSET TO CURRENT SCENE FILE', p=pf3, h=70, bgc=[1.0, 0.730158729907, 0.0], \
                    c=self.referenceAsset)

        cmds.showWindow()
        return

    def populateInformation(self,*args):
        #asset selection id
        assetName = cmds.textScrollList('assetContent',q=True,si=True)[0]
        assetType = cmds.optionMenu('assetType', q=True, v=True)
        assetPath = ASSET_ROOT+PRJ_NAME+'/'+assetType+'/'+assetName

        #populating asset information
        cmds.textField('assetName', e=True, tx=assetName)
        cmds.scrollField('assetDesc', e=True, tx='N/A')
        cmds.textField('assetPath', e=True, tx=assetPath)

        #populate image
        if os.path.isfile(assetPath+'/preview.png'):
            cmds.picture('preview',e=True,image=assetPath+'/preview.png')
        else:
            cmds.picture('preview',e=True,image=SCRIPT_ROOT+'/NA.png')
        return

    def populate(self,*args):
        #clear field
        cmds.picture('preview', e=True, image=SCRIPT_ROOT+'/NA.png')
        cmds.textField('assetName', e=True, tx='')
        cmds.scrollField('assetDesc', e=True, tx='')
        cmds.textField('assetPath', e=True, tx='')

        #search string
        search = cmds.textField('assetSearch', q=True, tx=True)

        #asset type
        type = cmds.optionMenu('assetType', q=True, v=True)

        #populating asset content
        cmds.textScrollList('assetContent', e=True, ra=True)
        temp = []
        write = []

        write = mncRegCore.listAsset(subType=type)

        if search!='':
            for chk in write:
                if chk.find(search) != -1:temp.append(chk)
            write = temp

        #populate textscroll
        cmds.textScrollList('assetContent', e=True, ra=True)
        for chk in write: cmds.textScrollList('assetContent', e=True, a=chk)
        return

    def referenceAsset(self,*args):
        assetRefPath = cmds.textField('assetPath',q=True,tx=True)
        assetName = cmds.textScrollList('assetContent',q=True,si=True)[0]
        type = cmds.optionMenu('assetType', q=True, v=True)
        if type == 'char': type = 'c'
        elif type == 'props': type = 'p'
        elif type == 'sets': type = 's'
        if os.path.isdir(assetRefPath):
            if assetRefPath is not None:
                try:
                    mncRegCore.referenceAsset(filePath=assetRefPath+'/'+type+'_'+assetName+'.ma', assetName=type+'_'+assetName)
                except Exception as e:
                    cmds.confirmDialog(icn='warning', t='Error', m=str(e), button=['OK'])

        else:
            cmds.confirmDialog(icn='warning', t='Error',message='Asset sub-type non-exists!\n'+assetRefPath, button=['OK'])

        return

shotBuilderCls()
