// This script extracts structured data from a character, specifically skills, and logs it to the console.
(async () => {
  // Retrieve the actor by name.
  const actor = game.actors.getName("Akira Masamune");
  if (!actor) {
    console.error("Actor not found!");
    return;
  }

  // Filter the actor’s items to get only those of type "skill".
  const skills = actor.items.filter((item) => item.type === "skill");

  // Map over each skill to extract structured data.
  const structuredSkills = skills.map((skill) => ({
    id: skill.id,
    name: skill.name,
    type: skill.type,
    // In DSA5, a skill's current value is typically stored under "talentValue" in its system data.
    skillValue: skill.system?.talentValue
      ? skill.system.talentValue.value
      : null,
    // You might also want to include the group this skill belongs to (e.g. "body", "social", etc.)
    group: skill.system?.group.value || null,
    // If an advancement cost has been calculated, you can include it here.
    advancementCost: skill.cost || null,
    // The skill’s description (if any) is usually found in skill.system.description.
    description: skill.system?.description || "",
    // If there are extra flags stored (for example under flags.dsa5.extra), include them.
    extra: skill.getFlag("dsa5", "extra") || {},
  }));

  console.log("Structured Skills Data:", structuredSkills);
})();
