import * as PIXI from "pixi.js";
/**
 * @typedef {import("$lib/relay_types/flow").Flow} Nodes
*  @typedef {import("$lib/relay_types/flow").Edges} Edges
*  @typedef {import("$lib/relay_types/flow").FlowEntry} Node
   @typedef {Object.<string, Node>} NodeMap 
   @typedef {{nodes:NodeMap}} Colisions
   @typedef  {{        
        nodes:Node[],
        isOverwraped: boolean
   }} GridInfo
   

         
 **/


let _triangleGrphics = {};

/**
     * 
     * @param {{id?:any, color?:number, width?:number, height?:number| null}} param0
     * @returns {PIXI.Graphics} 
     */

function getTriangleShape({ id = null, color = 0xFF0000, width = 10, height = 10 }) {
    if (id) {
        if (id in _triangleGrphics) {
            const ret = _triangleGrphics[id].clone()
            ret.pivot.set(width / 2, height)
            return ret
        }
    }
    const graphics = new PIXI.Graphics()
    graphics.lineStyle(1, color);
    graphics.moveTo(0, height);
    graphics.lineTo(width / 2, 0);
    graphics.moveTo(width / 2, 0);
    graphics.lineTo(width, height);
    graphics.pivot.set(width / 2, height)

    if (id) {

        _triangleGrphics[id] = graphics;
    }
    return graphics











}


const defaultOptions = {
    edge: {
        width: 2,
        color: 0xdad7d7
    }
}

export class FlowController {
    /**
     * 
     * @param {HTMLElement} container
     * @param {Partial<{[key:string]:any, edge:{color?:string, width?:number}, }>} options 
     */
    constructor(container, options = {}) {
        /**
         * @type {PIXI.Application<HTMLCanvasElement>}
         */
        this.app = new PIXI.Application({ antialias: true, backgroundAlpha: 0, resizeTo: container })
        this.app.stage.sortableChildren = true;
        this._gridMap = {};
        /**
         * @type {Object.<string, GridInfo>}
         */
        this._interactiveGrid = {};
        this._initParams();





        this.options = Object.assign({}, defaultOptions, options)


        this.padding = 10;
        this._initTansform()
        this.centerV = this.app.screen.height / 2

        const wheelHandler = this.onZoom.bind(this)
        container.addEventListener('wheel', wheelHandler)
        const onMouseDown = this.onMouseDown.bind(this)
        container.addEventListener('mousedown', onMouseDown)
        const onMouseMove = this.onMouseMove.bind(this)
        container.addEventListener('mousemove', onMouseMove)
        const onMouseUp = this.onMouseUp.bind(this)
        container.addEventListener('mouseup', onMouseUp)
        const onMouseOut = this.onMouseOut.bind(this);
        container.addEventListener('mouseout', onMouseOut)
        this._initEvent()
        this._scaleCache = {}

        this._offset = {
            x: container.parentElement.offsetLeft,
            y: container.parentElement.offsetTop
        }
        this._domContainer = container;



        this.app.ticker.add(this.onTick.bind(this))



        this.zoomLevelStepRatio = 0.3;

        container.appendChild(this.app.view)
        this._isOnDrag = false;




        this.centerHeight = container.clientHeight / 2
        this.dayStep = 30;
        this.dateDysplayLimit = 0.5;
        this.startMonth = 0
        this.startPosition = 10
        this._mousePosition = { x: 0, y: 0 };
        this._initContiners()
        this._initBackGroundScale();

        /**
         * @type {Object.<string, Object.<string, true>>}
         */
        this._edgeMaps = {}




        //this.setTransform({ scaleX: 1 / 30, scaleY: 1 / 30 })





    }
    /**
     * @param {"node.click"} event
     * @param {Function} callback
     */
    _on(event, callback) {
        const callbacks = this._events || [];
        callbacks.push(callback);
        this._events[event] = callbacks

    }
    /**
     * @param {"node.click"} event
     * @param {any} message
     */
    _emit(event, message) {
        const callbacks = this._events[event] || [];
        for (const callback of callbacks) {
            callback(message)
        }


    }


