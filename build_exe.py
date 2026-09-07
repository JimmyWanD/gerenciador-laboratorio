"""
Script to build the application as a standalone .exe file
Uses PyInstaller to create the executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_exe():
    """Build the application as a standalone .exe"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create build directory
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "GerenciadorLaboratorio",
        "--icon", "icon.ico",
        "--add-data", "icon.ico;.",
        "--clean",
        "main.py"
    ]
    
    print("Iniciando build do executável...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild concluído com sucesso!")
        print(f"Arquivo .exe criado em: {dist_dir / 'GerenciadorLaboratorio.exe'}")
        
        # Copy database file if exists
        if Path("laboratorio.db").exists():
            shutil.copy("laboratorio.db", dist_dir / "laboratorio.db")
            print(f"Banco de dados copiado para: {dist_dir / 'laboratorio.db'}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro durante o build: {e}")
        return False


def create_icon():
    """Create a simple icon file if it doesn't exist"""
    icon_path = Path("icon.ico")
    if not icon_path.exists():
        print("Criando ícone padrão...")
        # Create a simple icon using PIL
        try:
            from PIL import Image, ImageDraw
            
            # Create a simple icon
            img = Image.new('RGB', (64, 64), color=(0, 120, 215))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple flask icon
            draw.rectangle([10, 10, 54, 54], outline=(255, 255, 255), width=3)
            draw.polygon([(32, 10), (15, 40), (49, 40)], fill=(255, 255, 255))
            
            img.save(icon_path, format='ICO')
            print(f"Ícone criado: {icon_path}")
        except ImportError:
            print("PIL/Pillow não encontrado. Usando ícone padrão do sistema.")
            # Create a dummy file
            with open(icon_path, 'wb') as f:
                f.write(b'')


def main():
    """Main function"""
    print("=" * 60)
    print("Gerenciador de Laboratório - Build Script")
    print("=" * 60)
    
    # Create icon if needed
    create_icon()
    
    # Build the executable
    success = build_exe()
    
    if success:
        print("\nPara executar o aplicativo:")
        print("1. Copie o arquivo 'dist/GerenciadorLaboratorio.exe' para o pen drive")
        print("2. Copie também o arquivo 'laboratorio.db' (se existir)")
        print("3. Execute o .exe com um duplo clique")
    else:
        print("\nOcorreu um erro durante o build.")


if __name__ == '__main__':
    main()
