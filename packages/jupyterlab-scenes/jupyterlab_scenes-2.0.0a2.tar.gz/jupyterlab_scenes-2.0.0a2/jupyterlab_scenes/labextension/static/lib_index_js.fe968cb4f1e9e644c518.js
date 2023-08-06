"use strict";
(self["webpackChunkjupyterlab_scenes"] = self["webpackChunkjupyterlab_scenes"] || []).push([["lib_index_js"],{

/***/ "./lib/backend.js":
/*!************************!*\
  !*** ./lib/backend.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NotebookHandler": () => (/* binding */ NotebookHandler)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);




const NB_METADATA_KEY = 'scenes_data';
const SCENE_CELL_CLASS = 'scene-cell';
class NotebookHandler {
    constructor(nbTracker, settingRegistry) {
        this.scenesChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        /* ****************************************************************************************************************************************
         * Handle kernel (re-)starts
         * ****************************************************************************************************************************************/
        this._kernelStatusDict = {};
        this._nbTracker = nbTracker;
        this._sceneDB = new NotebookSceneDatabase(nbTracker);
        this._enableLegacyInits = false;
        // load settings
        if (settingRegistry) {
            settingRegistry.load('jupyterlab_scenes:plugin').then(settings => {
                this.updateSettings(settings);
                settings.changed.connect(() => { this.updateSettings(settings); });
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab_scenes.', reason);
            });
        }
        this._setupKernelListener();
    }
    updateSettings(settings) {
        this._enableLegacyInits = settings.composite.legacyInit;
    }
    _setupKernelListener() {
        this._nbTracker.widgetAdded.connect(async (sender, nbPanel) => {
            nbPanel.context.sessionContext.ready.then(() => {
                this._kernelStatusDict[nbPanel.context.sessionContext.session.kernel.id] = 'connecting';
                nbPanel.context.sessionContext.session.kernel.connectionStatusChanged.connect((kernel, conn_stat) => { this._kernelListener(kernel, conn_stat); });
            });
        });
    }
    _kernelListener(kernel, conn_stat) {
        if (conn_stat == 'connecting') {
            this._kernelStatusDict[kernel.id] = 'connecting';
        }
        else if (conn_stat == 'connected') {
            if (this._kernelStatusDict[kernel.id] == 'connecting') {
                let notebookPanelList = [];
                this._nbTracker.forEach((nbPanel) => {
                    if (nbPanel.context.sessionContext.session.kernel.id == kernel.id) {
                        notebookPanelList.push(nbPanel);
                    }
                });
                if (notebookPanelList.length > 0) {
                    let init_scene = this._sceneDB.getInitScene();
                    if (init_scene)
                        this.runSceneInNotebook(notebookPanelList[0], init_scene);
                }
            }
            delete this._kernelStatusDict[kernel.id];
        }
    }
    /* ****************************************************************************************************************************************
     * Functionality provided to the main widget
     * ****************************************************************************************************************************************/
    // **** simple scene getters *************************************************
    getNotebookTitle() {
        return this._sceneDB.getNotebookTitle();
    }
    getScenesList() {
        return this._sceneDB.getScenesList();
    }
    getActiveScene(notebook = null) {
        return this._sceneDB.getActiveScene(notebook);
    }
    getInitScene() {
        return this._sceneDB.getInitScene();
    }
    // **** scene setters ********************************************************
    toggleInitScene(scene_name) {
        this._sceneDB.toggleInitScene(scene_name);
        this._scenesChanged();
    }
    setActiveScene(scene_name) {
        this._sceneDB.setActiveScene(scene_name);
        this._scenesChanged();
    }
    renameScene(old_scene_name, new_scene_name) {
        const scenes_list = this.getScenesList();
        if (scenes_list.includes(new_scene_name))
            return 'fail';
        if (this._sceneDB.getInitScene() == old_scene_name) {
            this._sceneDB.toggleInitScene(new_scene_name);
        }
        if (this._sceneDB.getActiveScene() == old_scene_name) {
            this._sceneDB.setActiveScene(new_scene_name);
        }
        let idx = scenes_list.lastIndexOf(old_scene_name);
        scenes_list[idx] = new_scene_name;
        this._sceneDB.setScenesList(scenes_list);
        this._renameSceneTagFromAllCells(this._nbTracker.currentWidget, old_scene_name, new_scene_name);
        this._scenesChanged();
        return 'success';
    }
    deleteScene(scene_name) {
        let scenes_list = this._sceneDB.getScenesList();
        if (scenes_list.length == 1)
            return;
        if (this._sceneDB.getInitScene() == scene_name) {
            this._sceneDB.toggleInitScene(scene_name);
        }
        let resetActiveScene = this._sceneDB.getActiveScene() == scene_name;
        this._removeSceneTagFromAllCells(this._nbTracker.currentWidget, scene_name);
        let idx = scenes_list.lastIndexOf(scene_name);
        scenes_list.splice(idx, 1);
        this._sceneDB.setScenesList(scenes_list);
        if (resetActiveScene) {
            if (idx < scenes_list.length) {
                this.setActiveScene(scenes_list[idx]);
            }
            else {
                this.setActiveScene(scenes_list[idx - 1]);
            }
        }
        this._scenesChanged();
    }
    toggleSceneMembershipOfSelectedCells() {
        if (!this._nbTracker.currentWidget)
            return;
        if (!this._nbTracker.activeCell)
            return;
        const current_scene = this._sceneDB.getActiveScene();
        const is_init_scene = current_scene == this.getInitScene();
        const tag = 'scene__' + current_scene;
        const notebook = this._nbTracker.currentWidget.content;
        const set_membership = !this._nbTracker.activeCell.model.getMetadata(tag);
        //const set_membership = !this._nbTracker.activeCell.model.getMetadata(tag);
        notebook.widgets.forEach((cell) => {
            if (!notebook.isSelectedOrActive(cell))
                return;
            if (cell.model.type != 'code')
                return;
            if (set_membership) {
                cell.model.setMetadata(tag, true);
                if (is_init_scene) {
                    cell.model.setMetadata('init_cell', true);
                }
            }
            else {
                cell.model.deleteMetadata(tag);
                if (is_init_scene) {
                    cell.model.deleteMetadata('init_cell');
                }
            }
            this._updateCellClassAndTags(cell, tag);
        });
    }
    // **** scene management and running *****************************************
    runActiveSceneInCurrentNotebook() {
        const active_scene = this._sceneDB.getActiveScene();
        if (active_scene)
            this.runSceneInCurrentNotebook(active_scene);
    }
    runSceneInCurrentNotebook(scene_name) {
        if (!this._nbTracker.currentWidget)
            return;
        const notebookPanel = this._nbTracker.currentWidget;
        this.runSceneInNotebook(notebookPanel, scene_name);
    }
    runSceneInNotebook(notebookPanel, scene_name) {
        const tag = this._getSceneTag(scene_name);
        notebookPanel.content.widgets.map((cell) => {
            if (!!cell.model.getMetadata(tag)) {
                if (cell.model.type == 'code') {
                    _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(cell, notebookPanel.sessionContext, { recordTiming: notebookPanel.content.notebookConfig.recordTiming });
                }
            }
        });
    }
    createNewEmptyScene(scene_name) {
        const scene_list = this.getScenesList();
        if (scene_list.includes(scene_name))
            return 'fail';
        scene_list.push(scene_name);
        this._sceneDB.setScenesList(scene_list);
        this._sceneDB.setActiveScene(scene_name);
        this._scenesChanged();
        return 'success';
    }
    duplicateActiveScene(new_scene_name) {
        let retval = this.createNewEmptyScene(new_scene_name);
        if (retval == 'fail')
            return 'fail';
        this._duplicateSceneTagInAllCells(this._nbTracker.currentWidget, this.getActiveScene(), new_scene_name);
        this._sceneDB.setActiveScene(new_scene_name);
        this._scenesChanged();
        return retval;
    }
    moveActiveSceneUp() {
        this._moveScene(this._sceneDB.getActiveScene(), 'up');
        this._scenesChanged();
    }
    moveActiveSceneDown() {
        this._moveScene(this._sceneDB.getActiveScene(), 'down');
        this._scenesChanged();
    }
    // **** various **************************************************************
    updateCellClassesAndTags(notebook, scene_name = null, cell = null) {
        // console.log('updating', scene_name)
        if (scene_name == null)
            scene_name = this.getActiveScene();
        const scene_tag = this._getSceneTag(scene_name);
        if (cell == null) {
            notebook.widgets.map((cell) => {
                this._updateCellClassAndTags(cell, scene_tag);
            });
        }
        else {
            this._updateCellClassAndTags(cell, scene_tag);
        }
    }
    jumpToNextSceneCell() {
        const presentCell = this._nbTracker.activeCell;
        if (!presentCell)
            return;
        const tag = this._getSceneTag(this.getActiveScene());
        const cells = this._nbTracker.currentWidget.content.widgets;
        let cellIdx = cells.indexOf(presentCell);
        let numCells = cells.length;
        for (let n = cellIdx + 1; n < numCells; n++) {
            let cell = cells[n];
            if (cell.model.getMetadata(tag)) {
                this._activateCellAndExpandParentHeadings(cell);
                break;
            }
        }
    }
    jumpToPreviousSceneCell() {
        const presentCell = this._nbTracker.activeCell;
        if (!presentCell)
            return;
        const tag = this._getSceneTag(this.getActiveScene());
        const cells = this._nbTracker.currentWidget.content.widgets;
        let cellIdx = cells.indexOf(presentCell);
        for (let n = cellIdx - 1; n >= 0; n--) {
            let cell = cells[n];
            if (cell.model.getMetadata(tag)) {
                this._activateCellAndExpandParentHeadings(cell);
                break;
            }
        }
    }
    importLegacyInitializationCells(notebook) {
        if (!this._enableLegacyInits)
            return;
        let init_scenes_consistent = true;
        let legacy_init_cells_exist = false;
        let init_scene = this.getInitScene();
        let init_scene_tag = (init_scene != null) ? this._getSceneTag(init_scene) : null;
        // find out if there are legacy init cells and, if so, whether they are consistent with the scenes init cell
        notebook.widgets.map((cell) => {
            let is_legacy_init_cell = !!cell.model.getMetadata('init_cell');
            let is_scenes_init_cell = init_scene_tag != null && !!cell.model.getMetadata(init_scene_tag);
            if (is_legacy_init_cell) {
                legacy_init_cells_exist = true;
            }
            if (is_legacy_init_cell != is_scenes_init_cell) {
                init_scenes_consistent = false;
            }
        });
        if (!init_scenes_consistent && legacy_init_cells_exist) {
            const scene_name = 'Legacy Init';
            notebook.widgets.map((cell) => {
                let is_legacy_init_cell = !!cell.model.getMetadata('init_cell');
                if (is_legacy_init_cell) {
                    cell.model.setMetadata(this._getSceneTag(scene_name), true);
                }
            });
            const scene_list = this.getScenesList();
            if (!scene_list.includes(scene_name)) {
                scene_list.push(scene_name);
                this._sceneDB.setScenesList(scene_list);
            }
            this.toggleInitScene(scene_name);
            this.setActiveScene(scene_name);
        }
    }
    /* ****************************************************************************************************************************************
     * Various private helper methods
     * ****************************************************************************************************************************************/
    _updateCellClassAndTags(cell, scene_tag) {
        let cell_tags = [];
        if (cell.model.getMetadata('tags')) {
            cell_tags = cell.model.getMetadata('tags');
        }
        if (!!cell.model.getMetadata(scene_tag)) {
            cell.addClass(SCENE_CELL_CLASS);
            if (!cell_tags.includes('ActiveScene'))
                cell_tags.push('ActiveScene');
        }
        else {
            cell.removeClass(SCENE_CELL_CLASS);
            if (cell_tags.includes('ActiveScene'))
                cell_tags.splice(cell_tags.indexOf('ActiveScene'), 1);
        }
        if (cell_tags.length > 0) {
            cell.model.setMetadata("tags", cell_tags);
        }
        else {
            cell.model.deleteMetadata("tags");
        }
    }
    _writeCellMetadataForLegacyInitializationCellsPlugin(notebook) {
        if (!this._enableLegacyInits)
            return;
        let init_scene = this.getInitScene();
        let init_scene_tag = (init_scene != null) ? this._getSceneTag(init_scene) : null;
        notebook.widgets.map((cell) => {
            if (init_scene_tag != null && !!cell.model.getMetadata(init_scene_tag)) {
                cell.model.setMetadata('init_cell', true);
            }
            else {
                cell.model.deleteMetadata('init_cell');
            }
        });
    }
    _activateCellAndExpandParentHeadings(cell) {
        let notebook = this._nbTracker.currentWidget.content;
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.expandParent(cell, notebook);
        notebook.scrollToCell(cell).then(() => { notebook.activeCellIndex = notebook.widgets.indexOf(cell); });
    }
    _moveScene(scene_name, direction) {
        const scenes_list = this.getScenesList();
        let idx = scenes_list.indexOf(scene_name);
        if (direction == 'down') {
            if (idx == scenes_list.length - 1)
                return;
        }
        else { // direction = 'up'
            if (idx == 0)
                return;
            idx -= 1;
        }
        scenes_list.splice(idx, 2, scenes_list[idx + 1], scenes_list[idx]);
        this._sceneDB.setScenesList(scenes_list);
    }
    _removeSceneTagFromAllCells(nbPanel, scene_name) {
        const tag = this._getSceneTag(scene_name);
        const notebook = nbPanel.content;
        notebook.widgets.map((cell) => {
            if (!!cell.model.getMetadata(tag)) {
                cell.model.deleteMetadata(tag);
            }
        });
    }
    _renameSceneTagFromAllCells(nbPanel, old_scene_name, new_scene_name) {
        const old_tag = this._getSceneTag(old_scene_name);
        const new_tag = this._getSceneTag(new_scene_name);
        const notebook = nbPanel.content;
        notebook.widgets.map((cell) => {
            if (!!cell.model.getMetadata(old_tag)) {
                cell.model.deleteMetadata(old_tag);
                cell.model.setMetadata(new_tag, true);
            }
        });
    }
    _duplicateSceneTagInAllCells(nbPanel, source_scene_name, target_scene_name) {
        const source_tag = this._getSceneTag(source_scene_name);
        const target_tag = this._getSceneTag(target_scene_name);
        const notebook = nbPanel.content;
        notebook.widgets.map((cell) => {
            console.log('iter', source_tag, cell);
            if (!!cell.model.getMetadata(source_tag)) {
                console.log('inside', target_tag);
                cell.model.setMetadata(target_tag, true);
            }
        });
    }
    _scenesChanged() {
        const activeScene = this._sceneDB.getActiveScene();
        if (!activeScene)
            return;
        let activeNotebookPanel = this._nbTracker.currentWidget;
        this._nbTracker.forEach((nbPanel) => {
            if (nbPanel.context === activeNotebookPanel.context) {
                this.updateCellClassesAndTags(nbPanel.content, activeScene);
            }
        });
        this._writeCellMetadataForLegacyInitializationCellsPlugin(activeNotebookPanel.content);
        this.scenesChanged.emit(void 0);
    }
    _getSceneTag(scene_name) {
        return 'scene__' + scene_name;
    }
}
class NotebookSceneDatabase {
    constructor(nbTracker) {
        this._nbTracker = nbTracker;
    }
    /* ****************************************************************************************************************************************
     * Data access
     * ****************************************************************************************************************************************/
    // **** simple getters *************************************************
    getNotebookTitle() {
        if (!this._nbTracker.currentWidget) {
            return null;
        }
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.basename(this._nbTracker.currentWidget.context.localPath);
    }
    getScenesList() {
        let data = this._getSceneDataAndMaybeSetupDefaultData();
        if (!data)
            return [];
        return data['scenes'];
    }
    getActiveScene(notebook = null) {
        let data = this._getSceneDataAndMaybeSetupDefaultData(notebook);
        if (!data)
            return null;
        return data['active_scene'];
    }
    getInitScene() {
        let data = this._getSceneDataAndMaybeSetupDefaultData();
        if (!data)
            return null;
        return data['init_scene'];
    }
    // **** scene setters **************************************************
    toggleInitScene(scene_name) {
        let data = this._getSceneDataAndMaybeSetupDefaultData();
        if (!data)
            return;
        if (data['init_scene'] == scene_name) {
            data['init_scene'] = null;
        }
        else {
            data['init_scene'] = scene_name;
        }
        this._setSceneData(data);
    }
    setActiveScene(scene_name) {
        let data = this._getSceneDataAndMaybeSetupDefaultData();
        if (!data)
            return;
        data['active_scene'] = scene_name;
        this._setSceneData(data);
    }
    setScenesList(scene_list) {
        let data = this._getSceneDataAndMaybeSetupDefaultData();
        if (!data)
            return;
        data['scenes'] = scene_list;
        this._setSceneData(data);
    }
    /* ****************************************************************************************************************************************
     * Helpers
     * ****************************************************************************************************************************************/
    _getSceneDataAndMaybeSetupDefaultData(notebook = null) {
        if (!notebook) {
            notebook = this._nbTracker.currentWidget.content;
        }
        let model = notebook.model;
        if (!model) {
            return null;
        }
        if (model.getMetadata(NB_METADATA_KEY) == null) {
            console.log('setting default scene data!!!!!!!!!!!');
            model.setMetadata(NB_METADATA_KEY, { scenes: ['Default Scene'], active_scene: 'Default Scene', init_scene: '' });
        }
        let data_json = model.getMetadata(NB_METADATA_KEY);
        let retval = {
            scenes: data_json['scenes'],
            active_scene: data_json['active_scene'],
            init_scene: data_json['init_scene']
        };
        return retval;
    }
    _setSceneData(scene_data) {
        var _a;
        let notebook_model = (_a = this._nbTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model;
        if (!notebook_model)
            return;
        notebook_model.setMetadata(NB_METADATA_KEY, scene_data);
    }
}
;


/***/ }),

