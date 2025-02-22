(async () => {
  // Convert the game messages collection into an array.
  const messages = Array.from(game.messages);

  // Filter messages for those with rollType "talent"
  const talentMessages = messages.filter(
    (msg) => msg.flags?.data?.postData?.rollType === "talent"
  );

  // Map over each talent message to extract the data we need.
  const extractedData = talentMessages.map((msg) => {
    const preData = msg.flags.data.preData || {};
    const postData = msg.flags.data.postData || {};
    const source = preData.source || {};
    const system = source.system || {};

    return {
      event_id: msg._id,
      character_id: msg.speaker?.actor ?? null,
      timestamp: msg.timestamp,
      talent_name: source.name || null,
      talent_group: system.group?.value ?? null,
      talent_value: system.talentValue?.value ?? null,
      talent_trait_1: system.characteristic1?.value ?? null,
      talent_trait_2: system.characteristic2?.value ?? null,
      talent_trait_3: system.characteristic3?.value ?? null,
      modifier: postData.modifiers ?? 0,
      result: postData.result ?? null,
      quality_step: postData.qualityStep ?? null,
      success_level: postData.successLevel ?? null,
      description: postData.description ?? null,
    };
  });

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(extractedData, null, 2);
  console.log(jsonOutput);
})();
