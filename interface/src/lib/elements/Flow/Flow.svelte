<script>
  import { onMount, createEventDispatcher } from "svelte";
  import { FlowController } from "./flow";
  import { browser } from "$app/environment";
  import Tooltip from "./ToolTip.svelte";

  /**
   * @typedef {import("./Flow.event").NodeEventMessage} EventMessage
   */

  const dispatcher = createEventDispatcher();
  /**
   * @param {import("src/relay_types/flow").DataTransfer}
   * */
  export let flow = {};

  let isMounted = false;

  onMount(function () {
    isMounted = true;
  });
  $: if (browser === true && isMounted === true) {
    createFlowNetwork(flow);
  }

  let controller = null;
  /**
   * @type {HTMLElement | null}
   */
  let container = null;
  /**
   * @type {HTMLElement}
   */
  let containerRoot = null;

  let isToolTipVisible = false;
  let tooltipMessage = "";
  let tooltipPosition = { top: 0, left: 0 };

  /**
   *
   * @param {import("src/relay_types/flow").DataTransfer} data
   */
  function createFlowNetwork(data) {
    controller = new FlowController(container);
    controller.setData(data.nodes, data.edges);
    controller.on("node.over", onNodeOver);
    controller.on("node.over.out", onNodeOverOut);
    controller.on("node.click", onNodeClick);
  }
  /**
   * @param {import("./flow").GridInfo} gridInfo
   * @param {MouseEvent} mouseEvent
   */
  function onNodeOver(gridInfo, mouseEvent) {
    isToolTipVisible = true;
    /**
     * @type {EventMessage}
     *
     * */
    const message = { gridInfo, mouseEvent };
    tooltipMessage = `${gridInfo.nodes[0].title.slice(0, 10)}`;
    if (gridInfo.isOverwraped) {
      tooltipMessage += `and ${gridInfo.nodes.length - 1} articles`;
    }

    dispatcher("NodeOver", message);
  }
  /**
   *
   * @param {import("./flow").GridInfo} gridInfo
   * @param {MouseEvent} mouseEvent
   */
  function onNodeOverOut(gridInfo, mouseEvent) {
    isToolTipVisible = false;
    /**
     * @type {EventMessage}
     *
     * */
    const message = { gridInfo, mouseEvent };
    dispatcher("NodeOverOut", message);
  }
  function onNodeClick() {}
</script>

<div class="container root" bind:this={containerRoot}>
  <div class="container" bind:this={container} />
</div>
<Tooltip
  isVisible={isToolTipVisible}
  position={tooltipPosition}
  message={tooltipMessage}
/>

<style>
  .root {
    position: relative;
    top: 0%;
    left: 0%;
  }
  .container {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
</style>
