-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 02 oct. 2025 à 07:51
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
(5, 15, 8, '2025-09-30', '2025-09-30', 'rendu', '2025-10-21', 0.00),
(8, 2, 1, '2025-09-30', '2025-10-02', 'rendu', '2025-10-21', 0.00),
(9, 33, 7, '2025-09-30', NULL, 'emprunté', '2025-10-21', 0.00),
(10, 34, 7, '2025-09-30', NULL, 'emprunté', '2025-10-21', 0.00),
(11, 16, 2, '2025-09-30', NULL, 'emprunté', '2025-10-21', 0.00),
(12, 32, 2, '2025-09-30', NULL, 'emprunté', '2025-10-21', 0.00),
(13, 36, 2, '2025-09-30', NULL, 'emprunté', '2025-10-21', 0.00);

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
(60, 'Le Banquet', 'Platon'),
(62, 'Le Seigneur des Anneaux', 'J.R.R. Tolkien'),
(63, 'Les Secrets de l\'Océan Indien', 'Jean Rakoto'),
(64, 'Histoire de Madagascar', 'Solofo Randrianja'),
(65, 'Poèmes de l\'Aube', 'Lucie Rasoanaivo'),
(66, 'Voyage à Antananarivo', 'Pierre Raharison'),
(67, 'Les Mystères de Nosy Be', 'Noro Ravelomanana'),
(68, 'La Révolte des Merina', 'Jean-Pierre Rakotobe'),
(69, 'Sous le Soleil de Tana', 'Michèle Andriamanjato'),
(70, 'L\'Héritage des Ancêtres', 'Rado Andriamihaja'),
(71, 'Ny Ala Mainty', 'Tojo Rakotondrazaka'),
(72, 'Contes de la Côte Est', 'Henri Rabemananjara'),
(73, 'Le Silence des Hautes Terres', 'Fanja Rasolonjatovo'),
(74, 'Ny Fitiavana Tsy Mety Maty', 'Miora Randriamanga'),
(75, 'Anthologie Poétique Malagasy', 'Collectif'),
(76, 'Les Derniers Rois Sakalava', 'Louis Andriamanalina'),
(77, 'La Vallée Rouge', 'Claire Rakotomalala'),
(78, 'Les Voix du Sud', 'Augustin Ramamonjy'),
(79, 'Ny Masoandro Mitsiky', 'Fanilo Raveloson'),
(80, 'Épopée des Hauts Plateaux', 'Dox II'),
(81, 'Le Cri des Ancêtres', 'Serge Ramiandrisoa'),
(82, 'Ny Ala sy Ny Hazo', 'Rija Rakotoarisoa'),
(83, 'Légendes de l\'Imerina', 'Victor Ramiandrisoa'),
(84, 'Ny Rano sy ny Lanitra', 'Sahondra Rabeson'),
(85, 'Les Sentiers de la Brousse', 'Andry Rakotovao'),
(86, 'Le Destin des Hautes Terres', 'Bema Rasolondraibe'),
(87, 'La Voix des Ancêtres', 'Joséphine Randrianja'),
(88, 'Le Feu de l\'Est', 'Hery Andrianarisoa'),
(89, 'Tsara ny Fitiavana', 'Nivo Ravelomanana'),
(90, 'Les Portes de Betsileo', 'Clément Ramahatra'),
(91, 'Chroniques de la Grande Île', 'Solofo Andriamanga'),
(92, 'L\'Énigme du Sud', 'Henri Ramarokoto'),
(93, 'Ny Fo sy Ny Saina', 'Faniry Rakotobe'),
(94, 'Éclats de la Mer Rouge', 'Jean-Baptiste Andriamanana'),
(95, 'La Dernière Reine Merina', 'Mamy Rasoanirina'),
(96, 'Les Échos du Vent', 'Claire Rasoazanamanga'),
(97, 'Fahatsiarovana', 'Rindra Rakotomanga'),
(98, 'Sous le Ciel de Toliara', 'Tantely Rasolonjatovo'),
(99, 'La Pirogue des Ancêtres', 'Patrick Rabemananajara'),
(100, 'Ny Anjara sy Ny Tantara', 'Volatiana Andriamasinoro'),
(101, 'Les Îles du Nord', 'Michel Rakotondrabe'),
(102, 'Rêves de Baobab', 'Koto Ravelonandro'),
(103, 'Les Veillées de l\'Ouest', 'Georges Andriamalala'),
(104, 'Ny Lanitra Manga', 'Soa Rakotondrabe'),
(105, 'Échos des Hautes Plaines', 'Henriette Rasoamanana'),
(106, 'La Légende du Lac Alaotra', 'Joseph Rakotomanga'),
(107, 'Fahatsiarovana an\'i Madagasikara', 'Bako Rasoanirina'),
(108, 'Les Rivières Perdues', 'Patrick Rakotobe'),
(109, 'Ny Zanak\'i Madagasikara', 'Liva Andrianjafy'),
(110, 'Sous l\'Écorce du Baobab', 'Zo Randriamihaja'),
(111, 'La Légende des Betsimisaraka', 'Haja Razafimanantsoa'),
(112, 'Les Ailes de l\'Indri', 'Fanilo Raveloson'),
(113, 'L\'Horizon des Sakalava', 'Claire Rakotovao'),
(114, 'Ny Fanjakana Merina', 'Tsiry Ramaroson'),
(115, 'Les Gardiens de l\'Océan', 'Noely Andriamanga'),
(116, 'La Forêt Enchantée', 'Tiana Rabemananjara'),
(117, 'Chroniques de l\'Androy', 'Miora Randrianja'),
(118, 'Ny Nofo sy Ny Fanahy', 'Sarobidy Rakotomalala'),
(119, 'Les Tambours de la Cité', 'Joël Randriamanana'),
(120, 'Sous le Vent de Tamatave', 'Rina Rasoarimanana'),
(121, 'La Légende de l\'Orchidée Noire', 'Hanitra Ravelomanana'),
(122, 'Ny Tantara sy ny Lovantsofina', 'Onja Andrianantenaina'),
(123, 'Les Épopées de l\'Est', 'Augustin Rakotondramanana'),
(124, 'La Piste des Zébus', 'Rija Rabe'),
(125, 'Les Gardiens du Sud', 'Hery Ravelonandro'),
(126, 'Ny Andriamanitra sy ny Olona', 'Hasina Rakotomavo'),
(127, 'Contes et Chants Sakalava', 'Lalao Ramiandrisoa'),
(128, 'Les Ombres du Menabe', 'Solofonirina Andrianjaka'),
(129, 'La Lumière de Majunga', 'Elia Randriamisa'),
(130, 'Ny Masoandro mody', 'Vola Randriamihaja'),
(131, 'Les Rêves du Valiha', 'Jean-Claude Rakotondrainibe'),
(132, 'Les Routes de l\'Histoire Malgache', 'Feno Andriamampionona');

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
(22, 'Rakotobe', 'Cyprien', 18, 'cyprbe44@gmail.com'),
(23, 'Andriatsitohaina', 'Tsiry', 25, 'tsiry.andriatsitohaina@example.com'),
(24, 'Rakotoarisoa', 'Malala', 27, 'malala.rakotoarisoa@example.com'),
(25, 'Randriamanana', 'Joël', 30, 'joel.randriamanana@example.com'),
(26, 'Andrianjaka', 'Lova', 19, 'lova.andrianjaka@example.com'),
(27, 'Ranaivo', 'Hanitra', 23, 'hanitra.ranaivo@example.com'),
(28, 'Raveloson', 'Nirina', 34, 'nirina.raveloson@example.com'),
(29, 'Rabearivelo', 'Mamy', 28, 'mamy.rabearivelo@example.com'),
(30, 'Rakotomavo', 'Zo', 22, 'zo.rakotomavo@example.com'),
(31, 'Andrianina', 'Tahina', 29, 'tahina.andrianina@example.com'),
(32, 'Razafindrakoto', 'Onja', 21, 'onja.razafindrakoto@example.com'),
(33, 'Ratsimbazafy', 'Feno', 24, 'feno.ratsimbazafy@example.com'),
(34, 'Andriamampionona', 'Tovo', 26, 'tovo.andriamampionona@example.com'),
(35, 'Raharimalala', 'Holy', 20, 'holy.raharimalala@example.com'),
(36, 'Rakotomanga', 'Haja', 33, 'haja.rakotomanga@example.com'),
(37, 'Ravelo', 'Noely', 31, 'noely.ravelo@example.com'),
(38, 'Randriamihaja', 'Vola', 18, 'vola.randriamihaja@example.com'),
(39, 'Andriamasinoro', 'Koloina', 35, 'koloina.andriamasinoro@example.com'),
(40, 'Rasolonjatovo', 'Henintsoa', 27, 'henintsoa.rasolonjatovo@example.com'),
(41, 'Ravony', 'Andry', 23, 'andry.ravony@example.com'),
(42, 'Rakotovao', 'Hasina', 28, 'hasina.rakotovao@example.com'),
(43, 'Andrianantenaina', 'Tantely', 32, 'tantely.andrianantenaina@example.com'),
(44, 'Rasoarimanana', 'Lalasoa', 25, 'lalasoa.rasoarimanana@example.com'),
(45, 'Rakotondramanana', 'Armand', 29, 'armand.rakotondramanana@example.com'),
(46, 'Ramaroson', 'Zoely', 21, 'zoely.ramaroson@example.com'),
(47, 'Randrianarisoa', 'Tsiky', 19, 'tsiky.randrianarisoa@example.com'),
(48, 'Ratsiraka', 'Patrick', 36, 'patrick.ratsiraka@example.com'),
(49, 'Rakotomalala', 'Aina', 24, 'aina.rakotomalala@example.com'),
(50, 'Rasoanaivo', 'Miangaly', 28, 'miangaly.rasoanaivo@example.com'),
(51, 'Rakotomavo', 'Nomena', 26, 'nomena.rakotomavo@example.com'),
(52, 'Randrianambinina', 'Herizo', 23, 'herizo.randrianambinina@example.com'),
(53, 'Raharison', 'Ony', 20, 'ony.rahari@example.com'),
(54, 'Andrianjafy', 'Bako', 34, 'bako.andrianjafy@example.com'),
(55, 'Randriamisa', 'Tsiory', 22, 'tsiory.randriamisa@example.com'),
(56, 'Rakotobe', 'Mialy', 27, 'mialy.rakotobe@example.com'),
(57, 'Razafimanantsoa', 'Joana', 30, 'joana.razafimanantsoa@example.com'),
(58, 'Rakotomaharo', 'Julien', 31, 'julien.rakotomaharo@example.com'),
(59, 'Ravony', 'Elia', 18, 'elia.ravony@example.com'),
(60, 'Ravonison', 'Harisoa', 35, 'harisoa.ravonison@example.com'),
(61, 'Andriamalala', 'Vony', 28, 'vony.andriamalala@example.com'),
(62, 'Rakotondrainibe', 'Tovo', 33, 'tovo.rakotondrainibe@example.com');

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
-- Déchargement des données de la table `reservations`
--

INSERT INTO `reservations` (`id_reservation`, `id_livres`, `id_membres`, `date_reservation`, `statut`) VALUES
(1, 34, 8, '2025-10-02 08:15:49', 'en_attente'),
(2, 32, 7, '2025-10-02 08:21:40', 'en_attente');

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
  MODIFY `id_emprunts` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `livres`
--
ALTER TABLE `livres`
  MODIFY `id_livres` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT pour la table `membres`
--
ALTER TABLE `membres`
  MODIFY `id_membres` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT pour la table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id_reservation` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
