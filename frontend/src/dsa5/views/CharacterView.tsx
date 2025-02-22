import React from "react";
import { useParams } from "react-router-dom";
import Dashboard from "../components/dashboard/Dashboard";

const CharacterView: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div style={{ padding: "20px" }}>
      {id && <Dashboard characterId={id} />}
    </div>
  );
};

export default CharacterView;
