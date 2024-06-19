<h1>Опис</h1><br/>
Проєкт допомагає керувати вмістом Telegram бота для залучення абітурієнтів, виконувати розсилки та створювати вікторини для проходження абітурієнтами, а також надавати базову довідкову інформацію.<br/>
<h1>Встановлення та запуск</h1><br/>
pip install -r requirements.txt<br/>
Перейменувати файл .env-example на .env та встановити токен бота<br/>
python manage.py migrate<br/>
python manage.py runserver 0.0.0.0:8000<br/>
python manage.py runbot

<h1>Перед запуском перевірте чи відкритий порт 8000</h1>

<br>
nohup python3 manage.py runserver 0.0.0.0:8000 & 