    _initEvent() {
        this._events = {}
    }
    _initContiners() {
        this._frontContainer = new PIXI.Container()
        this._frontContainer.zIndex = 10;
        this.app.stage.addChild(this._frontContainer);
        this._graphContainer = new PIXI.Container();
        this._graphContainer.zIndex = 10;
        this._edgeContainer = new PIXI.Container();
        this._edgeContainer.zIndex = 0;
        this._edgeLineContainer = new PIXI.Container()
        this._edgeLineContainer.zIndex = 0;
        this._edgeContainer.addChild(this._edgeLineContainer)
        this._edgeArrowContainer = new PIXI.Container()
        this._edgeArrowContainer.zIndex = 10;
        this._edgeContainer.addChild(this._edgeArrowContainer)

        this._graphContainer.addChild(this._edgeContainer);
        this._vertexContainer = new PIXI.Container();
        this._vertexContainer.zIndex = 10;
        this._graphContainer.addChild(this._vertexContainer)
        this._graphContainer.sortableChildren = true;
        this._frontContainer.addChild(this._graphContainer)
        this._scaleContainer = new PIXI.Container()
        this._scaleContainer.zIndex = 0;
        this._frontContainer.addChild(this._scaleContainer)
        this._backgroundContainer = new PIXI.Container()
        this._backgroundContainer.zIndex = 0;
        this._backgroundContainer.sortableChildren = true;
        this.app.stage.addChild(this._backgroundContainer)
        this._dateScaleContainer = new PIXI.Container();
        this._dateScaleContainer.zIndex = 1
        this._backgroundContainer.addChild(this._dateScaleContainer)

    }

