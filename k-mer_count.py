import sys
from collections import Counter

# DNA nucleotide to binary encoding
ENCODING = {
    'A': 0b00,
    'C': 0b01,
    'G': 0b10,
    'T': 0b11
}

def encode_sequence(sequence):
    """Encodes a DNA sequence to a binary format."""
    binary_sequence = 0
    for nucleotide in sequence:
        binary_sequence = (binary_sequence << 2) | ENCODING[nucleotide]
    return binary_sequence

def read_fasta(file_path):
    """Reads a fasta file and returns the concatenated DNA sequence."""
    sequence = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip annotation lines starting with '>'
            if line.startswith(">"):
                continue
            # Append sequence lines
            sequence.append(line)
    return ''.join(sequence)

def count_kmers(sequence, k):
    """Counts all k-mers of length k in the given sequence using binary encoding."""
    kmer_counts = Counter()
    n = len(sequence)
    mask = (1 << (2 * k)) - 1  # Mask for extracting k-mer bits

    # Encode the first k-mer
    current_kmer = encode_sequence(sequence[:k])
    kmer_counts[current_kmer] += 1

    # Slide through the sequence to count k-mers
    for i in range(1, n - k + 1):
        # Shift left by 2 bits and add the new nucleotide
        current_kmer = ((current_kmer << 2) & mask) | ENCODING[sequence[i + k - 1]]
        kmer_counts[current_kmer] += 1

    return kmer_counts

def decode_kmer(binary_kmer, k):
    """Decodes a binary k-mer to its DNA string representation."""
    kmer = []
    for _ in range(k):
        nucleotide_bits = binary_kmer & 0b11
        for nucleotide, encoding in ENCODING.items():
            if encoding == nucleotide_bits:
                kmer.append(nucleotide)
                break
        binary_kmer >>= 2
    return ''.join(reversed(kmer))

def write_output(kmer_counts, k, student_id):
    """Writes the top 100 k-mer counts to an output file."""
    output_file = f"{student_id}.txt"
    with open(output_file, 'w') as f:
        # Sort k-mers by count (descending) and then by binary k-mer (for stable ordering)
        sorted_kmers = sorted(kmer_counts.items(), key=lambda x: (-x[1], x[0]))

        # Find the threshold count for top 100
        threshold_count = sorted_kmers[99][1] if len(sorted_kmers) > 100 else sorted_kmers[-1][1]
        
        # Write all k-mers with count >= threshold_count
        for binary_kmer, count in sorted_kmers:
            if count < threshold_count:
                break
            kmer_string = decode_kmer(binary_kmer, k)
            f.write(f"{kmer_string},{count}\n")
    print(f"Output written to {output_file}")

def main():

    k = 3
    sequence = 'ATGAACGCAGAGAAT'



    """
    # Command-line arguments
    if len(sys.argv) != 3:
        print("입력 변수 개수 이상")
        sys.exit(1)
    
    k = int(sys.argv[1])
    input_file = sys.argv[2]
    
    # Step 1: Read the DNA sequence from the fasta file
    sequence = read_fasta(input_file)
    """
    
    # Step 2: Count all k-mers of length k using binary encoding
    kmer_counts = count_kmers(sequence, k)
    print(kmer_counts)

    """
    # Step 3: Write the top 100 k-mers and any additional k-mers with the same count in the specified format
    write_output(kmer_counts, k, student_id)
    """

if __name__ == "__main__":
    main()
