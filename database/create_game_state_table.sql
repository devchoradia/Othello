CREATE TABLE `game_state` (
  `username` varchar(20) NOT NULL,
  `gameState` json NOT NULL,
  `gameMode` varchar(45) NOT NULL,
  `currentPlayer` int NOT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `username_fk` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
