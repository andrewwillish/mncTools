__author__ = 'Andrewwillish'

import maya.cmds as cmds
import os, imp, sys
import maya.mel as mel

#Determining root path
rootPathVar = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

#module launcher
def moduleLauncher(name,path):
    imp.load_compiled(name, path) if path.endswith('.pyc') is True else imp.load_source(name,path)
    return

#launch studioLibrary
def animlib(*args):
    import studioLibrary
    studioLibrary.main()
    return

#get main window name
mainWindow = mel.eval('$temp1=$gMainWindow')

#build menu tree
try:
    cmds.menu('m_mncTools',l='MNC Tools', tearOff=True,p=mainWindow)
except:
    pass

cmds.menuItem('scenePrep', l='Scene Preparation', p='m_mncTools', subMenu=True)
cmds.menuItem('sceneSetup',l='Scene Information Setup',p='scenePrep', \
              c=lambda*args: moduleLauncher('shotSetup',rootPathVar+'/mncToolsLaySceneSetup.pyc'))
cmds.menuItem('sceneBuilder',l='Scene Builder',p='scenePrep', \
              c=lambda*args: moduleLauncher('shotBuilder',rootPathVar+'/mncToolsLaySceneBuilder.pyc'))
cmds.menuItem('cameraGenerator',l='Camera Generator',p='scenePrep', \
              c=lambda*args: moduleLauncher('shotBuilder',rootPathVar+'/mncToolsLayCameraGenerator.pyc'))
cmds.menuItem('sceneInformation',l='Scene Information',p='scenePrep', \
              c=lambda*args: moduleLauncher('shotBuilder',rootPathVar+'/mncToolsLaySceneInfoViewer.pyc'))


cmds.menuItem('assetCreation', l='Asset Creation', p='m_mncTools', subMenu=True)
cmds.menuItem('setGroupManager',l='Set Group Manager',p='assetCreation', \
              c=lambda*args: moduleLauncher('setGroupManager',rootPathVar+'/mncToolsAssetSetGroupManager.pyc'))
cmds.menuItem('blindDataDeleter',l='Blind Data Node Deleter',p='assetCreation', \
              c=lambda*args: moduleLauncher('blindDataDeleter',rootPathVar+'/mncToolsAssetBlindDataDeleter.pyc'))
cmds.menuItem('assetImporter',l='Asset Importer',p='assetCreation', \
              c=lambda*args: moduleLauncher('assetImporter',rootPathVar+'/mncToolsAssetAssetImporter.pyc'))
cmds.menuItem('searchNode',l='Search Node',p='assetCreation', \
              c=lambda*args: moduleLauncher('searchNode',rootPathVar+'/mncToolsAssetNodeSearch.pyc'))
cmds.menuItem('subdivMan',l='Subdivision Manager',p='assetCreation', \
              c=lambda*args: moduleLauncher('subdivMan',rootPathVar+'/mncToolsAssetSubdivManager.pyc'))


cmds.menuItem('animationTools', l='Animation', p='m_mncTools', subMenu=True)
cmds.menuItem('tempGenerator',l='Temp Generator',p='animationTools', \
              c=lambda*args: moduleLauncher('tempGenerator',rootPathVar+'/mncToolsAnimTempGenerator.pyc'))
cmds.menuItem('nullGenerator',l='Null Generator',p='animationTools', \
              c=lambda*args: moduleLauncher('nullGenerator',rootPathVar+'/mncToolsAnimNullGenerator.pyc'))
cmds.menuItem('frameCountKiller',l='Frame Counter Killer',p='animationTools', \
              c=lambda*args: moduleLauncher('frameCountKiller',rootPathVar+'/mncToolsAnimFrameCounterKiller.pyc'))
cmds.menuItem(divider=True, p='animationTools')
cmds.menuItem('synGen', l='Synoptic Generator', p='animationTools', subMenu=True)
cmds.menuItem('synopticGeneratores',l='Synoptic Generator',p='synGen', \
              c=lambda*args: moduleLauncher('synopticGenerator',rootPathVar+'/mncToolsSynGenGenerator.pyc'))
cmds.menuItem('synopticServerLauncher',l='Synoptic Launcher Server',p='synGen', \
              c=lambda*args: moduleLauncher('synopticServerLauncher',rootPathVar+'/mncToolsSynGenLauncher.pyc'))
cmds.menuItem('synopticLocalLauncher',l='Synoptic Launcher Local',p='synGen', \
              c=lambda*args: moduleLauncher('synopticLocalLauncher',rootPathVar+'/mncToolsSynGenLauncherLocal.pyc'))
cmds.menuItem(divider=True, p='animationTools')
cmds.menuItem('sutdioLibrary',l='Studio Library',p='animationTools', \
              c=animlib)
cmds.menuItem(divider=True, p='animationTools')

cmds.menuItem(divider=True, p='m_mncTools')