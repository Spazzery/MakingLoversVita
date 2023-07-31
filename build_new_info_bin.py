import os, re

LABEL_COUNT = 510

def get_labels_from_file(filename):
    result = []
    with open(filename, "r", encoding="shift-jis") as f:
        all_lines = f.read().split("\n")
        for line in all_lines:
            if line.startswith("<label :"):
                result.append(line)
    return result
    
def get_labels_offsets_from_file(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        
    offsets = []
    byte_sequence = bytes.fromhex("3C 6C 61 62 65 6C 20 3A")
    offset = contents.find(byte_sequence)
    while offset != -1:
        offsets.append(offset)
        offset = contents.find(byte_sequence, offset + 1)

    return offsets

def build(directory):
    
    result = []
    
    # Header
    result.append(LABEL_COUNT.to_bytes(4, byteorder="little"))
    result.append(b'\x00\x00\x00\x00')
    
    # File info section
    for filename in os.listdir(directory):
        if filename.endswith("txt"): 
            all_labels_from_file = get_labels_from_file(directory + "/" + filename)
            all_labels_offsets_from_file = get_labels_offsets_from_file(directory + "/" + filename)
            
            # print(f"Labels count: {all_labels_from_file}")
            # print(f"Offsets count: {all_labels_offsets_from_file}")
            # print(f"Filename: {filename}")
            # print("-----")
            
            assert len(all_labels_from_file) == len(all_labels_offsets_from_file)
            
            for i in range(0, len(all_labels_from_file)):
                label = all_labels_from_file[i][7:-1]  # extracts label name from <label: name>
                offset = all_labels_offsets_from_file[i]
                
                # Write label (length 64)
                padded_label = label.encode() + b'\x00' + b'\xFE' * (64 - (len(label) + 1)) # +1 because of the 00 byte
                result.append(padded_label)
                
                # Write filename (length 64)
                padded_filename = filename.encode() + b'\x00' + b'\xFE' * (64 - (len(filename) + 1))
                result.append(padded_filename)
                
                # Write label offset (length 8)
                padded_offset = offset.to_bytes(4, byteorder="little") + b'\x00\x00\x00\x00'
                result.append(padded_offset)
                
    # Write the result into a binary file
    with open(directory + "/" + "00_info.bin", "wb") as bf:
        for i in result:
            bf.write(i)
            
    print("Finished creating a new 00_info.bin!")

if __name__ == '__main__':
    build("repack")


