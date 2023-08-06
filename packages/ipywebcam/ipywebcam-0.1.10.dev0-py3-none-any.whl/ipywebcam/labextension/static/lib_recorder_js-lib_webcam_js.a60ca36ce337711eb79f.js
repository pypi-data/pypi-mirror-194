(self["webpackChunkipywebcam"] = self["webpackChunkipywebcam"] || []).push([["lib_recorder_js-lib_webcam_js"],{

/***/ "./lib/charts.js":
/*!***********************!*\
  !*** ./lib/charts.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
exports.makeLineChart = void 0;
const d3 = __importStar(__webpack_require__(/*! d3 */ "webpack/sharing/consume/default/d3/d3"));
function makeLineChart(node, data, xRange, yRange, width, height) {
    const svg = node
        ? d3.select(node)
        : d3.create('svg');
    width =
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        width === undefined || width === null ? svg.node().clientWidth : width;
    height =
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        height === undefined || height === null ? svg.node().clientHeight : height;
    if (height > 16) {
        height -= 4;
    }
    if (!xRange) {
        const xData = data.map((d) => d[0]);
        xRange = [Math.min(...xData), Math.max(...xData)];
    }
    if (xRange[0] === xRange[1]) {
        xRange[1] += 1;
    }
    if (!yRange) {
        const yData = data.map((d) => d[1]);
        yRange = [Math.min(...yData), Math.max(...yData)];
    }
    if (yRange[0] === yRange[1]) {
        yRange[1] += 1;
    }
    const xOffset = -xRange[0];
    const xScale = width / (xRange[1] - xRange[0]);
    const yOffset = -yRange[0];
    const yScale = height / (yRange[1] - yRange[0]);
    const lineFunc = d3
        .line()
        .x((d) => (d[0] + xOffset) * xScale)
        .y((d) => (d[1] + yOffset) * yScale);
    let path = svg.select('path');
    if (path.size() === 0) {
        path = svg.append('path').attr('fill', 'none');
    }
    path.attr('d', lineFunc(data));
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    return svg.node();
}
exports.makeLineChart = makeLineChart;
//# sourceMappingURL=charts.js.map

/***/ }),

/***/ "./lib/common.js":
/*!***********************!*\
  !*** ./lib/common.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BaseModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
class BaseModel extends base_1.DOMWidgetModel {
    constructor(...args) {
        super(...args);
        this.messageHandlers = {};
        this.addMessageHandler = (cmd, handler) => {
            let handlers = this.messageHandlers[cmd];
            if (!handlers) {
                handlers = this.messageHandlers[cmd] = [];
            }
            handlers.push(handler);
        };
        this.removeMessageHandler = (cmd, handler) => {
            const handlers = this.messageHandlers[cmd];
            if (handlers) {
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                utils_1.arrayRemove(handlers, handler);
            }
        };
        this.send_cmd = this.send_cmd.bind(this);
        this.on('msg:custom', (msg, buffers) => {
            const { id, cmd } = msg;
            if (id && id !== this.message_id) {
                return;
            }
            Object.keys(this.messageHandlers).forEach((key) => {
                if (key === cmd) {
                    const handlers = this.messageHandlers[key];
                    if (handlers) {
                        handlers.forEach((handler) => {
                            handler(msg, buffers);
                        });
                    }
                }
            });
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _view_module: version_1.MODULE_NAME, _model_module: version_1.MODULE_NAME, _view_module_version: version_1.MODULE_VERSION, _model_module_version: version_1.MODULE_VERSION });
    }
    get message_id() {
        return this.model_id;
    }
    send_cmd(cmd, args, wait = true) {
        return __awaiter(this, void 0, void 0, function* () {
            const id = this.message_id;
            if (wait) {
                return new Promise((resolve) => {
                    // eslint-disable-next-line @typescript-eslint/no-this-alias
                    const self = this;
                    this.send({ cmd, id, args }, {});
                    function callback({ ans, id: t_id, res, }, buffers) {
                        if (ans === cmd && t_id === id) {
                            resolve({ content: res, buffers });
                            self.off('msg:custom', callback);
                        }
                    }
                    this.on('msg:custom', callback);
                });
            }
            else {
                this.send({ cmd, id, args }, {});
            }
        });
    }
}
exports.BaseModel = BaseModel;
//# sourceMappingURL=common.js.map

/***/ }),

/***/ "./lib/range.js":
/*!**********************!*\
  !*** ./lib/range.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RangeBar = void 0;
/* eslint-disable @typescript-eslint/no-non-null-assertion */
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
class RangeBar {
    constructor(container, option = {}) {
        this.selectedRange = [0, 0];
        this.markersChangeCallbacks = [];
        this.rangeSelectedCallbacks = [];
        this.destroy = () => {
            document.removeEventListener('mousemove', this.onSelectedMove);
            document.removeEventListener('mouseup', this.removeSelect);
        };
        this.toggle = () => {
            if (this.container.classList.contains('hidden')) {
                this.container.classList.remove('hidden');
                if (this.container.parentElement) {
                    this.container.parentElement.style.height = `${this.container.parentElement.clientHeight + 12}px`;
                }
            }
            else {
                this.container.classList.add('hidden');
                if (this.container.parentElement) {
                    this.container.parentElement.style.height = `${this.container.parentElement.clientHeight - 12}px`;
                }
            }
        };
        this.isEnabled = () => {
            return this.max > this.min;
        };
        this.adjustPos = (pos) => {
            const width = this.container.clientWidth;
            if (width === 0) {
                return 0;
            }
            if (this.step <= 0) {
                return (pos / width) * 100;
            }
            else {
                let v = (pos / width) * (this.max - this.min);
                v = Math.round(v / this.step) * this.step;
                return (v / (this.max - this.min)) * 100;
            }
        };
        this.pos2value = (pos) => {
            return this.min + (pos * (this.max - this.min)) / 100;
        };
        this.value2pos = (value) => {
            return ((value - this.min) / (this.max - this.min)) * 100;
        };
        this.addRangeSelectedCallback = (callback) => {
            this.rangeSelectedCallbacks.push(callback);
        };
        this.removeRangeSelectedCallback = (callback) => {
            utils_1.arrayRemove(this.rangeSelectedCallbacks, callback);
        };
        this.addMarkersChangeCallback = (callback) => {
            this.markersChangeCallbacks.push(callback);
        };
        this.removeMarkersChangeCallback = (callback) => {
            utils_1.arrayRemove(this.markersChangeCallbacks, callback);
        };
        this.calcRange = (pos) => {
            const res = [this.min, this.max];
            const value = this.pos2value(pos);
            for (const key of Object.keys(this.markers)) {
                const v = this.pos2value(Number.parseFloat(key));
                if (pos === v) {
                    return [0, 0];
                }
                else if (value > v && v > res[0]) {
                    res[0] = v;
                }
                else if (value < v && v < res[1]) {
                    res[1] = v;
                }
            }
            return res;
        };
        this.makeFloatingMarker = (pos) => {
            if (this.isEnabled()) {
                pos = this.adjustPos(pos);
                if (!this.floatingMarker) {
                    this.floatingMarker = document.createElement('div');
                    this.floatingMarker.classList.add('marker', 'floating');
                    this.container.appendChild(this.floatingMarker);
                }
                this.floatingMarker.style.left = `${pos}%`;
                this.floatingMarker.style.translate = '-50%';
            }
        };
        this.releaseFloatingMarker = () => {
            if (this.floatingMarker) {
                this.container.removeChild(this.floatingMarker);
                this.floatingMarker = undefined;
            }
        };
        this.findMarkderKey = (marker) => {
            for (const key of Object.keys(this.markers)) {
                const pos = Number.parseFloat(key);
                if (marker === this.markers[pos]) {
                    return pos;
                }
            }
            return undefined;
        };
        this.getMarkers = () => {
            return Object.keys(this.markers)
                .map((key) => {
                const pos = Number.parseFloat(key);
                return this.pos2value(pos);
            })
                .sort();
        };
        this.setMarkers = (markers) => {
            if (!markers) {
                markers = [];
            }
            if (utils_1.arrayEqual(this.getMarkers(), markers)) {
                return;
            }
            this.unselectRange();
            this.removeSelect();
            for (const key of Object.keys(this.markers)) {
                const marker = this.markers[key];
                this.removeMarkerByNode(marker, false);
            }
            for (const marker of markers) {
                this.addMarker(this.value2pos(marker), false);
            }
            this.execuateMarkersCallbacks();
        };
        this.execuateMarkersCallbacks = () => {
            const markers = this.getMarkers();
            for (const callback of this.markersChangeCallbacks) {
                callback(markers, this);
            }
        };
        this.removeMarkerByNode = (marker, triggerCallback = true) => {
            const key = this.findMarkderKey(marker);
            if (key !== undefined) {
                delete this.markers[key];
                this.container.removeChild(marker);
                if (triggerCallback) {
                    this.execuateMarkersCallbacks();
                }
            }
        };
        this.addMarker = (pos, triggerCallback = true) => {
            if (this.isEnabled()) {
                let marker = this.markers[pos];
                if (!marker) {
                    this.markers[pos] = marker = document.createElement('div');
                    marker.setAttribute('draggable', 'false');
                    marker.classList.add('marker');
                    this.container.appendChild(marker);
                    marker.style.left = `${pos}%`;
                    marker.style.translate = '-50%';
                    marker.addEventListener('click', (evt) => {
                        evt.stopPropagation();
                        if (evt.altKey) {
                            this.removeMarkerByNode(marker);
                        }
                    });
                    marker.addEventListener('mousedown', (evt) => {
                        evt.stopPropagation();
                        const key = this.findMarkderKey(marker);
                        if (key !== undefined) {
                            this.setSelect(key);
                        }
                    });
                    marker.addEventListener('mouseup', () => {
                        this.removeSelect();
                    });
                    if (triggerCallback) {
                        this.execuateMarkersCallbacks();
                    }
                }
            }
        };
        this.setSelect = (pos) => {
            this.selectedKey = pos;
            const marker = this.markers[pos];
            if (marker) {
                marker.classList.add('selected');
            }
        };
        this.removeSelect = () => {
            if (this.selectedKey !== undefined) {
                const marker = this.markers[this.selectedKey];
                if (marker) {
                    marker.classList.remove('selected');
                }
                this.selectedKey = undefined;
            }
        };
        this.canKeyMove = (posFrom, posTo) => {
            if (posFrom === posTo) {
                return false;
            }
            if (posTo < 0 || posTo > 100) {
                return false;
            }
            const keys = Object.keys(this.markers);
            for (const key of keys) {
                const pos = Number.parseFloat(key);
                if (pos === posFrom) {
                    continue;
                }
                if (pos === posTo) {
                    return false;
                }
                if (pos < posFrom && posTo > posFrom) {
                    continue;
                }
                if (pos > posFrom && posTo < posFrom) {
                    continue;
                }
                if (pos < posFrom && pos > posTo) {
                    return false;
                }
                if (pos > posFrom && pos < posTo) {
                    return false;
                }
            }
            return true;
        };
        this.onSelectedMove = (evt) => {
            let pos = utils_1.calcMouseOffsetX(evt, this.container);
            pos = this.adjustPos(pos);
            if (this.selectedKey !== undefined &&
                this.canKeyMove(this.selectedKey, pos)) {
                const marker = this.markers[this.selectedKey];
                if (marker) {
                    marker.style.left = `${pos}%`;
                    marker.style.translate = '-50%';
                    delete this.markers[this.selectedKey];
                    this.updateRangeSelectBecauseOfKeyChagne(this.selectedKey, pos);
                    this.selectedKey = pos;
                    this.markers[pos] = marker;
                    this.execuateMarkersCallbacks();
                }
            }
        };
        this.isRangeSelected = (range) => {
            if (!range) {
                range = this.selectedRange;
            }
            return range[1] > range[0];
        };
        this.updateRangeSelectBecauseOfKeyChagne = (posFrom, posTo) => {
            const valueFrom = this.pos2value(posFrom);
            if (this.isRangeSelected() &&
                (valueFrom === this.selectedRange[0] ||
                    valueFrom === this.selectedRange[1])) {
                const valueTo = this.pos2value(posTo);
                let valueOther;
                if (valueFrom === this.selectedRange[0]) {
                    valueOther = this.selectedRange[1];
                }
                else {
                    valueOther = this.selectedRange[0];
                }
                const newRange = valueTo <= valueOther ? [valueTo, valueOther] : [valueOther, valueTo];
                this.updateRangeSelect(newRange);
            }
        };
        this.updateRangeSelect = (newRange) => {
            if (this.isRangeSelected(newRange)) {
                const cWidth = this.container.clientWidth;
                const left = ((newRange[0] - this.min) / (this.max - this.min)) * cWidth;
                const right = ((newRange[1] - this.min) / (this.max - this.min)) * cWidth;
                this.rangeMasker.style.left = `${left}px`;
                this.rangeMasker.style.width = `${right - left}px`;
                this.rangeMasker.classList.remove('hidden');
            }
            this.selectedRange = newRange;
            for (const callback of this.rangeSelectedCallbacks) {
                callback(this.selectedRange, this);
            }
        };
        this.onMouseRangeSelect = (evt) => {
            if (this.selectedKey !== undefined) {
                // when moving key point, do nothing.
                return;
            }
            const cWidth = this.container.clientWidth;
            if (cWidth === 0) {
                return;
            }
            const pos = (utils_1.calcMouseOffsetX(evt, this.container) / cWidth) * 100;
            const range = this.calcRange(pos);
            this.updateRangeSelect(range);
        };
        this.selectRange = (range) => {
            if (utils_1.arrayEqual(this.selectedRange, range)) {
                return;
            }
            const posFrom = this.value2pos(range[0]);
            const posTo = this.value2pos(range[1]);
            if (this.markers[posFrom] && this.markers[posTo]) {
                this.updateRangeSelect(range);
            }
        };
        this.unselectRange = () => {
            this.rangeMasker.style.left = '0px';
            this.rangeMasker.style.width = '0px';
            this.rangeMasker.classList.add('hidden');
            this.selectedRange = [0, 0];
            for (const callback of this.rangeSelectedCallbacks) {
                callback(this.selectedRange, this);
            }
        };
        this.container = container;
        this.rangeMasker = document.createElement('div');
        this.rangeMasker.classList.add('range-mask', 'hidden');
        this.rangeMasker.addEventListener('click', (evt) => {
            evt.stopPropagation();
            this.unselectRange();
        });
        this.container.appendChild(this.rangeMasker);
        this.container.addEventListener('click', (evt) => {
            if (evt.ctrlKey) {
                const pos = this.adjustPos(evt.offsetX);
                this.addMarker(pos);
            }
            else {
                this.onMouseRangeSelect(evt);
            }
        });
        this.container.addEventListener('mouseover', (evt) => {
            const offsetX = utils_1.calcMouseOffsetX(evt, this.container);
            if (evt.ctrlKey) {
                this.makeFloatingMarker(offsetX);
            }
            else {
                this.releaseFloatingMarker();
            }
        });
        this.container.addEventListener('mousemove', (evt) => {
            const offsetX = utils_1.calcMouseOffsetX(evt, this.container);
            if (evt.ctrlKey) {
                this.makeFloatingMarker(offsetX);
            }
            else {
                this.releaseFloatingMarker();
            }
        });
        this.container.addEventListener('mouseout', () => {
            this.releaseFloatingMarker();
        });
        document.addEventListener('mousemove', this.onSelectedMove);
        document.addEventListener('mouseup', this.removeSelect);
        const { min = 0, max = 0, step = 1 } = option;
        this.min = min;
        this.max = max;
        this.step = step;
        this.markers = {};
    }
}
exports.RangeBar = RangeBar;
//# sourceMappingURL=range.js.map

