<script>
  import FlatHolder from "./FlatHolder.svelte";
  import ComponentLayout from "../ComponentLayout.svelte";
  import { onMount } from "svelte";
  /**
   * @type {FlatHolder}
   */
  let flatHolder;
  export let Hst;
  onMount(function () {
    flatHolder.addOverView(overviews, true);
  });
  function onNext() {
    alert("ok");
  }
  /**
   * @type {import("$lib/ml_api/api_types/TextOverView").TextOverView[]}
   */
  const overviews = [
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
    {
      id: "test",
      body: "loren epsum but efront number",
      author: "fooo hoge fuga",
      published: new Date().toDateString(),
    },
  ];
</script>

<ComponentLayout>
  <Hst.Story>
    <FlatHolder bind:this={flatHolder} on:next={onNext} />
  </Hst.Story>
</ComponentLayout>
