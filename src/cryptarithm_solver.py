from timeit import default_timer as timer
import os
from os.path import dirname,abspath

# Fungsi membaca file soal
def read_input():
    directory = dirname(dirname(abspath(__file__)))
    namafile = input("Masukkan nama file : ")
    pathfile = os.path.join(directory, 'test\\' + namafile)
    f = open(pathfile, "r")
    listkata = []
    content = f.readlines()
    for word in content:
        listkata.append(word.replace("\n", "").replace("+","").replace(" ",""))
    listkata.pop(-2)
    return listkata, content


# FUNGSI PERMUTASI
def permutations(iterable, r=None):
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

# Fungsi menghitung nilai kata
def word_val(word, dict):
    result = 0
    k = 1
    reversed_word = word[::-1]
    for x in range(len(reversed_word)):
        result += dict[reversed_word[x]] * k
        k *= 10
    return result

# FUNGSI UTAMA  
def cryptarithm_solver(list_of_strings):
    # Menggunakan metode join untuk menggabungkan semua kata dalam list_of_strings
    joined_list_of_strings = ''.join(list_of_strings)
    # Membuat menjadi set, sehingga assignment value ke key dalam dictionary tidak ada yang double
    set_list_of_strings = set(joined_list_of_strings)
    finalList = tuple(set_list_of_strings)
    # Membuat kamus dengan key dari set(list_kata) dan value berupa angka dari permutasi dengan metode 'zip'
    digits = list(range(10)) # Angka yang bisa digunakan adalah 0 - 9
    sub_try = 0 # Menghitung jumlah percobaan
    n = len(finalList)
    if(n > 10):
        return " "
    else:
        pass
    for possibility in permutations(digits,n):
        word_dict = dict(zip(finalList,possibility)) # Membentuk <key:value> dengan key adalah huruf dan value adalah angka
        # RESTRIKSI 0 untuk awal kata operand dan result
        count0 = 0
        for i in range(len(list_of_strings)):
            if(word_dict[list_of_strings[i][0]] == 0) :
                count0 += 1
        if count0 != 0:
            continue
        # LOLOS RESTRIKSI 0
        else:
            operand_result = 0
            # Untuk save hasil dari perhitungan
            solutions = []
            # Iterate sampai 1 elemen sebelum terakhir, karena dipakai sebagai result
            for i in range(len(list_of_strings)-1):
                operand_result += word_val(list_of_strings[i],word_dict)
                solutions.append(word_val(list_of_strings[i],word_dict))
            
            if (operand_result == word_val(list_of_strings[-1], word_dict)):
                solutions.append(word_val(list_of_strings[-1], word_dict))
                return solutions, sub_try
        sub_try += 1
    return "Tidak ditemukan solusi"


print("Pastikan mengisi persamaan di problems.txt, dan meletakkan file di tempat yang sama dengan source code Python")

while(True):
    start = str(input("Perhitungan akan dimulai, ketik 'Y' jika siap 'X' untuk keluar: ")).upper()
    if(start == 'Y'):
        problem = read_input()
        for word in problem[1]: #Print OUTPUT kedua dari fungsi read_input 
            print(word, end = '')
        print('\n')
        # MULAI
        start_time = timer()
        result = cryptarithm_solver(problem[0]) #Output fungsi read_input pertama menjadi parameter fungsi cryparithms solver
        end_time = timer()
        if (result == " "):
            print("Jumlah huruf lebih dari 10")
            break
        else:
            sols = result[0] # OUTPUT RESULT PERTAMA MENJADI SOLUSI
            print("Solusi dari persamaan adalah :")
            for i in range(len(sols)):
                if(i != len(sols) - 2):
                    print(str(sols[i]))
                else:
                    print(str(sols[i]) + " +")
                    print("-----")
            print("Dibutuhkan {} detik dan {} percobaan substitusi".format(end_time - start_time, result[1]))
        break
    else:
        print("Program selesai")
        break