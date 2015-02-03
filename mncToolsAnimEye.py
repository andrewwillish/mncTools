#MNCA EYE TOOLS
#Andrew Willis [MNCA]

import maya.cmds as cmds
import os, random
import xml.etree.cElementTree as ET

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
WIN_ROOT = os.environ['ProgramFiles'][:2]+'/'

#create eyeConfig.xml if not exists
if not os.path.isfile(SCRIPT_ROOT+'/xml/eyeConfig.xml'):
    root = ET.Element('root')
    writ = ET.SubElement(root, 'rUpEyeSuffix')
    writ.text = ''
    writ = ET.SubElement(root, 'lUpEyeSuffix')
    writ.text = ''
    writ = ET.SubElement(root, 'rLoEyeSuffix')
    writ.text = ''
    writ = ET.SubElement(root, 'lLoEyeSuffix')
    writ.text = ''
    writ = ET.SubElement(root, 'rEyeDirection')
    writ.text = ''
    writ = ET.SubElement(root, 'lEyeDirection')
    writ.text = ''
    tree = ET.ElementTree(root)
    tree.write(SCRIPT_ROOT+'/xml/eyeConfig.xml')

serverCache = SCRIPT_ROOT+'/library/blinkLib'
if not os.path.isdir(serverCache): os.makedirs(serverCache)