/***/ }),

/***/ "./lib/recorder.js":
/*!*************************!*\
  !*** ./lib/recorder.js ***!
  \*************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RecorderPlayerView = exports.RecorderPlayerModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const lru_cache_1 = __importDefault(__webpack_require__(/*! lru-cache */ "webpack/sharing/consume/default/lru-cache/lru-cache"));
const common_1 = __webpack_require__(/*! ./common */ "./lib/common.js");
const video_1 = __webpack_require__(/*! ./video */ "./lib/video.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
class RecorderPlayerModel extends common_1.BaseModel {
    constructor(...args) {
        super(...args);
        this.cache = new lru_cache_1.default({
            max: 10,
        });
        this.metaCache = new lru_cache_1.default({
            max: 100,
        });
        this.fetchStates = {};
        this.refresh_callbacks = [];
        this.addRefereshCallback = (callback) => {
            this.refresh_callbacks.push(callback);
        };
        this.removeRefreshCallback = (callback) => {
            const index = this.refresh_callbacks.indexOf(callback);
            if (index >= 0) {
                this.refresh_callbacks.splice(index, 1);
            }
        };
        this.triggerRefresh = (index, channel) => {
            this.refresh_callbacks.forEach((cb) => {
                cb(index, channel);
            });
        };
        this.createIndexKey = (index) => {
            return index === undefined || index === null ? 'global' : `${index}`;
        };
        this.fetchMeta = (index = undefined) => __awaiter(this, void 0, void 0, function* () {
            const key = this.createIndexKey(index);
            const cached = this.metaCache.get(key);
            if (cached) {
                return cached;
            }
            const args = {};
            if (index !== undefined) {
                args['index'] = index;
            }
            const { content } = yield this.send_cmd('fetch_meta', args);
            this.metaCache.set(key, content);
            return content;
        });
        this.fetchData = (index, channel) => __awaiter(this, void 0, void 0, function* () {
            const key = channel ? `${index}-${channel}` : `${index}`;
            const cached = this.cache.get(key);
            if (cached) {
                return cached;
            }
            let fetchState = this.fetchStates[key];
            if (!fetchState) {
                fetchState = {
                    callbacks: [],
                };
                this.fetchStates[key] = fetchState;
                const { content, buffers } = yield this.send_cmd('fetch_data', {
                    index,
                    channel,
                });
                const { format = this.get('format') } = content;
                const blob = new Blob(buffers, { type: `video/${format}` });
                this.cache.set(key, blob);
                fetchState.callbacks.forEach((callback) => callback(blob));
                delete this.fetchStates[key];
                return blob;
            }
            else {
                let theResolve = undefined;
                fetchState.callbacks.push((blob) => {
                    if (theResolve) {
                        theResolve(blob);
                    }
                    else {
                        throw new Error('This is impossible! No resovle method found. It seems that the promise is not invoked yet.');
                    }
                });
                return new Promise((resolve) => {
                    theResolve = resolve;
                });
            }
        });
        this.invalidateMeta = (index) => {
            const key = this.createIndexKey(index);
            this.metaCache.delete(key);
        };
        this.setMarkers = (index, markers) => __awaiter(this, void 0, void 0, function* () {
            yield this.send_cmd('set_markers', { index, markers });
            this.invalidateMeta(index);
        });
        this.addMessageHandler('channel_stale', (cmdMsg) => {
            const { args = {} } = cmdMsg;
            const { channel } = args;
            if (channel) {
                for (const key of this.cache.keys()) {
                    if (key.endsWith(`-${channel}`)) {
                        this.cache.delete(key);
                    }
                }
            }
            else {
                this.cache.clear();
            }
            this.triggerRefresh(undefined, channel);
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: RecorderPlayerModel.model_name, _view_name: RecorderPlayerModel.view_name, format: 'mp4', width: '', height: '', autoplay: true, loop: false, controls: true, autonext: true, selected_index: null, selected_channel: null, selected_range: [0, 0] });
    }
}
exports.RecorderPlayerModel = RecorderPlayerModel;
RecorderPlayerModel.model_name = 'RecorderPlayerModel';
RecorderPlayerModel.view_name = 'RecorderPlayerView'; // Set to null if no view
class RecorderPlayerView extends base_1.DOMWidgetView {
    constructor(...args) {
        super(...args);
        this.index = -1;
        this.indexSize = 0;
        this.channel = '';
        this.channels = [];
        this.loading = false;
        this.loadStateOnceCallbacks = [];
        this.selectedRange = [0, 0];
        this.isRangeSelected = () => {
            return this.selectedRange[1] > this.selectedRange[0];
        };
        this.addLoadStateOnceCallback = (callback) => {
            this.loadStateOnceCallbacks.push(callback);
        };
        this.setLoading = (loading) => {
            if (this.loading !== loading) {
                this.loading = loading;
                this.loadStateOnceCallbacks.forEach((callback) => callback(loading));
                this.loadStateOnceCallbacks.splice(0, this.loadStateOnceCallbacks.length);
            }
        };
        this.fetchMeta = (index = undefined) => __awaiter(this, void 0, void 0, function* () {
            const { record_count = 0, chanels = [], markers, statistics, statistics_meta, } = yield this.model.fetchMeta(index);
            this.indexSize = record_count;
            this.channels = chanels;
            this.markers = markers;
            this.statistics = statistics;
            this.statistics_meta = statistics_meta;
        });
        this.initVideo = () => __awaiter(this, void 0, void 0, function* () {
            if (!this.video) {
                this.video = new video_1.Video();
                this.video.addVideoInitHandler((video) => {
                    video.rangeBar.setMarkers(this.markers);
                });
                this.video.addIndexSelectHandler((i) => {
                    this.load(i, undefined);
                });
                this.video.addChannelSelectHandler((channel) => {
                    this.load(undefined, channel, false, true);
                });
                this.video.rangeBar.addRangeSelectedCallback((range) => {
                    var _a;
                    this.selectedRange = range;
                    if (this.isRangeSelected()) {
                        const video = (_a = this.video) === null || _a === void 0 ? void 0 : _a.video;
                        if (video) {
                            video.currentTime = range[0];
                        }
                        this.model.set('selected_index', this.index);
                        this.model.set('selected_channel', this.channel);
                    }
                    else {
                        this.model.set('selected_index', null);
                        this.model.set('selected_channel', null);
                    }
                    this.model.set('selected_range', range);
                    this.model.save_changes();
                });
                this.video.rangeBar.addMarkersChangeCallback((markers) => {
                    this.markers = markers;
                    this.model.setMarkers(this.index, markers);
                });
                this.model.on('change:selected_index', this.onSelectedIndexChange);
                this.model.on('change:selected_channel', this.onSelectedChannelChange);
                this.model.on('change:selected_range', this.onSelectedRangeChange);
                this.video.video.addEventListener('ended', () => __awaiter(this, void 0, void 0, function* () {
                    if (this.isRangeSelected()) {
                        return;
                    }
                    const autonext = this.model.get('autonext');
                    const loop = this.model.get('loop');
                    if (autonext) {
                        if (this.index < this.indexSize - 1) {
                            this.load(this.index + 1, undefined);
                        }
                        else if (this.index === this.indexSize - 1 && loop) {
                            this.load(0, undefined);
                        }
                    }
                }));
                this.video.video.addEventListener('timeupdate', () => {
                    var _a;
                    if (this.isRangeSelected()) {
                        const video = (_a = this.video) === null || _a === void 0 ? void 0 : _a.video;
                        if (video) {
                            if (video.currentTime >= this.selectedRange[1]) {
                                const loop = this.model.get('loop');
                                if (loop) {
                                    video.currentTime = this.selectedRange[0];
                                }
                                else {
                                    video.pause();
                                }
                            }
                        }
                    }
                });
                this.el.appendChild(this.video.container);
                this.update();
                yield this.load(0, '');
            }
        });
        this.onSelectedIndexChange = () => {
            const index = this.model.get('selected_index');
            if (index !== undefined && index !== null && this.index !== index) {
                this.load(index, undefined);
            }
        };
        this.onSelectedChannelChange = () => {
            const channel = this.model.get('selected_channel');
            if (channel && this.channel !== channel) {
                this.load(undefined, channel);
            }
        };
        this.onSelectedRangeChange = () => {
            var _a;
            const range = this.model.get('selected_range');
            if (!utils_1.arrayEqual(this.selectedRange, range)) {
                this.selectedRange = range;
                const rangeBar = (_a = this.video) === null || _a === void 0 ? void 0 : _a.rangeBar;
                if (rangeBar) {
                    rangeBar.selectRange(range);
                }
            }
        };
        this.waitForLoading = (loading) => __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve) => {
                if (this.loading === loading) {
                    resolve();
                }
                else {
                    this.addLoadStateOnceCallback((state) => {
                        if (state === loading) {
                            resolve();
                        }
                    });
                }
            });
        });
        this.load = (index, channel, force = false, resumeTime = false) => __awaiter(this, void 0, void 0, function* () {
            if (this.video) {
                if (typeof index === 'undefined') {
                    index = this.index;
                }
                if (typeof channel === 'undefined') {
                    channel = this.channel;
                }
                if (this.index === index && this.channel === channel && !force) {
                    return;
                }
                yield this.waitForLoading(false);
                this.setLoading(true);
                yield this.fetchMeta(index);
                try {
                    if (this.indexSize > 0) {
                        const blob = yield this.model.fetchData(index, channel);
                        this.video.updateData(blob, resumeTime);
                    }
                    this.index = index;
                    this.channel = channel;
                    this.video.rangeBar.unselectRange();
                    this.video.updateIndexerSize(this.indexSize);
                    this.video.updateIndexerIndex(this.index);
                    this.video.updateChannels(this.channels);
                    this.video.updateStatistics(this.statistics, this.statistics_meta);
                }
                catch (e) {
                    console.error(e);
                }
                finally {
                    this.setLoading(false);
                }
            }
        });
        this.updateWidth = () => {
            var _a, _b;
            const width = this.model.get('width');
            if (width !== undefined && width.length > 0) {
                (_a = this.video) === null || _a === void 0 ? void 0 : _a.video.setAttribute('width', width);
            }
            else {
                (_b = this.video) === null || _b === void 0 ? void 0 : _b.video.removeAttribute('width');
            }
        };
        this.updateHeight = () => {
            var _a, _b;
            const height = this.model.get('height');
            if (height !== undefined && height.length > 0) {
                (_a = this.video) === null || _a === void 0 ? void 0 : _a.video.setAttribute('height', height);
            }
            else {
                (_b = this.video) === null || _b === void 0 ? void 0 : _b.video.removeAttribute('height');
            }
        };
        this.updateOtherVideoAttributes = () => {
            var _a, _b;
            const video = (_a = this.video) === null || _a === void 0 ? void 0 : _a.video;
            if (video) {
                video.autoplay = this.model.get('autoplay') ? true : false;
                if (this.model.get('autonext')) {
                    video.loop = false;
                }
                else {
                    video.loop = this.model.get('loop') ? true : false;
                }
            }
            (_b = this.video) === null || _b === void 0 ? void 0 : _b.enableControls(this.model.get('controls'));
        };
        this.selectedRange = this.model.get('selected_range');
        this.model.addRefereshCallback((i, c) => {
            if (this.index === i &&
                ((!this.channel && !c) || (this.channel && c && this.channel === c))) {
                this.load(undefined, undefined, true);
            }
        });
    }
    render() {
        super.render();
        this.initVideo();
    }
    update() {
        this.updateWidth();
        this.updateHeight();
        this.updateOtherVideoAttributes();
        return super.update();
    }
    remove() {
        var _a;
        this.model.off('change:selected_index', this.onSelectedIndexChange);
        this.model.off('change:selected_channel', this.onSelectedChannelChange);
        this.model.off('change:selected_range', this.onSelectedRangeChange);
        (_a = this.video) === null || _a === void 0 ? void 0 : _a.destroy();
        this.video = undefined;
    }
}
exports.RecorderPlayerView = RecorderPlayerView;
//# sourceMappingURL=recorder.js.map

