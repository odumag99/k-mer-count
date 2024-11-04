k=3
sequence = 'ATGAACGCAGAGAAT'

bit_mask = (0b1 << (2 * k)) - 1

count = {}

def decode(code):
    result = []
    
    basic = (0b1 << 2) -1 # if 식별 문자 개수 2개인 경우를 가정함. 0b11.
    for i in range(k):    
        cur_code = code & basic
        if cur_code == 0b00:
            result.append('A')
        elif cur_code == 0b01:
            result.append('G')
        elif cur_code == 0b10:
            result.append('C')
        elif cur_code == 0b11:
            result.append('T')
        else: raise Exception(f'[decode({code:b})]: 존재하지 않는 cur_code {cur_code:b}')
        code = code >> 2

    return ''.join(result[::-1]) # result를 거꾸로 출력해야 함

# cur_sequence = 0b0 << (3 * k)

# cur_sequence 초기화
init_count = 0
i=0
cur_sequence = 0b0
while (init_count <= k):
    cur_gene = sequence[i]
    if cur_gene == 'A':
        cur_gene = 0b00
    elif cur_gene == 'G':
        cur_gene = 0b01
    elif cur_gene == 'C':
        cur_gene = 0b10
    elif cur_gene == 'T':
        cur_gene = 0b11
    else:
        i+=1
        continue
    cur_sequence = (cur_sequence << 2) | cur_gene
    i += 1
    init_count += 1
print(bin(cur_sequence))


for i in range(len(sequence)):
    cur_gene = sequence[i]
    if cur_gene == 'A':
        cur_gene = 0b00
    elif cur_gene == 'G':
        cur_gene = 0b01
    elif cur_gene == 'C':
        cur_gene = 0b10
    elif cur_gene == 'T':
        cur_gene = 0b11
    else: continue
    
    cur_sequence = ((cur_sequence << 2) | cur_gene) & bit_mask
    print(bin(cur_sequence))
    if cur_sequence not in count:
        count[cur_sequence] = 1
    else: count[cur_sequence] += 1

print(len(sequence))
print(count)
print('---result---')
for code, num in count.items():
    code = decode(code)
    print(f'{code}: {num}')