/***/ "./lib/components.js":
/*!***************************!*\
  !*** ./lib/components.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScenesDisplay": () => (/* binding */ ScenesDisplay)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _style_svg_cellUp_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/svg/cellUp.svg */ "./style/svg/cellUp.svg");
/* harmony import */ var _style_svg_cellDown_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/svg/cellDown.svg */ "./style/svg/cellDown.svg");
/* harmony import */ var _style_svg_arrowUp_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/svg/arrowUp.svg */ "./style/svg/arrowUp.svg");
/* harmony import */ var _style_svg_arrowDown_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/svg/arrowDown.svg */ "./style/svg/arrowDown.svg");








const cellUpIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({ name: 'cellUp', svgstr: _style_svg_cellUp_svg__WEBPACK_IMPORTED_MODULE_2__ });
const cellDownIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({ name: 'cellDown', svgstr: _style_svg_cellDown_svg__WEBPACK_IMPORTED_MODULE_3__ });
const arrowUpIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({ name: 'arrowUp', svgstr: _style_svg_arrowUp_svg__WEBPACK_IMPORTED_MODULE_4__ });
const arrowDownIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({ name: 'arrowDown', svgstr: _style_svg_arrowDown_svg__WEBPACK_IMPORTED_MODULE_5__ });
class ScenesDisplay extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-ScenesSidebar" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-Header" },
                this.props.nbTitle,
                ": Scenes"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(Toolbar, { commands: this.props.commands }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(ScenesList, { scenes: this.props.scenes, currentScene: this.props.currentScene, initScene: this.props.initScene, notebookHandler: this.props.notebookHandler, commands: this.props.commands })));
    }
}
class ScenesList extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        let list = this.props.scenes.map(scene_name => {
            const onClickActivate = () => {
                this.props.notebookHandler.setActiveScene(scene_name);
            };
            const onClickDelete = (event) => {
                event.preventDefault();
                event.stopPropagation();
                this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_delete_scene, { 'scene_name': scene_name });
            };
            const onClickEdit = (event) => {
                event.preventDefault();
                event.stopPropagation();
                this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_rename_scene, { 'scene_name': scene_name });
            };
            const onClickInit = (event) => {
                event.preventDefault();
                event.stopPropagation();
                this.props.notebookHandler.toggleInitScene(scene_name);
            };
            const onClickRun = (event) => {
                event.preventDefault();
                event.stopPropagation();
                this.props.notebookHandler.runSceneInCurrentNotebook(scene_name);
            };
            let active = this.props.currentScene == scene_name;
            let init = this.props.initScene == scene_name;
            let className = active ? "scenes-SceneItem scenes-active" : "scenes-SceneItem";
            let classNameInitButton = init ? "scenes-InitSceneButtonActive" : "scenes-InitSceneButton";
            let sceneNameDisplay = active ? "  " + scene_name + " (active)" : "  " + scene_name;
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: className, onClick: onClickActivate, key: scene_name },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ItemButton", title: "Delete Scene", onClick: onClickDelete },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.closeIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ItemButton", title: "Run Scene", onClick: onClickRun },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.runIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ItemButton", title: "Rename Scene", onClick: onClickEdit },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.editIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-ItemText" }, sceneNameDisplay),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-SceneItemSpacer" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { onClick: onClickInit, className: classNameInitButton }, "init")));
        });
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-SceneList" }, list));
    }
}
class Toolbar extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    render() {
        const onClickNew = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_new_empty_scene);
        };
        const onClickDuplicate = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_duplicate_scene);
        };
        const onClickUp = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_move_active_scene_up);
        };
        const onClickDown = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_move_active_scene_down);
        };
        const onClickNext = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_to_next_scene_cell);
        };
        const onClickPrev = () => {
            this.props.commands.execute(_widget__WEBPACK_IMPORTED_MODULE_6__.ScenesSidebar.command_id_to_previous_scene_cell);
        };
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-Toolbar" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "New Empty Scene", onClick: onClickNew },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.addIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "Duplicate Active Scene", onClick: onClickDuplicate },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.copyIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "Move Active Scene Up", onClick: onClickUp },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(arrowUpIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "Move Active Scene Down", onClick: onClickDown },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(arrowDownIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "scenes-SceneItemSpacer" }),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "Jump to Next Scene Cell", onClick: onClickNext },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(cellDownIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" })),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "scenes-ToolbarButton", title: "Move to Previous Scene Cell", onClick: onClickPrev },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(cellUpIcon.react, { tag: "span", className: "jp-ToolbarButtonComponent-icon f1vya9e0" }))));
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");





