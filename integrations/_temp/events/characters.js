(async () => {
  // Convert the game actors collection into an array.
  const allActors = Array.from(game.actors);

  // Filter out only those actors with type "character"
  const characterActors = allActors.filter(
    (actor) => actor.type === "character"
  );

  // Map over the filtered actors to extract the required fields, including the full image URL.
  const actorsData = characterActors.map((actor) => ({
    id: actor.id,
    name: actor.name,
    type: actor.type,
    image_url: actor.img ? `${game.data.addresses.remote}${actor.img}` : null,
    mu: actor.system?.characteristics?.mu?.value ?? null,
    kl: actor.system?.characteristics?.kl?.value ?? null,
    in: actor.system?.characteristics?.in?.value ?? null,
    ch: actor.system?.characteristics?.ch?.value ?? null,
    ff: actor.system?.characteristics?.ff?.value ?? null,
    ge: actor.system?.characteristics?.ge?.value ?? null,
    ko: actor.system?.characteristics?.ko?.value ?? null,
    kk: actor.system?.characteristics?.kk?.value ?? null,
    life_points_value: actor.system?.status?.wounds?.value ?? null,
    life_points_max: actor.system?.status?.wounds?.max ?? null,
    astral_energy_value: actor.system?.status?.astralenergy?.value ?? null,
    astral_energy_max: actor.system?.status?.astralenergy?.max ?? null,
    initiative: actor.system?.status?.initiative?.value ?? null,
    species: actor.system?.details?.species?.value ?? null,
    culture: actor.system?.details?.culture?.value ?? null,
    career: actor.system?.details?.career?.value ?? null,
    experience_total: actor.system?.details?.experience?.total ?? null,
    experience_spent: actor.system?.details?.experience?.spent ?? null,
  }));

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(actorsData, null, 2);
  console.log(jsonOutput);
})();

(async () => {
  const myGame = Array.from(game);
  const jsonOutput = JSON.stringify(game, null, 2);
  console.log(jsonOutput);
})();