    _initTansform() {
        this._isTransformed = false;
        this._transforms = {
            x: 0,
            y: 0,
            scaleX: 1,
            scaleY: 1,
            deltaX: 0,

        }

    }
    /**
     * @param {{x?:number, y?:number, scaleX?:number, scaleY?:number}} arg 
     */
    setTransform(arg) {


        this._transforms.x += arg.x || 0;
        this._transforms.y += arg.y || 0;
        this._transforms.deltaX = arg.x || 0;


        const scaleX = this._transforms.scaleX + arg.scaleX || 0
        const scaleY = this._transforms.scaleY + arg.scaleY || 0



        if (arg.scaleX && scaleX >= 1 / 30 && arg.scaleY && scaleY >= 1 / 30) {
            this._transforms.scaleX = scaleX;
            this._transforms.scaleY = scaleY
            this._isTransformed = true;
        }

        if (arg.x && arg.y) {

            this._isTransformed = true;


        }

    }
    /**
     * 
     * @param {WheelEvent} event 
     */
    onZoom(event) {
        event.preventDefault();
        const direction = event.deltaY >= 0 ? -1 : 1;
        let zoomDelta = direction * this.zoomLevelStepRatio;


        const scaleX = zoomDelta;
        const scaleY = zoomDelta;



        this.setTransform({ scaleX, scaleY })




    }
    /**
     * 
     * @param {MouseEvent} event 
     */
    onMouseDown(event) {
        this._isOnDrag = true
        this._mousePosition = { x: event.clientX, y: event.clientY }
        this._emitNodeClick(event)



    }
    /**
     * @param {Function} callback
     */
    onNodeClick(callback) {
        this._on('node.click', callback)
    }
    /**
     * @param {MouseEvent} event
     */
    _emitNodeClick(event) {

        const x = (event.clientX - this._offset.x - this._transforms.x) / this._transforms.scaleX
        const y = (event.clientY - this._offset.y - this._graphContainerAdjast.y) / this._transforms.scaleY;

        const grid = this._getGridFromAxis(x, y);

        if (grid in this._interactiveGrid) {

            this._emit('node.click', this._interactiveGrid[grid])
        }
    }
    onMouseOut() {
        this._isOnDrag = false
    }
    onMouseUp() {
        this._isOnDrag = false;
    }
    /**
     * 
     * @param {MouseEvent} event 
     */
    onMouseMove(event) {

        if (this._isOnDrag === false) {
            return
        }

        this.setTransform({
            x: event.clientX - this._mousePosition.x,
            y: event.clientY - this._mousePosition.y
        });
        this._mousePosition = { x: event.clientX, y: event.clientY }




    }
    destroy() {
        this.app.destroy()


        //this._domContainer.removeEventListener('wheel', this._wheelHandler)
        this._domContainer = null;
        this._initParams()

    }
    _initParams() {
        this._graphContainerAdjast = { y: 0 }
    }
    onTick() {
        if (this._isTransformed === false) {
            return
        }

        const yAdjast = (this.app.screen.height / 2) * (1 - this._transforms.scaleY);
        this._graphContainer.setTransform(0, yAdjast, this._transforms.scaleX, this._transforms.scaleY)
        this._isTransformed = false;

        this._graphContainer.position.set(this._transforms.x, this._transforms.y)
        this._scaleContainer.position.set(this._transforms.x, this._scaleContainer.position.y)
        this._graphContainerAdjast.y = this._transforms.y + yAdjast;
        /**
         * @type {{scale:PIXI.Container; year:number; month:number;}[]}
         */
        const scales = this._yearMonthScales
        if (this._transforms.scaleX !== 1) {
            for (const { scale, year, month } of scales) {
                const newX = this._calicurateX(year, month, 0, this._transforms.scaleX)
                scale.position.set(newX, scale.position.y)

                if (newX + this._transforms.x < this.padding) {
                    scale.visible = false
                }
                else {
                    scale.visible = true
                }


            }
        }

        this._circulerDayScale()
    }
    _circulerDayScale() {
        /**
         * @type {PIXI.Graphics[]}
         */
        const keeps = [];
        /**
         * @type {PIXI.Graphics[]}
         */
        const circleArounds = [];
        const isLeft = this._transforms.deltaX < 0;
        const screenRight = this.app.screen.width - this.padding;
        const scaleX = this._transforms.scaleX;

        const padding = this.padding


        let count = 0;
        const step = this.dayStep * this._transforms.scaleX

        const adjest = this._transforms.x % step
        for (const dateScale of this._dateScales) {
            const x = count * step + adjest + padding
            count++;
            dateScale.position.set(x, dateScale.position.y)
            if (x < this.padding || x > screenRight) {

                dateScale.visible = false;

                circleArounds.push(dateScale)

                continue;

            }
            dateScale.visible = true;
            keeps.push(dateScale)

        }
        let startX;

        while (circleArounds.length > 0 && (keeps.length === 0 || keeps[keeps.length - 1].x < screenRight)) {

            const x = keeps.length * step + adjest + padding
            const circleAround = circleArounds.shift()
            circleAround.x = x;
            circleAround.visible = true;


            keeps.push(circleAround);

        }


        if (keeps.length === 0) {
            startX = padding;
        }
        else {
            const targetIndex = isLeft ? keeps.length - 1 : 0;
            startX = keeps[targetIndex].position.x
            if (targetIndex === 0) {
                startX -= circleArounds.length * step;
            }

        }

        count = 1;
        const directionX = isLeft === true ? 1 : -1;

        for (const circleAround of circleArounds) {
            const x = startX + this.dayStep * scaleX * count * directionX;

            circleAround.position.set(x, circleAround.position.y);
            count += 1;
        }
        if (isLeft === true) {
            this._dateScales = keeps.concat(circleArounds)
        }
        else {
            this._dateScales = circleArounds.concat(keeps)
        }





    }

