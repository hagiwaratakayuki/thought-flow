<script>
  import { onMount, tick } from "svelte";
  import Card from "../TextOverview/Card.svelte";
  export let message;
  export let top = 0;
  export let left = 0;
  export let isVisible = false;

  let _framePosition = { top: 0, left: 0 };

  /**
   * @type {HTMLElement}
   */
  export let flowElement;
  /**
   * @type {HTMLElement}
   */
  let frameElement;
  let tip;
  /**
   * @typedef {"left" | "right" | "top" | "down"} ArrowDirection
   * @type {ArrowDirection}
   */
  let arrowDirection = "down";
  /**
   * @type {HTMLElement}
   */
  let arrowElement;
  const maxRadius = 10;
  const padding = 10;

  /**
   * @type {Object.<ArrowDirection, Function>}
   */
  const arrowDirections = {
    left: function () {
      if (
        left - frameElement.getBoundingClientRect().width / 2 <
        flowElement.clientLeft
      ) {
        _framePosition.top =
          top - frameElement.getBoundingClientRect().height / 2;
        _framePosition.left = left + maxRadius + padding;
        return true;
      }
      return false;
    },
    right: function () {
      if (
        left + frameElement.getBoundingClientRect().width / 2 >
        flowElement.clientLeft + flowElement.getBoundingClientRect().width
      ) {
        _framePosition.top =
          top - frameElement.getBoundingClientRect().height / 2;
        _framePosition.left =
          left -
          (maxRadius + padding) -
          frameElement.getBoundingClientRect().width;
        return true;
      }
      return false;
    },
    top: function () {
      if (
        top -
          (maxRadius + padding) -
          frameElement.getBoundingClientRect().height -
          arrowElement.clientHeight <
        flowElement.clientTop
      ) {
        _framePosition.top =
          top +
          (maxRadius + padding) +
          frameElement.getBoundingClientRect().height;
        _framePosition.left =
          left -
          (maxRadius + padding) -
          frameElement.getBoundingClientRect().width / 2;
        return true;
      }
      return false;
    },
    down: function () {
      _framePosition.top =
        top -
        (maxRadius + padding) +
        frameElement.getBoundingClientRect().height;
      _framePosition.left =
        left -
        (maxRadius + padding) -
        frameElement.getBoundingClientRect().width / 2;
      return true;
    },
  };

  onMount(function () {
    tick(function () {
      Array.from(document.getElementsByTagName("body"))[0].appendChild(tip);
    });
  });
  $: if (isVisible === false) {
    _framePosition = { top: -10000, left: -10000 };
  }

  $: if (isVisible === true) {
    tick(function () {
      for (const [direction, func] of Object.entries(arrowDirections)) {
        if (func() === true) {
          arrowDirection = direction;
          break;
        }
      }
    });
  }
</script>

<div
  class:hiden={isVisible === false}
  class:visible={isVisible === true}
  class="tooltip-frame"
  bind:this={frameElement}
  style="top:{position.top}px; left:{position.left}px;"
>
  <div class="text-white bg-black p-1" bind:this={messageDom}>
    {message}
  </div>
  <div
    class="bg-black arrow"
    bind:this={arrowElement}
    class:top={arrowDirection === "top"}
    class:down={arrowDirection === "down"}
    class:right={arrowDirection === "right"}
    class:left={arrowDirection === "left"}
  />
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
  .tooltip-frame {
    position: absolute;
    width: fit-content;
  }
  .arrow {
    position: absolute;
    width: 0.8em;
    height: 0.8;
  }

  .up {
    clip-path: polygon(50% 0, 100% 100%, 0 100%);
    top: -0.4em;
    left: calc(50% - 0.4em);
  }
  .right {
    clip-path: polygon(0 0, 100% 50%, 0 100%);
    top: calc(50% - 0.4em);
    left: 100%;
  }

  .down {
    clip-path: polygon(0 0, 100% 0, 50% 100%);
    top: 100%;
    left: calc(50% - 0.4em);
  }

  .left {
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
    top: calc(50% - 0.4em);
    left: -0.4em;
  }
</style>
