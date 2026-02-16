# Dossier Images Sources

Ce dossier doit contenir vos images sources pour la génération des atlas.

## Structure

Placez vos images directement dans ce dossier ou dans des sous-dossiers. Le générateur d'atlas lira récursivement tous les fichiers images.

```
images/
├── poster1.png
├── poster2.jpg
├── art/
│   ├── artwork1.png
│   └── artwork2.png
└── photos/
    ├── photo1.jpg
    └── photo2.jpg
```

## Formats supportés

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- BMP (`.bmp`)
- WebP (`.webp`)

## Notes importantes

- Les images seront automatiquement redimensionnées si elles dépassent 2048x2048 pixels
- L'algorithme de packing optimisera l'utilisation de l'espace dans les atlas
- Des atlas downscalés (x2, x4, etc.) seront créés automatiquement si nécessaire pour respecter la limite de taille

## Workflow GitHub Actions

Le workflow `.github/workflows/generate-atlas.yml` :
1. Surveille les changements dans ce dossier `images/`
2. Génère automatiquement les atlas
3. Déploie les atlas sur GitHub Pages

Pour déclencher la génération :
- Commitez et poussez vos images dans ce dossier
- Ou utilisez l'option "Run workflow" manuellement sur GitHub Actions

## Utilisation locale

Pour générer les atlas localement :

```bash
cd Generator
python generate_posters.py
```

Les atlas générés seront dans `Generator/output_atlases/`.
