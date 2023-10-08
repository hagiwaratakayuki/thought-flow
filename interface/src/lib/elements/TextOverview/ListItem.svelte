<script>
  export let selectedId;
  import { createEventDispatcher } from "svelte";

  /**
   * @type  {import("$lib/ml_api/api_types/TextOverView").TextOverView}
   */
  export let overview;
  const dispatcher = createEventDispatcher();
  let element;
  $: {
    if (selectedId === overview) {
      dispatcher("matchSelect", element);
    }
  }
</script>

<li class="list-group-item border-start-0 border-end-0" bind:this={element}>
  <a href="/text/{overview.id}" class:selected={selectedId == overview.id}>
    {overview.body.slice(0, 10)}
  </a>
</li>

<style>
  a {
    text-decoration: none;
    display: inline-block;
  }
  a::before {
    content: "◇";
    margin-right: 1rem;
  }
  li:hover {
    background-color: var(--bs-secondary-bg-subtle);
    border-radius: var(--bs-border-radius-sm);
  }
  a.selected::before {
    content: "●";
    color: var(--bs-teal);
  }
</style>
