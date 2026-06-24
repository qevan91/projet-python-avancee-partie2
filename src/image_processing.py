import io
import os

import requests
from PIL import Image, UnidentifiedImageError, ImageDraw

# Constantes codées en dur selon les spécifications
IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/"
    "7/7b/Moby_Dick_p510_illustration.jpg"
)
LOGO_PATH = "data/logo.png"
OUTPUT_PATH = "data/image_finale.jpg"


class ImageProcessingError(Exception):
    """Exception personnalisée pour les erreurs de traitement d'image.

    Permet de distinguer nos erreurs métiers des exceptions standards.
    """

    def __init__(self, message: str) -> None:
        """Initialise l'exception avec un message spécifique.

        Args:
            message: Le texte explicatif de l'erreur rencontrée.
        """
        super().__init__(message)


def download_image(url: str) -> Image.Image:
    """Télécharge une image depuis une URL distante en mémoire.

    Args:
        url: L'URL directe vers l'image à télécharger.

    Returns:
        L'image chargée sous forme d'objet PIL.Image.

    Raises:
        ImageProcessingError: En cas d'échec réseau ou si le contenu
            téléchargé n'est pas une image valide.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        with requests.get(
                url, headers=headers, stream=True, timeout=10
        ) as response:
            response.raise_for_status()
            content = response.content
    except requests.RequestException as e:
        raise ImageProcessingError(f"Échec du téléchargement : {e}")

    try:
        image = Image.open(io.BytesIO(content))
        image.load()
        return image
    except UnidentifiedImageError:
        raise ImageProcessingError(
            "Le contenu récupéré n'est pas une image lisible."
        )


def crop_and_resize(image: Image.Image) -> Image.Image:
    """Recadre l'image de 10% sur les bords, puis la redimensionne.

    Args:
        image: L'objet image source à manipuler.

    Returns:
        Une nouvelle instance d'image recadrée et redimensionnée.
    """
    width, height = image.size

    left = int(width * 0.1)
    top = int(height * 0.1)
    right = int(width * 0.9)
    bottom = int(height * 0.9)

    cropped_image = image.crop((left, top, right, bottom))

    target_size = (800, 600)
    resized_image = cropped_image.resize(target_size)

    return resized_image


def apply_logo(base_image: Image.Image, logo_path: str) -> Image.Image:
    """Superpose un logo pivoté sur l'image de base.

    Args:
        base_image: L'image principale qui servira de fond.
        logo_path: Le chemin local vers le fichier image du logo.

    Returns:
        L'image composite finale avec le logo intégré.

    Raises:
        ImageProcessingError: Si le fichier logo est introuvable ou illisible.
    """
    try:
        with Image.open(logo_path) as logo:
            # Conversion explicite en niveaux de gris (L) pour le noir et blanc
            bw_logo = logo.convert("L")

            # Création d'un masque transparent pour la rotation
            rgba_logo = bw_logo.convert("RGBA")
            rotated_logo = rgba_logo.rotate(45, expand=True)

            composite = base_image.copy()
            position_x = 50
            position_y = 50

            # On utilise le canal alpha du logo pivoté comme masque de collage
            composite.paste(
                rotated_logo,
                (position_x, position_y),
                rotated_logo
            )

            return composite
    except FileNotFoundError:
        raise ImageProcessingError(f"Le fichier logo est absent: {logo_path}")
    except OSError as e:
        raise ImageProcessingError(f"Erreur de lecture du logo: {e}")


def _generate_mock_logo(path: str) -> None:
    """Génère un logo temporaire en noir et blanc si manquant sur le disque."""

    # Création d'une image carrée de 100x100 en mode niveaux de gris (L)
    img = Image.new("L", (100, 100), color=0)# Fond noir (0), dessin d'un carré blanc (255) au centre
    draw = ImageDraw.Draw(img)
    draw.rectangle([25, 25, 75, 75], fill=255)
    img.save(path)


def main() -> None:
    """Orchestre les opérations de téléchargement et de traitement."""
    try:
        # Si pas de logo on en crée un automatiquement
        if not os.path.exists(LOGO_PATH):
            print(f"{LOGO_PATH} n'existe pas. Génération d'un logo de test")
            _generate_mock_logo(LOGO_PATH)

        # Déroulement du script
        source_image = download_image(IMAGE_URL)
        formatted_image = crop_and_resize(source_image)
        final_image = apply_logo(formatted_image, LOGO_PATH)

        final_image.save(OUTPUT_PATH)
        print(f"L'image finale est sauvegardée : {OUTPUT_PATH}")

    except ImageProcessingError as custom_error:
        print(f"Opération interrompue : {custom_error}")
    except Exception as unexpected_error:
        print(f"Erreur inattendue du système : {unexpected_error}")


if __name__ == "__main__":
    main()