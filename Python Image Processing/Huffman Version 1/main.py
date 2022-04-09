import tempfile
import huffman
import imageProcessing

def main():
    imageData = imageProcessing.getImageData()
    
    print("Raw image uses " + str(len(imageData) * 2) + " bytes")

    hTable = huffman.createTable(imageData)

    encodedImage = huffman.encode(hTable, imageData)

    # st = "this is a test"
    # cha = []
    # for ch in st:
    #     cha.append(ch)
    # h = huffman.createTable(cha)
    # print(h)

if __name__ == '__main__':
    main()