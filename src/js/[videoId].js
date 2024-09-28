import React from "react";
import "../css/VideoPage.css";
import { useState, useEffect } from "react";
import like from "../like.svg";
import dislike from "../dislike.svg";
import share from "../Share.svg";

let videoData = null;
function VideoPage() {
  const [data, setData] = useState(null);
  // const { id } = useParams();
  const id = window.location.search.split("=")[1];
  const url = "http://127.0.0.1:5005/video?id=" + id;

  function get_video_data(url) {
    console.log(url);

    fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => {
        console.log(response);
        return response.json();
      })
      .then((data) => setData(data))
      .catch((error) => console.error(error));
  }

  useEffect(() => get_video_data(url), [url]);

  console.log(data);
  if (data == null || videoData != null) return;
  console.log("test");

  videoData = data;
  console.log(videoData);

  const handleRefresh = () => {
    window.location.reload();
  };

  // Обработчики кликов
  const handleLikeClick = async (event) => {
    event.preventDefault();
    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=1";

    await fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error(error));
  };

  const handleDislikeClick = async (event) => {
    event.preventDefault();
    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=0";

    await fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error(error));
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
      <div className="body-container content">
        <div className="card">
          <div className="img_container">
            <img
              className="videoImg"
              src="https://avatars.mds.yandex.net/i?id=4f7586d49edaa427e07a8819562fc284_l-5248434-images-thumbs&n=13"
            />
            <div className="category_section">
              <h3>{videoData.title}</h3>
              <p>Категория {videoData.category}</p>
            </div>
            <div className="react-section">
              {/* Лайк */}
              <div className="like-section" onClick={handleLikeClick}>
                <img src={like} alt="Likes" />
                <p>{videoData.v_likes}</p>
              </div>

              {/* Дизлайк */}
              <div className="dislike-section" onClick={handleDislikeClick}>
                <img src={dislike} alt="Dislikes" />
                <p>{videoData.v_dislikes}</p>
              </div>

              {/* Шаринг */}
              <div className="shared_section">
                <img src={share} alt="Share" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoPage;
