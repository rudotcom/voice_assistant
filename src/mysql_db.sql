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

# Статистика дыхания по методу Вима Хофа
DROP TABLE IF EXISTS `whm_breath`;
CREATE TABLE `whm_breath` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `result` int(3) NOT NULL,
	`timeBreath` TIMESTAMP NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
AUTO_INCREMENT=1 ;

# Конфиг интентов
DROP TABLE IF EXISTS `intent_intent`;
CREATE TABLE `intent_intent` (
    `id` SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) UNIQUE NOT NULL,
    `action` VARCHAR(25) NULL
) ENGINE=InnoDB
AUTO_INCREMENT=1 ;

# Конфиг фраз интентов
DROP TABLE IF EXISTS `intent_phrase`;
CREATE TABLE `intent_phrase` (
    `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `intent` SMALLINT UNSIGNED NOT NULL,
	`phrase_type` SET(
		'request',
		'reply',
		'subject',
		'subject_missing',
		'not_exists',
		'target',
		'target_missing',
		'text_missing',
		'location_missing',
		'mood_status'
		) NOT NULL,
    `phrase` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `diary`;
CREATE TABLE `diary` (
    `id` SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`timestamp` TIMESTAMP NOT NULL,
    `text` TEXT NOT NULL,
    `color` BINARY(3)
) ENGINE=InnoDB
AUTO_INCREMENT=1 ;

# Напоминания
CREATE TABLE `reminders` (
    `id` SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `date` DATE NULL,
    `weekday` TINYINT DEFAULT NULL,
    `time` TIME NOT NULL,
    `text` TEXT NOT NULL
);

DROP TABLE IF EXISTS `reminded`;
CREATE TABLE `reminded` (
    `id` SMALLINT PRIMARY KEY UNIQUE NOT NULL,
    `time_reminded` TIMESTAMP NULL
);
