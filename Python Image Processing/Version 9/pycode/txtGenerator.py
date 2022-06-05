def generateHuffmanTableTxt(huffmanTable):
    with open('Huffman Table.txt', 'w') as f:
        for row in huffmanTable:
            for item in row:
                f.write(str(item) + ", ")
            f.write("\n")