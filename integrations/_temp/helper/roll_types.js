(async () => {
  // Convert the game messages collection into an array.
  const messages = Array.from(game.messages);

  // Extract rollType values from messages where rollType exists
  const rollTypes = new Set(
    messages
      .map((msg) => msg.flags?.data?.postData?.rollType)
      .filter((type) => type !== undefined) // Remove undefined values
  );

  // Convert Set to an array and log it
  console.log("Unique roll types:", Array.from(rollTypes));
})();
