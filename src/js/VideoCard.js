import '../css/card.css';
import eye from "../Eye.svg"

function VideoCard(rec, index) {

  return (
    <a href={'/video?id=' + rec.id} className="card border" key={index}>
      <h3>{rec.title}</h3>
      <div className='category_section'>
        <p>Категория {rec.category}</p>
      </div>
      <div className='watches_section'>
        <div className='views_container'>
          <img src={eye} alt='Watches ' />
          <p>{rec.views}</p>
        </div>
        <div className='circle' />
        <p>{rec.post_time}</p>
      </div>
    </a>
  );
}

export default VideoCard;
