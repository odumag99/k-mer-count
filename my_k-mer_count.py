import sys
import heapq
from collections import deque


def decode(code):
    result = []
    
    basic = (0b1 << 2) -1 # if 식별 문자 개수 4개인 경우(=각 문자당 2bit)를 가정함. 0b11.
    for i in range(k):    
        cur_code = code & basic
        if cur_code == 0b11:
            result.append('A')
        elif cur_code == 0b10:
            result.append('C')
        elif cur_code == 0b01:
            result.append('G')
        elif cur_code == 0b00:
            result.append('T')
        else: raise Exception(f'[decode({code:b})]: 존재하지 않는 cur_code {cur_code:b}')
        code = code >> 2

    return ''.join(result[::-1]) # result를 거꾸로 출력해야 함


def kmer_count(sequence):
    # cur_sequence 초기화
    init_count = 0
    i=0
    cur_sequence = 0b0
    while (init_count < k-1):
        cur_gene = sequence[i]
        if cur_gene == 'A':
            cur_gene = 0b11
        elif cur_gene == 'C':
            cur_gene = 0b10
        elif cur_gene == 'G':
            cur_gene = 0b01
        elif cur_gene == 'T':
            cur_gene = 0b00
        else:
            i+=1
            continue
        cur_sequence = (cur_sequence << 2) | cur_gene
        i += 1
        init_count += 1
    # print(bin(cur_sequence))

    # count 시작
    for idx in range(i, len(sequence)):
        cur_gene = sequence[idx]
        if cur_gene == 'A':
            cur_gene = 0b11
        elif cur_gene == 'C':
            cur_gene = 0b10
        elif cur_gene == 'G':
            cur_gene = 0b01
        elif cur_gene == 'T':
            cur_gene = 0b00
        else: continue
        
        cur_sequence = ((cur_sequence << 2) | cur_gene) & bit_mask
        # print(decode(cur_sequence))
        count[cur_sequence] += 1 # count는 전역변수 -> sequence별 총합되게끔



# print(count)
# print('---result---')

# sort 과정에서 효율성 개선해 볼 여지 있긴 할 듯.

def sort_mers(count, num_cutline):
    result = deque()
    min_heap = []
    threshold = deque()
    for code, num in count.items():
        heapq.heappush(min_heap, (num, code))
        if len(min_heap) > num_cutline:
            temp = heapq.heappop(min_heap)
            print('temp:', temp)
            if len(threshold)>0 and min_heap[0][0] > threshold[0][0]:
                print('threshold reset')
                threshold = deque()
            if min_heap[0][0] == temp[0]:
                print('threshold append')
                threshold.append(temp)
    
    while min_heap:
        result.appendleft(heapq.heappop(min_heap))
    
    print('threshold:', threshold)
    while threshold:
        result.append(threshold.pop())

    result = sorted(result, key = lambda x: (x[0], x[1]), reverse=True)

    return result



"""
sorted_count = sorted(count.items(), key=lambda x: (x[1], x[0]), reverse=True)
print_count = 0
prev_num = -1
for code, num in sorted_count:
    # 100이 넘었고, 그 이전 값과 다른 경우는 break
    if print_count > num_cutline and num != prev_num:
        break
    code = decode(code)
    print(f'{code},{num}')
    print_count += 1
    prev_num = num
"""

def read_fasta(file_path):
    """Reads a fasta file and returns the concatenated DNA sequence."""
    sequences = []
    sequence_buffer = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if sequence_buffer:
                    sequences.append(''.join(sequence_buffer))
                    sequence_buffer = []
                continue
            else:
                sequence_buffer.append(line)
        
        if sequence_buffer:
            sequences.append(''.join(sequence_buffer))
        
    return sequences

if __name__ == '__main__':
    num_cutline = 10

    if len(sys.argv) != 3:
        print("입력 변수 개수 이상")
        sys.exit(1)

    k = int(sys.argv[1])
    input_file = sys.argv[2]

    bit_mask = (0b1 << (2 * k)) - 1
    
    # count 초기화
    count = {}
    for i in range(0, 4**k):
        count[i] = 0
    
    sequences = read_fasta(input_file)

    for sequence in sequences:
        kmer_count(sequence)
    
    sorted_count = sort_mers(count, num_cutline)

    with open('201815042.txt', 'w') as f:
        f.write(f'{decode(sorted_count[0][1])},{sorted_count[0][0]}')
        if len(sorted_count) > 1:
            for num, code in sorted_count[1:]:
                f.write(f'\n{decode(code)},{num}')