(async () => {
  // This object will hold our extracted data.
  const output = {
    actors: [],
    talentRolls: [],
  };

  // Iterate over all actors of type "character"
  game.actors.forEach((actor) => {
    if (actor.type === "character") {
      // Extract items of type "skill" from the actor
      const skills = actor.items.filter((item) => item.type === "skill");
      const structuredSkills = skills.map((skill) => ({
        id: skill.id,
        name: skill.name,
        type: skill.type,
        // In DSA5 a skill’s value is stored under talentValue in its system data.
        skillValue: skill.system?.talentValue
          ? skill.system.talentValue.value
          : null,
        // Group (e.g., "body", "social", etc.) as defined in the system data.
        group: skill.system?.group?.value || null,
        // If an advancement cost has been set, include it.
        advancementCost: skill.cost || null,
        // The skill’s description (if any) is typically under system.description.
        description: skill.system?.description || "",
        // Extra flags stored under "dsa5" (if any) are returned here.
        extra: skill.getFlag("dsa5", "extra") || {},
      }));

      // Add this actor's structured skills to our output.
      output.actors.push({
        actorId: actor.id,
        actorName: actor.name,
        skills: structuredSkills,
      });
    }
  });

  // Now, extract talent roll information from chat messages.
  // Chat messages may include flags with detailed roll data.
  game.messages.forEach((msg) => {
    // Retrieve the data flag (assuming the system stores it under "data")
    const flagData = msg.data.flags?.data;
    if (
      flagData &&
      flagData.postData &&
      flagData.postData.rollType === "talent"
    ) {
      output.talentRolls.push({
        // Extract the createdTime from the message's stats (if available)
        createdTime: msg._stats ? msg._stats.createdTime : null,
        // Use the title from the flags or the message data.
        title: msg.data.flags?.title || null,
        // The postData usually holds the results of the roll (characteristics, modifiers, etc.)
        postData: flagData.postData,
        // The preData (for example, the source talent's details) is also included.
        preData: flagData.preData,
        // Speaker information can tie the roll back to an actor.
        speaker: msg.data.speaker,
      });
    }
  });

  // Log the final JSON output to the console.
  console.log(JSON.stringify(output, null, 2));
})();
