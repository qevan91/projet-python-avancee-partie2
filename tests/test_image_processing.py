import unittest
from unittest.mock import patch, MagicMock

from PIL import Image

# Import du module à tester
from src.image_processing import crop_and_resize
from src.image_processing import download_image
from src.image_processing import ImageProcessingError


class TestImageProcessing(unittest.TestCase):
    """Regroupe les cas de tests pour les différentes manipulations d'images."""

    def setUp(self) -> None:
        """Initialise les ressources partagées pour les tests."""
        # Création d'une image factice de 1000x1000 pixels (en mémoire brute)
        self.image_test = Image.new("RGB", (1000, 1000), color="white")

    def test_crop_and_resize_dimensions(self) -> None:
        """Vérifie que la fonction retourne systématiquement la taille cible."""
        image_resultat = crop_and_resize(self.image_test)

        largeur, hauteur = image_resultat.size

        # Validation des dimensions (800x600 définies en dur dans le script)
        self.assertEqual(largeur, 800)
        self.assertEqual(hauteur, 600)

    @patch('src.image_processing.requests.get')
    def test_download_image_succes(self, mock_get: MagicMock) -> None:
        """Valide le flux de téléchargement face à une réponse HTTP correcte."""
        # Configuration de la fausse réponse réseau
        mock_reponse = MagicMock()
        mock_reponse.content = b"octets_image_factices"
        mock_reponse.raise_for_status.return_value = None

        # Simule le gestionnaire de contexte "with requests.get(...) as response"
        mock_get.return_value.__enter__.return_value = mock_reponse

        # On simule Image.open pour empêcher PIL d'essayer de lire nos faux octets
        with patch('src.image_processing.Image.open') as mock_open:
            mock_image_pil = MagicMock()
            mock_open.return_value = mock_image_pil

            resultat = download_image("https://domaine-test.com/image.jpg")

            # Vérification via l'opérateur "is not None" comme exigé
            self.assertTrue(resultat is not None)
            mock_open.assert_called_once()

    @patch('src.image_processing.requests.get')
    def test_download_image_echec_reseau(self, mock_get: MagicMock) -> None:
        """Vérifie le déclenchement de notre exception métier en cas de crash HTTP."""
        import requests
        # Simule une chute de connexion brutale
        mock_get.side_effect = requests.RequestException("Erreur réseau")

        with self.assertRaises(ImageProcessingError) as contexte:
            download_image("https://domaine-test.com/image.jpg")

        # L'utilisation d'une méthode de chaîne native plutôt que des slices
        self.assertTrue(
            str(contexte.exception).startswith("Échec du téléchargement")
        )

    def tearDown(self) -> None:
        """Nettoie proprement la RAM après chaque fonction de test."""
        self.image_test.close()


if __name__ == "__main__":
    unittest.main()