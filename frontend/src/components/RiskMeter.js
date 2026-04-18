import React from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart, ArcElement } from "chart.js";

Chart.register(ArcElement);

function RiskMeter({ score }) {

  const data = {
    datasets: [
      {
        data: [score * 100, 100 - score * 100],
        backgroundColor: ["#ff4d4d", "#e6e6e6"],
        borderWidth: 0
      }
    ]
  };

  const options = {
    cutout: "80%",
    plugins: {
      legend: { display: false }
    }
  };

  return (
    <div style={{ width: "200px", margin: "auto" }}>
      <Doughnut data={data} options={options} />
      <h3 style={{ textAlign: "center" }}>
        {(score * 100).toFixed(1)}%
      </h3>
    </div>
  );
}

export default RiskMeter;