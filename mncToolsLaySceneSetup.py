__author__ = 'andrew.willis'

#Shot Setup - MNC Version
#Andrew Willis 2014

#Developer Notes:

#License Parsing
import licenseParsing
licenseParsing.licParse()

import maya.cmds as cmds
import maya.mel as mel
import asiist, os, getpass
import xml.etree.cElementTree as ET

#declare standard variable
epsInts = []
dataHeader = None

#CURRENT_USER
CURRENT_USER = str(getpass.getuser())
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
WIN_ROOT = os.environ['ProgramFiles'][:2]+'/'

#get project name and project code from asiist
for chk in asiist.getEnvi():
    if chk[0] == 'projName': PRJ_NAME = chk[1]
    if chk[0] == 'projCode': PRJ_CODE = chk[1]

#determine root location assetRoot and sequenceRoot
if not os.path.isfile(SCRIPT_ROOT+'/xml/root.xml'): raise StandardError, 'root.xml not exists'
root = (ET.parse(SCRIPT_ROOT+'/xml/root.xml')).getroot()
ASSET_ROOT = root[0].text
SEQUENCE_ROOT = root[1].text
ECF_ROOT = root[2].text
SOUND_ROOT = root[3].text

class shotSetupCls:
    def __init__(self):
        if cmds.window('mncShotSetup', exists=True):cmds.deleteUI('mncShotSetup',wnd=True)

        win = cmds.window(t='Shot Setup - ['+PRJ_NAME+']', s=False, mb=False)
        cmds.renameUI(win, 'mncShotSetup')
        cmas = cmds.columnLayout(adj=True)

        f1=cmds.frameLayout(l='ECF File',p=cmas)
        cmds.rowColumnLayout(nc=2)
        cmds.textScrollList('ecfList', w=220, h=150, sc=self.populateContent)

        f2=cmds.frameLayout(l='Episode Content',p=cmas)
        cmds.columnLayout(adj=True)
        cmds.textScrollList('shotContent',w=220, h=300)
        cmds.showWindow()

        f4=cmds.frameLayout(l='Command',p=cmas)
        cmds.rowColumnLayout(nc=3)
        cmds.button(l='SETUP SHOT',c=lambda*args:self.setupShot(new=True),bgc=[1.0, 0.643835616566, 0.0])
        cmds.button(l='UPDATE SHOT',c=lambda*args:self.setupShot(new=False))
        cmds.button(l='CLEAR SHOT',c=self.deleteShot)

        self.populateECF()
        return

    def populateECF(self):
        if not os.path.isdir(ECF_ROOT+'/'+PRJ_NAME): os.makedirs(ECF_ROOT+'/'+PRJ_NAME)
        cmds.textScrollList('ecfList', e=True, ra=True)

        for chk in os.listdir(ECF_ROOT+'/'+PRJ_NAME):
            if chk.endswith('.ecfx'): cmds.textScrollList('ecfList', e=True, a=chk.replace('.ecfx',''))
        return

    def deleteShot(self,*args):
        repVar = cmds.confirmDialog(icn='question', t='New',\
                                  m='This will clear current sequence. Proceed?',\
                                  button=['Ok', 'Cancel'])
        if repVar == 'Ok':cmds.file(new=True,f=True)
        return

    def populateContent(self,*args):
        global epsInts,dataHeader
        ecfName = cmds.textScrollList('ecfList', q=True, si=True)[0]
        file = ECF_ROOT+'/'+PRJ_NAME+'/'+ecfName+'.ecfx'
        reader = open(file, 'r')
        data=reader.readlines()
        reader.close()

        dataHeader = file[file.rfind('/')+1:]
        dataHeader = dataHeader.replace('.ecfx', '')

        epsInts = []
        for chk in data:
            chk = chk.replace('\r\n','')
            epsInts.append([chk[:chk.find(':')],chk[chk.find(':')+1:]])

        cmds.textScrollList('shotContent',e=True,ra=True)
        prev = None
        for chk in epsInts:
            seqName = chk[0][:chk[0].find('_')]
            if seqName != prev:
                cmds.textScrollList('shotContent', e=True, a=seqName)
                prev = seqName
        return

    def setupShot(self,new=False):
        global epsInts,dataHeader
        if epsInts == [] or dataHeader is None:
            cmds.confirmDialog(icn='error',t='Error',m='No episode opened!',button=['OK'])
            cmds.error('error : no episode opened')

        seqShot = cmds.textScrollList('shotContent',q=True,si=True)
        if seqShot is None:
            cmds.confirmDialog(icn='error',t='Error',m='No shot selected!',button=['OK'])
            cmds.error('error : no shot selected')


        if new:
            if cmds.objExists('shotMaster'):
                cmds.confirmDialog(icn='error',t='Error',m='Shot master exists!',button=['OK'])
                cmds.error('error : shot master exists')
            cmds.group(em=True,n='shotMaster')
            self.sceneInfo()
            cmds.confirmDialog(icn='information',t='Done',m='Shot setup done.',button=['Ok'])
        else:
            if cmds.objExists('sceneInfo'):cmds.delete('sceneInfo')
            self.sceneInfo()
            cmds.confirmDialog(icn='information',t='Done',m='Shot update done.',button=['Ok'])
        return

    def sceneInfo(self):
        seqInfo = cmds.textScrollList('shotContent', q=True, si=True)[0]
        episodeName = cmds.textScrollList('ecfList', q=True, si=True)[0]
        record = []
        for chk in epsInts:
            if chk[0].find(seqInfo) != -1:record.append(chk)

        #implement sequence information
        enviFetch = asiist.getEnvi()
        for chk in enviFetch:
            if chk[0] == 'resWidth': resWidth = chk[1]
            if chk[0] == 'resHeight': resHeight = chk[1]
            if chk[0] == 'resAspectRatio': resAspectRatio = chk[1]

        cmds.setAttr('defaultResolution.width', float(resWidth))
        cmds.setAttr('defaultResolution.height', float(resHeight))
        cmds.setAttr('defaultResolution.deviceAspectRatio', float(resAspectRatio))

        #create empty group
        cmds.group(em=True, n='sceneInfo', p='shotMaster')
        if not cmds.objExists('char'): cmds.group(em=True, n='char', p='shotMaster')
        if not cmds.objExists('prop'): cmds.group(em=True, n='prop', p='shotMaster')
        if not cmds.objExists('sets'): cmds.group(em=True, n='sets', p='shotMaster')

        #generate data from record
        duration = 0
        for chk in record:
            duration = duration+int(chk[1])

        #additional data to sceneInfo
        cmds.select('sceneInfo')
        for chk in asiist.getEnvi():
            cmds.addAttr(ln=str(chk[0]), k=True, at='enum', en=str(chk[1]))
            cmds.setAttr('sceneInfo.'+str(chk[0]), l=True)
            if chk[0] == 'unit':cmds.currentUnit(time=chk[1])

        cmds.addAttr(ln='__________',k=True,at='enum',en='__________')
        cmds.setAttr('sceneInfo.__________',l=True)
        cmds.addAttr(ln='episodeName',k=True,at='enum', en=str(episodeName))
        cmds.setAttr('sceneInfo.episodeName',l=True)
        cmds.addAttr(ln='sequenceName',k=True,at='enum', en=str(seqInfo))
        cmds.setAttr('sceneInfo.sequenceName',l=True)
        cmds.addAttr(ln='startFrame',k=True,at='enum',en='101')
        cmds.setAttr('sceneInfo.startFrame',l=True)
        cmds.addAttr(ln='endFrame',k=True,at='enum',en=str(100+(duration)))
        cmds.setAttr('sceneInfo.endFrame',l=True)
        cmds.addAttr(ln='key',k=True)
        cmds.addAttr(ln='___________',k=True,at='enum',en='__________')
        cmds.setAttr('sceneInfo.___________',l=True)

        base = 101

        for chk in epsInts:
            if chk[0].find(seqInfo) != -1:
                #create shot entry
                cmds.addAttr(ln=chk[0],k=True,at='enum',en=str(chk[1]))
                cmds.setAttr('sceneInfo.'+chk[0],l=True)

                #create shot key
                shotNum = chk[0]
                shotNum = shotNum[shotNum.rfind('_')+1:]
                shotNum = int(shotNum.replace('SH',''))

                cmds.setAttr('sceneInfo.key', shotNum)
                cmds.setKeyframe('sceneInfo', attribute='key', t=base)

                base = base+(int(chk[1])-1)
                cmds.setAttr('sceneInfo.key', shotNum)
                cmds.setKeyframe('sceneInfo', attribute='key', t=base)

                base = base+1
                #cmds.setKeyframe('sceneInfo', attribute='key', t=base)


        #lock standard channel
        for object in ['shotMaster', 'sceneInfo', 'char', 'prop', 'sets']:
            for channel in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility']:
                cmds.setAttr(object+'.'+channel, l=True, cb=False, k=False)

        #impose shot range
        cmds.rangeControl(min=101, max=101+(int(duration)-1))
        cmds.playbackOptions(min = 101, max = 101+(int(duration)-1))

        #insert sound
        soundName = str(shotNum)
        if len(soundName) == 1: soundName = '0'+soundName
        if not os.path.isfile(SOUND_ROOT+'/'+PRJ_NAME+'/'+episodeName+'/SQ'+str(soundName)+'.wav'):
            cmds.confirmDialog(icn='information', t='Missing File', m='Missing sound file. Skip sound insertion process.', button=['OK'])
        else:
            if cmds.objExists('seqSoundtrack'): cmds.delete('seqSoundtrack')
            ret = mel.eval('doSoundImportArgList ("1", {"'+SOUND_ROOT+'/'+PRJ_NAME+'/'+episodeName+'/SQ'+str(soundName)+'.wav'+'","101.0"});')
            cmds.rename(ret, 'seqSoundtrack')
        return

shotSetupCls()