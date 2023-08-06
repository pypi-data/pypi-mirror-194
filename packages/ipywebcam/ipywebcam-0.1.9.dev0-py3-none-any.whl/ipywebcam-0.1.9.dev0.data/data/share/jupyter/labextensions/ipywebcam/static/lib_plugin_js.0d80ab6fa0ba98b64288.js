"use strict";
(self["webpackChunkipywebcam"] = self["webpackChunkipywebcam"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const widgetsExports = __importStar(__webpack_require__(/*! ./widgets */ "./lib/widgets.js"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const EXTENSION_ID = 'ipywebcam:plugin';
/**
 * The example plugin.
 */
const webcamPlugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.
exports["default"] = webcamPlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: version_1.MODULE_NAME,
        version: version_1.MODULE_VERSION,
        exports: widgetsExports,
    });
}
//# sourceMappingURL=plugin.js.map

/***/ }),

/***/ "./lib/widgets.js":
/*!************************!*\
  !*** ./lib/widgets.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RecorderPlayerView = exports.RecorderPlayerModel = exports.WebCamView = exports.WebCamModel = void 0;
var webcam_1 = __webpack_require__(/*! ./webcam */ "./lib/webcam.js");
Object.defineProperty(exports, "WebCamModel", ({ enumerable: true, get: function () { return webcam_1.WebCamModel; } }));
Object.defineProperty(exports, "WebCamView", ({ enumerable: true, get: function () { return webcam_1.WebCamView; } }));
var recorder_1 = __webpack_require__(/*! ./recorder */ "./lib/recorder.js");
Object.defineProperty(exports, "RecorderPlayerModel", ({ enumerable: true, get: function () { return recorder_1.RecorderPlayerModel; } }));
Object.defineProperty(exports, "RecorderPlayerView", ({ enumerable: true, get: function () { return recorder_1.RecorderPlayerView; } }));
//# sourceMappingURL=widgets.js.map

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.0d80ab6fa0ba98b64288.js.map