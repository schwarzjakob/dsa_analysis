(async () => {
  // Convert the game messages collection into an array.
  const messages = Array.from(game.messages);

  // Filter messages for those with rollType "talent"
  const talentMessages = messages.filter(
    (msg) =>
      msg.flags?.data?.postData?.rollType === "weapon" &&
      msg.flags?.data?.preData?.mode === "attack"
  );

  // Map over each talent message to extract the data we need.
  const extractedData = talentMessages.map((msg) => {
    const preData = msg.flags.data.preData || {};
    const postData = msg.flags.data.postData || {};
    const source = preData.source || {};
    const system = source.system || {};
    const characteristics = postData.characteristics || [];

    let attackValue = null;

    if (source.type == "trait") {
      attackValue = system.at.value;
    } else {
      attackValue = source.attack;
    }

    return {
      event_id: msg._id,
      character_id: msg.speaker?.actor ?? null,
      timestamp: msg.timestamp,
      attack_name: source.name ?? null,
      attack_type: source.type ?? null,
      attack_value: attackValue,
      modifier: postData.modifiers ?? 0,
      roll_result: characteristics[0].res ?? null,
      damage: postData.damage ?? null,
      description: postData.description ?? null,
    };
  });

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(extractedData, null, 2);
  console.log(jsonOutput);
})();
