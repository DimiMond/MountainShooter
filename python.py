from pathlib import Path
from PIL import Image

#Código criado para não dar erros nas imagens após o fechamento do game!!

root = Path(__file__).parent
assets = root / "asset"

count = 0
for p in assets.rglob("*.png"):
    try:
        img = Image.open(p)
        mode = "RGBA" if "A" in img.getbands() else "RGB"
        if img.mode != mode:
            img = img.convert(mode)
        had_icc = "icc_profile" in img.info
        img.save(p, icc_profile=None, optimize=True)
        count += 1
        print(f"[OK] {p}  (perfil removido: {had_icc})")
    except Exception as e:
        print(f"[ERRO] {p}: {e}")

print(f"Concluído. {count} arquivos processados.")