<script>
  import TopPage from "./+page.svelte";
  import ComponentLayout from "$lib/elements/ComponentLayout.svelte";
  export let Hst;
</script>

<Hst.Story>
  <ComponentLayout>
    <TopPage />
  </ComponentLayout>
</Hst.Story>
