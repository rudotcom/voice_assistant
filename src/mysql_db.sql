DROP TABLE IF EXISTS `citation`;

CREATE TABLE `citation` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `quoteText` varchar(255) UNIQUE COLLATE utf8_bin NOT NULL,
    `quoteAuthor` varchar(255) COLLATE utf8_bin NULL,
	`keyword1` varchar(16) COLLATE utf8_bin NULL,
	`keyword2` varchar(16) COLLATE utf8_bin NULL,
	`keyword3` varchar(16) COLLATE utf8_bin NULL,
	`timeCited` DATETIME NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;

"INSERT INTO `citation` (`quoteText`, `quoteAuthor`) VALUES (%s, %s)"

# Статистика дыхания по методу Вима Хофа
DROP TABLE IF EXISTS `whm_breath`;
CREATE TABLE `whm_breath` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `result` int(3) NOT NULL,
	`timeBreath` TIMESTAMP NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
AUTO_INCREMENT=1 ;
