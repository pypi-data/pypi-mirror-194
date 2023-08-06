import { ILabShell, JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IMainMenu } from '@jupyterlab/mainmenu';


import { ScenesSidebar } from './widget';

function activateScenes(app: JupyterFrontEnd, settingRegistry: ISettingRegistry, nbTracker: INotebookTracker, mainMenu: IMainMenu, labShell: ILabShell) {

  // create the ScenesSidebar widget
  const scenesSidebar = new ScenesSidebar(app, nbTracker, mainMenu, settingRegistry);
  app.shell.add(scenesSidebar, 'left', { rank: 1000 });
}

/**
 * Initialization data for the jupyterlab_scenes extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_scenes:plugin',
  autoStart: true,
  optional: [ISettingRegistry, INotebookTracker, IMainMenu, ILabShell],
  activate: activateScenes
};

export default plugin;
