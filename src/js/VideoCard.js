import '../css/card.css';
import eye from "../Eye.svg"

// Модуль описывающий одно видео
function VideoCard(rec, index) {
  // Преобразуем строку в объект Date
  const date = new Date(rec.pub_datetime);

  // Получаем день, месяц и год
  const day = String(date.getUTCDate()).padStart(2, '0'); // добавляем ведущий 0 для дней меньше 10
  const month = date.toLocaleString('en-US', { month: 'short' }); // короткое название месяца
  const year = date.getUTCFullYear();

  // Формируем строку
  const formattedDate = `${day} ${month} ${year}`;

  const d = formattedDate; // Вывод: 04 Aug 2024

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
        <p>{d}</p>
      </div>
    </a>
  );
}

export default VideoCard;