/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.calcMouseOffsetX = exports.calcPageX = exports.isMac = exports.arrayEqual = exports.arrayRemove = exports.arrayIndexOf = exports.arrayFind = exports.arrayInclude = void 0;
function arrayInclude(arr, target) {
    return !!~arr.indexOf(target);
}
exports.arrayInclude = arrayInclude;
function arrayFind(arr, cond) {
    for (let i = 0; i < arr.length; ++i) {
        const e = arr[i];
        if (cond(e, i)) {
            return e;
        }
    }
    return undefined;
}
exports.arrayFind = arrayFind;
function arrayIndexOf(arr, target) {
    for (let i = 0; i < arr.length; ++i) {
        if (arr[i] === target) {
            return i;
        }
    }
    return -1;
}
exports.arrayIndexOf = arrayIndexOf;
function arrayRemove(arr, target) {
    const index = arrayIndexOf(arr, target);
    if (index !== -1) {
        arr.splice(index, 1);
        return true;
    }
    else {
        return false;
    }
}
exports.arrayRemove = arrayRemove;
function arrayEqual(arr1, arr2) {
    if (arr1 === arr2) {
        return true;
    }
    return (Array.isArray(arr1) &&
        Array.isArray(arr2) &&
        arr1.length === arr2.length &&
        arr1.every((val, index) => val === arr2[index]));
}
exports.arrayEqual = arrayEqual;
function isMac() {
    return window.navigator.userAgent.indexOf('Mac') !== -1;
}
exports.isMac = isMac;
function calcPageX(element) {
    const { left } = element.getBoundingClientRect();
    return left + document.body.scrollLeft;
}
exports.calcPageX = calcPageX;
function calcMouseOffsetX(evt, target) {
    return evt.pageX - calcPageX(target);
}
exports.calcMouseOffsetX = calcMouseOffsetX;
//# sourceMappingURL=utils.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/video.js":
/*!**********************!*\
  !*** ./lib/video.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* eslint-disable @typescript-eslint/no-non-null-assertion */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Video = exports.createVideoContainer = exports.createPlaybackAnimation = exports.createSelectiveUses = exports.makeId = void 0;
