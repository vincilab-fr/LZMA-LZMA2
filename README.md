# Outil LZMA (Python)

Petit programme CLI pour compresser/decompresser des fichiers en **LZMA/XZ**.

## Prerequis

- Python 3 (module `lzma` inclus dans la bibliotheque standard)

## Utilisation

### Compression

```powershell
python .\lzma_tool.py compress .\mon_fichier.txt
```

Sortie par defaut: `mon_fichier.txt.xz`

### Decompression

```powershell
python .\lzma_tool.py decompress .\mon_fichier.txt.xz
```

### Options utiles

- `-o, --output` : definir le fichier de sortie
- `-p, --preset` : niveau de compression `0` a `9` (defaut `6`)
- `-f, --force` : ecraser la sortie existante

Exemple:

```powershell
python .\lzma_tool.py compress .\logs.txt -p 9 -o .\logs.txt.xz -f
```
