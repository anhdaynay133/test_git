
chars = []
codes = []
f = open("Chars.txt", 'r', errors="ignore")
Tables_chars = f.read().split("\n")
file = open("Codes.txt", 'r', errors="ignore")
Tables_codes = file.read().split("\n")
# print(unicode_table)
for i in Tables_chars:  
    chars.append(i) 
print(chars)

for j in Tables_codes:  
    codes.append(j)
print(codes)
