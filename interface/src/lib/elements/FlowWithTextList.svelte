<script>
  import Flow from "./Flow/Flow.svelte";
  import TextList from "$lib/elements/TextOverview/List.svelte";
  import { Row, Col } from "sveltestrap";
  import { overviews_to_flow } from "./Flow/overviews_to_flow";
  /**
   * @type {TextList}
   * */
  let textList;
  let _flow;
  let _overViews;
  let _isLoading = true;
  let _isError = false;
  let _isNextExist = false;

  export function setInitData(overViews, isNextExist = false) {
    _overViews = overViews;
    _flow = overviews_to_flow(overViews);
    _isLoading = false;
    _isNextExist = isNextExist;
  }
  export function initError() {
    _isLoading = false;
    _isError = true;
  }
  //@todo add flow
  //@todo add additional loading
  export function addOverViews(overViews, isNextExist) {
    if (typeof textList === "undefined") {
      return;
    }
    textList.addOverViews(overViews, isNextExist);
  }
</script>

{#if _isLoading == true}
  loading
{:else if _isError == false}
  <Row id="toppage">
    <Col class="h-100" sm="8">
      <Flow flow={_flow} />
    </Col>
    <Col class="h100 vertical-scroll" sm="4">
      <TextList overViews={_overViews} isNextExist={_isNextExist} />
    </Col>
  </Row>
{:else}
  error
{/if}
