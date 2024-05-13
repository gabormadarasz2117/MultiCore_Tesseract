# Tesseract OCR N (X4) szálon
Az input mappában található összes .pdf fájlon OCR-t hajt végre a Tesseract 5.0 verziójával. Egyszerre N fájlt dolgoz fel (N*4 szálon).


Figyelem: A memóriahasználat magas lehet, ha sok szálon fut. Érdemes úgy számolni, hogy -p 10 = 100GB RAM!

## Install

### Build docker

```bash
bash ./build_docker.sh
```

## Run program on a folder
Opciók: 

-i <PATH> : Az input mappa elérési útvonala (Az OCR-ezendő .pdf fájlokat tartalmazó mappa)

-o <PATH> : Az output mappa elérési útvonala (Ha nincs megadva, akkor a  .txt fájlokat az input mappába menti.)

-p <int>  : A processek száma. Default = 2 (Note: A Tesseract 4 szálat használ processenként, ezért legfeljebb a processzorok 24%-a)

-l <string> : Az OCR-ezni kívánt dokumentumok nyelve. Default = "hun" (Note: Csak a magyar és angol nyelvi szótár van feltelepítve.)

-d <bool> : A modell megbízhatósága a karakterfelismeréssel kapcsolatban. Default = False

```bash
python3 run_docker2.py -i /home/pdf -o /home/txt -p 10 -l hun -d True
```
