// frontend/src/dsa5/components/Dashboard/Dashboard.tsx
import React from "react";
import { Grid2 as Grid, Card, CardContent } from "@mui/material";
import DashboardElement from "./DashboardElement";
import TraitSpiderChart from "./charts/TraitSpiderChart";
import { useCharacterData } from "../../hooks/useCharacterData";
import "../../../App.css";

interface DashboardProps {
  characterId: string;
}

const Dashboard: React.FC<DashboardProps> = ({ characterId }) => {
  const { data: characterData, loading, error } = useCharacterData(characterId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <Grid container spacing={4} sx={{ padding: 2 }}>
      <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
        <Card
          sx={{
            borderRadius: "2rem",
            backgroundColor: "#000",
            boxShadow: "2px 2px 10px 4px rgba(16, 16, 16, 0.5)",
            transition: "box-shadow 0.3s ease, transform 0.3s ease",
            overflow: "hidden",
          }}
        >
          <CardContent>
            <DashboardElement>
              <TraitSpiderChart characterData={characterData} />
            </DashboardElement>
          </CardContent>
        </Card>
      </Grid>
      {/* You can add additional dashboard elements here as needed */}
    </Grid>
  );
};

export default Dashboard;