    /**
     * @param {Nodes} nodes
     * @param {Edges} edges
     */
    setData(nodes, edges) {
        const { yearDiff, minYear } = this.addNode(nodes, edges)

        this._createForegroundScale(yearDiff);
        this._createSubscale(minYear, yearDiff)


    }
    /**
     * @param {number} yearDiff
     */
    _createForegroundScale(yearDiff) {

        let lineHeight = null;

        this._monthScaleContainer = new PIXI.Container();
        this._yearScaleContainer = new PIXI.Container()
        /**
         * @type {{ scale: PIXI.Container; month:number; year:number; }[]}
         */
        this._yearMonthScales = [];




        for (let year = 0; year < yearDiff; year++) {
            for (let month = 0; month < 12; month++) {
                /**
                * @type {PIXI.Container}
                */
                let scaleContainer;


                const x = this._calicurateX(year, month, 0, 1)
                let scaleType;
                if (month === 0) {
                    scaleType = 'year';

                    scaleContainer = this._yearScaleContainer;

                    lineHeight = 10;



                }
                else {
                    scaleType = 'month';
                    scaleContainer = this._monthScaleContainer
                    lineHeight = 8;

                }
                const scale = this._createScale(x, lineHeight, scaleType)




                scaleContainer.addChild(scale)
                this._yearMonthScales.push({ scale, year, month });


            }




        }
        this._scaleContainer.addChild(this._yearScaleContainer, this._monthScaleContainer)
        const centerScale = new PIXI.Graphics()
        centerScale.lineStyle(4, 0x994233);
        centerScale.moveTo(5, this.centerV);
        centerScale.lineTo(this.app.screen.width - 5, this.centerV);
        this.app.stage.addChild(centerScale);



    }
    _initBackGroundScale() {
        const repeatCount = this.app.screen.width / (this.dayStep / 3)

        /**
         * @type {PIXI.Graphics[]}
         */
        this._dateScales = []
        for (let index = 0; index < repeatCount; index++) {
            const x = index * this.dayStep + this.padding;

            const scale = this._createScale(x, 6, 'day')
            this._dateScaleContainer.addChild(scale)
            this._dateScales.push(scale)





        }



    }

