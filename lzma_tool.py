import argparse
import lzma
import os
import sys
from pathlib import Path


CHUNK_SIZE = 1024 * 1024


def compress_file(input_path: Path, output_path: Path, preset: int) -> None:
    with input_path.open("rb") as src, lzma.open(output_path, "wb", preset=preset, format=lzma.FORMAT_XZ) as dst:
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            dst.write(chunk)


def decompress_file(input_path: Path, output_path: Path) -> None:
    with lzma.open(input_path, "rb") as src, output_path.open("wb") as dst:
        while True:
            chunk = src.read(CHUNK_SIZE)
            if not chunk:
                break
            dst.write(chunk)


def default_output_for_compress(input_path: Path) -> Path:
    return input_path.with_suffix(input_path.suffix + ".xz") if input_path.suffix else Path(str(input_path) + ".xz")


def default_output_for_decompress(input_path: Path) -> Path:
    if input_path.suffix == ".xz":
        return input_path.with_suffix("")
    return Path(str(input_path) + ".out")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Outil simple de compression/decompression LZMA (.xz)."
    )
    parser.add_argument(
        "mode",
        choices=["compress", "decompress"],
        help="Mode: compress (compresser) ou decompress (decompresser).",
    )
    parser.add_argument("input", help="Fichier source.")
    parser.add_argument("-o", "--output", help="Fichier de sortie.")
    parser.add_argument(
        "-p",
        "--preset",
        type=int,
        default=6,
        help="Niveau de compression LZMA (0-9, defaut: 6). Utilise seulement en mode compress.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Ecraser le fichier de sortie s'il existe.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Erreur: fichier introuvable: {input_path}", file=sys.stderr)
        return 1

    if args.mode == "compress":
        if not 0 <= args.preset <= 9:
            print("Erreur: --preset doit etre entre 0 et 9.", file=sys.stderr)
            return 1
        output_path = Path(args.output) if args.output else default_output_for_compress(input_path)
    else:
        output_path = Path(args.output) if args.output else default_output_for_decompress(input_path)

    if output_path.exists() and not args.force:
        print(f"Erreur: le fichier de sortie existe deja: {output_path} (utilisez --force)", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if args.mode == "compress":
            compress_file(input_path, output_path, args.preset)
        else:
            decompress_file(input_path, output_path)
    except lzma.LZMAError as exc:
        print(f"Erreur LZMA: {exc}", file=sys.stderr)
        if output_path.exists():
            try:
                output_path.unlink()
            except OSError:
                pass
        return 2
    except OSError as exc:
        print(f"Erreur fichier: {exc}", file=sys.stderr)
        return 3

    in_size = input_path.stat().st_size
    out_size = output_path.stat().st_size

    if args.mode == "compress" and in_size > 0:
        ratio = out_size / in_size
        print(f"Compression terminee: {input_path} -> {output_path}")
        print(f"Taille: {in_size} -> {out_size} octets (ratio {ratio:.2%})")
    else:
        print(f"Operation terminee: {input_path} -> {output_path}")
        print(f"Taille: {in_size} -> {out_size} octets")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