class EYETOOLScls:
    def __init__(self):
        if cmds.window('mncAnimEyeTools', exists=True):cmds.deleteUI('mncAnimEyeTools', wnd=True)

        win = cmds.window(t='Eye Tools',s=False,w=200)
        cmds.renameUI(win, 'mncAnimEyeTools')
        cmas = cmds.columnLayout(adj=True)

        suffixFrame = cmds.frameLayout(l='Suffixes')
        anc = cmds.columnLayout(adj=True, p=suffixFrame)
        cmds.rowColumnLayout(nc=2, cw=[(1,100), (2,100)])
        cmds.text(l='R. Eye Up Suffix:', fn='boldLabelFont', bgc=[1,1,0])
        cmds.text(l='L. Eye Up Suffix:', fn='boldLabelFont', bgc=[0,1,1])
        cmds.text('rightEyeUpSuffix', l='')
        cmds.text('leftEyeUpSuffix', l='')
        cmds.text(l='R. Eye Lo Suffix:', fn='boldLabelFont', bgc=[1,1,0])
        cmds.text(l='L. Eye Lo Suffix:', fn='boldLabelFont', bgc=[0,1,1])
        cmds.text('rightEyeLoSuffix', l='')
        cmds.text('leftEyeLoSuffix', l='')
        cmds.separator()
        cmds.separator()
        cmds.button(l='SET R.EYE UP', c=lambda*args: self.setSuffix(rightEyeUp=True))
        cmds.button(l='SET L.EYE UP', c=lambda*args: self.setSuffix(leftEyeUp=True))
        cmds.button(l='SET R.EYE LO', c=lambda*args: self.setSuffix(rightEyeLo=True))
        cmds.button(l='SET L.EYE LO', c=lambda*args: self.setSuffix(leftEyeLo=True))

        cmds.separator(p=anc)
        cmds.text(l='Eye Dir Suffix:', fn='boldLabelFont', p=anc, bgc=[0, 1, 0])
        cmds.text('eyeDirControl', l='', p=anc)
        cmds.button(l='SET RIGHT DIRECTION EYE CONTROLLER', c=lambda*args: self.setSuffix(rDirEye=True), p=anc)
        cmds.button(l='SET LEFT DIRECTION EYE CONTROLLER', c=lambda*args: self.setSuffix(lDirEye=True), p=anc)

        namespaceFrame = cmds.frameLayout(l='Namespace', p=cmas)
        cmds.columnLayout(adj=True)
        cmds.text('namespaceText', l='n/a')
        cmds.separator()
        cmds.button(l='SET NAMESPACE', c=self.setNamespace)
        
        TABS = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, p=cmas)
        
        child1 = cmds.columnLayout(adj=True,w=200)
        
        f1=cmds.frameLayout(l='BLINK LIBRARY')
        fc1=cmds.columnLayout(adj=True)
        cmds.textScrollList('blinkLib', p=fc1,h=225)
        for chk in os.listdir(serverCache):
            if chk.endswith('.blf')==True:
                cmds.textScrollList('blinkLib',e=True,a=chk[:-4])
        cmds.popupMenu(p='blinkLib')
        cmds.menuItem(l='Export/Update Blink',c=self.EXPORTBLINKfn)
        cmds.menuItem(l='Rename Blink',c=self.RENAMEBLINKfn)
        cmds.menuItem(l='Delete Blink',c=self.DELETEBLINKfn)    
        
        f11=cmds.frameLayout(l='SINGLE BLINK')
        cmds.button(l='APPLY SINGLE BLINK',h=40,bgc=[1.0,0.643835616566,0.0],c=self.EYEBLINKfn)
        
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        child2=cmds.columnLayout()
        
        cf1=cmds.frameLayout(l='DARTS SETTINGS')
        cfc2=cmds.columnLayout(adj=True,w=200)
        cmds.text(l='Dart Movement Range:',fn='boldLabelFont')
        cmds.separator()
        cmds.textField('dartMoveTextField',tx='0.1',cc=lambda*args:self.TEXTDEFAULT1fn(cmds.textField('dartMoveTextField',q=True,tx=True)))
        cmds.text(l='',h=3)
        cmds.text(l='Between Dart Max Range (Auto):',fn='boldLabelFont')
        cmds.separator()
        cmds.textField('dartMaxRanTextField', tx='5',cc=lambda*args:self.TEXTDEFAULT2fn(cmds.textField('dartMaxRanTextField',q=True,tx=True)))
        cmds.text(l='',h=3)     
        cmds.text(l='Maximum Dart Range (Auto):',fn='boldLabelFont')
        cmds.separator()
        cmds.textField('dartLimitRangeTextField', tx='1',cc=lambda*args:self.TEXTDEFAULT2fn(cmds.textField('dartLimitRangeTextField',q=True,tx=True)))
        cmds.text(l='',h=3)             
        
        cf2=cmds.frameLayout(l='GENERATE SINGLE DART',p=child2)
        cmds.columnLayout(adj=True)
        cmds.button(l='GENERATE SINGLE DART',w=200,bgc=[1.0,0.643835616566,0.0],h=40,c=self.SINGLEDARTfn)
        
        cf3=cmds.frameLayout(l='AUTODART',p=child2)
        cfc3=cmds.columnLayout(adj=True,w=200)
        cmds.text(l='Range:',fn='boldLabelFont')
        cmds.separator()
        cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 98),(2,2) ,(3, 98)],p=cfc3)
        cmds.textField('startDartRange', pht='n/a',tx='0.0',cc=lambda*args:self.TEXTDEFAULT4fn(cmds.textField('startDartRange',q=True,tx=True)))
        cmds.popupMenu(p='startDartRange')
        cmds.menuItem(l='Set Current Time as Start Range',c=lambda*args:self.SETRANGEfn('startDartRange'))
        cmds.text(l='')
        cmds.textField('endDartRange', pht='n/a',tx='0.0',cc=lambda*args:self.TEXTDEFAULT5fn(cmds.textField('endDartRange',q=True,tx=True)))
        cmds.popupMenu(p='endDartRange')
        cmds.menuItem(l='Set Current Time as End Range',c=lambda*args:self.SETRANGEfn('endDartRange'))
        
        cmds.text(l='',h=3,p=cfc3)
        cmds.separator(p=cfc3)
        cmds.button(l='RUN AUTODART',p=cfc3,h=40,bgc=[1.0,0.643835616566,0.0],c=self.AUTODARTfn)                
        cmds.setParent('..')
        
        cmds.tabLayout( TABS, edit=True, tabLabel=((child1, 'EYE BLINK'), (child2, 'EYE DART')) )
        cmds.showWindow()

        #populate
        tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
        root = tree.getroot()
        cmds.text('rightEyeUpSuffix', e=True, l=str(root[0].text))
        cmds.text('leftEyeUpSuffix', e=True, l=str(root[1].text))
        cmds.text('rightEyeLoSuffix', e=True, l=str(root[2].text))
        cmds.text('leftEyeLoSuffix', e=True, l=str(root[3].text))
        cmds.text('eyeDirControl', e=True, l=str(root[4].text)+'-'+str(root[5].text))
        return

    def setNamespace(self, *args):
        sel = cmds.ls(sl=True)
        if sel != []:
            selItem = sel[0]
            prefix = selItem[:selItem.find(':')]
            cmds.text('namespaceText', e=True, l=prefix)
        return

    def setSuffix(self, rightEyeUp = None, leftEyeUp = None, rightEyeLo = None, leftEyeLo = None, rDirEye = None, lDirEye = None):
        if len(cmds.ls(sl=True)) != 1:
            cmds.confirmDialog(icn='warning', t='Eye Tools', m='Single Object only.', button=['OK'])
        else:
            selItem = cmds.ls(sl=True)[0]
            selItem = selItem[selItem.find(':')+1:]
            tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
            root = tree.getroot()
            if rightEyeUp:
                root[0].text = selItem
            if leftEyeUp:
                root[1].text = selItem
            if rightEyeLo:
                root[2].text = selItem
            if leftEyeLo:
                root[3].text = selItem
            if rDirEye:
                root[4].text = selItem
            if lDirEye:
                root[5].text = selItem
            tree = ET.ElementTree(root)
            tree.write(SCRIPT_ROOT+'/xml/eyeConfig.xml')

            import mncToolsAnimEye
            reload (mncToolsAnimEye)
        return

    def TEXTDEFAULT1fn(self,text):
        if text=='':
            cmds.textField('dartMoveTextField',e=True,tx='0.1')
        elif float(text)>float(cmds.textField('dartLimitRangeTextField',q=True,tx=True))/2:
            cmds.confirmDialog(icon='warning',t='Error',m='Dart movement can not be more than half the maximum dart limit!',button=['Ok'])
            cmds.textField('dartMoveTextField',e=True,tx='0.1')
            cmds.error('CREDENTIAL ERROR')
        return
    
    def TEXTDEFAULT2fn(self,text):
        if text=='':
            cmds.textField('dartMaxRanTextField',e=True,tx='5')
        elif int(text)<5:
            cmds.textField('dartMaxRanTextField',e=True,tx='5')
        return    
    
    def TEXTDEFAULT3fn(self,text):
        if text=='':
            cmds.textField('dartLimitRangeTextField',e=True,tx='1')
        elif int(text)<1:
            cmds.textField('dartMaxRanTextField',e=True,tx='1')
        return        
    
    def TEXTDEFAULT4fn(self,text):
        if text=='':
            cmds.textField('startDartRange',e=True,tx='0.0')
        return      
    
    def TEXTDEFAULT5fn(self,text):
        if text=='':
            cmds.textField('endDartRange',e=True,tx='0.0')
        return              
    
    def AUTODARTfn(self,*args):
        namespace= cmds.text('namespaceText', q=True, l=True)
        if namespace == 'n/a':
            cmds.confirmDialog(icn='warning', t='Eye Tools', m='No Namespace selected.', button=['OK'])
            cmds.error('no namespace selected')

        #get current suffix
        tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
        root = tree.getroot()
        rUpBlinkControl = root[0].text
        rightEyeControl = root[4].text
        leftEyeControl = root[5].text

        try:
            sel=cmds.ls(sl=True)
            namespace=sel[0][:sel[0].find(':')]
            cmds.select(namespace+':'+rightEyeControl)
        except:
            cmds.confirmDialog(icon='warning',t='Error',m='Invalid character selection!', button=['Ok'])
            cmds.error('INVALID CHARACTER SELECTION')     
        
        if cmds.textField('startDartRange',q=True,tx=True)=='' or cmds.textField('endDartRange',q=True,tx=True)==''    :
            cmds.confirmDialog(icon='warning',t='Error',m='One of the scan range is empty!', button=['Ok'])
            cmds.error('SCAN RANGE EMPTY') 
        
        start= float(cmds.textField('startDartRange',q=True,tx=True))
        end=float(cmds.textField('endDartRange',q=True,tx=True))
        
        if end - start < 0:
            cmds.confirmDialog(icon='warning',t='Error',m='Negative scan range!', button=['Ok'])
            cmds.error('NEGATIVE SCAN RANGE')  
        elif end == start:
            cmds.confirmDialog(icon='warning',t='Error',m='Equal scan range!!', button=['Ok'])
            cmds.error('EQUAL SCAN RANGE')                                
        
        cnt = start
        while cnt < end:
            cmds.currentTime(cnt)

            eval1 = cnt
            eval2 = cmds.findKeyframe(namespace+':'+rUpBlinkControl,w='next')
            
            if eval2-eval1>5:
                max=cmds.getAttr(namespace+':'+rightEyeControl+'.tx')+float(cmds.textField('dartLimitRangeTextField',q=True,tx=True))
                while eval1<eval2:
                    cmds.currentTime(eval1)                    
                    cmds.currentTime(eval1+random.randint(5,int(cmds.textField('dartMaxRanTextField',q=True,tx=True))))
                    
                    if cmds.currentTime(q=True) > eval2:
                        break
                    
                    #DART PROCEEDINGS
                    affectedChan = random.sample(['tx','ty',''],2)
                    for chk in affectedChan:
                        if chk=='tx' or chk=='ty':
                            cmds.setKeyframe(namespace+':'+rightEyeControl, attribute=chk, t=[cmds.currentTime(q=True),cmds.currentTime(q=True)])
                            cmds.setKeyframe(namespace+':'+leftEyeControl, attribute=chk, t=[cmds.currentTime(q=True),cmds.currentTime(q=True)])
                            oldVal=cmds.getAttr(namespace+':'+leftEyeControl+'.'+chk)
                            
                            addOn=float(cmds.textField('dartMoveTextField',q=True,tx=True))*random.sample([1.0,-1.0],1)[0]
                            
                            newVal=oldVal+addOn
                            
                            #Limit Check
                            checker=newVal
                            if checker<0:
                                checker=checker*-1.0
                            if checker>max:
                                newVal=oldVal*(addOn*-1.0)
                            
                            cmds.setKeyframe(namespace+':'+rightEyeControl, attribute=chk, t=[cmds.currentTime(q=True)+1,cmds.currentTime(q=True)+1], v=newVal)
                            cmds.setKeyframe(namespace+':'+leftEyeControl, attribute=chk, t=[cmds.currentTime(q=True)+1,cmds.currentTime(q=True)+1], v=newVal)

                    eval1=cmds.currentTime(q=True)
                cnt=eval2
            elif cnt==eval2:
                eval1=cnt
                eval2=end
                
                if eval2-eval1>5:
                    while eval1<eval2:
                        cmds.currentTime(eval1)
                        cmds.currentTime(eval1+random.randint(5,int(cmds.textField('dartMaxRanTextField',q=True,tx=True))))
                        
                        #DART PROCEEDINGS
                        affectedChan=random.sample(['tx','ty',''],2)
                        for chk in affectedChan:
                            if chk=='tx' or chk=='ty':
                                cmds.setKeyframe(namespace+':'+rightEyeControl, attribute=chk, t=[cmds.currentTime(q=True),cmds.currentTime(q=True)])
                                cmds.setKeyframe(namespace+':'+leftEyeControl, attribute=chk, t=[cmds.currentTime(q=True),cmds.currentTime(q=True)])
                                oldVal=cmds.getAttr(namespace+':'+leftEyeControl+'.'+chk)
                                
                                addOn=float(cmds.textField('dartMoveTextField',q=True,tx=True))*random.sample([1.0,-1.0],1)[0]
                                
                                newVal=oldVal+addOn
                                
                                #Limit Check
                                checker=newVal
                                if checker<0:
                                    checker=checker*-1
                                if checker>max:
                                    newVal=newVal*-1
                                
                                cmds.setKeyframe(namespace+':'+rightEyeControl, attribute=chk, t=[cmds.currentTime(q=True)+1,cmds.currentTime(q=True)+1], v=newVal)
                                cmds.setKeyframe(namespace+':'+leftEyeControl, attribute=chk, t=[cmds.currentTime(q=True)+1,cmds.currentTime(q=True)+1], v=newVal)
    
                        eval1=cmds.currentTime(q=True)
                    break                    
                else:
                    break   
            else:
                cnt=eval2
        cmds.select([namespace+':'+rightEyeControl,namespace+':'+leftEyeControl])
        return
    
    def SINGLEDARTfn(self,*args):
        namespace= cmds.text('namespaceText', q=True, l=True)
        if namespace == 'n/a':
            cmds.confirmDialog(icn='warning', t='Eye Tools', m='No Namespace selected.', button=['OK'])
            cmds.error('no namespace selected')

        #get current suffix
        tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
        root = tree.getroot()
        rightEyeControl = root[4].text
        leftEyeControl = root[5].text

        try:
            sel=cmds.ls(sl=True)
            cmds.select(namespace+':'+rightEyeControl)
        except:
            cmds.confirmDialog(icon='warning',t='Error',m='Invalid character selection!', button=['Ok'])
            cmds.error('INVALID CHARACTER SELECTION')
        
        if cmds.textField('dartMoveTextField',q=True,tx=True)=='' or cmds.textField('dartMaxRanTextField',q=True,tx=True)=='':
            cmds.confirmDialog(icon='warning',t='Error',m='Insufficient credential to proceed!', button=['Ok'])
            cmds.error('INSUFFICIENT CREDENTIAL TO PROCEED')  
                      
        cmds.select([namespace+':'+rightEyeControl,namespace+':'+leftEyeControl])
        cmds.setKeyframe()
        cmds.currentTime(cmds.currentTime(q=True)+1)
        
        ATTRvar=random.sample(['tx','ty'],1)
        OPERANDvar=random.sample([1,-1],1)
        
        cmds.setAttr(namespace+':'+rightEyeControl+'.'+ATTRvar[0],float(cmds.getAttr(namespace+':'+rightEyeControl+'.'+ATTRvar[0]))+(float(cmds.textField('dartMoveTextField',q=True,tx=True))*OPERANDvar[0]))
        cmds.setAttr(namespace+':'+leftEyeControl+'.'+ATTRvar[0],float(cmds.getAttr(namespace+':'+leftEyeControl+'.'+ATTRvar[0]))+(float(cmds.textField('dartMoveTextField',q=True,tx=True))*OPERANDvar[0]))
        cmds.setKeyframe()
        return
    
    def SETRANGEfn(self,item):
        global blinkLib, THRESfltsld, THREStxtfld, TOtxtfld, TOintsld, BLINKTYPEtxtfld
        cmds.textField(item,e=True,tx=str(cmds.currentTime(q=True)))
        return
    
    def EYEBLINKfn(self,*args):
        global blinkLib

        namespace= cmds.text('namespaceText', q=True, l=True)
        if namespace == 'n/a':
            cmds.confirmDialog(icn='warning', t='Eye Tools', m='No Namespace selected.', button=['OK'])
            cmds.error('no namespace selected')

        #get current suffix
        tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
        root = tree.getroot()
        rightUpSuffix = root[0].text
        leftUpSuffix = root[1].text
        rightLoSuffix = root[2].text
        leftLoSuffix = root[3].text

        if cmds.textScrollList('blinkLib',q=True,si=True) is None:
            cmds.confirmDialog(icon='warning',t='Error',m='Please select blink to be applied!', button=['Ok'])
            cmds.error('SELECT BLINK TO BE APPLIED')

        try:
            cmds.select([namespace+':'+rightUpSuffix,namespace+':'+leftUpSuffix,namespace+':'+rightLoSuffix,namespace+':'+leftLoSuffix])
        except:
            cmds.confirmDialog(icon='warning',t='Error',m='Invalid character selection!', button=['Ok'])
            cmds.error('INVALID CHARACTER SELECTION')
        
        opn=open(serverCache+'/'+cmds.textScrollList('blinkLib',q=True,si=True)[0]+'.blf','r')
        INSTRUCTIONlis=opn.readlines()
        opn.close()
        
        cmds.select(namespace+':'+rightUpSuffix,namespace+':'+leftUpSuffix,namespace+':'+rightLoSuffix,namespace+':'+leftLoSuffix)
        cmds.setKeyframe()
        for chk in INSTRUCTIONlis:
            if chk=='\r\n':
                cmds.currentTime(cmds.currentTime(q=True)+1)
            else:
                ATTRIBUTElis=chk.split('\t')
                for chk in ATTRIBUTElis:
                    cmds.setAttr(namespace+chk[:chk.find('-')],float(chk[chk.find('-')+1:]))
                cmds.setKeyframe()
                cmds.currentTime(cmds.currentTime(q=True)+1)
        return
    
    def RENAMEBLINKfn(self,*args):
        global blinkLib
        if cmds.textScrollList('blinkLib',q=True,si=True) is None:
            cmds.confirmDialog(icon='warning',t='Error',m='Please select blink to be renamed!', button=['Ok'])
            cmds.error('SELECT BLINK TO BE RENAMED')
        
        if cmds.ls(sl=True) == []:
            cmds.confirmDialog(icon='warning',t='Error',m='Select character to apply the blink!', button=['Ok'])
            cmds.error('SELECT BLINK TO BE RENAMED')            
        
        input=cmds.promptDialog(title='New Name', message='Enter new name for the blink library:', button=['Ok', 'Cancel'])
        if input=='Cancel':
            cmds.error('CANCELLED BY USER')
        else:
            input=cmds.promptDialog(q=True,text=True)
            if input=='':
                cmds.error('NEW NAME CAN NOT BE BLANK')

        os.rename(serverCache+'/'+cmds.textScrollList('blinkLib',q=True,si=True)[0]+'.blf',serverCache+'/'+input+'.blf')

        cmds.textScrollList('blinkLib',e=True,ra=True)
        for chk in os.listdir(serverCache):
            if chk.endswith('.blf')==True:
                cmds.textScrollList('blinkLib',e=True,a=chk[:-4])
        return
    
    def DELETEBLINKfn(self,*args):
        global blinkLib
        if cmds.textScrollList('blinkLib',q=True,si=True)==None:
            cmds.confirmDialog(icon='warning',t='Error',m='Please select blink to be deleted!', button=['Ok'])
            cmds.error('SELECT BLINK TO BE DELETED')        
        
        repVar=cmds.confirmDialog(icon='question',title='Message', message='This will delete the blink exported?',button=['Yes','No'])
        if repVar=='No':
            cmds.error('CANCELLED BY USER') 
        
        os.remove(serverCache+'/'+cmds.textScrollList('blinkLib',q=True,si=True)[0]+'.blf')
        
        cmds.textScrollList('blinkLib',e=True,ra=True)
        for chk in os.listdir(serverCache):
            if chk.endswith('.blf')==True:
                cmds.textScrollList('blinkLib',e=True,a=chk[:-4])
        return
    
    def EXPORTBLINKfn(self,*args):
        global blinkLib
        #get current suffix
        tree = ET.parse(SCRIPT_ROOT+'/xml/eyeConfig.xml')
        root = tree.getroot()
        rightUpSuffix = root[0].text
        leftUpSuffix = root[1].text
        rightLoSuffix = root[2].text
        leftLoSuffix = root[3].text

        sel = cmds.ls(sl=True)
        if sel == []:
           cmds.confirmDialog(icon='warning',title='Error',message='No controller selected!',button=['Ok'])
           cmds.error('NO CONTROLLER SELECTED') 
           
        krg = cmds.timeControl('timeControl1',q=True,rng=True)
        krglen = len(krg)
        krgns = krg.find(':')
        strtkt = krg[1:krgns]
        start = int(strtkt)
        endkt = krg[krgns+1:krglen-1]
        end = int(endkt)
        end -= 1
        
        if end == start:
           cmds.confirmDialog(icon='warning',title='Error',message='Start time is the same as end range!',button=['Ok'])
           cmds.error('SAME START AND END RANGE')    
           
        #Writing procedure
        blinkName = cmds.promptDialog(title='Input', message='Input new name for blink library.',button=['Ok','Cancel'],cancelButton='Cancel' )
        if blinkName == 'Cancel':
            cmds.error('CANCELLED BY USER')
        elif blinkName == '':
            cmds.error('NAME CAN NOT BE BLANK')
        else:
            blinkName = cmds.promptDialog(q=True,text=True)
        
        if os.path.isfile(serverCache+'/'+blinkName+'.blk'):
            repVar=cmds.confirmDialog(icon='question',title='Message', message='There is a file with same name exist in server. Proceed?',button=['Yes','No'])
            if repVar=='No':
                cmds.error('CANCELLED BY USER')                 
        
        namespace = cmds.text('namespaceText', q=True, l=True)
        
        write=''
        
        cmds.currentTime(start)
        prog=start
        nextKey=cmds.findKeyframe(w='next')
        escape=''
        while prog<=end:
            cmds.select(namespace+':'+rightUpSuffix,namespace+':'+leftUpSuffix,namespace+':'+rightLoSuffix,namespace+':'+leftLoSuffix)
            prog=float(prog)
            if prog==nextKey:
                rUpBlink=str(cmds.getAttr(namespace+':'+rightUpSuffix+'.ty',asString=True))
                lUpBlink=str(cmds.getAttr(namespace+':'+leftUpSuffix+'.ty',asString=True))
                rLoBlink=str(cmds.getAttr(namespace+':'+rightLoSuffix+'.ty',asString=True))
                lLoBlink=str(cmds.getAttr(namespace+':'+leftLoSuffix+'.ty',asString=True))

                write=write+':'+rightUpSuffix+'.ty-'+rUpBlink+'\t'+':'+leftUpSuffix+'.ty-'+lUpBlink+'\t'+':'+rightLoSuffix+'.ty-'+rLoBlink+'\t'+':'+leftLoSuffix+'.ty-'+lLoBlink+'\r\n'
            else:
                write=write+'\r\n'
              
            nextKey=cmds.findKeyframe(w='next')
            if escape==prog:
                break
            escape=prog
            
            
            prog+=1
            cmds.currentTime(prog)

        opn=open(serverCache+'/'+blinkName+'.blf','w')
        opn.write(write)
        opn.close()
        cmds.textScrollList('blinkLib',e=True,ra=True)
        for chk in os.listdir(serverCache):
            if chk.endswith('.blf')==True:
                cmds.textScrollList('blinkLib',e=True,a=chk[:-4])
        cmds.confirmDialog(icon='information',title='Message', message='Blink exported.',button=['Ok'])
        return
    
EYETOOLScls()