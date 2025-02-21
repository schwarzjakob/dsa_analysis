import React from "react";
import { useNavigate } from "react-router-dom";
import { Button, Box } from "@mui/material";
import { styled, keyframes } from "@mui/system";

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const LandingContainer = styled(Box)(({ theme }) => ({
  width: "100vw",
  height: "100vh",
  color: "#f7f1e1",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
}));

const Title = styled("h1")(({ theme }) => ({
  margin: 0,
  animation: `${fadeIn} 1s ease forwards`,
}));

const Subtitle = styled("p")(({ theme }) => ({
  margin: "20px 0",
  opacity: 0,
  animation: `${fadeIn} 1s ease forwards`,
  animationDelay: "0.5s",
}));

const ButtonBox = styled(Box)(({ theme }) => ({
  display: "flex",
  gap: "20px",
  marginTop: "20px",
  opacity: 0,
  animation: `${fadeIn} 1s ease forwards`,
  animationDelay: "1s",
}));

const LandingPage = () => {
  const navigate = useNavigate();

  const buttons = [
    { name: "DSA 5", link: "/dsa5/" },
    { name: "DSA 4", link: "/dsa4/" },
  ];

  const handleClick = (link) => {
    navigate(link);
  };

  return (
    <LandingContainer>
      <Title>Welcome to our DSA Insights Hub</Title>
      <Subtitle>Please Choose Your Game Version</Subtitle>
      <ButtonBox>
        {buttons.map((button) => (
          <Button
            key={button.name}
            variant="contained"
            onClick={() => handleClick(button.link)}
            sx={{
              position: "relative",
              overflow: "hidden",
              backgroundColor: "#000",
              color: "#f7f1e1",
              width: "150px",
              border: "1px solid #f7f1e1",
              borderRadius: "8px",
              padding: "10px 20px",
              transition: "color 0.5s ease, transform 0.5s ease",
              "&::before": {
                content: '""',
                position: "absolute",
                top: 0,
                left: 0,
                height: "100%",
                width: 0,
                backgroundColor: "#f7f1e1",
                zIndex: -1,
                transition: "width 0.5s ease",
              },
              "&:hover": {
                transform: "scale(1.05)",
                color: "#000",
                "&::before": {
                  width: "100%",
                },
              },
            }}
          >
            {button.name}
          </Button>
        ))}
      </ButtonBox>
    </LandingContainer>
  );
};

export default LandingPage;
