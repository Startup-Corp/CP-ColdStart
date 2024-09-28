import '../css/card.css';
import eye from "../Eye.svg"

function VideoCard(rec, index) {
  return (
    <div className="card" key={index}>
      <h3>{rec.title}</h3>
      <div className='category_section'>
        <p>Категория {rec.category} | {rec.tags.slice(0, 3).map(tag => `#${tag}`).join(' ')}</p>
      </div>
      <div className='watches_section'>
        <div className='views_container'>
          <img src={eye} alt='Watches ' />
          <p>{rec.views}</p>
        </div>
        <div className='circle' />
        <p>{rec.post_time}</p>
      </div>
    </div>
  );
}

export default VideoCard;
