import "../css/ChooseVideoPage.css";
import VideoCard from "./VideoCard";
import React, { useState, useEffect } from "react";

let recommendations = null;
function ChooseVideoPage() {
  const [data, setData] = useState(null);

  function get_data() {
    fetch("http://127.0.0.1:5005/predict")
    .then((response) => response.json())
    .then((data) => setData(data))
    .catch((error) => console.error(error));
  }

  useEffect(() => get_data(), []);
  
  console.log(data);
  if (data == null || recommendations != null) return;
  console.log("test");

  // recommendations = Array(10).fill({
  //   title: "Звёзды в джунглях, 1 сезон, 1 выпуск",
  //   category: "Природа",
  //   tags: ["Звезды", "Природа"],
  //   views: "55",
  //   post_time: "5 дней назад",
  // });
  recommendations = data.predictions;
  console.log(recommendations);

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="ChooseVideoPage">
      <header className="ChooseVideoPage-header">
        <div className="top-bar content">
          <div className="label">
            <h1>RUTUBE</h1>
            <div id="label-circle"></div>
          </div>
          <button className="refresh-button" onClick={handleRefresh}>
            REFRESH
          </button>
        </div>
      </header>
      <div className="content">
        <h2>Рекомендации</h2>
        <div className="recommendation-grid">
          {recommendations.map((rec, index) => VideoCard(rec, index))}
        </div>
      </div>
    </div>
  );
}

export default ChooseVideoPage;
