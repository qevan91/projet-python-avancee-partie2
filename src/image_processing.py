import io
import requests
from PIL import Image, UnidentifiedImageError

# Constantes
IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/"
    "3/36/Moby-Dick_p510_illustration.jpg"
)
LOGO_PATH = "logo_nb.png"
OUTPUT_PATH = "moby_dick_final.jpg"


class ImageProcessingError(Exception):
    """Exception personnalisée levée pour les erreurs de traitement d'image.

    Args:
        message (str): Le message d'erreur expliquant la cause de l'échec.
    """
    def __init__(self, message: str):
        super().__init__(message)


def download_image(url: str) -> Image.Image:
    """Télécharge une image depuis une URL donnée.

    Args:
        url (str): Le lien direct vers l'image.

    Returns:
        Image.Image: L'objet image Pillow téléchargé et chargé en mémoire.

    Raises:
        ImageProcessingError: Si l'URL est invalide ou le réseau échoue.
    """
    if not url.startswith("http"):
        raise ImageProcessingError("L'URL fournie doit commencer par 'http'.")

    # Utilisation du gestionnaire de contexte pour sécuriser la session réseau
    try:
        # Ajout du User-Agent pour passer la sécurité de Wikimedia
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ImageProcessingError(f"Erreur réseau lors de la requête : {e}")

    # Portée try/except très réduite, isolant uniquement l'ouverture Pillow
    try:
        image_data = io.BytesIO(response.content)
        image = Image.open(image_data)
        image.load()
        return image
    except UnidentifiedImageError:
        raise ImageProcessingError("Les données ne sont pas une image valide.")


def process_and_merge_images(
        base_img: Image.Image, logo_path: str
) -> Image.Image:
    """Recadre, redimensionne et incruste un logo sur l'image de base.

    Args:
        base_img (Image.Image): L'image principale téléchargée.
        logo_path (str): Le chemin vers l'image du logo sur le disque.

    Returns:
        Image.Image: La nouvelle image combinée et traitée.

    Raises:
        ImageProcessingError: Si le fichier du logo est introuvable.
    """
    assert base_img is not None, "L'image de base ne doit pas être nulle."

    # Suppression de 10% des bordures
    width, height = base_img.size
    crop_box = (
        int(width * 0.1),
        int(height * 0.1),
        int(width * 0.9),
        int(height * 0.9)
    )
    cropped_img = base_img.crop(crop_box)

    # Redimensionnement à une taille standard arbitraire
    resized_img = cropped_img.resize((600, 400))

    # Chargement, rotation et incrustation du logo
    try:
        with Image.open(logo_path) as logo:
            logo.load()

            # Conversion stricte en noir et blanc et rotation
            bw_logo = logo.convert("L")
            rotated_logo = bw_logo.rotate(45, expand=True)

            # Redimensionnement proportionnel du logo pour l'incrustation
            rotated_logo.thumbnail((150, 150))

            # Calcul des coordonnées pour un placement en bas à droite
            pos_x = resized_img.width - rotated_logo.width - 20
            pos_y = resized_img.height - rotated_logo.height - 20

            # Utilisation de copy() pour préserver l'image source intacte
            final_img = resized_img.copy()
            final_img.paste(rotated_logo, (pos_x, pos_y))

            return final_img

    except FileNotFoundError:
        raise ImageProcessingError(f"Logo introuvable au chemin : {logo_path}")


def main():
    """Exécute la séquence principale de téléchargement et traitement."""
    print("Début du traitement des images")

    try:
        img_moby_dick = download_image(IMAGE_URL)
        final_result = process_and_merge_images(img_moby_dick, LOGO_PATH)

        # Enregistrement du résultat sur le disque
        final_result.save(OUTPUT_PATH)
        print(f"L'image combinée a été générée avec succès sous le nom '{OUTPUT_PATH}'.")

    except ImageProcessingError as e:
        print(f"L'opération a été interrompue : {e}")


if __name__ == "__main__":
    main()