(async () => {
  // Convert the game messages collection into an array.
  const messages = Array.from(game.messages);

  // Filter messages for those with rollType "talent"
  const talentMessages = messages.filter(
    (msg) => msg.flags?.data?.postData?.rollType === "talent"
  );

  // Map over each talent message to extract the data we need.
  const extractedData = talentMessages.map((msg) => ({
    id: msg._id,
    speaker: msg.speaker, // Contains alias, actor, token, and scene.
    title: msg.flags.title || null,
    timestamp: msg.timestamp,
    createdTime: msg._stats?.createdTime || null,
    // preData usually holds the source talent's details (like characteristics, roll mode, etc.)
    preData: msg.flags.data.preData,
    // postData contains the roll result, characteristics array, modifiers, etc.
    postData: msg.flags.data.postData,
  }));

  // Convert the extracted data into a JSON string.
  const jsonOutput = JSON.stringify(extractedData, null, 2);
  console.log(jsonOutput);

  // Optional: Create and trigger a download of the JSON file.
  const blob = new Blob([jsonOutput], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "talentRolls.json";
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
})();
