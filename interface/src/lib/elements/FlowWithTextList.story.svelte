<script>
  import FlowWithTextList from "./FlowWithTextList.svelte";
  import Layout from "./ComponentLayout.svelte";
  import { onMount } from "svelte";
  import { all_summary } from "$lib/ml_api/api/text/all_summary";
  import Flow from "./Flow/Flow.svelte";
  export let Hst;
  /**
   * @type {FlowWithTextList}
   */
  let flowWithTextList;
  //@todo change to mockdata;
  onMount(async function () {
    const textOverView = await all_summary();
    flowWithTextList.setInitData(textOverView);
  });
</script>

<Hst.Story>
  <Layout>
    <FlowWithTextList bind:this={flowWithTextList} />
  </Layout>
</Hst.Story>