    /**
     * @param {number} x
     * @param {number} lineHeight
     * @param {string} scaleType
     * @returns {PIXI.Graphics}
     
     */
    _createScale(x, lineHeight, scaleType) {
        if ((scaleType in this._scaleCache) === false) {

            const scale = new PIXI.Graphics()
            scale.lineStyle(1, 0xdad7d7);
            scale.moveTo(0, 5)
            scale.lineTo(0, 10 + lineHeight);
            /*scale.lineStyle(circleR + 1, 0xFFFFFF)
            scale.beginFill(0x994233);
            scale.drawCircle(0, this.centerV, 6);
            scale.endFill();
            */

            this._scaleCache[scaleType] = scale;

        }
        const clone = this._scaleCache[scaleType].clone()
        clone.position.set(x, 0);
        return clone;


    }
    /**
     * 
     * @param {number} minYear 
     * @param {number} yearDiff 
     */
    _createSubscale(minYear, yearDiff) {
        let scaleContainer;
        let lineHeight;
        const style = new PIXI.TextStyle({
            fontFamily: 'Arial',
            fontSize: 14,
            fill: ['#000000'],
        });
        for (let yearStep = 0; yearStep < yearDiff; yearStep++) {
            const year = minYear + yearStep;
            for (let month = 0; month < 12; month++) {

                const x = this._calicurateX(yearStep, month, 0, 1)
                let scaleType;
                if (month === 0) {
                    scaleType = 'year';

                    scaleContainer = this._yearScaleContainer;

                    lineHeight = 10;



                }
                else {
                    scaleType = 'month';
                    scaleContainer = this._monthScaleContainer
                    lineHeight = 8;

                }

                const scale = this._createScale(0, lineHeight, scaleType)
                const label = new PIXI.Text(`${year}/${String(month + 1).padStart(2, '0')}`, style)
                label.position.set(5, 5)
                const wrapContainer = new PIXI.Container()

                wrapContainer.addChild(scale)
                wrapContainer.addChild(label)
                wrapContainer.position.set(x, this.app.screen.height - 15 - lineHeight);
                scaleContainer.addChild(wrapContainer)
                this._yearMonthScales.push({ scale: wrapContainer, year: yearStep, month });
            }

        }

    }
    /**
     * @param {number} yearDiff
     * @param {number} month
     * @param {number?} date
     * @param {number} scaleRatio
     */
    _calicurateX(yearDiff, month, date = 0, scaleRatio = 1) {
        return (yearDiff * 365 + month * 31 + date) * this.dayStep * scaleRatio + this.padding
    }
    /**
     
     * @param {Nodes} nodes 
     * @param {Edges} edges 
     */
    addNode(nodes, edges) {
        let total = 0;
        const weights = [];
        /**
         * @typedef {Node & {x?:number,y?:number, size?:number, grids?:Object.<string, true>}} nodePosition
         * @type {Object.<string, nodePosition>}        
         * */
        const index = {};
        let maxYear = 0;
        let minYear = Infinity;
        /**
         * @type {{year:number, month:number, date:number}[]}
         *  */
        const yearMonthDates = [];
        const pt = /\d+/g

        for (const node of nodes) {
            index[node.id] = node;
            total += node.weight;
            weights.push(node.weight)


            const [year, month, date] = Array.from(node.published.matchAll(pt)).map(Number);
            if (year > maxYear) {
                maxYear = year;
            }
            if (year < minYear) {
                minYear = year;
            }
            yearMonthDates.push({ year, month, date })

        }
        if (!this._minYear) {
            this._minYear = minYear
        }
        const yearDiff = maxYear - minYear || 1;
        const avg = total / nodes.length
        const sigma = Math.sqrt(weights.reduce(function (prev, cur) {
            return prev + Math.pow(cur - avg, 2)

        }, 0) / nodes.length)
        /**
         * @type {[Node, {year:number,month:number, date:number}, number][]}
         */
        const nodeDatas = weights.map(function (weight, index) {
            const x = sigma === 0 ? 1 : (weight - avg) / sigma;

            return [nodes[index], yearMonthDates[index], (Math.tanh(x / 2) + 1) / 2]

        });
        /**
         * @type {Object.<string,PIXI.DisplayObject>}
         */

        const nodeGraphics = {};




        for (const [node, yearMonthDate, weight] of nodeDatas) {

            //当たり判定と重複処理
            const x = (((yearMonthDate.year - minYear) * 12 * 31 + (yearMonthDate.month - 1)) * 31 + yearMonthDate.date) * 20;

            const y = (1 - node.y) * this.app.screen.height / 2;

            const size = (5 + 15 * weight) / 2;





            const end = y + size;
            let _y = y - size;
            /**
             * @type {Object.<string, true>}
             */
            const grids = {};
            while (_y < end) {
                const grid = [yearMonthDate.year, yearMonthDate.month, yearMonthDate.date, Math.floor(_y / 5)].join('_');

                _y += 5;
                grids[grid] = true


                const interactiveData = this._interactiveGrid[grid] || {
                    nodes: [],
                    isOverwraped: false


                }
                interactiveData.nodes.push(node)
                if (interactiveData.isOverwraped === false) {
                    interactiveData.isOverwraped = grid in this._interactiveGrid;
                }
                this._interactiveGrid[grid] = interactiveData

            }
            index[node.id] = Object.assign(node, { x, y, size, grids })

            //@todo 中心を基準に並び順を変更
            //@task ズームした時の大きさを変わらないように(保留。年モード→月モード→日モード(チャットのみ?))
            const graphic = new PIXI.Graphics()


            graphic.beginFill("#0683c9ff")
            graphic.drawCircle(x, y, size);
            graphic.endFill();
            nodeGraphics[node.id] = graphic





        }

        const nodeGraphicsArr = Array.from(Object.values(nodeGraphics))

        if (nodeGraphicsArr.length > 0) {
            this._vertexContainer.addChild(...Array.from(Object.values(nodeGraphics)))

        }



        const edgeLines = [];
        const edgeArrows = [];

        for (const edge of edges) {
            /**
             * @type {nodePosition}
             */
            const fromData = index[edge.from]
            /**
             * @type {nodePosition}
             */
            const toData = index[edge.to]
            if (!fromData || !toData) {
                continue;
            }

            let isColide = false;
            for (const grid of Object.keys(fromData.grids)) {
                if (toData.grids[grid] === true) {
                    isColide = true;
                    break;
                }
            }
            if (isColide === true) {
                continue;
            }
            let isEdgeExist = false;
            let isReverseEdge = false;
            for (const fromGrid in fromData.grids) {
                let edgeMap = this._edgeMaps[fromGrid] || {};
                for (const toGrid in toData.grids) {
                    isEdgeExist = isEdgeExist || edgeMap[toGrid] == true;
                    isReverseEdge = isReverseEdge || (this._edgeMaps[toGrid] || {})[fromGrid] == true;
                    isEdgeExist = isEdgeExist || isReverseEdge
                    edgeMap[toGrid] = true;
                }
                this._edgeMaps[fromGrid] = edgeMap
            }
            if (isEdgeExist === true && isReverseEdge === false) {
                continue;
            }





            const vecX = toData.x - fromData.x;
            const vecY = toData.y - fromData.y;
            const vecLength = (vecX ** 2 + vecY ** 2) ** 0.5
            const toGap = toData.size + 15
            const toX = toData.x - vecX * toGap / vecLength;
            const toY = toData.y - vecY * toGap / vecLength;
            const antiLock = toData.y > fromData.y ? -1 : 1
            const ang = antiLock * Math.acos((toData.x - fromData.x) / vecLength);

            //PIXI のメッシュの座標系は右上起点。回転は時計回り
            //メッシュの底、左右中央をpivotに。90度回転して接続して向きを線の角度に



            const fromGap = fromData.size + 5
            const fromX = fromData.x + vecX * fromGap / vecLength
            const fromY = fromData.y + vecY * fromGap / vecLength



            const triangle = getTriangleShape({ id: 'santri' })

            triangle.position.set(toX, toY)

            if (isEdgeExist === false) {
                const line = new PIXI.Graphics();
                line.lineStyle(this.options.edge.width || 2, this.options.edge.color || 0xdad7d7);
                line.moveTo(fromX, fromY)
                line.lineTo(toX, toY);
                edgeLines.push(line);


            }

            const triAng = ang - Math.PI / 2;
            triangle.rotation -= triAng;
            edgeArrows.push(triangle)




        }
        this._edgeLineContainer.addChild(...edgeLines)
        this._edgeArrowContainer.addChild(...edgeArrows)
        return { nodeGraphics, yearDiff, minYear };







    }
    /**
     * @param {number} x
     * @param {number} y
     */
    _getGridFromAxis(x, y) {
        const baseX = x / 20;
        const yearDiff = 12 * 31;
        const monthDiff = 31;
        const year = Math.floor(baseX / yearDiff) + this._minYear;
        const month = Math.ceil(Math.abs(baseX % yearDiff) / 31);
        const date = Math.ceil(Math.abs(baseX % yearDiff) % monthDiff);


        return this._getGrid(year, month, date, y);


    }
    /**
     * @param {number} year
     * @param {number} month
     * @param {number} date
     * @param {number} y
     */
    _getGrid(year, month, date, y) {
        return [year, month, date, Math.floor(y / 5)].join('_');
    }


}