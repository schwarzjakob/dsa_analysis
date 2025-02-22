(async () => {
  // Convert the game messages collection into an array.
  const messages = Array.from(game.messages);

  // Filter messages for those with rollType "talent"
  const talentMessages = messages.filter(
    (msg) => msg.flags?.data?.postData?.rollType === "dodge"
  );

  // Map over each talent message to extract the data we need.
  const extractedData = talentMessages.map((msg) => {
    const preData = msg.flags.data.preData || {};
    const postData = msg.flags.data.postData || {};
    const source = preData.source || {};
    const system = source.system || {};
    const characteristics = postData.characteristics || [];

    return {
      event_id: msg._id,
      character_id: msg.speaker?.actor ?? null,
      timestamp: msg.timestamp,
      dodge_value: system.value,
      modifier: postData.modifiers ?? 0,
      roll_result: characteristics[0].res ?? null,
      description: postData.description ?? null,
    };
  });

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(extractedData, null, 2);
  console.log(jsonOutput);
})();
