<script>
  import { Button, ListGroup } from "sveltestrap";

  import { createEventDispatcher } from "svelte";
  import { onMount } from "svelte";
  import ListItem from "./ListItem.svelte";
  const dispatcher = createEventDispatcher();
  export let selectedId = "";
  export let overViews = undefined;
  export let isNextExist = false;
  onMount(function () {
    if (typeof overViews !== "undefined") {
      addOverViews(overViews, isNextExist);
    }
  });

  /**
   * @typedef  {import("$lib/ml_api/api_types/TextOverView").TextOverView[]} OverViews
   */
  /**
   *
   * @param {OverViews} overViews
   * @param {bool} isNextExist
   */
  export function addOverViews(overViews, isNextExist) {
    _overviews = overViews.concat(overViews);
    _isNextExist = isNextExist;
  }

  /**
   * @type {OverViews}
   */
  let _overviews = [];
  let _isNextExist = false;
  function _getNext() {
    dispatcher("next");
  }
  function createCheckSeleceted(id) {
    return function () {
      selectedId == id;
    };
  }
</script>

<ListGroup>
  {#each _overviews as overview}
    <ListItem {overview} {selectedId} on:matchSelect />
  {/each}
</ListGroup>

{#if _isNextExist}
  <p class="text-center">
    <Button type="button" color="link" on:click={_getNext}>...more</Button>
  </p>
{/if}
