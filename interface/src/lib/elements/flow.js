import * as PIXI from "pixi.js";



let _triangleGrphics = {};

/**
     * 
     * @param {{id?:any, color?:number, width?:number, height?:number| null}} param0
     * @returns {PIXI.Graphics} 
     */

function getTriangleShape({ id = null, color = 0xFF0000, width = 10, height = 10 }) {
    if (id) {
        if (id in _triangleGrphics) {
            return _triangleGrphics[id].clone()
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
        this._scaleCache = {}

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

        const nodes = [{
            id: 1,
            y: 0.5,
            date: '1990/01/01',
            weight: 1
        }, {
            id: 2,
            y: -0.7,
            date: '1990/01/10',
            weight: 0.5
        }];
        const edges = [
            {
                from: 1,
                to: 2
            }

        ];
        this.setData(nodes, edges)
        //this.setTransform({ scaleX: 1 / 30, scaleY: 1 / 30 })





    }
    _initContiners() {
        this._frontContainer = new PIXI.Container()
        this._frontContainer.zIndex = 10;
        this.app.stage.addChild(this._frontContainer);
        this._graphContainer = new PIXI.Container();
        this._graphContainer.zIndex = 10;
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

    }
    onTick() {
        if (this._isTransformed === false) {
            return
        }

        const yPosition = (this.app.screen.height / 2) * (1 - this._transforms.scaleY);
        this._graphContainer.setTransform(0, yPosition, this._transforms.scaleX, this._transforms.scaleY)
        this._isTransformed = false;

        this._graphContainer.position.set(this._transforms.x, this._transforms.y)
        this._scaleContainer.position.set(this._transforms.x, this._scaleContainer.position.y)

        /**
         * @type {{scale:PIXI.Graphics; year:number; month:number;}[]}
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
        const circleArounds = [];
        const isLeft = this._transforms.deltaX < 0;
        const screenRight = this.app.screen.width - this.padding;
        const scaleX = this._transforms.scaleY;

        const padding = this.padding


        let count = 0;
        const step = this.dayStep * this._transforms.scaleX
        const adjest = this._transforms.x % step
        for (const dateScale of this._dateScales) {
            const x = count * step + adjest + padding
            count++;
            dateScale.position.set(x, dateScale.position.y)
            if (x < this.padding) {
                dateScale.visible = false
                if (isLeft === true) {
                    circleArounds.push(dateScale)
                }
                continue;
            }
            if (x > screenRight) {
                dateScale.visible = false;
                if (isLeft === false) {
                    circleArounds.push(dateScale)
                }
                continue;

            }
            dateScale.visible = true;
            keeps.push(dateScale)

        }
        let startX;
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
     * @param {{ date: string; y: number; weight: number; id: any; }[]} nodes
     * @param {{ from: any; to: any; }[]} edges
     */
    setData(nodes, edges) {
        const { nodeGraphics, yearDiff, minYear } = this.addNode(nodes, edges)

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
     * @typedef {{date:string, y:number, weight:number, id:any}} node 
     * @typedef {{from:any, to:any}} edge
     * @param {node[]} nodes 
     * @param {edge[]} edges 
     */
    addNode(nodes, edges) {
        let total = 0;
        const weights = [];
        const index = {};
        let maxYear = 0;
        let minYear = Infinity;
        /**
         * @type {{year:number, month:number, date:number}[]}
         *  */
        const yearMonthDates = [];

        for (const node of nodes) {
            index[node.id] = { node };
            total += node.weight;
            weights.push(node.weight)
            const [year, month, date] = node.date.split('/').map(Number);
            if (year > maxYear) {
                maxYear = year;
            }
            if (year < minYear) {
                minYear = year;
            }
            yearMonthDates.push({ year, month, date })

        }
        const yearDiff = maxYear - minYear || 1;
        const avg = total / nodes.length
        const sigma = Math.sqrt(weights.reduce(function (prev, cur) {
            return prev + Math.pow(cur - avg, 2)

        }, 0) / nodes.length)
        /**
         * @type {[node, {year:number,month:number, date:number}, number][]}
         */
        const nodeDatas = weights.map(function (weight, index) {
            const x = sigma === 0 ? 1 : (weight - avg) / sigma;

            return [nodes[index], yearMonthDates[index], (Math.tanh(x / 2) + 1) / 2]

        });
        const nodeGraphics = []
        for (const [node, yearMonthDate, weight] of nodeDatas) {

            const x = (((yearMonthDate.year - minYear) * 12 + (yearMonthDate.month - 1)) * 31 + yearMonthDate.date) * 20;
            const y = (1 - node.y) * this.app.screen.height / 2;
            const size = (2 + 15 * weight) / 2;
            const graphic = new PIXI.Graphics()
            index[node.id] = Object.assign(index[node.id], { x, y, size })
            graphic.beginFill(0x6C9BD2)
            graphic.drawCircle(x, y, size);
            graphic.endFill()
            this._graphContainer.addChild(graphic)


            nodeGraphics.push({ graphic, node })
        }
        /**
         * @typedef {{x:number,y:number, size:number}} nodePosition
         */
        for (const edge of edges) {
            /**
             * @type {nodePosition}
             */
            const fromData = index[edge.from]
            /**
             * @type {nodePosition}
             */
            const toDdata = index[edge.to]

            const ang = Math.atan((toDdata.y - fromData.y) / (toDdata.x - fromData.x));

            const directinX = toDdata.x > fromData.x ? 1 : -1
            const directinY = toDdata.y > fromData.y ? 1 : -1

            //PIXI のメッシュの座標系は右上起点。回転は時計回り
            //メッシュの底、左右中央をpivotに。90度回転して接続して向きを線の角度に

            const toX = toDdata.x - directinX * Math.cos(ang) * (toDdata.size + 15);
            const toY = toDdata.y - directinY * Math.sin(ang) * (toDdata.size + 15);
            const fromX = fromData.x + directinX * Math.cos(ang) * fromData.size
            const fromY = fromData.y + directinX * Math.sin(ang) * fromData.size;

            const triangle = getTriangleShape({ id: 'santri' })

            triangle.position.set(toX, toY)

            const triAng = (fromData.x < toDdata.x ? Math.PI / -2 : Math.PI / 2) - ang;
            triangle.rotation -= triAng
            const line = new PIXI.Graphics()


            line.lineStyle(this.options.edge.width || 2, this.options.edge.color || 0xdad7d7);
            line.moveTo(fromX, fromY)
            line.lineTo(toX, toY);
            this._graphContainer.addChild(line)
            this._graphContainer.addChild(triangle)





        }

        return { nodeGraphics, yearDiff, minYear };







    }




}