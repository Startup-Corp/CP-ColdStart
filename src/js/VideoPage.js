// import "../css/VideoPage.css";
// import { useParams } from "react-router-dom";
// // import VideoCard from "./VideoCard";
// import React, { useState, useEffect } from "react";

// let videoData = null;
// function VideoPage() {
//   const [data, setData] = useState(null);
//   let { id } = useParams();

//   function get_video_data(id) {
//     fetch("http://127.0.0.1:5005/video?id=" + id)
//       .then((response) => response.json())
//       .then((data) => setData(data))
//       .catch((error) => console.error(error));
//   }

//   useEffect(() => get_video_data(id), [id]);

//   console.log(data);
//   if (data == null || videoData != null) return;
//   console.log("test");

//   videoData = data;
//   console.log(videoData);

//   const handleRefresh = () => {
//     window.location.reload();
//   };

//   return (
//     <div className="ChooseVideoPage">
//       <header className="ChooseVideoPage-header">
//         <div className="top-bar content">
//           <div className="label">
//             <h1>RUTUBE</h1>
//             <div id="label-circle"></div>
//           </div>
//           <button className="refresh-button" onClick={handleRefresh}>
//             REFRESH
//           </button>
//         </div>
//       </header>
//       <div className="content">
//         <div class="Video">
//           <div className="card">
//             <img src="https://avatars.mds.yandex.net/i?id=4f7586d49edaa427e07a8819562fc284_l-5248434-images-thumbs&n=13" />
//             <h3>{videoData.title}</h3>
//             <div className="category_section">
//               <p>
//                 Категория {videoData.category} |{" "}
//                 {videoData.tags
//                   .slice(0, 3)
//                   .map((tag) => `#${tag}`)
//                   .join(" ")}
//               </p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default VideoPage;
