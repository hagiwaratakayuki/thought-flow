<script>
  import Flow from "$lib/elements/Flow.svelte";
  import { all_summary } from "$lib/ml_api/api/text/all_summary";
  import { onMount } from "svelte";

  let res;
  onMount(function () {
    res = load();
  });

  async function load() {
    let maxConnected = -Infinity;
    /**
     * @typedef {import("$lib/ml_api/api_types/TextOverView").TextOverView} TextOverView
     * @type {Array<TextOverView>}
     */
    const overviews = await all_summary();
    /**
     * @type {import("$lib/relay_types/flow").Edges}
     */
    const edges = [];

    for (const overview of overviews) {
      maxConnected = Math.max(maxConnected, overview.linked_count);
      for (const to of overview.link_to || []) {
        edges.push({
          from: overview.id,
          to,
        });
      }
    }
    const maxWeight = Math.log(maxConnected);
    const nodes = overviews.map(function (row) {
      if (row.linked_count === 0) {
        row.weight = 0.1;
      } else {
        row.weight = Math.max(Math.log(row.linked_count) / maxWeight, 0.1);
      }

      row.y = row.position;
      return row;
    });

    return {
      overviews,
      data: {
        nodes,
        edges,
      },
    };
  }
</script>

<div style="width: 100%; height:300px;">
  {#if res}
    {#await res}
      loading
    {:then processed}
      <Flow data={processed.data} />
    {:catch}
      error
    {/await}
  {/if}
</div>