function activateScenes(app, settingRegistry, nbTracker, mainMenu, labShell) {
    // create the ScenesSidebar widget
    const scenesSidebar = new _widget__WEBPACK_IMPORTED_MODULE_4__.ScenesSidebar(app, nbTracker, mainMenu, settingRegistry);
    app.shell.add(scenesSidebar, 'left', { rank: 1000 });
}
/**
 * Initialization data for the jupyterlab_scenes extension.
 */
const plugin = {
    id: 'jupyterlab_scenes:plugin',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: activateScenes
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ScenesSidebar": () => (/* binding */ ScenesSidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components */ "./lib/components.js");
/* harmony import */ var _backend__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./backend */ "./lib/backend.js");
/* harmony import */ var _style_svg_scenesLogo_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/svg/scenesLogo.svg */ "./style/svg/scenesLogo.svg");







const scenesIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon({ name: 'scenes', svgstr: _style_svg_scenesLogo_svg__WEBPACK_IMPORTED_MODULE_4__ });
class ScenesSidebar extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(app, nbTracker, mainMenu, settingRegistry) {
        super();
        this._app = app;
        this._nbTracker = nbTracker;
        this._mainMenu = mainMenu;
        this._scenesMenu = null;
        this._notebookHandler = new _backend__WEBPACK_IMPORTED_MODULE_5__.NotebookHandler(nbTracker, settingRegistry);
        this._setupWidget();
        this._setupGlobalCommands();
        this._setupKeyboardShortcuts();
        this._setupScenesMenu();
        // this is needed to sync ScenesSidebar and code cells on load
        this._nbTracker.widgetAdded.connect((_x, nbpanel) => {
            //console.log('widgetAdded', nbpanel.context.path)
            nbpanel.context.ready.then(() => {
                //console.log('context ready', nbpanel.context.path);
                this._notebookHandler.updateCellClassesAndTags(nbpanel.content, this._notebookHandler.getActiveScene(nbpanel.content));
                this._notebookHandler.importLegacyInitializationCells(nbpanel.content);
                this.update();
            });
            // this is needed for handling copy/paste
            nbpanel.content.activeCellChanged.connect((notebook, cell) => {
                this._notebookHandler.updateCellClassesAndTags(notebook, this._notebookHandler.getActiveScene(), cell);
            });
        });
        // this is needed syncing the ScenesSidebar to the current notebook panel
        this._nbTracker.currentChanged.connect((sender, nbpanel) => {
            //console.log('currentChanged', nbpanel!.context.path)
            if (!(nbpanel === null || nbpanel === void 0 ? void 0 : nbpanel.context.isReady))
                return;
            this.update();
        });
        this._notebookHandler.scenesChanged.connect(() => { this.update(); });
    }
    render() {
        let nb_title = this._notebookHandler.getNotebookTitle();
        if (!nb_title)
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null));
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_components__WEBPACK_IMPORTED_MODULE_6__.ScenesDisplay, { nbTitle: nb_title, scenes: this._notebookHandler.getScenesList(), currentScene: this._notebookHandler.getActiveScene(), initScene: this._notebookHandler.getInitScene(), commands: this._app.commands, notebookHandler: this._notebookHandler }));
    }
    onNotebookChanged() {
        this.update();
    }
    /* ****************************************************************************************************************************************
     * Private helper methods
     * ****************************************************************************************************************************************/
    // **** setup helpers ****************************************************************************************************************
    _setupWidget() {
        this.id = 'scenes';
        this.title.caption = 'Scenes';
        this.title.icon = scenesIcon;
    }
    _setupGlobalCommands() {
        this._app.commands.addCommand(ScenesSidebar.command_id_toggle_scene_cell, {
            label: 'Toggle Scene Cell',
            execute: () => { this._notebookHandler.toggleSceneMembershipOfSelectedCells(); }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_run_scene, {
            label: 'Run Scene',
            execute: () => { this._notebookHandler.runActiveSceneInCurrentNotebook(); }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_new_empty_scene, {
            label: 'New Empty Scene',
            execute: () => {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({ title: 'Name of the New Scene:' }).then((new_scene) => {
                    if (!new_scene.value)
                        return;
                    if (this._notebookHandler.createNewEmptyScene(new_scene.value) == 'fail') {
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Error: New Scene Creation', 'Scene with name "' + new_scene.value + '" already exists!');
                    }
                });
            }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_duplicate_scene, {
            label: 'Duplicate Active Scene',
            execute: () => {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({ title: 'Name of the Duplicated Scene:' }).then((new_scene) => {
                    if (!new_scene.value)
                        return;
                    if (this._notebookHandler.duplicateActiveScene(new_scene.value) == 'fail') {
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Error: Scene Duplication', 'Scene with name "' + new_scene.value + '" already exists!');
                    }
                });
            }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_delete_scene, {
            label: 'Delete Scene',
            execute: async (scene_name_obj) => {
                let scene_name = scene_name_obj['scene_name'];
                const result = await (new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog({
                    title: 'Delete Scene "' + scene_name + '" permanently?',
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Delete' })]
                }).launch());
                if (result.button.label == 'Delete') {
                    this._notebookHandler.deleteScene(scene_name);
                }
            }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_rename_scene, {
            label: 'Rename Scene',
            execute: async (scene_name_obj) => {
                let scene_name = scene_name_obj['scene_name'];
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({ title: 'New Name of Scene "' + scene_name + '":' }).then((new_scene_name) => {
                    if (!new_scene_name.value)
                        return;
                    if (this._notebookHandler.renameScene(scene_name, new_scene_name.value) == 'fail') {
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Error: Scene Renaming', 'Scene with name "' + new_scene_name.value + '" already exists!');
                    }
                });
            }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_move_active_scene_up, {
            label: 'Move Active Scene Up',
            execute: () => { this._notebookHandler.moveActiveSceneUp(); }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_move_active_scene_down, {
            label: 'Move Active Scene Down',
            execute: () => { this._notebookHandler.moveActiveSceneDown(); }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_to_next_scene_cell, {
            label: 'Jump to Next Scene Cell',
            execute: () => { this._notebookHandler.jumpToNextSceneCell(); }
        });
        this._app.commands.addCommand(ScenesSidebar.command_id_to_previous_scene_cell, {
            label: 'Jump to Previous Scene Cell',
            execute: () => { this._notebookHandler.jumpToPreviousSceneCell(); }
        });
    }
    _setupKeyboardShortcuts() {
        this._app.commands.addKeyBinding({
            command: ScenesSidebar.command_id_toggle_scene_cell,
            args: {},
            keys: ['Accel I'],
            selector: '.jp-Notebook'
        });
        this._app.commands.addKeyBinding({
            command: ScenesSidebar.command_id_run_scene,
            args: {},
            keys: ['Ctrl Alt R'],
            selector: '.jp-Notebook'
        });
    }
    _setupScenesMenu() {
        this._scenesMenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Menu({ commands: this._app.commands });
        this._scenesMenu.title.label = 'Scenes';
        this._scenesMenu.addItem({ command: ScenesSidebar.command_id_toggle_scene_cell });
        this._scenesMenu.addItem({ command: ScenesSidebar.command_id_run_scene });
        this._scenesMenu.addItem({ type: 'separator' });
        this._scenesMenu.addItem({ command: ScenesSidebar.command_id_new_empty_scene });
        this._scenesMenu.addItem({ command: ScenesSidebar.command_id_duplicate_scene });
        this._mainMenu.addMenu(this._scenesMenu);
    }
}
ScenesSidebar.command_id_toggle_scene_cell = 'scenes:toggle-scene-cell';
ScenesSidebar.command_id_run_scene = 'scenes:run-scene';
ScenesSidebar.command_id_new_empty_scene = 'scenes:new-empty-scene';
ScenesSidebar.command_id_duplicate_scene = 'scenes:duplicate-scene';
ScenesSidebar.command_id_rename_scene = 'scenes:rename-scene';
ScenesSidebar.command_id_delete_scene = 'scenes:delete-scene';
ScenesSidebar.command_id_move_active_scene_up = 'scenes:move-active-scene-up';
ScenesSidebar.command_id_move_active_scene_down = 'scenes:move-active-scene-down';
ScenesSidebar.command_id_to_next_scene_cell = 'scenes:jump-to-next-scene-cell';
ScenesSidebar.command_id_to_previous_scene_cell = 'scenes:jump-to-previous-scene-cell';

;


/***/ }),

/***/ "./style/svg/arrowDown.svg":
/*!*********************************!*\
  !*** ./style/svg/arrowDown.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n     <g transform=\"matrix(0,1,-1,0,25.7,0.9)\" class=\"jp-icon3\" fill=\"#616161\">\n          <path transform=\"matrix(0.7,0,0,0.8,6.6,2.8)\" d=\"M 12 6.5 v 14 l 11 -7 z\"/>\n          <rect x=\"0.2\" y=\"11.8\" width=\"12.3\" height=\"3\"/>\n     </g>\n</svg>\n";

/***/ }),

/***/ "./style/svg/arrowUp.svg":
/*!*******************************!*\
  !*** ./style/svg/arrowUp.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n     <g transform=\"matrix(0,-1,1,0,-1.5,23.7)\" class=\"jp-icon3\" fill=\"#616161\">\n          <path transform=\"matrix(0.7,0,0,0.8,6.6,2.8)\" d=\"M 12 6.5 v 14 l 11 -7 z\"/>\n          <rect x=\"0.2\" y=\"11.8\" width=\"12.3\" height=\"3\"/>\n     </g>\n</svg>\n";

/***/ }),

/***/ "./style/svg/cellDown.svg":
/*!********************************!*\
  !*** ./style/svg/cellDown.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n    <g transform=\"matrix(0,1,-1,0,23.9,-0.1)\" class=\"jp-icon3\" fill=\"#616161\">\n         <path transform=\"matrix(1,0,0,1.2,0,-2.9)\" d=\"M 0.6 6 v 14 l 11 -7 z\"/>\n    </g>\n <ellipse transform=\"matrix(0,1,-1,0,23.9,-0.1)\" rx=\"6.5\" ry=\"6.4\"\n     fill=\"#771e90\"\n     cx=\"17.6\"\n     cy=\"12.7\"\n     />\n</svg>\n";

/***/ }),

