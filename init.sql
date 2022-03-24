SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
USE `carts`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

INSERT INTO `cartrige_nmax` (`zapis`, `nmax`) VALUES (0, 100);

INSERT INTO `cartrige_operation` (`kod`, `operation_name`) VALUES
(1, 'Регистрация'),
(2, 'Перевод со склада(+рег)'),
(3, 'Редактирование'),
(4, 'Прием пустого'),
(5, 'Выдача в работу'),
(6, 'Передача на заправку'),
(7, 'Прием с заправки'),
(8, 'Списание');

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
