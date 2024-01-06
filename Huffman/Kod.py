class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_huffman_tree(data):
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1

    nodes = [Node(char, freq) for char, freq in frequency.items()]

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        new_node = Node(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        nodes.append(new_node)

    return nodes[0]

def generate_huffman_codes(root, current_code="", codes={}):
    if root is not None:
        if root.char is not None:
            codes[root.char] = current_code
        generate_huffman_codes(root.left, current_code + "0", codes)
        generate_huffman_codes(root.right, current_code + "1", codes)
    return codes

def compress_data(data, huffman_codes):
    compressed_data = ""
    for char in data:
        compressed_data += huffman_codes[char]
    return compressed_data

def encode_tree(root):
    encoded_tree = ""

    def encode_node(node):
        nonlocal encoded_tree
        if node is not None:
            if node.char is not None:
                encoded_tree += "1" + bin(ord(node.char))[2:].zfill(8)  # Leaf node
            else:
                encoded_tree += "0"  # Internal node
                encode_node(node.left)
                encode_node(node.right)

    encode_node(root)
    return encoded_tree

def decode_data(compressed_data, root):
    decoded_data = ""
    current_node = root

    for bit in compressed_data:
        if bit == "0":
            current_node = current_node.left
        elif bit == "1":
            current_node = current_node.right

        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = root  # Reset na korijen za sljedeći znak

    return decoded_data

# Primjer upotrebe:
data_to_compress = "abracadabra"

# Korak 1: Izgradnja Huffmanovog stabla
root = build_huffman_tree(data_to_compress)

# Korak 2: Generiranje Huffman kodova
huffman_codes = generate_huffman_codes(root)

# Korak 3: Kompresija podataka
compressed_data = compress_data(data_to_compress, huffman_codes)

# Korak 4: Pohrana stabla u komprimiranoj datoteci
encoded_tree = encode_tree(root)

# Korak 5: Dekompresija podataka
decoded_data = decode_data(compressed_data, root)

# Testiranje
print("Original Data:", data_to_compress)
print("Compressed Data:", compressed_data)
print("Encoded Tree:", encoded_tree)
print("Decoded Data:", decoded_data)
print("Are original and decoded data equal?", data_to_compress == decoded_data)