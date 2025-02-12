(async () => {
  // Convert the game actors collection into an array.
  const allActors = Array.from(game.actors);

  // Filter out only those actors with type "character"
  const characterActors = allActors.filter(
    (actor) => actor.type === "character"
  );

  // Map over the filtered actors to extract the data you need.
  // You can modify the properties below as necessary.
  const actorsData = characterActors.map((actor) => ({
    id: actor.id,
    name: actor.name,
    type: actor.type,
    system: actor.system,
    flags: actor.flags,
    // If you want to include all items, uncomment the next line:
    // items: actor.items.map(item => ({ id: item.id, name: item.name, type: item.type, system: item.system }))
  }));

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(actorsData, null, 2);
  console.log(jsonOutput);

  // Create a Blob from the JSON string and trigger a download.
  const blob = new Blob([jsonOutput], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "characterActors.json";
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
})();
