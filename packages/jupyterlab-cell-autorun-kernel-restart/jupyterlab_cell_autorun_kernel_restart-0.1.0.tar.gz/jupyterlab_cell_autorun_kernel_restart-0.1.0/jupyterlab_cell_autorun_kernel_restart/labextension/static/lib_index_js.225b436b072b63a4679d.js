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
/* harmony import */ var _style_icons_reinit_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/reinit.svg */ "./style/icons/reinit.svg");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);





const ic = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({ name: 'test', svgstr: _style_icons_reinit_svg__WEBPACK_IMPORTED_MODULE_4__["default"] });
//import { find } from '@lumino/algorithm';
const EXT_NAME = 'cell_autorun_kernel_restart';
const INITCELL = '${EXT_NAME}:initcell';
const INITCELL_ENABLED_CLASS = 'cell-autorun-kernel-restart-enabled';
class KernelReInitButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton {
    constructor(app, nbtracker) {
        super({ onClick: () => { this.onReInitButtonClicked(); }, icon: ic });
        this.app = app;
        this.nbtracker = nbtracker;
        this.kernel_status_listener_connected = false;
        this.init_on_connect_stage = 'ignore reconnect';
    }
    attach(nbpanel) {
        console.log('Adding ReInit button');
        const toolbar = nbpanel.toolbar;
        let insertionPoint = 7;
        /*
        find(toolbar.children(), (tbb, index) => {
          console.log(tbb.);
          if (tbb.hasClass('jp-Notebook-toolbarRestart')) {
            insertionPoint = index;
            return true;
          }
          return false;
        });
        */
        toolbar.insertItem(insertionPoint + 1, 'reinit_button', this);
        this.setupContextMenu();
        this.setCellStyles(nbpanel);
        nbpanel.context.sessionContext.ready.then(() => { this.setCellStyles(nbpanel); });
    }
    /**
     * Privates
     */
    setCellStyles(nbpanel) {
        const notebook = nbpanel.content;
        notebook.widgets.map((cell) => {
            if (!!cell.model.metadata.get(INITCELL)) {
                cell.addClass(INITCELL_ENABLED_CLASS);
            }
        });
    }
    setupContextMenu() {
        const command_id = '${EXT_NAME}:toggle_autorun';
        this.app.commands.addCommand(command_id, {
            label: 'Toggle Init Cell',
            execute: () => { this.toggleInitCell(); }
        });
        this.app.contextMenu.addItem({
            command: command_id,
            selector: '.jp-Cell',
            rank: 0
        });
    }
    async doKernelInitialization() {
        console.log('Initializing the Kernel');
        if (this.nbtracker.currentWidget) {
            const notebook = this.nbtracker.currentWidget.content;
            const notebookPanel = this.nbtracker.currentWidget;
            notebook.widgets.map((cell) => {
                console.log('x', cell.model.metadata.get(INITCELL));
                if (!!cell.model.metadata.get(INITCELL)) {
                    if (cell.model.type == 'code') {
                        _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(cell, notebookPanel.sessionContext);
                    }
                }
            });
        }
    }
    /**
     * Callbacks
     */
    toggleInitCell() {
        console.log('Toggle init cell');
        const cell = this.nbtracker.activeCell;
        if (cell) {
            if (!!cell.model.metadata.get(INITCELL)) {
                cell.model.metadata.set(INITCELL, false);
                cell.removeClass(INITCELL_ENABLED_CLASS);
            }
            else {
                cell.model.metadata.set(INITCELL, true);
                cell.addClass(INITCELL_ENABLED_CLASS);
            }
        }
    }
    onReInitButtonClicked() {
        var _a, _b, _c, _d, _e, _f;
        console.log('Re-Initializing the Kernel');
        if (!this.kernel_status_listener_connected) {
            (_c = (_b = (_a = this.nbtracker.currentWidget) === null || _a === void 0 ? void 0 : _a.context.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.connectionStatusChanged.connect((_unused, conn_stat) => {
                this.kernelConnectionStatusListener(conn_stat);
            });
            this.kernel_status_listener_connected = true;
        }
        this.init_on_connect_stage = 0;
        (_f = (_e = (_d = this.nbtracker.currentWidget) === null || _d === void 0 ? void 0 : _d.context.sessionContext.session) === null || _e === void 0 ? void 0 : _e.kernel) === null || _f === void 0 ? void 0 : _f.restart();
    }
    kernelConnectionStatusListener(conn_stat) {
        console.log('kernelstatus', conn_stat);
        if (this.init_on_connect_stage == 'ignore reconnect') {
            return;
        }
        if (this.init_on_connect_stage == 0 && conn_stat == 'connecting') {
            this.init_on_connect_stage = 1;
            return;
        }
        if (this.init_on_connect_stage == 1 && conn_stat == 'connected') {
            this.doKernelInitialization();
            this.init_on_connect_stage = 'ignore reconnect';
            return;
        }
    }
}
/**
 * Initialization data for the jupyterlab_cell_autorun_kernel_restart extension.
 */
const plugin = {
    id: EXT_NAME,
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker],
    activate: (app, nbtracker) => {
        nbtracker.widgetAdded.connect((nbtracker_, nbpanel) => {
            if (nbpanel) {
                let but = new KernelReInitButton(app, nbtracker_);
                but.attach(nbpanel);
            }
        });
        console.log('jupyterlab_cell_autorun_kernel_restart is activated!');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./style/icons/reinit.svg":
/*!********************************!*\
  !*** ./style/icons/reinit.svg ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" viewBox=\"0 0 18 18\">\n    <g class=\"jp-icon3\" fill=\"#616161\">\n        <path d=\"M9 13.5c-2.49 0-4.5-2.01-4.5-4.5S6.51 4.5 9 4.5c1.24 0 2.36.52 3.17 1.33L10 8h5V3l-1.76 1.76C12.15 3.68 10.66 3 9 3 5.69 3 3.01 5.69 3.01 9S5.69 15 9 15c2.97 0 5.43-2.16 5.9-5h-1.52c-.46 2-2.24 3.5-4.38 3.5z\"/>\n    </g>\n <circle\n     class=\"jp-icon-accent0\"\n     fill=\"#00f\"\n     cx=\"8.9121799\"\n     cy=\"8.9046097\"\n     r=\"3.3522882\" />\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.225b436b072b63a4679d.js.map