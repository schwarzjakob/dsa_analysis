import { useState, useEffect } from "react";
import axios from "axios";

export const useCharacterData = (characterId: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/dsa5/characters/${characterId}`
        );
        setData(response.data);
        console.log(JSON.stringify(response.data));
      } catch (err) {
        setError("Failed to fetch character data");
      } finally {
        setLoading(false);
      }
    };

    if (characterId) fetchData();
  }, [characterId]);

  return { data, loading, error };
};
