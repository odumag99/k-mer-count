import sys

# Command-line arguments
if len(sys.argv) != 3:
    print("입력 변수 개수 이상")
    sys.exit(1)

k = int(sys.argv[1])
input_file = sys.argv[2]
print('k:', k)
print('input_file:', input_file)
print(sys.argv)

if __name__ == "__main__":
    print(f'__name__:{__name__}')
    print('Line 1')
    print('Line 2')