__webpack_require__(/*! ../css/video.css */ "./css/video.css");
const charts_1 = __webpack_require__(/*! ./charts */ "./lib/charts.js");
const range_1 = __webpack_require__(/*! ./range */ "./lib/range.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const svgNS = 'http://www.w3.org/2000/svg';
const prefix = 'ipywebcam-video-';
function makeId(id) {
    return `${prefix}${id}`;
}
exports.makeId = makeId;
function createSymbol(id, pathD, viewBox = '0 0 24 24', gTrans = '') {
    const symbol = document.createElementNS(svgNS, 'symbol');
    symbol.id = makeId(id);
    symbol.setAttribute('viewBox', viewBox);
    if (Array.isArray(pathD)) {
        const group = document.createElementNS(svgNS, 'g');
        if (gTrans) {
            group.setAttribute('transform', gTrans);
        }
        for (const p of pathD) {
            const path = document.createElementNS(svgNS, 'path');
            path.setAttribute('d', p);
            group.appendChild(path);
        }
        symbol.appendChild(group);
    }
    else {
        const path = document.createElementNS(svgNS, 'path');
        path.setAttribute('d', pathD);
        symbol.appendChild(path);
    }
    return symbol;
}
function createControlsSvg() {
    const svg = document.createElementNS(svgNS, 'svg');
    svg.id = makeId('icons');
    svg.setAttribute('style', 'display: none');
    const defs = document.createElementNS(svgNS, 'defs');
    svg.appendChild(defs);
    defs.appendChild(createSymbol('pause', 'M14.016 5.016h3.984v13.969h-3.984v-13.969zM6 18.984v-13.969h3.984v13.969h-3.984z'));
    defs.appendChild(createSymbol('play-icon', 'M8.016 5.016l10.969 6.984-10.969 6.984v-13.969z'));
    defs.appendChild(createSymbol('volume-high', 'M14.016 3.234q3.047 0.656 5.016 3.117t1.969 5.648-1.969 5.648-5.016 3.117v-2.063q2.203-0.656 3.586-2.484t1.383-4.219-1.383-4.219-3.586-2.484v-2.063zM16.5 12q0 2.813-2.484 4.031v-8.063q1.031 0.516 1.758 1.688t0.727 2.344zM3 9h3.984l5.016-5.016v16.031l-5.016-5.016h-3.984v-6z'));
    defs.appendChild(createSymbol('volume-low', 'M5.016 9h3.984l5.016-5.016v16.031l-5.016-5.016h-3.984v-6zM18.516 12q0 2.766-2.531 4.031v-8.063q1.031 0.516 1.781 1.711t0.75 2.32z'));
    defs.appendChild(createSymbol('volume-mute', 'M12 3.984v4.219l-2.109-2.109zM4.266 3l16.734 16.734-1.266 1.266-2.063-2.063q-1.547 1.313-3.656 1.828v-2.063q1.172-0.328 2.25-1.172l-4.266-4.266v6.75l-5.016-5.016h-3.984v-6h4.734l-4.734-4.734zM18.984 12q0-2.391-1.383-4.219t-3.586-2.484v-2.063q3.047 0.656 5.016 3.117t1.969 5.648q0 2.203-1.031 4.172l-1.5-1.547q0.516-1.266 0.516-2.625zM16.5 12q0 0.422-0.047 0.609l-2.438-2.438v-2.203q1.031 0.516 1.758 1.688t0.727 2.344z'));
    defs.appendChild(createSymbol('fullscreen', 'M14.016 5.016h4.969v4.969h-1.969v-3h-3v-1.969zM17.016 17.016v-3h1.969v4.969h-4.969v-1.969h3zM5.016 9.984v-4.969h4.969v1.969h-3v3h-1.969zM6.984 14.016v3h3v1.969h-4.969v-4.969h1.969z'));
    defs.appendChild(createSymbol('fullscreen-exit', 'M15.984 8.016h3v1.969h-4.969v-4.969h1.969v3zM14.016 18.984v-4.969h4.969v1.969h-3v3h-1.969zM8.016 8.016v-3h1.969v4.969h-4.969v-1.969h3zM5.016 15.984v-1.969h4.969v4.969h-1.969v-3h-3z'));
    defs.appendChild(createSymbol('pip', 'M21 19.031v-14.063h-18v14.063h18zM23.016 18.984q0 0.797-0.609 1.406t-1.406 0.609h-18q-0.797 0-1.406-0.609t-0.609-1.406v-14.016q0-0.797 0.609-1.383t1.406-0.586h18q0.797 0 1.406 0.586t0.609 1.383v14.016zM18.984 11.016v6h-7.969v-6h7.969z'));
    defs.appendChild(createSymbol('left-arrow', 'M15.293 3.293 6.586 12l8.707 8.707 1.414-1.414L9.414 12l7.293-7.293-1.414-1.414z'));
    defs.appendChild(createSymbol('right-arrow', 'M7.293 4.707 14.586 12l-7.293 7.293 1.414 1.414L17.414 12 8.707 3.293 7.293 4.707z'));
    defs.appendChild(createSymbol('statistics', [
        'M2096 2741 c-15 -10 -37 -32 -47 -47 -18 -28 -19 -65 -19 -984 l0 -955 25 -37 c32 -48 47 -50 268 -46 l179 3 29 33 29 32 0 969 c0 967 0 968 -21 995 -40 50 -64 56 -246 56 -148 0 -171 -2 -197 -19z',
        'M1308 2088 c-30 -8 -41 -18 -58 -52 -19 -41 -20 -58 -20 -643 0 -330 3 -613 6 -629 3 -16 16 -42 30 -59 l24 -30 210 0 210 0 24 30 c14 17 27 43 30 59 3 16 6 299 6 629 0 584 -1 602 -20 643 -18 36 -27 43 -65 53 -53 13 -326 13 -377 -1z',
        'M504 1426 c-64 -28 -64 -28 -64 -373 l0 -313 29 -32 29 -33 179 -3 c221 -4 236 -2 268 46 l25 37 0 293 c0 328 -3 347 -65 376 -44 21 -353 22 -401 2z',
        'M42 468 c-39 -32 -41 -35 -41 -91 -1 -42 3 -59 14 -63 8 -3 17 -13 20 -23 3 -9 18 -24 34 -34 27 -16 124 -17 1431 -17 1307 0 1404 1 1431 17 16 10 31 25 34 34 3 10 12 20 20 23 11 4 15 21 15 58 0 49 -3 56 -40 91 l-40 37 -1419 0 -1419 0 -40 -32z',
    ], '0 0 1000 1000', 'translate(100, 900) scale(0.25, -0.25)'));
    return svg;
}
function createSelectiveUses(active, ...ids) {
    const svg = document.createElementNS(svgNS, 'svg');
    ids.forEach((id) => {
        const use = document.createElementNS(svgNS, 'use');
        use.classList.add(`use-${id}`);
        use.setAttribute('href', `#${makeId(id)}`);
        if (id !== active) {
            use.classList.add('hidden');
        }
        svg.appendChild(use);
    });
    return svg;
}
exports.createSelectiveUses = createSelectiveUses;
function createPlaybackAnimation() {
    const div = document.createElement('div');
    div.id = makeId('playback-animation');
    div.className = 'playback-animation';
    const svg = createSelectiveUses('pause', 'play-icon', 'pause');
    svg.classList.add('playback-icons');
    div.appendChild(svg);
    return div;
}
exports.createPlaybackAnimation = createPlaybackAnimation;
function createVideoProgress() {
    const container = document.createElement('div');
    container.classList.add('video-progress');
    const progress = document.createElement('progress');
    progress.id = makeId('progress-bar');
    progress.classList.add('progress-bar');
    progress.value = progress.max = 0;
    const input = document.createElement('input');
    input.id = makeId('seek');
    input.classList.add('seek');
    input.type = 'range';
    input.value = '0';
    input.min = '0';
    input.step = '1';
    const rangeBar = document.createElement('div');
    rangeBar.setAttribute('draggable', 'false');
    rangeBar.classList.add('range-bar', 'hidden');
    const tooltip = document.createElement('div');
    tooltip.id = makeId('seek-tooltip');
    tooltip.classList.add('seek-tooltip');
    tooltip.innerText = '00:00';
    container.appendChild(progress);
    container.appendChild(input);
    container.appendChild(tooltip);
    container.appendChild(rangeBar);
    return container;
}
function createStatisticsContainer() {
    const container = document.createElement('div');
    container.classList.add('statistics-container', 'hidden', 'unused');
    const svg = document.createElementNS(svgNS, 'svg');
    container.appendChild(svg);
    return container;
}
function createPlaybackButton(options) {
    const button = document.createElement('button');
    button.id = makeId('play');
    button.classList.add('play');
    button.setAttribute('data-title', `Play (${descShortcut(options.shortcuts.play)})`);
    const svg = createSelectiveUses('play-icon', 'play-icon', 'pause');
    svg.classList.add('playback-icons');
    button.appendChild(svg);
    return button;
}
function createVolumeButton(options) {
    const button = document.createElement('button');
    button.id = makeId('volume-button');
    button.classList.add('volume-button');
    button.setAttribute('data-title', `Mute (${descShortcut(options.shortcuts.mute)})`);
    const svg = createSelectiveUses('volume-high', 'volume-mute', 'volume-low', 'volume-high');
    svg.classList.add('volume-icons');
    button.appendChild(svg);
    return button;
}
function createVolumeInput() {
    const input = document.createElement('input');
    input.id = makeId('volume');
    input.classList.add('volume');
    input.value = '1';
    input.type = 'range';
    input.min = '0';
    input.max = '1';
    input.step = '0.01';
    input.setAttribute('data-mute', '0.5');
    return input;
}
function createVolumeControls(options) {
    const container = document.createElement('div');
    container.classList.add('volume-controls');
    const button = createVolumeButton(options);
    container.appendChild(button);
    const input = createVolumeInput();
    container.appendChild(input);
    return container;
}
function createTime() {
    const container = document.createElement('div');
    container.classList.add('time');
    const elapsed = document.createElement('time');
    elapsed.id = makeId('time-elapsed');
    elapsed.classList.add('time-elapsed');
    elapsed.innerText = '00:00';
    container.appendChild(elapsed);
    const span = document.createElement('span');
    span.innerText = ' / ';
    container.appendChild(span);
    const duration = document.createElement('time');
    duration.id = makeId('duration');
    duration.classList.add('duration');
    duration.innerText = '00:00';
    container.appendChild(duration);
    return container;
}
function createLeftControls(options) {
    const container = document.createElement('div');
    container.classList.add('left-controls');
    const playbackButton = createPlaybackButton(options);
    container.appendChild(playbackButton);
    const volumeControls = createVolumeControls(options);
    container.appendChild(volumeControls);
    const time = createTime();
    container.appendChild(time);
    return container;
}
function createIndexSelector() {
    const container = document.createElement('button');
    container.id = makeId('index-selector');
    container.classList.add('index-selector');
    container.classList.add('text-button');
    container.classList.add('hidden');
    container.setAttribute('data-title', 'Select Index');
    const text = document.createElement('div');
    text.classList.add('text');
    container.appendChild(text);
    return container;
}
function createSpeedSelector() {
    const container = document.createElement('button');
    container.id = makeId('speed-selector');
    container.classList.add('speed-selector');
    container.classList.add('text-button');
    container.setAttribute('data-title', 'Select Speed');
    const text = document.createElement('div');
    text.classList.add('text');
    container.appendChild(text);
    return container;
}
function createChannelSelector() {
    const container = document.createElement('button');
    container.id = makeId('channel-selector');
    container.classList.add('channel-selector');
    container.classList.add('text-button');
    container.classList.add('hidden');
    container.setAttribute('data-title', 'Select Channel');
    const text = document.createElement('div');
    text.classList.add('text');
    container.appendChild(text);
    return container;
}
function createStatsSelector() {
    const container = document.createElement('button');
    container.classList.add('stats-selector', 'hidden');
    container.setAttribute('data-title', 'Select Statistics Type');
    const icon = createSelectiveUses('statistics', 'statistics');
    icon.classList.add('icon');
    container.appendChild(icon);
    const text = document.createElement('div');
    text.classList.add('text');
    container.appendChild(text);
    return container;
}
function createPipButton(options) {
    const button = document.createElement('button');
    button.id = makeId('pip-button');
    button.classList.add('pip-button');
    if (!isPipEnabled()) {
        button.classList.add('hidden');
    }
    button.setAttribute('data-title', `PIP (${descShortcut(options.shortcuts.pip)})`);
    const svg = createSelectiveUses('pip', 'pip');
    button.appendChild(svg);
    return button;
}
function createFullscreenButton(options) {
    const button = document.createElement('button');
    button.id = makeId('fullscreen-button');
    button.classList.add('fullscreen-button');
    button.setAttribute('data-title', `Full screen (${descShortcut(options.shortcuts.fullscreen)})`);
    const svg = createSelectiveUses('fullscreen', 'fullscreen', 'fullscreen-exit');
    button.appendChild(svg);
    return button;
}
function createRightControls(options) {
    const container = document.createElement('div');
    container.classList.add('right-controls');
    const statsSelector = createStatsSelector();
    container.appendChild(statsSelector);
    const indexSelector = createIndexSelector();
    container.appendChild(indexSelector);
    const channelSelector = createChannelSelector();
    container.appendChild(channelSelector);
    const speedSelector = createSpeedSelector();
    container.appendChild(speedSelector);
    const pipButton = createPipButton(options);
    container.appendChild(pipButton);
    const fullscreenButton = createFullscreenButton(options);
    container.appendChild(fullscreenButton);
    return container;
}
function createBottomControls(options) {
    const container = document.createElement('div');
    container.classList.add('bottom-controls');
    const leftControls = createLeftControls(options);
    container.appendChild(leftControls);
    const rightControls = createRightControls(options);
    container.appendChild(rightControls);
    return container;
}
function createVideoControls(options) {
    const container = document.createElement('div');
    container.setAttribute('draggable', 'false');
    container.classList.add('video-controls');
    container.tabIndex = 0;
    const videoProgress = createVideoProgress();
    container.appendChild(videoProgress);
    const statistics = createStatisticsContainer();
    container.appendChild(statistics);
    const bottomControls = createBottomControls(options);
    container.appendChild(bottomControls);
    return container;
}
const VIDEO_WORKS = !!document.createElement('video').canPlayType;
function createVideoContainer(options) {
    const container = document.createElement('div');
    container.id = makeId('container');
    container.classList.add('ipywebcam');
    container.classList.add('video-container');
    const playbackAnimation = createPlaybackAnimation();
    container.appendChild(playbackAnimation);
    const video = document.createElement('video');
    video.id = makeId('video');
    video.classList.add('video');
    container.appendChild(video);
    const videoControls = createVideoControls(options);
    container.appendChild(videoControls);
    return container;
}
exports.createVideoContainer = createVideoContainer;
function iconShow(svg, id) {
    const uses = svg.getElementsByTagNameNS(svgNS, 'use');
    for (let i = 0; i < uses.length; ++i) {
        const use = uses[i];
        if (use.classList.contains(`use-${id}`)) {
            use.classList.remove('hidden');
        }
        else {
            use.classList.add('hidden');
        }
    }
}
function isPipEnabled() {
    return !!document.pictureInPictureEnabled;
}
class SelectorPannel {
    constructor(options) {
        this.options = [];
        this.optionButtons = [];
        this.clickHandlers = [];
        this.realClickHandlers = [];
        this.layout = () => {
            const { width, height } = this.container.getBoundingClientRect();
            this.container.style.left = `-${width / 2}px`;
            this.container.style.top = `-${height}px`;
        };
        this.show = () => {
            this.container.classList.remove('hidden');
            this.layout();
            this.container.focus();
        };
        this.hidden = () => {
            this.container.classList.add('hidden');
        };
        this.toggle = () => {
            if (this.container.classList.contains('hidden')) {
                this.show();
            }
            else {
                this.hidden();
            }
        };
        this.findOption = (options, label) => {
            for (let i = 0; i < options.length; ++i) {
                const option = options[i];
                if (option.label === label) {
                    return i;
                }
            }
            return -1;
        };
        this.updateViewAfterSelect = (label) => {
            const index = this.findOption(this.options, label);
            if (index === -1) {
                return;
            }
            this.container.querySelectorAll('button.selector-option').forEach((e) => {
                e.classList.remove('selected');
            });
            const option = this.container.querySelector(`button.selector-option-${index}`);
            if (option) {
                option.classList.add('selected');
            }
        };
        this.select = (label) => {
            const index = this.findOption(this.options, label);
            if (index !== -1) {
                const option = this.options[index];
                (this.clickHandlers || []).forEach((handler) => {
                    handler(option);
                });
                this.updateViewAfterSelect(option.label);
            }
        };
        this.install = (element, handler, initLabel = undefined) => {
            this.trigger = element;
            this.hidden();
            this.addClickHandler(handler);
            element.appendChild(this.container);
            element.addEventListener('click', () => {
                this.toggle();
            });
            if (initLabel) {
                this.select(initLabel);
            }
            return this;
        };
        this.addClickHandler = (handler) => {
            this.clickHandlers.push(handler);
        };
        this.createHandler = (option) => {
            return (evt) => {
                evt.stopPropagation();
                try {
                    this.select(option.label);
                    this.hidden();
                }
                catch (e) {
                    console.error(e);
                }
            };
        };
        this.updateView = (options) => {
            const buttons = this.optionButtons;
            const handlers = this.realClickHandlers;
            const newLen = options.length;
            const oldLen = buttons.length;
            for (let i = 0; i < oldLen; ++i) {
                const button = buttons[i];
                const handler = handlers[i];
                if (i < newLen) {
                    const option = options[i];
                    button.innerText = option.label;
                    button.removeEventListener('click', handler);
                    const newHandler = this.createHandler(option);
                    button.addEventListener('click', newHandler);
                    handlers[i] = newHandler;
                }
                else {
                    button.removeEventListener('click', handler);
                    this.container.removeChild(button);
                }
            }
            if (oldLen > newLen) {
                buttons.splice(newLen, oldLen - newLen);
                handlers.splice(newLen, oldLen - newLen);
            }
            if (oldLen < newLen) {
                for (let i = oldLen; i < newLen; ++i) {
                    const option = options[i];
                    const button = document.createElement('button');
                    button.innerText = option.label;
                    button.classList.add('selector-option');
                    button.classList.add('no-tooltip');
                    button.classList.add(`selector-option-${i}`);
                    button.setAttribute('data-index', `${i}`);
                    const handler = this.createHandler(option);
                    button.addEventListener('click', handler);
                    this.container.appendChild(button);
                    buttons.push(button);
                    handlers.push(handler);
                }
            }
            this.options = options;
        };
        this.container = document.createElement('div');
        this.container.classList.add('selector-panel');
        this.container.classList.add('selector-options');
        this.container.tabIndex = -1;
        this.container.addEventListener('focusout', (evt) => {
            if (!this.container.contains(evt.relatedTarget) &&
                evt.relatedTarget !== this.trigger) {
                this.hidden();
            }
        });
        this.updateView(options);
    }
}
class IndexSelectorPannel {
    constructor(size) {
        this.clickHandlers = [];
        this.realClickHandlers = [];
        this.calcLayout = (pageIndex) => {
            this.row = Math.ceil(this.size / 4);
            this.column = Math.min(this.size, 4);
            this.hasPager = this.row > 6;
            this.pageIndex = pageIndex;
            this.pageSize = Math.ceil(this.size / 24);
            const curRow = this.pageIndex < this.pageSize ? 6 : this.row - (this.pageIndex - 1) * 6;
            this.optionsWidth = this.column * 32 + (this.column - 1) * 6 + 6;
            this.optionsHeight = curRow * 32 + (curRow - 1) * 6 + 6;
            const height = this.optionsHeight + (this.hasPager ? 32 : 0);
            this.container.style.width = `${this.optionsWidth}px`;
            this.container.style.height = `${height}px`;
            this.container.style.left = `${-this.optionsWidth / 2}px`;
            this.container.style.top = `${-height}px`;
        };
        this.show = () => {
            this.container.classList.remove('hidden');
            this.container.focus();
        };
        this.hidden = () => {
            this.container.classList.add('hidden');
        };
        this.toggle = () => {
            if (this.container.classList.contains('hidden')) {
                this.show();
            }
            else {
                this.hidden();
            }
        };
        this.addClickHandler = (handler) => {
            this.clickHandlers.push(handler);
        };
        this.calcPageIndexFromIndex = (index) => {
            if (index < 0 || index >= this.size) {
                throw new Error(`Invalid index ${index}`);
            }
            return Math.ceil((index + 1) / 24);
        };
        this.setSelectIndex = (index) => {
            this.updatePage(this.calcPageIndexFromIndex(index));
            this.selected = index;
            this.container.querySelectorAll('button.selector-option').forEach((e) => {
                e.classList.remove('selected');
            });
            const option = this.container.querySelector(`button.selector-option-${index}`);
            if (option) {
                option.classList.add('selected');
            }
        };
        this.createHandler = (index) => {
            return (evt) => {
                evt.stopPropagation();
                try {
                    (this.clickHandlers || []).forEach((handler) => {
                        handler(index);
                    });
                    this.hidden();
                }
                catch (e) {
                    console.error(e);
                }
            };
        };
        this.updatePage = (pageIndex) => {
            if (pageIndex !== this.pageIndex) {
                this.calcLayout(pageIndex);
                const optNum = this.pageIndex < this.pageSize ? 24 : this.size % 24;
                let len = this.options.children.length;
                let idx = 0;
                for (let i = 0; i < len; ++i) {
                    const child = this.options.children.item(i);
                    if (child === null || child === void 0 ? void 0 : child.classList.contains('selector-option')) {
                        const button = child;
                        const oldHandler = this.realClickHandlers[idx];
                        const dataIdx = idx + (pageIndex - 1) * 24;
                        if (idx < optNum) {
                            const newHandler = (this.realClickHandlers[idx] =
                                this.createHandler(dataIdx));
                            button.removeEventListener('click', oldHandler);
                            button.addEventListener('click', newHandler);
                            button.innerText = `${dataIdx}`;
                            button.className = '';
                            button.classList.add('selector-option');
                            button.classList.add('no-tooltip');
                            button.classList.add(`selector-option-${dataIdx}`);
                            if (dataIdx === this.selected) {
                                button.classList.add('selected');
                            }
                            else {
                                button.classList.remove('selected');
                            }
                            ++idx;
                        }
                        else {
                            button.removeEventListener('click', oldHandler);
                            this.options.removeChild(button);
                            --i;
                            --len;
                        }
                    }
                }
                if (this.realClickHandlers.length > optNum) {
                    this.realClickHandlers.splice(optNum, this.realClickHandlers.length - optNum);
                }
                if (idx < optNum) {
                    for (let i = idx; i < optNum; ++i) {
                        const dataIdx = i + (pageIndex - 1) * 24;
                        const option = document.createElement('button');
                        option.innerText = `${dataIdx}`;
                        option.classList.add('selector-option');
                        option.classList.add('no-tooltip');
                        option.classList.add(`selector-option-${dataIdx}`);
                        if (dataIdx === this.selected) {
                            option.classList.add('selected');
                        }
                        else {
                            option.classList.remove('selected');
                        }
                        option.setAttribute('data-index', `${dataIdx}`);
                        const handler = this.createHandler(dataIdx);
                        this.realClickHandlers.push(handler);
                        option.addEventListener('click', handler);
                        this.options.appendChild(option);
                    }
                }
                if (this.hasPager) {
                    if (this.pager) {
                        if (this.pagerLeft && this.pageIndex <= 1) {
                            this.pagerLeft.classList.add('disabled');
                        }
                        else if (this.pagerLeft) {
                            this.pagerLeft.classList.remove('disabled');
                        }
                        if (this.pagerNumber) {
                            this.pagerNumber.innerText = `${pageIndex} / ${this.pageSize}`;
                        }
                        if (this.pagerRight && this.pageIndex >= this.pageSize) {
                            this.pagerRight.classList.add('disabled');
                        }
                        else if (this.pagerRight) {
                            this.pagerRight.classList.remove('disabled');
                        }
                    }
                    else {
                        this.pager = document.createElement('div');
                        this.pager.classList.add('selector-pager');
                        this.pagerLeft = document.createElement('button');
                        this.pagerLeft.classList.add('page-left');
                        this.pagerLeft.classList.add('no-tooltip');
                        this.pagerLeft.tabIndex = -1;
                        this.pagerLeft.appendChild(createSelectiveUses('left-arrow', 'left-arrow'));
                        if (this.pageIndex <= 1) {
                            this.pagerLeft.classList.add('disabled');
                        }
                        this.pagerLeft.addEventListener('click', (evt) => {
                            evt.stopPropagation();
                            if (this.pageIndex > 1) {
                                this.updatePage(this.pageIndex - 1);
                            }
                        });
                        this.pager.appendChild(this.pagerLeft);
                        this.pagerNumber = document.createElement('div');
                        this.pagerNumber.innerText = `${pageIndex} / ${this.pageSize}`;
                        this.pager.appendChild(this.pagerNumber);
                        this.pagerRight = document.createElement('button');
                        this.pagerRight.classList.add('page-right');
                        this.pagerRight.classList.add('no-tooltip');
                        this.pagerRight.tabIndex = -1;
                        this.pagerRight.appendChild(createSelectiveUses('right-arrow', 'right-arrow'));
                        if (this.pageIndex >= this.pageSize) {
                            this.pagerRight.classList.add('disabled');
                        }
                        this.pagerRight.addEventListener('click', (evt) => {
                            evt.stopPropagation();
                            if (this.pageIndex < this.pageSize) {
                                this.updatePage(this.pageIndex + 1);
                            }
                        });
                        this.pager.appendChild(this.pagerRight);
                        this.container.appendChild(this.pager);
                    }
                }
                else {
                    if (this.pager) {
                        this.container.removeChild(this.pager);
                        this.pager = undefined;
                        this.pagerNumber = undefined;
                    }
                }
            }
        };
        this.updateSize = (size) => {
            if (this.size !== size) {
                this.size = size;
                this.pageIndex = 0;
                this.updatePage(1);
            }
        };
        this.container = document.createElement('div');
        this.container.id = makeId('selector-panel');
        this.container.classList.add('selector-panel');
        this.container.tabIndex = -1;
        this.options = document.createElement('div');
        this.options.classList.add('selector-options');
        this.options.classList.add('grid');
        this.container.appendChild(this.options);
        this.container.addEventListener('focusout', (evt) => {
            if (!this.container.contains(evt.relatedTarget) &&
                evt.relatedTarget !== this.trigger) {
                this.hidden();
            }
        });
        this.updateSize(size);
    }
}
function descShortcut(shortcut) {
    const parts = [];
    if (shortcut.ctrl) {
        parts.push('ctrl');
    }
    if (shortcut.alt) {
        parts.push('alt');
    }
    if (shortcut.shift) {
        parts.push('shift');
    }
    parts.push(shortcut.key);
    return parts.join(' + ');
}
const DEFAULT_OPTIONS = {
    shortcuts: {
        play: 'k',
        mute: 'm',
        fullscreen: 'f',
        pip: 'p',
        range: 'v',
        stats: 's',
    },
};
function makeShortcut(shortcut) {
    if (typeof shortcut === 'string') {
        return {
            key: shortcut,
            ctrl: false,
            alt: false,
            shift: false,
        };
    }
    else {
        return {
            key: shortcut.key,
            ctrl: shortcut.ctrl || false,
            alt: shortcut.alt || false,
            shift: shortcut.shift || false,
        };
    }
}
function makeOptions(otps) {
    const options = Object.assign({}, DEFAULT_OPTIONS, otps);
    options.shortcuts = Object.assign({}, DEFAULT_OPTIONS.shortcuts, otps.shortcuts);
    options.shortcuts.fullscreen = makeShortcut(options.shortcuts.fullscreen);
    options.shortcuts.mute = makeShortcut(options.shortcuts.mute);
    options.shortcuts.pip = makeShortcut(options.shortcuts.pip);
    options.shortcuts.play = makeShortcut(options.shortcuts.play);
    options.shortcuts.range = makeShortcut(options.shortcuts.range);
    options.shortcuts.stats = makeShortcut(options.shortcuts.stats);
    return options;
}
const SpeedOptions = [
    { label: '0.25x', value: 0.25 },
    { label: '0.5x', value: 0.5 },
    { label: '0.75x', value: 0.75 },
    { label: '1.0x', value: 1 },
    { label: '1.25x', value: 1.25 },
    { label: '1.5x', value: 1.5 },
    { label: '1.75x', value: 1.75 },
    { label: '2.0x', value: 2 },
    { label: '2.5x', value: 2.5 },
    { label: '3.0x', value: 3 },
];
class Video {
    constructor(opts = {}) {
        this.indexSelectHandlers = [];
        this.indexerIndex = -1;
        this.indexerSize = 0;
        this.stats = '';
        this.statsData = {};
        this.statsMeta = {};
        this.speed = 1;
        this.channelSelectHandlers = [];
        this.channel = '';
        this.videoInitHandlers = [];
        this.destroy = () => {
            document.removeEventListener('keyup', this.keyboardShortcuts);
            const url = this.video.src;
            this.video.src = '';
            if (url) {
                URL.revokeObjectURL(url);
            }
            this.rangeBar.destroy();
        };
        this.addVideoInitHandler = (handler) => {
            this.videoInitHandlers.push(handler);
        };
        this.removeVideoInitHandler = (handler) => {
            utils_1.arrayRemove(this.videoInitHandlers, handler);
        };
        this.updateStatistics = (statistics = {}, statistics_meta = {}) => {
            this.statsData = statistics;
            this.statsMeta = statistics_meta;
            const keys = Object.keys(statistics);
            if (keys.length > 0) {
                this.statsSelector.classList.remove('hidden');
                this.statsSelectorPannel.updateView(keys.map((key) => ({ label: key, value: key })));
                this.statisticsBar.classList.remove('unused');
                if (!utils_1.arrayInclude(keys, this.stats)) {
                    this.statsSelectorPannel.select(keys[0]);
                }
            }
            else {
                this.statsSelector.classList.add('hidden');
                this.statsSelectorPannel.updateView([]);
                this.statisticsBar.classList.add('unused');
            }
        };
        this.updateChannels = (channels = []) => {
            if (channels.length > 0) {
                this.channelSelector.classList.remove('hidden');
                const options = [{ label: 'Default', value: '' }];
                channels.forEach((channel) => {
                    options.push({ label: channel, value: channel });
                });
                this.channelSelectorPannel.updateView(options);
                if (!utils_1.arrayInclude(channels, this.channel)) {
                    this.channelSelectorPannel.select('Default');
                }
            }
            else {
                this.channelSelector.classList.add('hidden');
                this.channelSelectorPannel.updateView([]);
            }
        };
        this.addChannelSelectHandler = (handler) => {
            this.channelSelectHandlers.push(handler);
        };
        this.updateIndexerSize = (size) => {
            if (!this.indexSelectorPannel) {
                if (size > 0) {
                    this.indexSelectorPannel = new IndexSelectorPannel(size);
                    this.indexSelectorPannel.hidden();
                    this.indexSelectHandlers.forEach((handler) => {
                        var _a;
                        (_a = this.indexSelectorPannel) === null || _a === void 0 ? void 0 : _a.addClickHandler(handler);
                    });
                    this.indexSelectorPannel.trigger = this.indexSelector;
                    this.indexSelector.appendChild(this.indexSelectorPannel.container);
                    this.indexSelector.addEventListener('click', () => {
                        var _a, _b;
                        (_a = this.indexSelectorPannel) === null || _a === void 0 ? void 0 : _a.toggle();
                        const index = this.indexSelector.getAttribute('data-index');
                        if (index) {
                            (_b = this.indexSelectorPannel) === null || _b === void 0 ? void 0 : _b.setSelectIndex(Number.parseInt(index));
                        }
                    });
                    this.indexSelector.classList.remove('hidden');
                }
                else {
                    this.indexSelector.classList.add('hidden');
                }
            }
            else {
                if (size <= 0) {
                    this.indexSelectorPannel.hidden();
                    this.indexSelector.classList.add('hidden');
                }
                else {
                    this.indexSelectorPannel.updateSize(size);
                    this.indexSelector.classList.remove('hidden');
                }
            }
            this.indexerSize = size;
        };
        this.updateIndexerIndex = (index) => {
            var _a;
            const text = this.indexSelector.querySelector('div.text');
            text.innerText = `${index}`;
            this.indexSelector.setAttribute('data-index', `${index}`);
            (_a = this.indexSelectorPannel) === null || _a === void 0 ? void 0 : _a.setSelectIndex(index);
            this.indexerIndex = index;
        };
        this.addIndexSelectHandler = (handler) => {
            this.indexSelectHandlers.push(handler);
            if (this.indexSelectorPannel) {
                this.indexSelectorPannel.addClickHandler(handler);
            }
        };
        this.updateData = (blob, resumeTime = false) => {
            const oldUrl = this.video.src;
            const url = URL.createObjectURL(blob);
            this.video.src = url;
            if (oldUrl) {
                this.video.load();
                if (resumeTime && this.currentTime) {
                    this.video.currentTime = this.currentTime;
                }
                URL.revokeObjectURL(oldUrl);
            }
        };
        this.installSvg = () => {
            const id = makeId('icons');
            const svg = document.getElementById(id);
            if (!svg) {
                document.body.appendChild(createControlsSvg());
            }
        };
        this.togglePlay = () => {
            if (this.video.paused || this.video.ended) {
                this.video.play();
            }
            else {
                this.video.pause();
            }
        };
        this.enableControls = (enabled) => {
            if (enabled) {
                if (VIDEO_WORKS) {
                    this.video.controls = false;
                    this.videoControls.classList.remove('hidden');
                }
                else {
                    this.video.controls = true;
                    this.videoControls.classList.add('hidden');
                }
            }
            else {
                this.video.controls = false;
                this.videoControls.classList.add('hidden');
            }
        };
        this.updatePlayButton = () => {
            const svg = this.playButton.getElementsByClassName('playback-icons')[0];
            const shortcut = descShortcut(this.options.shortcuts.play);
            if (this.video.paused || this.video.ended) {
                iconShow(svg, 'play-icon');
                this.playButton.setAttribute('data-title', `Play (${shortcut})`);
            }
            else {
                iconShow(svg, 'pause');
                this.playButton.setAttribute('data-title', `Pause (${shortcut})`);
            }
        };
        this.initializeVideo = () => {
            const videoDuration = Math.floor(this.video.duration);
            this.seek.setAttribute('max', `${videoDuration}`);
            this.progress.setAttribute('max', `${videoDuration}`);
            const time = formatTime(videoDuration);
            this.duration.innerText = `${time.minutes}:${time.seconds}`;
            this.duration.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`);
            this.rangeBar.max = videoDuration;
            for (const handler of this.videoInitHandlers) {
                handler(this);
            }
            if (this.stats) {
                this.statsSelectorPannel.select(this.stats);
            }
        };
        this.updateCurrentTime = () => {
            this.currentTime = this.video.currentTime;
        };
        // updateTimeElapsed indicates how far through the video
        // the current playback is by updating the timeElapsed element
        this.updateTimeElapsed = () => {
            const time = formatTime(Math.floor(this.video.currentTime));
            this.timeElapsed.innerText = `${time.minutes}:${time.seconds}`;
            this.timeElapsed.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`);
        };
        // updateProgress indicates how far through the video
        // the current playback is by updating the progress bar
        this.updateProgress = () => {
            this.seek.value = `${Math.floor(this.video.currentTime)}`;
            this.progress.value = Math.floor(this.video.currentTime);
        };
        // updateSeekTooltip uses the position of the mouse on the progress bar to
        // roughly work out what point in the video the user will skip to if
        // the progress bar is clicked at that point
        this.updateSeekTooltip = (event) => {
            const skipTo = Math.round((event.offsetX / this.seek.clientWidth) *
                parseInt(this.seek.getAttribute('max') || '0', 10));
            this.seek.setAttribute('data-seek', `${skipTo}`);
            const t = formatTime(skipTo);
            this.seekTooltip.textContent = `${t.minutes}:${t.seconds}`;
            const rect = this.video.getBoundingClientRect();
            this.seekTooltip.style.left = `${event.pageX - rect.left}px`;
        };
        // skipAhead jumps to a different point in the video when the progress bar
        // is clicked
        this.skipAhead = () => {
            const skipTo = this.seek.dataset.seek
                ? this.seek.dataset.seek
                : this.seek.value;
            this.video.currentTime = Number.parseFloat(skipTo);
            this.progress.value = Number.parseFloat(skipTo);
            this.seek.value = skipTo;
        };
        // updateVolume updates the video's volume
        // and disables the muted state if active
        this.updateVolume = () => {
            if (this.video.muted) {
                this.video.muted = false;
            }
            this.video.volume = Number.parseFloat(this.volume.value);
        };
        // updateVolumeIcon updates the volume icon so that it correctly reflects
        // the volume of the video
        this.updateVolumeIcon = () => {
            const shortcut = descShortcut(this.options.shortcuts.mute);
            this.volumeButton.setAttribute('data-title', `Mute (${shortcut})`);
            if (this.video.muted || this.video.volume === 0) {
                this.volumeButton.setAttribute('data-title', `Unmute (${shortcut})`);
                iconShow(this.volumeIcons, 'volume-mute');
            }
            else if (this.video.volume > 0 && this.video.volume <= 0.5) {
                iconShow(this.volumeIcons, 'volume-low');
            }
            else {
                iconShow(this.volumeIcons, 'volume-high');
            }
        };
        // toggleMute mutes or unmutes the video when executed
        // When the video is unmuted, the volume is returned to the value
        // it was set to before the video was muted
        this.toggleMute = () => {
            this.video.muted = !this.video.muted;
            if (this.video.muted) {
                this.volume.setAttribute('data-volume', this.volume.value);
                this.volume.value = '0';
            }
            else {
                this.volume.value = this.volume.dataset.volume || `${this.video.volume}`;
            }
        };
        // animatePlayback displays an animation when
        // the video is played or paused
        this.animatePlayback = () => {
            this.playbackAnimation.animate([
                {
                    opacity: 1,
                    transform: 'scale(1)',
                },
                {
                    opacity: 0,
                    transform: 'scale(1.3)',
                },
            ], {
                duration: 500,
            });
        };
        // toggleFullScreen toggles the full screen state of the video
        // If the browser is currently in fullscreen mode,
        // then it should exit and vice versa.
        this.toggleFullScreen = () => {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            }
            else if (document.webkitFullscreenElement) {
                // Need this to support Safari
                document.webkitExitFullscreen();
            }
            else if (this.container.webkitRequestFullscreen) {
                // Need this to support Safari
                this.container.webkitRequestFullscreen();
            }
            else {
                this.container.requestFullscreen();
            }
        };
        this.isFullscreen = () => {
            return (document.fullscreenElement ||
                document.webkitFullscreenElement ||
                this.container.webkitRequestFullscreen);
        };
        // updateFullscreenButton changes the icon of the full screen button
        // and tooltip to reflect the current full screen state of the video
        this.updateFullscreenButton = () => {
            const shortcut = descShortcut(this.options.shortcuts.fullscreen);
            if (this.isFullscreen()) {
                this.fullscreenButton.setAttribute('data-title', `Exit full screen (${shortcut})`);
                iconShow(this.fullscreenIcons, 'fullscreen-exit');
            }
            else {
                this.fullscreenButton.setAttribute('data-title', `Full screen (${shortcut})`);
                iconShow(this.fullscreenIcons, 'fullscreen');
            }
        };
        // togglePip toggles Picture-in-Picture mode on the video
        this.togglePip = () => __awaiter(this, void 0, void 0, function* () {
            try {
                if (this.video !== document.pictureInPictureElement) {
                    this.pipButton.disabled = true;
                    yield this.video.requestPictureInPicture();
                }
                else {
                    yield document.exitPictureInPicture();
                }
            }
            catch (error) {
                console.error(error);
            }
            finally {
                this.pipButton.disabled = false;
            }
        });
        this.toggleRangeBar = () => {
            this.rangeBar.toggle();
        };
        this.toggleStatisticsBar = () => {
            this.statisticsBar.classList.toggle('hidden');
        };
        // hideControls hides the video controls when not in use
        // if the video is paused, the controls must remain visible
        this.hideControls = () => {
            if (this.video.paused) {
                return;
            }
            this.videoControls.classList.add('hide');
        };
        // showControls displays the video controls
        this.showControls = () => {
            this.videoControls.classList.remove('hide');
        };
        this.isInFocus = () => {
            var _a;
            return ((_a = document.activeElement) === null || _a === void 0 ? void 0 : _a.contains(this.container)) || false;
        };
        // keyboardShortcuts executes the relevant functions for
        // each supported shortcut key
        this.keyboardShortcuts = (event) => {
            if (!this.isInFocus()) {
                return;
            }
            const { key, ctrlKey, altKey, shiftKey } = event;
            const { play, mute, fullscreen, pip, range, stats } = this.options.shortcuts;
            if (key === play.key &&
                (play.ctrl === !!ctrlKey ||
                    play.alt === !!altKey ||
                    play.shift === !!shiftKey)) {
                this.togglePlay();
                this.animatePlayback();
                if (this.video.paused) {
                    this.showControls();
                }
                else {
                    setTimeout(() => {
                        this.hideControls();
                    }, 2000);
                }
            }
            else if (key === mute.key &&
                (mute.ctrl === !!ctrlKey ||
                    mute.alt === !!altKey ||
                    mute.shift === !!shiftKey)) {
                this.toggleMute();
            }
            else if (key === fullscreen.key &&
                (fullscreen.ctrl === !!ctrlKey ||
                    fullscreen.alt === !!altKey ||
                    fullscreen.shift === !!shiftKey)) {
                this.toggleFullScreen();
            }
            else if (key === pip.key &&
                (pip.ctrl === !!ctrlKey ||
                    pip.alt === !!altKey ||
                    pip.shift === !!shiftKey)) {
                this.togglePip();
            }
            else if (key === range.key &&
                (range.ctrl === !!ctrlKey ||
                    range.alt === !!altKey ||
                    range.shift === !!shiftKey)) {
                this.toggleRangeBar();
            }
            else if (key === stats.key &&
                (stats.ctrl === !!ctrlKey ||
                    stats.alt === !!altKey ||
                    stats.shift === !!shiftKey)) {
                this.toggleStatisticsBar();
            }
        };
        this.options = makeOptions(opts);
        this.installSvg();
        this.container = createVideoContainer(this.options);
        this.video = this.container.querySelector('video.video');
        this.videoControls = this.container.querySelector('div.video-controls');
        this.playButton = this.container.querySelector('button.play');
        this.timeElapsed = this.container.querySelector('time.time-elapsed');
        this.duration = this.container.querySelector('time.duration');
        this.progress = this.container.querySelector('progress.progress-bar');
        this.seek = this.container.querySelector('input.seek');
        this.seekTooltip = this.container.querySelector('div.seek-tooltip');
        this.rangeBar = new range_1.RangeBar(this.container.querySelector('div.range-bar'));
        this.statisticsBar = this.container.querySelector('div.statistics-container');
        this.statisticsSvg = this.statisticsBar.querySelector('svg');
        this.volume = this.container.querySelector('input.volume');
        this.volumeButton = this.container.querySelector('button.volume-button');
        this.volumeIcons = this.volumeButton.querySelector('svg');
        this.playbackAnimation = this.container.querySelector('div.playback-animation');
        this.fullscreenButton = this.container.querySelector('button.fullscreen-button');
        this.fullscreenIcons = this.fullscreenButton.querySelector('svg');
        this.pipButton = this.container.querySelector('button.pip-button');
        this.indexSelector = this.container.querySelector('button.index-selector');
        this.statsSelector = this.container.querySelector('button.stats-selector');
        this.statsSelectorPannel = new SelectorPannel([]).install(this.statsSelector, (option) => {
            var _a;
            const text = this.statsSelector.querySelector('div.text');
            text.innerText = option.label;
            this.stats = option.value;
            if (this.video.duration > 0) {
                charts_1.makeLineChart(this.statisticsSvg, this.statsData[this.stats], [0, this.video.duration], (_a = this.statsMeta[this.stats]) === null || _a === void 0 ? void 0 : _a.y_range, this.video.clientWidth - 20, 30);
            }
        });
        this.speedSelector = this.container.querySelector('button.speed-selector');
        this.speedSelectorPannel = new SelectorPannel(SpeedOptions).install(this.speedSelector, (option) => {
            const text = this.speedSelector.querySelector('div.text');
            text.innerText = option.label;
            this.video.playbackRate = option.value;
            this.speed = option.value;
        }, '1.0x');
        this.channelSelector = this.container.querySelector('button.channel-selector');
        this.channelSelectorPannel = new SelectorPannel([]).install(this.channelSelector, (option) => {
            const text = this.channelSelector.querySelector('div.text');
            text.innerText = option.label;
            this.channelSelectHandlers.forEach((handler) => {
                handler(option.value);
            });
            this.channel = option.value;
        });
        this.playButton.addEventListener('click', this.togglePlay);
        this.video.addEventListener('play', this.updateCurrentTime);
        this.video.addEventListener('play', this.updatePlayButton);
        this.video.addEventListener('play', () => {
            this.video.playbackRate = this.speed;
        });
        this.video.addEventListener('pause', this.updatePlayButton);
        this.video.addEventListener('loadedmetadata', this.initializeVideo);
        this.video.addEventListener('timeupdate', this.updateCurrentTime);
        this.video.addEventListener('timeupdate', this.updateTimeElapsed);
        this.video.addEventListener('timeupdate', this.updateProgress);
        this.video.addEventListener('volumechange', this.updateVolumeIcon);
        this.video.addEventListener('click', this.togglePlay);
        this.video.addEventListener('click', this.animatePlayback);
        this.video.addEventListener('mouseenter', this.showControls);
        this.video.addEventListener('mouseleave', this.hideControls);
        this.videoControls.addEventListener('mouseenter', this.showControls);
        this.videoControls.addEventListener('mouseleave', this.hideControls);
        this.seek.addEventListener('mousemove', this.updateSeekTooltip);
        this.seek.addEventListener('input', this.skipAhead);
        this.volume.addEventListener('input', this.updateVolume);
        this.volumeButton.addEventListener('click', this.toggleMute);
        this.fullscreenButton.addEventListener('click', this.toggleFullScreen);
        this.container.addEventListener('fullscreenchange', this.updateFullscreenButton);
        this.pipButton.addEventListener('click', this.togglePip);
        document.addEventListener('keyup', this.keyboardShortcuts);
    }
}
exports.Video = Video;
// formatTime takes a time length in seconds and returns the time in
// minutes and seconds
function formatTime(timeInSeconds) {
    const result = new Date(timeInSeconds * 1000).toISOString().substr(11, 8);
    return {
        minutes: result.substr(3, 2),
        seconds: result.substr(6, 2),
    };
}
//# sourceMappingURL=video.js.map

