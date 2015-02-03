__author__ = 'andrew.willis'

#import module
import maya.cmds as cmds

#License Parsing==========================================================================================
import licenseParsing
licenseParsing.licParse()

class assetNodeDeleter:
    def __init__(self):
        if cmds.window('assetNodeDeleter', exists=True):
            cmds.deleteUI('assetNodeDeleter', window=True)
        if cmds.window('progressBarWindow', exists=True):
            cmds.deleteUI('progressBarWindow', window=True)

        cmds.window('assetNodeDeleter',t='Asset Node Deleter',s=False,w=200)
        cmas=cmds.columnLayout(adj=True)

        cmds.button(l='DELETE blindDataTemplate',c=lambda*args:self.deleteMode(0),w=300)
        cmds.button(l='DELETE polyBlindData',c=lambda*args:self.deleteMode(1))
        cmds.button(l='DELETE hyperView',c=lambda*args:self.deleteMode(2))

        cmds.showWindow()
        return

    def deleteMode(self,mode):
        if mode==0:
            tempLis=[]
            for chk in cmds.ls(type='blindDataTemplate'):
                tempLis.append(chk)

            cmds.window('progressBarWindow',s=False)
            cmds.columnLayout(adj=True)
            cmds.progressBar('progressBar',maxValue=len(tempLis),w=500)
            cmds.showWindow()
            cnt=0
            for chk in tempLis:
                try:
                    cmds.delete(chk)
                except:
                    pass
                cnt+=1
                cmds.progressBar('progressBar',e=True,pr=cnt)

        elif mode==1:
            tempLis=[]
            for chk in cmds.ls(type='polyBlindData'):
                tempLis.append(chk)

            cmds.window('progressBarWindow',s=False)
            cmds.columnLayout(adj=True)
            cmds.progressBar('progressBar',maxValue=len(tempLis),w=500)
            cmds.showWindow()
            cnt=0
            for chk in tempLis:
                try:
                    cmds.delete(chk)
                except:
                    pass
                cnt+=1
                cmds.progressBar('progressBar',e=True,pr=cnt)
        elif mode==2:
            tempLis=[]
            for chk in cmds.ls():
                if chk.find('hyperView')!=-1:
                    tempLis.append(chk)
            cmds.window('progressBarWindow',s=False)
            cmds.columnLayout(adj=True)
            cmds.progressBar('progressBar',maxValue=len(tempLis),w=500)
            cmds.showWindow()
            cnt=0
            for chk in tempLis:
                try:
                    cmds.delete(chk)
                except:
                    pass
                cnt+=1
                cmds.progressBar('progressBar',e=True,pr=cnt)
        cmds.deleteUI('progressBarWindow', window=True)
        return

assetNodeDeleter()