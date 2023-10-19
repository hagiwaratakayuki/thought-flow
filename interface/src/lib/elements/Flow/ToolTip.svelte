<script>
  import { onMount } from "svelte";
  import Card from "../TextOverview/Card.svelte";
  export let message;
  export let position = { top: 0, left: 0 };
  export let isVisible = false;

  let tip;

  onMount(function () {
    Array.from(document.getElementsByTagName("body"))[0].appendChild(tip);
  });
  $: if (isVisible === false) {
    position = { top: 0, left: 0 };
  }
</script>

<div
  class="bg-black p-1"
  class:hiden={isVisible === false}
  class:visible={isVisible === true}
  style="top:{position.top}; left:{position.left}"
>
  {message}
</div>

<style>
  .visible {
    position: absolute;
    text-align: center;
  }
  .hiden {
    visibility: hidden;
    position: relative;
  }
</style>
