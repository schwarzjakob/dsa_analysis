(async () => {
  // Convert the game actors collection into an array.
  const allActors = Array.from(game.actors);

  // Filter out only those actors with type "character"
  const characterActors = allActors.filter(
    (actor) => actor.type === "character"
  );

  // Map over the filtered actors to extract the required fields.
  const actorsData = characterActors.map((actor) => {
    const system = actor.system || {};
    const characteristics = system.characteristics || {};
    const status = system.status || {};
    const details = system.details || {};

    return {
      id: actor.id,
      name: actor.name,
      type: actor.type,
      mu: characteristics.mu?.value || null,
      kl: characteristics.kl?.value || null,
      in: characteristics.in?.value || null,
      ch: characteristics.ch?.value || null,
      ff: characteristics.ff?.value || null,
      ge: characteristics.ge?.value || null,
      ko: characteristics.ko?.value || null,
      kk: characteristics.kk?.value || null,
      life_points_value: status.wounds?.value || null,
      life_points_max: status.wounds?.max || null,
      astral_energy_value: status.astralenergy?.value || null,
      astral_energy_max: status.astralenergy?.max || null,
      initiative: status.initiative?.value || null,
      species: details.species?.value || null,
      culture: details.culture?.value || null,
      career: details.career?.value || null,
      experience_total: details.experience?.total || null,
      experience_spent: details.experience?.spent || null,
    };
  });

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
