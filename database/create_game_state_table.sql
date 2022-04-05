CREATE TABLE `game_state` (
  `username` varchar(20) NOT NULL,
  `gameState` json NOT NULL,
  `gameMode` varchar(45) NOT NULL,
  `currentPlayer` int NOT NULL,
  `aiLevel` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`username`),
  CONSTRAINT `username_fk` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ai_has_level` CHECK (((`aiLevel` <> 0) or (`gameMode` <> _utf8mb4'AI')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
