import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Grid2 as Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  CardActionArea,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const Characters = () => {
  const navigate = useNavigate();
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCharacters = async () => {
    try {
      const response = await axios.get("http://localhost:5000/dsa5/characters");
      setCharacters(response.data || []);
    } catch (error) {
      console.error("Error fetching characters", error);
      setCharacters([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCharacters();
  }, []);

  const handleTileClick = (id) => {
    navigate(`/dsa5/character/${id}`);
  };

  return (
    <Grid container spacing={4} sx={{ padding: 2 }}>
      {Array.isArray(characters) && characters.length === 0 && !loading ? (
        <Grid size={12} sx={{ textAlign: "center" }}>
          <Typography
            variant="h4"
            align="center"
            sx={{
              marginTop: 4,
              color: "#f7f1e1",
              display: "inline-block",
            }}
          >
            Ups, no characters found 🤔
          </Typography>
        </Grid>
      ) : (
        characters.map((character) => (
          <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={character.id}>
            <Card
              sx={{
                borderRadius: "2rem",
                backgroundColor: "#000",
                boxShadow: "0 0 2px 1px rgba(247, 241, 225, 0.3)",
                transition: "box-shadow 0.3s ease, transform 0.3s ease",
                overflow: "hidden",
                "&:hover": {
                  transform: "scale(1.02)",
                  boxShadow: "0 0 5px 2px rgba(247, 241, 225, 0.5)",
                },
              }}
            >
              <CardActionArea onClick={() => handleTileClick(character.id)}>
                <CardMedia
                  component="img"
                  image={character.image_url}
                  alt={character.name}
                  sx={{
                    position: "relative",
                    zIndex: 0,
                    borderTopLeftRadius: "1.4rem",
                    borderTopRightRadius: "1.4rem",
                  }}
                />
                <CardContent sx={{ color: "#f7f1e1" }}>
                  <Typography variant="h6" align="center">
                    {character.name}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))
      )}
    </Grid>
  );
};

export default Characters;
