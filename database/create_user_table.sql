CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(45) NOT NULL,
  `ELORating` int DEFAULT '0',
  `gameState` json DEFAULT NULL,
  `currentPlayer` int DEFAULT NULL,
  `gameMode` varchar(45) DEFAULT 'local',
  `boardColor` varchar(45) DEFAULT 'green',
  `boardSize` int DEFAULT '4',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
