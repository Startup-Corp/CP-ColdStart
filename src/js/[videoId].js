import React from "react";
import "../css/VideoPage.css";
import { useState, useEffect } from "react";
import like from "../like.svg";
import dislike from "../dislike.svg";
import share from "../Share.svg";

let videoData = null;
let likeClicked = false;
let dislikeClicked = false;
let isShared = false;
let commentIsClicked = false;
function VideoPage() {
  const [data, setData] = useState(null);
  // const { id } = useParams();
  const id = window.location.search.split("=")[1];
  // const url = "http://87.242.86.81:5005/video?id=" + id;
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

  const handleCommentClick = async (event) => {
    if (commentIsClicked) return;
    commentIsClicked = true;
    event.preventDefault();
    // const url = "http://87.242.86.81:5005/react?id=" + id + "&rating=1";
    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=comment";

    await fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error(error));

    const likeP = document.getElementById("likes");
    likeP.textContent = Number(likeP.textContent) + 1;
  }

  // Обработчики кликов
  const handleLikeClick = async (event) => {
    if (likeClicked) return;
    likeClicked = true;
    event.preventDefault();
    // const url = "http://87.242.86.81:5005/react?id=" + id + "&rating=1";
    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=like";

    await fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error(error));

    const likeP = document.getElementById("likes");
    likeP.textContent = Number(likeP.textContent) + 1;
  };

  const handleDislikeClick = async (event) => {
    if (dislikeClicked) return;
    dislikeClicked = true;

    event.preventDefault();
    // const url = "http://87.242.86.81:5005/react?id=" + id + "&rating=0";
    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=dislike";

    await fetch(url, {
      method: "GET",
      headers: {
        ContentType: "application/json",
      },
    })
      .then((response) => response.json())
      .catch((error) => console.error(error));

    const dislikeP = document.getElementById("dislikes");
    dislikeP.textContent = Number(dislikeP.textContent) + 1;
  };

  const handleShareClick = () => {
    const copy = window.location.href;
    const textArea = document.createElement("textarea");
    textArea.value = copy;
    // Добавляем его в DOM
    document.body.appendChild(textArea);
    // Выделяем текст
    textArea.select();
    textArea.setSelectionRange(0, 99999); // Для мобильных устройств
    // Копируем текст
    document.execCommand("copy");
    // Удаляем временный элемент
    document.body.removeChild(textArea);

    const toast = document.getElementById("Toast");
    toast.classList.add("toast-show");

    setTimeout(() => {
      toast.classList.remove("toast-show");
    }, 2000);

    if (isShared) return;
    isShared = true;

    const url = "http://127.0.0.1:5005/react?id=" + id + "&rating=share";

    fetch(url, {
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
            <h1>
              <a href="/">RUTUBE</a>
            </h1>
            <div id="label-circle"></div>
          </div>
          <a href="/" className="refresh-button">
            REFRESH
          </a>
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
              <p>Категория: {videoData.category_id}</p>
            </div>
            <div className="react-section">
              {/* Комментарий */}
              <div className="comments-section" onClick={handleCommentClick}>
                <p id="comments">Комментировать</p>
              </div>

              {/* Лайк */}
              <div className="like-section" onClick={handleLikeClick}>
                <img src={like} alt="Likes" />
                <p id="likes">{videoData.v_likes}</p>
              </div>

              {/* Дизлайк */}
              <div className="dislike-section" onClick={handleDislikeClick}>
                <img src={dislike} alt="Dislikes" />
                <p id="dislikes">{videoData.v_dislikes}</p>
              </div>

              {/* Шаринг */}
              <div className="shared_section" onClick={handleShareClick}>
                <img src={share} alt="Share" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div id="Toast" className="">
        <p>Ссылка скопирована!</p>
      </div>
    </div>
  );
}

export default VideoPage;
