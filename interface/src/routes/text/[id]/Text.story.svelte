<script>
  import Text from "./+page.svelte";
  import ComponentLayout from "$lib/elements/ComponentLayout.svelte";
  /**
   * @type {import("histoire").StoryFile}
   */
  export let Hst;

  /**
   * @type {import("$lib/ml_api/api_types/TextOverView").TextOverView[]}
   */
  const linked = [
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

  /**
   * @type {import("$lib/ml_api/api_types/TextFull").TextFull}
   */
  const data = {
    auther: "Test Auther",
    body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porttitor massa vitae arcu pretium bibendum. Cras et ipsum eget massa bibendum accumsan. Suspendisse vitae massa at diam cursus mattis vitae vel lectus. Fusce vel lorem vehicula, rhoncus ipsum vestibulum, interdum ligula. Aliquam varius risus neque, bibendum consequat sem tempus a. Cras ullamcorper ligula arcu, non suscipit sem pretium vel. Pellentesque quis magna turpis. Cras laoreet convallis gravida. Donec luctus vehicula erat a semper. Cras nec vehicula enim, quis efficitur quam. In pulvinar sem urna, at gravida lacus scelerisque gravida. Vestibulum iaculis sed est blandit semper. Nunc ut ante accumsan, tincidunt lorem a, consequat tellus. Nam ullamcorper eget orci imperdiet volutpat. Integer eu ipsum eu lectus gravida fringilla. Nunc eu neque a enim tincidunt tristique.",
    link_to: linked,
    linked_from: linked,
    linked_from_next: "hoge",
    keywords:
      "Cras fringilla accumsan velit, at mattis massa placerat eget. Vivamus convallis finibus metus".split(
        " "
      ),
  };
</script>

<Hst.Story>
  <ComponentLayout>
    <Text {data} />
  </ComponentLayout>
</Hst.Story>
