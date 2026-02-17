"""
Script pour générer les atlas dans le contexte de CI/CD
Utilisé par le workflow GitHub Actions
"""

import sys
import os
from pathlib import Path


def generate_atlases_ci(input_folder: str, output_folder: str):
    """
    Génère les atlas à partir des images sources pour CI
    
    Args:
        input_folder: Dossier contenant les images sources
        output_folder: Dossier de sortie pour les atlas
    """
    # Ajouter le dossier parent au path pour importer generate_posters
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from generate_posters import main as generate_atlases
    
    print(f"📂 Dossier d'entrée: {input_folder}")
    print(f"📂 Dossier de sortie: {output_folder}")
    
    # Vérifier que le dossier d'entrée existe
    if not os.path.exists(input_folder):
        print(f"❌ Erreur: Le dossier '{input_folder}' n'existe pas!")
        sys.exit(1)
    
    # Compter les images
    image_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))
    ]
    print(f"🖼️ {len(image_files)} images trouvées")
    
    if not image_files:
        print("⚠️ Aucune image valide trouvée")
        sys.exit(1)
    
    # Générer les atlas en utilisant la fonction refactorisée
    atlas_data = generate_atlases(input_folder, output_folder)
    
    if not atlas_data:
        print("❌ Échec de la génération des atlas")
        sys.exit(1)
    
    return atlas_data


def generate_static_ci(atlas_folder: str, output_static_folder: str):
    """
    Génère la version statique pour GitHub Pages dans le contexte de CI
    
    Args:
        atlas_folder: Dossier contenant les atlas générés
        output_static_folder: Dossier de sortie pour la version statique
    """
    # Ajouter le dossier parent au path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from generate_static import generate_static_version
    
    print(f"📂 Dossier d'atlas: {atlas_folder}")
    print(f"📂 Dossier de sortie: {output_static_folder}")
    
    # Vérifier que le dossier d'atlas existe
    if not os.path.exists(atlas_folder):
        print(f"❌ Erreur: Le dossier '{atlas_folder}' n'existe pas!")
        sys.exit(1)
    
    json_file = Path(atlas_folder) / 'atlas_data.json'
    if not json_file.exists():
        print(f"❌ Erreur: Le fichier {json_file} n'existe pas")
        print("Les atlas n'ont probablement pas été générés correctement")
        sys.exit(1)
    
    # Générer la version statique en utilisant la fonction refactorisée
    result = generate_static_version(atlas_folder, output_static_folder)
    
    if not result:
        print("❌ Échec de la génération de la version statique")
        sys.exit(1)
    
    return result


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Génération d\'atlas pour CI/CD')
    parser.add_argument('command', choices=['generate', 'static'], 
                       help='Commande à exécuter')
    parser.add_argument('--input', default='../images',
                       help='Dossier des images sources')
    parser.add_argument('--output', default='output_atlases',
                       help='Dossier de sortie des atlas')
    parser.add_argument('--static-output', default='output_static',
                       help='Dossier de sortie de la version statique')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_atlases_ci(args.input, args.output)
    elif args.command == 'static':
        generate_static_ci(args.output, args.static_output)
