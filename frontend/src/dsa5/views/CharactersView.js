import React from "react";
import {
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  CardActionArea,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const dummyCharacters = [
  {
    id: 1,
    name: "Akira Masamune",
    image: "https://foundry.rlxd.de/Akira%20Masamune-min.jpg",
  },
  {
    id: 2,
    name: 'Baargan "Treuwal" Helgason',
    image: "https://foundry.rlxd.de/Baargan%20Treuwallen%20Helgason.jpg",
  },
  {
    id: 3,
    name: "Walla Burija Sabu Hasmanin",
    image: "https://foundry.rlxd.de/Wall%20Birija%20Saba%20Hasmanin-min.jpg",
  },
  {
    id: 4,
    name: "Elanor Walham",
    image: "https://foundry.rlxd.de/Elanor%20Walham-min.jpg",
  },
  {
    id: 5,
    name: "Aleron von Sturmfels",
    image: "https://foundry.rlxd.de/Torgan%20Rehernagrot-min.jpg",
  },
];

const Characters = () => {
  const navigate = useNavigate();

  const handleTileClick = (id) => {
    navigate(`/dsa5/character/${id}`);
  };

  return (
    <Grid container spacing={4} sx={{ padding: 2 }}>
      {dummyCharacters.map((char) => (
        <Grid item xs={12} sm={6} md={4} lg={3} key={char.id}>
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
            <CardActionArea onClick={() => handleTileClick(char.id)}>
              {/* CardMedia inside the wrapper */}
              <CardMedia
                component="img"
                image={char.image}
                alt={char.name}
                sx={{
                  position: "relative",
                  zIndex: 0,
                  borderTopLeftRadius: "1.4rem",
                  borderTopRightRadius: "1.4rem",
                }}
              />
              <CardContent sx={{ color: "#f7f1e1" }}>
                <Typography variant="h6" align="center">
                  {char.name}
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default Characters;
