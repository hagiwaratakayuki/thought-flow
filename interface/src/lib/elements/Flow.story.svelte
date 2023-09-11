<script>
  import Flow from "./Flow.svelte";
  export let Hst;
  /**
   * @type {import("src/relay_types/flow").Flow}
   */
  const flow = [
    {
      id: 0,
      x: 1,
      y: 1,
      size: 1,
      label: "node1",
      color: "blue",
    },
    { id: 1, x: -1, y: -1, size: 3, label: "Mary", color: "red" },
  ];

  /**
   * @type {import("src/relay_types/flow").Edges}
   */
  const edges = [
    {
      from: 0,
      to: 1,
      type: "arrow",
    },
  ];

  const data = {
    flow,
    edges,
  };
</script>

<Hst.Story>
  <div style="width: 100%; height:300px;">
    <Flow {data} />
  </div>
</Hst.Story>