/***/ "./style/svg/cellUp.svg":
/*!******************************!*\
  !*** ./style/svg/cellUp.svg ***!
  \******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n    <g transform=\"matrix(0,-1,1,0,-1.6,24.4)\" class=\"jp-icon3\" fill=\"#616161\">\n         <path transform=\"matrix(1,0,0,1.2,0,-2.9)\" d=\"M 0.6 6.1 v 14 l 11 -7 z\"/>\n    </g>\n <ellipse transform=\"matrix(0,-1,1,0,-1.6,24.4)\" rx=\"6.5\" ry=\"6.4\"\n     fill=\"#771e90\"\n     cx=\"17.6\"\n     cy=\"12.9\"\n     />\n</svg>\n";

/***/ }),

/***/ "./style/svg/scenesLogo.svg":
/*!**********************************!*\
  !*** ./style/svg/scenesLogo.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\">\n    <g class=\"jp-icon3\" fill=\"#616161\">\n         <path transform=\"matrix(1,0,0,1.2,0,-2.9)\" d=\"M 13.1 5.3 v 14 l 11 -7 z\"/>\n    </g>\n <ellipse rx=\"6.5\" ry=\"6.4\"\n     fill=\"#771e90\"\n     cx=\"6.4\"\n     cy=\"12\"\n     />\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.fe968cb4f1e9e644c518.js.map