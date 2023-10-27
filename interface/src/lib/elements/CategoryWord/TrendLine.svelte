<script>
  import { Line } from "svelte-chartjs";
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
  } from "chart.js";

  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
  );
  import { onMount } from "svelte";
  /**
   * @typedef {Object.<string, {backgroundColor?:string, borderColor?:string}>} ColorSetting
   */

  let frameHeight;
  let frameWidth;
  /**
   * @type {import('chart.js').Chart}
   */
  let chart;

  /**
   *
   * @param {Object.<string, Array<{datetime:string, score:float}>>}datasMap
   * @param {ColorSetting} colors
   */
  export function setData(datasMap, colors = {}) {
    /**
     * @type {Object.<string, true>}
     */
    let dates = {};

    /**
     * @type {Object.<string,import("chart.js").ChartDataset>}
     */
    let datasetMap = {};

    /**
     * @type {Object.<string, Object.<string, number>>}
     */
    let scoresMap = {};

    for (const [keyword, datas] of Object.entries(datasMap)) {
      const scores = scoresMap[keyword] || {};
      for (const data of datas) {
        dates[data.datetime] = true;

        scores[data.datetime] = data.score;
      }
      scoresMap[keyword] = scores;
    }

    const datesArray = Array.from(Object.keys(dates)).sort();
    const datasetList = [];
    for (const keyword in scoresMap) {
      if (Object.hasOwnProperty.call(scoresMap, keyword)) {
        /**
         * @type {import("chart.js").ChartDataset}
         */
        const dataSet = datasetMap[keyword] || {};
        const scores = scoresMap[keyword] || {};
        const data = [];
        for (const date of datesArray) {
          const score = scores[date];
          data.push(score);
        }
        dataSet.data = data;
        if (keyword in colors) {
          const color = colors;
          if (color.backgroundColor) {
            dataSet.backgroundColor = colors.backgroundColor;
          }
          if (color.borderColor) {
            dataSet.borderColor = colors.borderColor;
          }
        }
        dataSet.label = keyword;
        datasetMap[keyword] = dataSet;
        datasetList.push(dataSet);
      }
    }

    chart.data = {
      labels: datesArray,
      dataset: datasetList,
    };
    chart.update();
  }
</script>

<div
  class="frame"
  bind:clientHeight={frameHeight}
  bind:clientWidth={frameWidth}
>
  <Line bind:chart label={["a", "b", "c"]} />
</div>
