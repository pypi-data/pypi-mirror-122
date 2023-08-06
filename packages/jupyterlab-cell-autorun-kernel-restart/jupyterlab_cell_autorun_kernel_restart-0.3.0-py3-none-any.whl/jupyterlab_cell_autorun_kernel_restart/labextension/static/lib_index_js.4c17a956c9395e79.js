"use strict";
(self["webpackChunkjupyterlab_cell_autorun_kernel_restart"] = self["webpackChunkjupyterlab_cell_autorun_kernel_restart"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);




//import { ConnectionStatus } from '@jupyterlab/services/lib/kernel/kernel';
//import { LabIcon } from '@jupyterlab/ui-components'

//import reinit from '../style/icons/reinit.svg';
//const reinit_icon = new LabIcon({name: 'test', svgstr: reinit})
const verbose = true;
class ReInit {
    constructor(app, nbtracker, mainmenu) {
        this.command_id_new_empty_scene = 'cell-autorun-kernel-restart:new-scene';
        this.command_id_duplicate_scene = 'cell-autorun-kernel-restart:duplicate-scene';
        this.command_id_rename_scene = 'cell-autorun-kernel-restart:rename-scene';
        this.command_id_delete_scene = 'cell-autorun-kernel-restart:delete-scene';
        this.command_id_toggle_init_cell = 'cell-autorun-kernel-restart:toggle-initcell';
        this.command_id_do_reinit = 'cell-autorun-kernel-restart:do-reinit';
        if (verbose)
            console.log('Called constructor of ReInit');
        this.app = app;
        this.nbtracker = nbtracker;
        this.mainmenu = mainmenu;
        this.submenu = null;
    }
    initialize() {
        this.setupGlobalCommands();
        this.setupReinitMenu();
        // connect some callbacks
        this.nbtracker.widgetAdded.connect((sender, nbpanel) => { this.onNotebookTabAdded(nbpanel); });
        this.nbtracker.currentChanged.connect((sender, nbpanel) => { this.onActiveNotebookChanged(nbpanel); });
    }
    /** ****************************************************************************************************************************************
     * Internal Helper Methods
     */
    // **** setup helpers **********************************************************************************************************************
    setupReinitMenu() {
        const reinit_menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Menu({ commands: this.app.commands });
        reinit_menu.title.label = 'ReInit';
        reinit_menu.addItem({ command: this.command_id_do_reinit });
        reinit_menu.addItem({ command: this.command_id_toggle_init_cell });
        reinit_menu.addItem({ type: 'separator' });
        reinit_menu.addItem({ command: this.command_id_new_empty_scene });
        reinit_menu.addItem({ command: this.command_id_duplicate_scene });
        reinit_menu.addItem({ command: this.command_id_rename_scene });
        reinit_menu.addItem({ command: this.command_id_delete_scene });
        reinit_menu.addItem({ type: 'separator' });
        this.submenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Menu({ commands: this.app.commands });
        reinit_menu.addItem({ type: 'submenu', submenu: this.submenu });
        this.mainmenu.addMenu(reinit_menu);
        this.updateSceneMenu();
    }
    setupGlobalCommands() {
        // setup all commands this.command_id_* including key bindings
        this.app.commands.addCommand(this.command_id_do_reinit, {
            label: 'Restart kernel and launch init cells',
            execute: () => { this.doReInit(); }
        });
        this.app.commands.addKeyBinding({
            command: this.command_id_do_reinit,
            args: {},
            keys: ['Accel 0', 'Accel 0'],
            selector: '.jp-Notebook'
        });
        this.app.commands.addCommand(this.command_id_toggle_init_cell, {
            label: 'Toggle Init Cell',
            execute: () => { this.toggleInitCell(); }
        });
        this.app.commands.addKeyBinding({
            command: this.command_id_toggle_init_cell,
            args: {},
            keys: ['Accel I'],
            selector: '.jp-Notebook'
        });
        this.app.commands.addCommand(this.command_id_new_empty_scene, {
            label: 'New empty Scene',
            execute: () => { this.newEmptyScene(); }
        });
        this.app.commands.addCommand(this.command_id_duplicate_scene, {
            label: 'Duplicate Present Scene',
            execute: () => { this.duplicatePresentScene(); }
        });
        this.app.commands.addCommand(this.command_id_rename_scene, {
            label: 'Rename Present Scene',
            execute: () => { this.renamePresentScene(); }
        });
        this.app.commands.addCommand(this.command_id_delete_scene, {
            label: 'Delete Present Scene',
            execute: () => { this.deletePresentScene(); }
        });
    }
    // **** access to ReInit metadata **********************************************************************************************************
    // TODO: some initialization/update widget problem???
    addDefaultReinitDataCellIfNotPresent(nbpanel) {
        if (nbpanel.content.model) {
            const cell0 = nbpanel.content.widgets[0];
            if (!cell0 || !cell0.model.metadata.get('reinit_data')) {
                if (verbose)
                    console.log('Adding default ReInit Data Cell');
                var reinit_cell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CellModel({
                    cell: { cell_type: 'raw', source: ['ReInit Data Cell'], metadata: { reinit_data: true, scenes: ['Default Scene'], present_scene: 'Default Scene' } }
                });
                nbpanel.content.model.cells.insert(0, reinit_cell);
                nbpanel.content.update(); // doesn't seem to help
            }
        }
        else {
            console.error('Could not add default ReInit Data Cell');
        }
    }
    getCurrentNotebookReinitDataCell() {
        var _a;
        if (verbose)
            console.log('getCurrentNotebookReinitDataCell', (_a = this.nbtracker.currentWidget) === null || _a === void 0 ? void 0 : _a.context.path);
        const nbpanel = this.nbtracker.currentWidget;
        if (!nbpanel)
            return null;
        let datacell = nbpanel.content.widgets[0];
        if (!datacell.model.metadata.get('reinit_data')) {
            console.error('inconsistent reinit data');
            return null;
        }
        return datacell;
    }
    getCurrentNotebookSceneList() {
        const datacell = this.getCurrentNotebookReinitDataCell();
        if (!datacell)
            return null;
        return datacell.model.metadata.get('scenes');
    }
    getCurrentNotebookPresentScene() {
        var _a;
        const datacell = this.getCurrentNotebookReinitDataCell();
        if (!datacell)
            return null;
        const scene_list = this.getCurrentNotebookSceneList();
        if (scene_list == null || scene_list.length == 0) {
            console.error('scene_list is empty');
            return null;
        }
        const present_scene = (_a = datacell.model.metadata.get('present_scene')) === null || _a === void 0 ? void 0 : _a.toString();
        if (!present_scene) {
            return scene_list[0];
        }
        else {
            return present_scene;
        }
    }
    setCurrentNotebookPresentScene(scene_name) {
        const datacell = this.getCurrentNotebookReinitDataCell();
        if (!datacell)
            return;
        const scene_list = this.getCurrentNotebookSceneList();
        if (scene_list == null || scene_list.length == 0) {
            console.error('scene_list is empty');
            return;
        }
        if (!scene_list.includes(scene_name)) {
            console.error('scene not in scene_list');
        }
        datacell.model.metadata.set('present_scene', scene_name);
    }
    setCurrentNotebookSceneList(scene_list) {
        const datacell = this.getCurrentNotebookReinitDataCell();
        if (!datacell)
            return;
        datacell.model.metadata.set('scenes', scene_list);
    }
    // **** various ****************************************************************************************************************************
    updateSceneMenu() {
        if (!this.submenu)
            return;
        this.submenu.title.label = 'Present Scene: <none>';
        this.submenu.clearItems();
        const scene_list = this.getCurrentNotebookSceneList();
        const present_scene = this.getCurrentNotebookPresentScene();
        if (scene_list == null)
            return;
        this.submenu.title.label = 'Present Scene: ' + present_scene;
        for (const scene_name of scene_list) {
            const command_id = this.ensureSceneActivationCommandExistsAndReturnCommandId(scene_name);
            this.submenu.addItem({ command: command_id });
        }
    }
    ensureSceneActivationCommandExistsAndReturnCommandId(scene) {
        const command_id = 'init_scene_activate__' + scene;
        if (!this.app.commands.hasCommand(command_id)) {
            this.app.commands.addCommand(command_id, {
                label: scene,
                isToggled: () => { return scene == this.getCurrentNotebookPresentScene(); },
                execute: () => {
                    this.setCurrentNotebookPresentScene(scene);
                    this.updateInitCellDots();
                    this.updateSceneMenu();
                }
            });
        }
        return command_id;
    }
    updateInitCellDots() {
        const nbpanel = this.nbtracker.currentWidget;
        if (!nbpanel)
            return;
        const present_scene = this.getCurrentNotebookPresentScene();
        const md_tag_ext = 'init_scene__' + present_scene;
        const notebook = nbpanel.content;
        notebook.widgets.map((cell) => {
            if (!!cell.model.metadata.get(md_tag_ext)) {
                cell.addClass('cell-autorun-kernel-restart-enabled');
            }
            else {
                cell.removeClass('cell-autorun-kernel-restart-enabled');
            }
        });
    }
    /** ****************************************************************************************************************************************
     * Callbacks
     */
    // **** handle own commands ****************************************************************************************************************
    doReInit() {
    }
    toggleInitCell() {
        if (verbose)
            console.log('Toggle Init Cell');
        const cell = this.nbtracker.activeCell;
        if (!cell)
            return;
        const present_scene = this.getCurrentNotebookPresentScene();
        const md_tag_ext = 'init_scene__' + present_scene;
        if (!cell.model.metadata.get(md_tag_ext)) {
            cell.model.metadata.set(md_tag_ext, true);
            cell.addClass('cell-autorun-kernel-restart-enabled');
        }
        else {
            cell.model.metadata.delete(md_tag_ext);
            cell.removeClass('cell-autorun-kernel-restart-enabled');
        }
    }
    newEmptyScene() {
        if (verbose)
            console.log('Generating new empty scene');
        const old_scene_list = this.getCurrentNotebookSceneList();
        if (!old_scene_list)
            return;
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({ title: 'Name of the new scene:' }).then(new_scene => {
            if (!new_scene.value)
                return;
            const new_scene_list = Object.assign([], old_scene_list); // copy old_scene_list over
            new_scene_list.push(new_scene.value);
            this.setCurrentNotebookSceneList(new_scene_list);
            this.setCurrentNotebookPresentScene(new_scene.value);
            this.updateSceneMenu();
            this.updateInitCellDots();
        });
    }
    duplicatePresentScene() {
        if (verbose)
            console.log('Duplicating present scene');
        const present_scene = this.getCurrentNotebookPresentScene();
        if (!present_scene)
            return;
        const old_scene_list = this.getCurrentNotebookSceneList();
        if (!old_scene_list)
            return;
        const nbpanel = this.nbtracker.currentWidget;
        if (!nbpanel)
            return;
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({ title: 'Name of the new scene:' }).then(new_scene => {
            if (!new_scene.value)
                return;
            // TODO: make sure new scene is not in old scene list
            const new_scene_list = Object.assign([], old_scene_list); // copy old_scene_list over
            new_scene_list.push(new_scene.value);
            this.setCurrentNotebookSceneList(new_scene_list);
            // set the init_scene__* tags for the new scene
            const md_tag_old = 'init_scene__' + present_scene;
            const md_tag_new = 'init_scene__' + new_scene.value;
            const notebook = nbpanel.content;
            notebook.widgets.map((cell) => {
                if (!!cell.model.metadata.get(md_tag_old)) {
                    cell.model.metadata.set(md_tag_new, true);
                }
            });
            this.setCurrentNotebookPresentScene(new_scene.value);
            this.updateSceneMenu();
            this.updateInitCellDots();
        });
    }
    renamePresentScene() {
        if (verbose)
            console.log('Renaming present scene');
        const present_scene = this.getCurrentNotebookPresentScene();
        if (!present_scene)
            return;
        const old_scene_list = this.getCurrentNotebookSceneList();
        if (!old_scene_list)
            return;
        const nbpanel = this.nbtracker.currentWidget;
        if (!nbpanel)
            return;
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({ title: 'New name of the scene:' }).then(new_scene_name => {
            if (!new_scene_name.value)
                return;
            const new_scene_list = [];
            for (let scene of old_scene_list) {
                if (scene != present_scene) {
                    new_scene_list.push(scene);
                }
                else {
                    new_scene_list.push(new_scene_name.value);
                }
            }
            this.setCurrentNotebookSceneList(new_scene_list);
            const md_tag_old = 'init_scene__' + present_scene;
            const md_tag_new = 'init_scene__' + new_scene_name.value;
            const notebook = nbpanel.content;
            notebook.widgets.map((cell) => {
                if (!!cell.model.metadata.get(md_tag_old)) {
                    cell.model.metadata.set(md_tag_new, true);
                }
                cell.model.metadata.delete(md_tag_old);
            });
            this.setCurrentNotebookPresentScene(new_scene_name.value);
            this.updateSceneMenu();
            this.updateInitCellDots();
        });
    }
    deletePresentScene() {
        if (verbose)
            console.log('Deleting present scene');
        const present_scene = this.getCurrentNotebookPresentScene();
        if (!present_scene)
            return;
        const old_scene_list = this.getCurrentNotebookSceneList();
        if (!old_scene_list)
            return;
        if (old_scene_list.length == 1) {
            console.log('cannot delete the last scene');
            return;
        }
        const nbpanel = this.nbtracker.currentWidget;
        if (!nbpanel)
            return;
        const new_scene_list = [];
        for (let scene of old_scene_list) {
            if (scene != present_scene) {
                new_scene_list.push(scene);
            }
        }
        this.setCurrentNotebookSceneList(new_scene_list);
        const md_tag_old = 'init_scene__' + present_scene;
        const notebook = nbpanel.content;
        notebook.widgets.map((cell) => {
            cell.model.metadata.delete(md_tag_old);
        });
        this.setCurrentNotebookPresentScene(new_scene_list[0]);
        this.updateSceneMenu();
        this.updateInitCellDots();
    }
    // **** react to jupyterlab UI events ******************************************************************************************************
    onNotebookTabAdded(nbpanel) {
        // this is called whenever a new tab for a notebook is opened (includes a new view)
        if (verbose)
            console.log('Got new notebook tab for path:', nbpanel.context.path);
        nbpanel.context.sessionContext.ready.then(() => { this.onAllCellsInNotebookReady(nbpanel); });
    }
    onActiveNotebookChanged(nbpanel) {
        if (!nbpanel)
            return;
        if (verbose)
            console.log('Changed active notebook tab:', nbpanel.context.path);
        if (!nbpanel.context.sessionContext.isReady) {
            if (verbose)
                console.log('Notebook not ready yet:', nbpanel.context.path);
            return;
        }
        this.updateSceneMenu();
        this.updateInitCellDots();
    }
    onAllCellsInNotebookReady(nbpanel) {
        if (verbose)
            console.log('All cells ready:', nbpanel.context.path);
        this.addDefaultReinitDataCellIfNotPresent(nbpanel);
        this.updateInitCellDots();
    }
}
/*

class KernelReInitButton extends ToolbarButton {

  app: JupyterFrontEnd;
  nbtracker: INotebookTracker;
  mainmenu: IMainMenu;
  submenu: Menu | null;

  kernel_status_listener_connected: boolean;
  init_on_connect_stage: 'ignore reconnect' | 0 | 1;

  constructor(app: JupyterFrontEnd, nbtracker: INotebookTracker, mainmenu: IMainMenu) {
    super({onClick: () => { this.onReInitButtonClicked(); }, icon: reinit_icon, tooltip: 'Restart kernel and launch init cells'});

    this.kernel_status_listener_connected = false;

    this.init_on_connect_stage = 'ignore reconnect';
  }

  attach(nbpanel: NotebookPanel) {
    return
    const toolbar = nbpanel.toolbar;
    let insertionPoint = 7;

    toolbar.insertItem(insertionPoint + 1, 'reinit_button', this);

    this.setupContextMenu();
    this.setupRestartCommand();
    this.setupMainMenu();

    nbpanel.context.sessionContext.ready.then(() => { this.onAllCellsInNotebookReady(nbpanel); });
  }

  private setReinitDataCellStyle(nbpanel: NotebookPanel) {
      this.getReinitDataCell(nbpanel).hide();
  }

  private deletePresentScene() {
    const nbpanel = this.nbtracker.currentWidget;
    if(nbpanel) {

      const present_scene = this.getPresentScene(nbpanel);

      const old_scene_list = this.getReinitDataCell(nbpanel).model.metadata.get('scenes');
      const new_scene_list: string[] = [];
      for(let scene of old_scene_list as string[]) {
        if(scene != present_scene) {
          new_scene_list.push(scene);
        }
      }
      this.getReinitDataCell(nbpanel).model.metadata.set('scenes', new_scene_list);

      const md_tag_old = 'init_scene__' + present_scene;
      const notebook = nbpanel.content;
      notebook.widgets.map((cell: Cell) => {
        if(!!cell.model.metadata.get(md_tag_old)) {
          cell.model.metadata.delete(md_tag_old);
        } else {
          cell.model.metadata.delete(md_tag_old);
        }
      });

      this.updateScenesInMenu(nbpanel);
    }
  }

  private setupContextMenu() {

    const command_id = 'cell-autorun-kernel-restart:toggle-autorun';

    this.app.contextMenu.addItem({
      command: command_id,
      selector: '.jp-Cell',
      rank: 501
    });
  }

 

  private async doKernelInitialization() {

    const md_tag = 'init_scene__';
    
    if(this.nbtracker.currentWidget) {
      const present_scene = this.getPresentScene(this.nbtracker.currentWidget);
      const md_tag_ext = md_tag + present_scene;
      console.log('executing all cell with tag', md_tag_ext)

      const notebook = this.nbtracker.currentWidget.content;
      const notebookPanel = this.nbtracker.currentWidget;

      notebook.widgets.map((cell: Cell) => {

        if(!!cell.model.metadata.get(md_tag_ext)) {
          if(cell.model.type == 'code') {
            CodeCell.execute(cell as CodeCell, notebookPanel.sessionContext);
          }
        }

      });
    }
  }

  

 

  onAllCellsInNotebookReady(nbpanel: NotebookPanel) {
    this.addDefaultReinitDataCellIfNotPresent(nbpanel);
    this.setReinitDataCellStyle(nbpanel);
    this.updateScenesInMenu(nbpanel);

    this.setCellStyles(nbpanel);
  }

  onReInitButtonClicked() {

    if(!this.kernel_status_listener_connected) {
      this.nbtracker.currentWidget?.context.sessionContext.session?.kernel?.connectionStatusChanged.connect((_unused, conn_stat) => {
        this.kernelConnectionStatusListener(conn_stat);
      });
      this.kernel_status_listener_connected = true;
    }
    this.init_on_connect_stage = 0;
    this.nbtracker.currentWidget?.context.sessionContext.session?.kernel?.restart();
  }

  kernelConnectionStatusListener(conn_stat: ConnectionStatus) {
    
    if(this.init_on_connect_stage == 'ignore reconnect') {
      return;
    }

    if(this.init_on_connect_stage == 0 && conn_stat == 'connecting') {
      this.init_on_connect_stage = 1;
      return;
    }

    if(this.init_on_connect_stage == 1 && conn_stat == 'connected') {
      this.doKernelInitialization();
      this.init_on_connect_stage = 'ignore reconnect';
      return;
    }
  }
}

*/
/**
 * Initialization data for the jupyterlab_cell_autorun_kernel_restart extension.
 */
const plugin = {
    id: 'cell-autorun-kernel-restart',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__.IMainMenu],
    activate: (app, nbtracker_, mainmenu) => {
        const reinit_obj = new ReInit(app, nbtracker_, mainmenu);
        reinit_obj.initialize();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4c17a956c9395e79.js.map