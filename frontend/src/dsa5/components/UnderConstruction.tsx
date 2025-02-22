import React, { useState, useEffect } from "react";
import { Typography, Container } from "@mui/material";

const UnderConstruction = () => {
  const [text, setText] = useState("");
  const [dots, setDots] = useState("");
  const [showCursor, setShowCursor] = useState(true);

  useEffect(() => {
    const fullText = "This page is under construction";
    let index = 0;

    const typeText = setInterval(() => {
      if (index < fullText.length) {
        setText(fullText.slice(0, index + 1));
        index++;
      } else {
        clearInterval(typeText);
      }
    }, 100);

    return () => clearInterval(typeText);
  }, []);

  useEffect(() => {
    if (text === "This page is under construction") {
      let dotCount = 0;
      setShowCursor(false);
      const dotsInterval = setInterval(() => {
        if (dotCount < 3) {
          setDots(".".repeat(dotCount + 1));
          dotCount++;
        } else {
          setDots("");
          dotCount = 0;
        }
      }, 500);

      return () => {
        clearInterval(dotsInterval);
      };
    }
  }, [text]);

  return (
    <Container sx={{ padding: 2, textAlign: "center" }}>
      {/* Typewriter Text */}
      <Typography
        variant="h4"
        sx={{
          marginTop: 4,
          color: "#f7f1e1",
          display: "inline-block",
          borderRight: showCursor ? "3px solid #f7f1e1" : "none",
          paddingRight: "5px",
          animation: showCursor ? "blink 0.8s infinite" : "none", // Restore blinking
          "@keyframes blink": {
            "50%": { borderColor: "transparent" },
          },
        }}
      >
        {text}
      </Typography>

      {/* New Line for Dots */}
      {text === "This page is under construction" && (
        <Typography
          variant="h4"
          sx={{
            color: "#f7f1e1",
            display: "block",
            height: "40px",
            fontWeight: "bold",
          }}
        >
          {dots}
        </Typography>
      )}
    </Container>
  );
};

export default UnderConstruction;
