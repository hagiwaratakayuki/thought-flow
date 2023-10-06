<script>
  import { onMount, tick } from "svelte";
  import { FlowController } from "./flow";
  /**
   * @param {import("src/relay_types/flow").DataTransfer}
   * */
  export let data = {};

  /**
   * @type {SVGAElement | null}
   */
  let svg = null;
  let isClient = false;

  onMount(function () {
    isClient = true;
  });
  $: if (isClient === true) {
    createFlowNetwork(data);
  }

  let controller = null;
  /**
   * @type {HTMLElement | null}
   */
  let container = null;

  /**
   *
   * @param {import("src/relay_types/flow").DataTransfer} data
   */
  function createFlowNetwork(data) {
    controller = new FlowController(container);
    controller.setData(data.nodes, data.edges);
  }
</script>

<div class="container root">
  <div class="container" bind:this={container} />
</div>

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