/***/ }),

/***/ "./lib/webcam.js":
/*!***********************!*\
  !*** ./lib/webcam.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WebCamView = exports.WebCamModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const common_1 = __webpack_require__(/*! ./common */ "./lib/common.js");
const webrtc_1 = __webpack_require__(/*! ./webrtc */ "./lib/webrtc.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const supportsSetCodecPreferences = window.RTCRtpTransceiver &&
    'setCodecPreferences' in window.RTCRtpTransceiver.prototype;
class WebCamModel extends common_1.BaseModel {
    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    constructor(...args) {
        super(...args);
        this.getDevice = (type) => __awaiter(this, void 0, void 0, function* () {
            const stream = yield navigator.mediaDevices.getUserMedia({
                video: type === 'video_input',
                audio: type === 'audio_input' || type === 'audio_output',
            });
            try {
                const n_type = type.replace('_', '');
                const devices = yield navigator.mediaDevices.enumerateDevices();
                return devices.filter((device) => device.kind === n_type && device.deviceId);
            }
            finally {
                stream.getTracks().forEach((track) => track.stop());
            }
        });
        this.resetPeer = () => {
            this.pc = undefined;
            this.client_stream = undefined;
            this.server_stream = undefined;
        };
        this.waitForStateWhen = (checker) => __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve) => {
                const state = this.get('state');
                if (checker(state)) {
                    resolve(state);
                }
                else {
                    const checkState = () => {
                        const state = this.get('state');
                        if (checker(state)) {
                            this.off('change:state', checkState);
                            resolve(state);
                        }
                    };
                    this.on('change:state', checkState);
                }
            });
        });
        this.waitForStateIn = (...states) => __awaiter(this, void 0, void 0, function* () {
            return this.waitForStateWhen((state) => states.indexOf(state) !== -1);
        });
        this.getState = () => this.get('state');
        this.setState = (state) => {
            this.set('state', state);
        };
        this.getConstraints = () => {
            let { video, audio } = this.get('constraints') || { audio: false, video: true };
            const videoId = this.videoInput;
            const audioId = this.audioInput;
            if (audio && audioId) {
                if (typeof audio === 'boolean') {
                    audio = {
                        deviceId: audioId,
                    };
                }
                else {
                    audio.deviceId = audioId;
                }
            }
            if (video && videoId) {
                if (typeof video === 'boolean') {
                    video = {
                        deviceId: videoId,
                    };
                }
                else {
                    video.deviceId = videoId;
                }
            }
            return { video, audio };
        };
        this.closePeer = () => __awaiter(this, void 0, void 0, function* () {
            const state = yield this.waitForStateIn('closed', 'connected', 'error', 'new', 'error');
            if (state === 'new') {
                throw new Error(`This should not happen. We can't close the peer when the state is ${state}. Because at this time, we haven't start the peer.`);
            }
            if (state === 'closed' || state === 'error') {
                return;
            }
            const pc = this.pc;
            if (!pc) {
                this.setState('closed');
                return;
            }
            this.setState('closing');
            try {
                pc.close();
                if (pc.connectionState !== 'closed') {
                    yield new Promise((resolve) => {
                        pc.addEventListener('connectionstatechange', () => {
                            if (pc.connectionState === 'closed') {
                                resolve();
                            }
                        });
                    });
                }
                this.resetPeer();
                this.setState('closed');
            }
            catch (err) {
                this.setState('error');
            }
        });
        this.fetchCodecs = () => {
            const codecs = this.getCodecs();
            this.set('video_codecs', codecs);
            this.save_changes();
        };
        this.getCodecs = () => {
            if (supportsSetCodecPreferences) {
                const { codecs = [] } = RTCRtpSender.getCapabilities('video') || {};
                return codecs
                    .filter((codec) => !utils_1.arrayInclude(['video/red', 'video/ulpfec', 'video/rtx'], codec.mimeType))
                    .map((codec) => {
                    return (codec.mimeType + ' ' + (codec.sdpFmtpLine || '')).trim();
                });
            }
            else {
                return [];
            }
        };
        this.getPeerConfig = () => {
            const config = {};
            const iceServers = this.get('iceServers');
            if (iceServers && iceServers.length > 0) {
                config.iceServers = iceServers.map((server) => {
                    if (typeof server === 'string') {
                        return { urls: server };
                    }
                    else {
                        return server;
                    }
                });
            }
            return config;
        };
        this.syncDevice = (track) => {
            const type = track.kind === 'video' ? 'video_input' : 'audio_input';
            let curDeviceId;
            if (typeof track.getCapabilities !== 'undefined') {
                curDeviceId = track.getCapabilities().deviceId;
            }
            else {
                curDeviceId = track.getSettings().deviceId;
            }
            if (type === 'video_input') {
                this.videoInput = curDeviceId;
            }
            else {
                this.audioInput = curDeviceId;
            }
            this.send_cmd('sync_device', { type, id: curDeviceId }, false);
        };
        this.connect = (video, force_reconnect = false, only_reconnect = false) => __awaiter(this, void 0, void 0, function* () {
            const state = yield this.waitForStateIn('closed', 'connected', 'error', 'new');
            if (state === 'closed' || state === 'error' || state === 'new') {
                if (only_reconnect) {
                    return;
                }
                try {
                    this.setState('connecting');
                    const pc = webrtc_1.createPeerConnection(this.getPeerConfig());
                    this.pc = pc;
                    this.bindVideo(video);
                    pc.addEventListener('connectionstatechange', () => {
                        const state = pc.connectionState;
                        if (state === 'failed' ||
                            state === 'disconnected' ||
                            state === 'closed') {
                            pc.close();
                            if (this.pc === pc) {
                                this.resetPeer();
                            }
                        }
                    });
                    pc.addEventListener('track', (evt) => {
                        if (evt.track.kind === 'video') {
                            console.log('track gotten');
                            this.server_stream = evt.streams[0];
                        }
                    });
                    const stream = yield navigator.mediaDevices.getUserMedia(this.getConstraints());
                    this.client_stream = stream;
                    stream.getTracks().forEach((track) => {
                        this.syncDevice(track);
                        pc.addTrack(track, stream);
                    });
                    yield webrtc_1.negotiate(pc, (offer) => __awaiter(this, void 0, void 0, function* () {
                        console.log(offer);
                        const { content } = yield this.send_cmd('exchange_peer', {
                            desc: offer,
                        });
                        return content;
                    }));
                    const pcState = yield webrtc_1.waitForConnectionState(pc, (state) => state !== 'connecting' && state !== 'new');
                    if (pcState === 'connected') {
                        this.setState('connected');
                    }
                    else {
                        yield this.closePeer();
                    }
                }
                catch (err) {
                    this.setState('error');
                    console.error(err);
                }
            }
            else if (force_reconnect) {
                yield this.closePeer();
                yield this.connect(video, force_reconnect);
            }
            else {
                this.bindVideo(video);
            }
        });
        this.bindVideo = (video) => {
            const pc = this.pc;
            if (!pc || !video) {
                return;
            }
            if (pc.connectionState === 'connected' && this.server_stream) {
                video.srcObject = this.server_stream;
            }
            else {
                const handler = (evt) => {
                    if (evt.track.kind === 'video') {
                        console.log('track gotten');
                        this.server_stream = evt.streams[0];
                        video.srcObject = this.server_stream;
                        pc.removeEventListener('track', handler);
                    }
                };
                pc.addEventListener('track', handler);
            }
        };
        this.fetchCodecs();
        // this.fetchDevices();
        // this.on('change:video_input_device', (...args) => {
        //   console.log('change:video_input_device');
        //   console.log(args);
        //   this.connect(undefined, true, true);
        // });
        // this.on('change:audio_input_device', (...args) => {
        //   console.log('change:audio_input_device');
        //   console.log(args);
        //   this.connect(undefined, true, true);
        // });
        this.on('change:iceServers', () => {
            this.connect(undefined, true, true);
        });
        this.addMessageHandler('request_devices', (cmdMsg) => {
            const { cmd, id, args } = cmdMsg;
            const { type } = args;
            this.getDevice(type).then((devices) => {
                console.log(devices);
                this.send({ ans: cmd, id, res: devices }, {});
            });
        });
        this.addMessageHandler('notify_device_change', (cmdMsg) => {
            const { args } = cmdMsg;
            const { type, change } = args;
            if (type === 'video_input') {
                if (this.videoInput !== change.new) {
                    this.videoInput = change.new;
                    this.connect(undefined, true, true);
                }
            }
            else if (type === 'audio_input') {
                if (this.audioInput !== change.new) {
                    this.audioInput = change.new;
                    this.connect(undefined, true, true);
                }
            }
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: WebCamModel.model_name, _view_name: WebCamModel.view_name, server_desc: null, client_desc: null, iceServers: [], constraints: null, video_codecs: [], video_codec: null, state: 'new', autoplay: true, controls: true, crossOrigin: 'not-support', width: null, height: null, playsInline: true, muted: false });
    }
}
exports.WebCamModel = WebCamModel;
WebCamModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
WebCamModel.model_name = 'WebCamModel';
WebCamModel.view_name = 'WebCamView'; // Set to null if no view
function attachSinkId(element, sinkId) {
    return __awaiter(this, void 0, void 0, function* () {
        if (typeof element.sinkId !== 'undefined') {
            if (sinkId) {
                yield element.setSinkId(sinkId);
            }
        }
        else {
            console.warn('Browser does not support output device selection.');
        }
    });
}
class WebCamView extends base_1.DOMWidgetView {
    render() {
        const video = document.createElement('video');
        video.playsInline = true;
        this.el.appendChild(video);
        this.model.connect(video);
        this.model.on('change:state', () => {
            const model = this.model;
            if (model.getState() === 'connected') {
                model.connect(video);
            }
        });
        const { deviceId } = this.model.get('audio_output_device') || {};
        attachSinkId(video, deviceId);
        this.model.on('change:audio_output_device', () => {
            const { deviceId } = this.model.get('audio_output_device') || {};
            attachSinkId(video, deviceId);
        });
        video.autoplay = this.model.get('autoplay');
        this.model.on('change:autoplay', () => {
            video.autoplay = this.model.get('autoplay');
        });
        video.controls = this.model.get('controls');
        this.model.on('change:controls', () => {
            video.controls = this.model.get('controls');
        });
        const width = this.model.get('width');
        if (width) {
            video.width = width;
        }
        this.model.on('change:width', () => {
            const width = this.model.get('width');
            if (width) {
                video.width = width;
            }
            else {
                video.removeAttribute('width');
            }
        });
        const height = this.model.get('height');
        if (height) {
            video.height = height;
        }
        this.model.on('change:height', () => {
            const height = this.model.get('height');
            if (height) {
                video.height = height;
            }
            else {
                video.removeAttribute('height');
            }
        });
        video.playsInline = this.model.get('playsInline');
        this.model.on('change:playsInline', () => {
            video.playsInline = this.model.get('playsInline');
        });
        video.muted = this.model.get('muted');
        this.model.on('change:muted', () => {
            video.muted = this.model.get('muted');
        });
        const crossOrigin = this.model.get('crossOrigin');
        if (crossOrigin === 'not-support') {
            video.crossOrigin = null;
        }
        else {
            video.crossOrigin = crossOrigin;
        }
        this.model.on('change:crossOrigin', () => {
            const crossOrigin = this.model.get('crossOrigin');
            if (crossOrigin === 'not-support') {
                video.crossOrigin = null;
            }
            else {
                video.crossOrigin = crossOrigin;
            }
        });
    }
}
exports.WebCamView = WebCamView;
//# sourceMappingURL=webcam.js.map

