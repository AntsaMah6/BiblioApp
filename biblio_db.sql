-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 30 sep. 2025 à 12:08
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `biblio_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth`
--

CREATE TABLE `auth` (
  `id_auth` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth`
--

INSERT INTO `auth` (`id_auth`, `username`, `password`) VALUES
(1, 'admin1', '17052004');

-- --------------------------------------------------------

--
-- Structure de la table `emprunts`
--

CREATE TABLE `emprunts` (
  `id_emprunts` int(11) NOT NULL,
  `id_livres` int(11) DEFAULT NULL,
  `id_membres` int(11) DEFAULT NULL,
  `date_emprunt` date DEFAULT NULL,
  `date_retour` date DEFAULT NULL,
  `statut` enum('emprunté','rendu','en_retard') DEFAULT 'emprunté',
  `date_retour_prevue` date NOT NULL,
  `penalite` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `emprunts`
--

INSERT INTO `emprunts` (`id_emprunts`, `id_livres`, `id_membres`, `date_emprunt`, `date_retour`, `statut`, `date_retour_prevue`, `penalite`) VALUES
(1, 1, 1, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00),
(2, 2, 7, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00),
(3, 34, 8, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00),
(4, 33, 8, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00),
(5, 15, 8, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00);

-- --------------------------------------------------------

--
-- Structure de la table `livres`
--

CREATE TABLE `livres` (
  `id_livres` int(11) NOT NULL,
  `titre` varchar(255) NOT NULL,
  `auteur` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `livres`
--

INSERT INTO `livres` (`id_livres`, `titre`, `auteur`) VALUES
(1, 'Le Petit Prince', 'Saint-Exupéry'),
(2, 'Harry Potter', 'J.K. Rowling'),
(3, 'L\'Étranger', 'Albert Camus'),
(9, 'Pâtisserie pour les nuls', 'Chef Jean'),
(10, 'Les Misérables', 'Victor Hugo'),
(11, 'Bel-Ami', 'Guy de Maupassant'),
(12, 'Madame Bovary', 'Gustave Flaubert'),
(13, 'La Condition Humaine', 'André Malraux'),
(14, 'L?Étranger', 'Albert Camus'),
(15, 'Germinal', 'Émile Zola'),
(16, 'Notre-Dame de Paris', 'Victor Hugo'),
(17, 'Le Rouge et le Noir', 'Stendhal'),
(18, 'Candide', 'Voltaire'),
(19, 'La Peste', 'Albert Camus'),
(20, 'Du côté de chez Swann', 'Marcel Proust'),
(21, 'Antsa', 'Jean-Joseph Rabearivelo'),
(22, 'Lamba', 'Elie Rajaonarison'),
(23, 'Ny Ranomasina', 'Esther Nirina'),
(24, 'La Saga des Sakalava', 'Jacques Rabemananjara'),
(25, 'Le Temps d?un Poème', 'Jean Verdi Salomon Razakandraina'),
(26, 'Haizina', 'Flavien Ranaivo'),
(27, 'Ny Fitiavana', 'Rado'),
(28, 'Poèmes', 'Michèle Rakotoson'),
(29, 'L?Île Rouge', 'Dox'),
(30, 'Ambioka', 'Jean-Joseph Rabearivelo'),
(31, 'L\'Éducation sentimentale', 'Gustave Flaubert'),
(32, 'La Chartreuse de Parme', 'Stendhal'),
(33, 'Voyage au centre de la Terre', 'Jules Verne'),
(34, 'Vingt mille lieues sous les mers', 'Jules Verne'),
(35, 'Les Trois Mousquetaires', 'Alexandre Dumas'),
(36, 'La Reine Margot', 'Alexandre Dumas'),
(37, 'La Comédie Humaine', 'Honoré de Balzac'),
(38, 'Eugénie Grandet', 'Honoré de Balzac'),
(39, 'Les Fleurs du mal', 'Charles Baudelaire'),
(40, 'Les Contemplations', 'Victor Hugo'),
(41, 'Les Chants de Maldoror', 'Lautréamont'),
(42, 'Le Père Goriot', 'Honoré de Balzac'),
(43, 'La Symphonie pastorale', 'André Gide'),
(44, 'Les Nourritures terrestres', 'André Gide'),
(45, 'Sylvie', 'Gérard de Nerval'),
(46, 'Atala', 'Chateaubriand'),
(47, 'René', 'Chateaubriand'),
(48, 'Thérèse Raquin', 'Émile Zola'),
(49, 'Nana', 'Émile Zola'),
(50, 'L\'Assommoir', 'Émile Zola'),
(51, 'Le Livre de la Jungle', 'Rudyard Kipling'),
(52, 'Crime et Châtiment', 'Fiodor Dostoïevski'),
(53, 'Les Frères Karamazov', 'Fiodor Dostoïevski'),
(54, 'Anna Karénine', 'Léon Tolstoï'),
(55, 'Guerre et Paix', 'Léon Tolstoï'),
(56, 'Le Joueur', 'Fiodor Dostoïevski'),
(57, 'La Métamorphose', 'Franz Kafka'),
(58, 'Le Procès', 'Franz Kafka'),
(59, 'Ainsi parlait Zarathoustra', 'Friedrich Nietzsche'),
(60, 'Le Banquet', 'Platon');

-- --------------------------------------------------------

--
-- Structure de la table `membres`
--

CREATE TABLE `membres` (
  `id_membres` int(11) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `age` int(2) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `membres`
--

INSERT INTO `membres` (`id_membres`, `nom`, `prenom`, `age`, `email`) VALUES
(1, 'Jean', 'Pascal', 21, 'jean3@gmail.coom'),
(2, 'Dupont', 'Jean', 33, 'jean.dupont@example.com'),
(3, 'Martin', 'Marie', 34, 'marie.martin@example.com'),
(4, 'Durand', 'Paul', 30, 'paul.durand@example.com'),
(5, 'Bernard', 'Alice', 34, 'alice.bernard@example.com'),
(6, 'Leroy', 'Sophie', 38, 'sophie.leroy@example.com'),
(7, 'Rabe', 'Toky', 24, 'toky.rabe@example.com'),
(8, 'Rakoto', 'Fara', 17, 'fara.rakoto@example.com'),
(9, 'Randri', 'Tiana', 24, 'tiana.randri@example.com'),
(10, 'Andrianina', 'Hery', 28, 'hery.andrianina@example.com'),
(11, 'Rasoa', 'Miora', 26, 'miora.rasoa@example.com'),
(12, 'Robert', 'Julien', 35, 'julien.robert@example.com'),
(13, 'Richard', 'Chloé', 29, 'chloe.richard@example.com'),
(14, 'Rasoanaivo', 'Anjara', 24, 'anjara.rasoanaivo@example.com'),
(15, 'Rakotobe', 'Ony', 21, 'ony.rakotobe@example.com'),
(16, 'Lefèvre', 'Louis', 18, 'louis.lefevre@example.com'),
(17, 'Lambert', 'Élise', 37, 'elise.lambert@example.com'),
(18, 'Ravelomanana', 'Fanilo', 38, 'fanilo.ravelomanana@example.com'),
(19, 'Andriamihaja', 'Sarobidy', 39, 'sarobidy.andriamihaja@example.com'),
(20, 'Razafindrakoto', 'Voahirana', 15, 'voahirana.razafindrakoto@example.com'),
(21, 'Rakotomanga', 'Rado', 22, 'rado.rakotomanga@example.com'),
(22, 'Rakotobe', 'Cyprien', 18, 'cyprbe44@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `reservations`
--

CREATE TABLE `reservations` (
  `id_reservation` int(11) NOT NULL,
  `id_livres` int(11) NOT NULL,
  `id_membres` int(11) NOT NULL,
  `date_reservation` datetime DEFAULT current_timestamp(),
  `statut` enum('en_attente','annulée','honorée') DEFAULT 'en_attente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth`
--
ALTER TABLE `auth`
  ADD PRIMARY KEY (`id_auth`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `emprunts`
--
ALTER TABLE `emprunts`
  ADD PRIMARY KEY (`id_emprunts`),
  ADD KEY `id_livre` (`id_livres`),
  ADD KEY `id_membre` (`id_membres`),
  ADD KEY `idx_emprunts_statut` (`statut`);

--
-- Index pour la table `livres`
--
ALTER TABLE `livres`
  ADD PRIMARY KEY (`id_livres`);

--
-- Index pour la table `membres`
--
ALTER TABLE `membres`
  ADD PRIMARY KEY (`id_membres`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id_reservation`),
  ADD KEY `id_livres` (`id_livres`),
  ADD KEY `id_membres` (`id_membres`),
  ADD KEY `idx_reservations_statut` (`statut`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth`
--
ALTER TABLE `auth`
  MODIFY `id_auth` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `emprunts`
--
ALTER TABLE `emprunts`
  MODIFY `id_emprunts` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `livres`
--
ALTER TABLE `livres`
  MODIFY `id_livres` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT pour la table `membres`
--
ALTER TABLE `membres`
  MODIFY `id_membres` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT pour la table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id_reservation` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `emprunts`
--
ALTER TABLE `emprunts`
  ADD CONSTRAINT `emprunts_ibfk_1` FOREIGN KEY (`id_livres`) REFERENCES `livres` (`id_livres`),
  ADD CONSTRAINT `emprunts_ibfk_2` FOREIGN KEY (`id_membres`) REFERENCES `membres` (`id_membres`);

--
-- Contraintes pour la table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`id_livres`) REFERENCES `livres` (`id_livres`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`id_membres`) REFERENCES `membres` (`id_membres`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
