# cartriges-django
 Система учета принтерных картриджей

 # Создание db mySQL
 Создать пустую базу с названием 'carts'
Выполнить 
    manage.py makemigrations 
и затем 
    manage.py migrate

Выполнить запросы к db:
"INSERT INTO `cartrige_nmax` (`zapis`, `nmax`) VALUES (0, 100);

INSERT INTO `cartrige_operation` (`kod`, `operation_name`) VALUES
(1, 'Регистрация'),
(2, 'Перевод со склада(+рег)'),
(3, 'Редактирование'),
(4, 'Прием пустого'),
(5, 'Выдача в работу'),
(6, 'Передача на заправку'),
(7, 'Прием с заправки'),
(8, 'Списание');

DELIMITER $$
CREATE TRIGGER `plus1` AFTER INSERT ON `cartrige_records` FOR EACH ROW UPDATE cartrige_nmax SET nmax =  NEW.inventar
$$
DELIMITER ;
"
Создать superuser'a:
    manage.py createsuperuser

