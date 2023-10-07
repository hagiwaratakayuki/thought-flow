<script>
  import { onMount, tick } from "svelte";
  import { FlowController } from "./flow";
  import { browser } from "$app/environment";

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
