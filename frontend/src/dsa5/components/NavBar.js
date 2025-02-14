import React from "react";
import { AppBar, Toolbar, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const NavBar = () => {
  const navigate = useNavigate();

  const handleCharactersClick = () => {
    navigate("/dsa5/characters");
  };

  return (
    <AppBar
      position="static"
      sx={{
        padding: 0,
        margin: 0,
        backgroundColor: "#000",
        color: "#f7f1e1",
        borderBottom: "1px solid rgba(247, 241, 225, 0.2)", // Added alpha to the border color
      }}
    >
      <Toolbar sx={{ height: 80 }}>
        <Box
          component="img"
          onClick={() => navigate("/")}
          sx={{
            borderRadius: 1,
            marginRight: 3,
            width: 50,
            aspectRatio: "1/1",
            backgroundColor: "transparent",
            cursor: "pointer",
            transition: "transform 0.3s ease",

            "&:hover": {
              transform: "rotate(90deg)",
            },
          }}
          alt="The house from the offer."
          src="/logo/logo_bright.png"
        />
        <Button
          color="inherit"
          onClick={handleCharactersClick}
          disableRipple
          sx={{
            fontSize: "1.2rem",
            fontWeight: 600,
            position: "relative",
            transition: "transform 0.2s ease, color 0.2s ease",

            "&:hover": {
              transform: "scale(1.05)",
            },

            "&::after": {
              content: '""',
              position: "absolute",
              left: "50%",
              bottom: 0,
              width: 0,
              height: "2px",
              backgroundColor: "#f7f1e1",
              transition: "width 0.3s ease, left 0.3s ease",
            },

            "&:hover::after": {
              width: "100%",
              left: 0,
            },
          }}
        >
          Characters
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