/***/ }),

/***/ "./lib/webrtc.js":
/*!***********************!*\
  !*** ./lib/webrtc.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* eslint-disable @typescript-eslint/no-non-null-assertion */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.negotiate = exports.waitForConnectionState = exports.createPeerConnection = void 0;
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const DEFAULT_ICE_SERVERS = [
    { urls: ['stun:stun.l.google.com:19302'] },
    { urls: ['stun:23.21.150.121'] },
    { urls: ['stun:stun01.sipphone.com'] },
    { urls: ['stun:stun.ekiga.net'] },
    { urls: ['stun:stun.fwdnet.net'] },
    { urls: ['stun:stun.ideasip.com'] },
    { urls: ['stun:stun.iptel.org'] },
    { urls: ['stun:stun.rixtelecom.se'] },
    { urls: ['stun:stun.schlund.de'] },
    { urls: ['stun:stunserver.org'] },
    { urls: ['stun:stun.softjoys.com'] },
    { urls: ['stun:stun.voiparound.com'] },
    { urls: ['stun:stun.voipbuster.com'] },
    { urls: ['stun:stun.voipstunt.com'] },
    { urls: ['stun:stun.voxgratia.org'] },
    { urls: ['stun:stun.xten.com'] },
];
function createPeerConnection(config) {
    const pc = new RTCPeerConnection(Object.assign({}, { iceServers: DEFAULT_ICE_SERVERS }, config || {}));
    pc.addEventListener('connectionstatechange', () => {
        console.log(`connection -> ${pc.connectionState}`);
    }, false);
    // register some listeners to help debugging
    pc.addEventListener('icegatheringstatechange', () => {
        console.log(`iceGathering -> ${pc.iceGatheringState}`);
    }, false);
    pc.addEventListener('iceconnectionstatechange', () => {
        console.log(`iceConnection -> ${pc.iceConnectionState}`);
    }, false);
    pc.addEventListener('signalingstatechange', () => {
        console.log(`signaling -> ${pc.signalingState}`);
    }, false);
    return pc;
}
exports.createPeerConnection = createPeerConnection;
function waitForConnectionState(pc, checker) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve) => {
            if (checker(pc.connectionState)) {
                resolve(pc.connectionState);
            }
            else {
                const checkState = () => {
                    if (checker(pc.connectionState)) {
                        pc.removeEventListener('connectionstatechange', checkState);
                        resolve(pc.connectionState);
                    }
                };
                pc.addEventListener('connectionstatechange', checkState);
            }
        });
    });
}
exports.waitForConnectionState = waitForConnectionState;
function waitIceGathering(pc) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve) => {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            }
            else {
                const checkState = () => {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                };
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    });
}
function negotiate(pc, answerFunc, codec) {
    return __awaiter(this, void 0, void 0, function* () {
        let offer = yield pc.createOffer();
        yield pc.setLocalDescription(offer);
        yield waitIceGathering(pc);
        offer = pc.localDescription;
        if (codec) {
            if (codec.audio && codec.audio !== 'default') {
                offer.sdp = sdpFilterCodec('audio', codec.audio, offer.sdp);
            }
            if (codec.video && codec.video !== 'default') {
                offer.sdp = sdpFilterCodec('video', codec.video, offer.sdp);
            }
        }
        const answer = yield answerFunc(offer);
        yield pc.setRemoteDescription(answer);
    });
}
exports.negotiate = negotiate;
function sdpFilterCodec(kind, codec, realSdp) {
    const allowed = [];
    const rtxRegex = new RegExp('a=fmtp:(\\d+) apt=(\\d+)\\r$');
    const codecRegex = new RegExp('a=rtpmap:([0-9]+) ' + escapeRegExp(codec));
    const videoRegex = new RegExp('(m=' + kind + ' .*?)( ([0-9]+))*\\s*$');
    const lines = realSdp.split('\n');
    let isKind = false;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        }
        else if (lines[i].startsWith('m=')) {
            isKind = false;
        }
        if (isKind) {
            let match = lines[i].match(codecRegex);
            if (match) {
                allowed.push(parseInt(match[1]));
            }
            match = lines[i].match(rtxRegex);
            if (match && utils_1.arrayInclude(allowed, parseInt(match[2]))) {
                allowed.push(parseInt(match[1]));
            }
        }
    }
    const skipRegex = 'a=(fmtp|rtcp-fb|rtpmap):([0-9]+)';
    let sdp = '';
    isKind = false;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        }
        else if (lines[i].startsWith('m=')) {
            isKind = false;
        }
        if (isKind) {
            const skipMatch = lines[i].match(skipRegex);
            if (skipMatch && !utils_1.arrayInclude(allowed, parseInt(skipMatch[2]))) {
                continue;
            }
            else if (lines[i].match(videoRegex)) {
                sdp += lines[i].replace(videoRegex, '$1 ' + allowed.join(' ')) + '\n';
            }
            else {
                sdp += lines[i] + '\n';
            }
        }
        else {
            sdp += lines[i] + '\n';
        }
    }
    return sdp;
}
function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}
//# sourceMappingURL=webrtc.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/video.css":
/*!*************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/video.css ***!
  \*************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "/* ==========================================================================\r\n   #Custom HTML5 Video Player\r\n   ========================================================================== */\r\n\r\n:root {\r\n  --youtube-red: rgb(254, 9, 0);\r\n}\r\n\r\n.ipywebcam.video-container {\r\n  width: 800px;\r\n  border-radius: 4px;\r\n  margin: 0 auto;\r\n  position: relative;\r\n  display: flex;\r\n  flex-direction: column;\r\n  justify-content: center;\r\n}\r\n\r\n.ipywebcam.video-container .video {\r\n  width: 100%;\r\n  height: 100%;\r\n  border-radius: 4px;\r\n}\r\n\r\n.ipywebcam.video-container .video-controls {\r\n  right: 0;\r\n  left: 0;\r\n  padding: 10px;\r\n  position: absolute;\r\n  bottom: 0;\r\n  transition: all 0.2s ease;\r\n  background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.5));\r\n}\r\n\r\n.ipywebcam.video-container .video-controls.hide {\r\n  opacity: 0;\r\n  pointer-events: none;\r\n}\r\n\r\n.ipywebcam.video-container .video-progress {\r\n  position: relative;\r\n  height: 8.4px;\r\n  margin-bottom: 10px;\r\n}\r\n\r\n.ipywebcam.video-container progress {\r\n  -webkit-appearance: none;\r\n  -moz-appearance: none;\r\n  appearance: none;\r\n  border-radius: 2px;\r\n  width: 100%;\r\n  height: 8.4px;\r\n  pointer-events: none;\r\n  position: absolute;\r\n  top: 0;\r\n}\r\n\r\n.ipywebcam.video-container progress::-webkit-progress-bar {\r\n  background-color: #474545;\r\n  border-radius: 2px;\r\n}\r\n\r\n.ipywebcam.video-container progress::-webkit-progress-value {\r\n  background: var(--youtube-red);\r\n  border-radius: 2px;\r\n}\r\n\r\n.ipywebcam.video-container progress::-moz-progress-bar {\r\n  border: 1px solid var(--youtube-red);\r\n  background: var(--youtube-red);\r\n}\r\n\r\n.ipywebcam.video-container .seek {\r\n  position: absolute;\r\n  top: 0;\r\n  width: 100%;\r\n  cursor: pointer;\r\n  margin: 0;\r\n}\r\n\r\n.ipywebcam.video-container .seek:hover+.seek-tooltip {\r\n  display: block;\r\n}\r\n\r\n.ipywebcam.video-container .seek-tooltip {\r\n  display: none;\r\n  position: absolute;\r\n  top: -30px;\r\n  margin-left: -20px;\r\n  font-size: 12px;\r\n  padding: 3px;\r\n  content: attr(data-title);\r\n  font-weight: bold;\r\n  color: #fff;\r\n  background-color: rgba(0, 0, 0, 0.6);\r\n}\r\n\r\n.ipywebcam.video-container .range-bar {\r\n  position: absolute;\r\n  top: 12px;\r\n  width: 100%;\r\n  height: 8.4px;\r\n  background-color: #474545;\r\n  cursor: pointer;\r\n  border-radius: 2px;\r\n  overflow: visible;\r\n}\r\n\r\n.ipywebcam.video-container .range-bar .marker {\r\n  position: absolute;\r\n  width: 4px;\r\n  height: 10px;\r\n  top: -0.8px;\r\n  background-color: rgb(254, 9, 0);\r\n  border-radius: 1px;\r\n}\r\n\r\n.ipywebcam.video-container .range-bar .marker.floating {\r\n  background-color: rgba(254, 9, 0, 0.7);\r\n}\r\n\r\n.ipywebcam.video-container .range-bar .marker.selected {\r\n  background-color: rgba(254, 0, 120, 0.7);\r\n}\r\n\r\n.ipywebcam.video-container .range-bar .range-mask {\r\n  position: absolute;\r\n  height: 8.4px;\r\n  background-color: #00c569;\r\n  cursor: pointer;\r\n  border-radius: 2px;\r\n}\r\n\r\n.ipywebcam.video-container .statistics-container {\r\n  position: relative;\r\n}\r\n\r\n.ipywebcam.video-container .statistics-container svg {\r\n  display: block;\r\n  width: 100%;\r\n  height: 30px;\r\n}\r\n\r\n.ipywebcam.video-container .statistics-container.unused svg {\r\n  display: none;\r\n}\r\n\r\n.ipywebcam.video-container .bottom-controls {\r\n  display: flex;\r\n  justify-content: space-between;\r\n  align-items: center;\r\n}\r\n\r\n.ipywebcam.video-container .left-controls {\r\n  display: flex;\r\n  align-items: center;\r\n  color: #fff;\r\n}\r\n\r\n.ipywebcam.video-container .volume-controls {\r\n  display: flex;\r\n  align-items: center;\r\n  margin-right: 10px;\r\n}\r\n\r\n.ipywebcam.video-container .volume-controls input {\r\n  width: 100px;\r\n  opacity: 1;\r\n  transition: all 0.4s ease;\r\n}\r\n\r\n.ipywebcam.video-container .volume-controls:hover input, .volume-controls input:focus {\r\n  width: 100px;\r\n  opacity: 1;\r\n}\r\n\r\n.ipywebcam.video-container button {\r\n  cursor: pointer;\r\n  position: relative;\r\n  margin-right: 7px;\r\n  font-size: 12px;\r\n  padding: 3px;\r\n  border: none;\r\n  outline: none;\r\n  background-color: transparent;\r\n}\r\n\r\n.ipywebcam.video-container button * {\r\n  pointer-events: none;\r\n}\r\n\r\n.ipywebcam.video-container button:not(.no-tooltip)::before {\r\n  content: attr(data-title);\r\n  position: absolute;\r\n  display: none;\r\n  right: 0;\r\n  top: -50px;\r\n  background-color: rgba(0, 0, 0, 0.6);\r\n  color: #fff;\r\n  font-weight: bold;\r\n  padding: 4px 6px;\r\n  word-break: keep-all;\r\n  white-space: pre;\r\n}\r\n\r\n.ipywebcam.video-container button:not(.no-tooltip):hover::before {\r\n  display: inline-block;\r\n}\r\n\r\n.ipywebcam.video-container .fullscreen-button {\r\n  margin-right: 0;\r\n}\r\n\r\n.ipywebcam.video-container .stats-selector svg.icon {\r\n  display: inline;\r\n  margin-right: 2px;\r\n  vertical-align: middle;\r\n}\r\n\r\n.ipywebcam.video-container .stats-selector div.text {\r\n  display: inline;\r\n  color: #fff;\r\n  vertical-align: middle;\r\n}\r\n\r\n.ipywebcam.video-container .index-selector {\r\n  min-width: 26px;\r\n  height: 26px;\r\n}\r\n\r\n.ipywebcam.video-container .text-button {\r\n  color: #fff;\r\n}\r\n\r\n.ipywebcam.video-container .selector-panel {\r\n  position: absolute;\r\n  border: none;\r\n  border-radius: 4px;\r\n  background: rgba(21, 21, 21, .9);\r\n  padding: 6px 12px;\r\n}\r\n\r\n.ipywebcam.video-container .selector-options {\r\n  display: flex;\r\n  flex-wrap: nowrap;\r\n  flex-direction: column;\r\n}\r\n\r\n.ipywebcam.video-container .selector-options.grid {\r\n  flex-wrap: wrap;\r\n  flex-direction: row;\r\n}\r\n\r\n.ipywebcam.video-container .selector-pager {\r\n  display: flex;\r\n  justify-content: space-between;\r\n  align-items: center;\r\n}\r\n\r\n.ipywebcam.video-container .selector-pager svg {\r\n  width: 20px;\r\n  height: 20px;\r\n}\r\n\r\n.ipywebcam.video-container .selector-pager button.disabled svg {\r\n  fill: #999;\r\n  stroke: #999;\r\n}\r\n\r\n.ipywebcam.video-container .selector-pager button {\r\n  pointer-events: auto;\r\n}\r\n\r\n.ipywebcam.video-container button.selector-option {\r\n  color: #fff;\r\n  min-width: 26px;\r\n  height: 26px;\r\n  margin: 3px;\r\n  pointer-events: auto;\r\n}\r\n\r\n.ipywebcam.video-container button.selector-option .text {\r\n  display: inline-block;\r\n}\r\n\r\n.ipywebcam.video-container button.selector-option:hover {\r\n  background: rgba(120, 120, 120, 0.9);\r\n}\r\n\r\n.ipywebcam.video-container button.selector-option.selected {\r\n  background: rgba(81, 81, 81, 0.9);\r\n}\r\n\r\n.ipywebcam.video-container .pip-button svg {\r\n  width: 26px;\r\n  height: 26px;\r\n}\r\n\r\n.ipywebcam.video-container .playback-animation {\r\n  pointer-events: none;\r\n  position: absolute;\r\n  top: 50%;\r\n  left: 50%;\r\n  margin-left: -40px;\r\n  margin-top: -40px;\r\n  width: 80px;\r\n  height: 80px;\r\n  border-radius: 80px;\r\n  background-color: rgba(0, 0, 0, 0.6);\r\n  display: flex;\r\n  justify-content: center;\r\n  align-items: center;\r\n  opacity: 0;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range] {\r\n  -webkit-appearance: none;\r\n  -moz-appearance: none;\r\n  height: 8.4px;\r\n  background: transparent;\r\n  cursor: pointer;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]:focus {\r\n  outline: none;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]::-webkit-slider-runnable-track {\r\n  width: 100%;\r\n  cursor: pointer;\r\n  border-radius: 1.3px;\r\n  -webkit-appearance: none;\r\n  transition: all 0.4s ease;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]::-webkit-slider-thumb {\r\n  height: 16px;\r\n  width: 16px;\r\n  border-radius: 16px;\r\n  background: var(--youtube-red);\r\n  cursor: pointer;\r\n  -webkit-appearance: none;\r\n  margin-left: -1px;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]:focus::-webkit-slider-runnable-track {\r\n  background: transparent;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range].volume {\r\n  height: 5px;\r\n  background-color: #fff;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range].volume::-webkit-slider-runnable-track {\r\n  background-color: transparent;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range].volume::-webkit-slider-thumb {\r\n  margin-left: 0;\r\n  height: 14px;\r\n  width: 14px;\r\n  background: #fff;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]::-moz-range-track {\r\n  width: 100%;\r\n  height: 8.4px;\r\n  cursor: pointer;\r\n  border: 1px solid transparent;\r\n  background: transparent;\r\n  border-radius: 1.3px;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]::-moz-range-thumb {\r\n  height: 14px;\r\n  width: 14px;\r\n  border-radius: 50px;\r\n  border: 1px solid var(--youtube-red);\r\n  background: var(--youtube-red);\r\n  cursor: pointer;\r\n  margin-top: 5px;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range]:focus::-moz-range-track {\r\n  outline: none;\r\n}\r\n\r\n.ipywebcam.video-container input[type=range].volume::-moz-range-thumb {\r\n  border: 1px solid #fff;\r\n  background: #fff;\r\n}\r\n\r\n.ipywebcam.video-container .hidden {\r\n  display: none;\r\n}\r\n\r\n.ipywebcam.video-container svg {\r\n  width: 28px;\r\n  height: 28px;\r\n  fill: #fff;\r\n  stroke: #fff;\r\n  cursor: pointer;\r\n  vertical-align: middle;\r\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./css/video.css":
/*!***********************!*\
  !*** ./css/video.css ***!
  \***********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./video.css */ "./node_modules/css-loader/dist/cjs.js!./css/video.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipywebcam","version":"0.1.10","description":"A Custom Jupyter Widget Library for Web Camera using WebRTC","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/vipcxj/ipywebcam","bugs":{"url":"https://github.com/vipcxj/ipywebcam/issues"},"license":"BSD-3-Clause","author":{"name":"Xiaojing Chen","email":"vipcxj@126.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/vipcxj/ipywebcam"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipywebcam/labextension","clean:nbextension":"rimraf ipywebcam/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","d3":"^7.8.2","lru-cache":"^7.14.1"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/d3":"^7.4.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipywebcam/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_recorder_js-lib_webcam_js.a60ca36ce337711eb79f.js.map