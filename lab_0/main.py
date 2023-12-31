import time
import math

def cache_proteins(str, p):
    d = 0
    for i, s in enumerate(str):
        d += ord(s) / pow(p, i)
    return d

def main():
    # Аргумент для функции хэширования
    p = 3
    # Нуклеотидные последовательности, для которых ищем топ-100 похожих
    str1 = cache_proteins("MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNA\
            VAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSK", p)
    str2 = cache_proteins("MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGG\
            GPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN", p)
    str3 = cache_proteins("MKSIYFVAGLFVMLVQGSWQRSLQDTEEKSRSFSASQADPLSDPDQMNEDKRHSQGTFTSDYSKYLDSRR\
            AQDFVQWLMNTKRNRNNIAKRHDEFERHAEGTFTSDVSSYLEGQAAKEFIAWLVKGRGRRDFPEEVAIVE\
            ELGRRHADGSFSDEMNTILDNLAARDFINWLIQTKITDRK", p)

    # Создаем пустой словарь для хранения оглавления и названия белка
    protein_dict = {}

    seconds = time.time()
    # Открываем файл для чтения
    with open('uniprot_sprot.txt', 'r') as file:
        lines = file.readlines()
    
    # Итерируемся по строкам файла
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Если строка начинается с ">", это оглавление белка
        if line.startswith('>'):
            # Извлекаем идентификатор белка из оглавления
            header = line[1:]
            protein_name = ''

            # Считываем строки с белком, пока не встретим новое оглавление или достигнем конца файла
            i += 1
            while i < len(lines) and not lines[i].startswith('>'):
                protein_name += lines[i].strip()
                i += 1

            # Добавляем запись в словарь
            protein_dict[header] = cache_proteins(protein_name, p)

    dict1 = {}
    dict2 = {}
    dict3 = {}

    for protein in protein_dict:
        dict1[protein] = abs(str1 - protein_dict[protein])
        dict2[protein] = abs(str2 - protein_dict[protein])
        dict3[protein] = abs(str3 - protein_dict[protein])

    # Выводим результат
    file1 = open('result.txt', 'w')
    file1.write('top 100 for sp|P69905.2|HBA_HUMAN\n')
    dict1_sorted = dict(sorted(dict1.items(), key=lambda item: item[1]))
    for i, x in enumerate(list(dict1_sorted)[0:100]):
        file1.write(f'{i+1}. {x} \n\t Delta: {dict1_sorted[x]}\n')

    file1.write('\n\ntop 100 for sp|P01308.1|INS_HUMAN\n')
    dict2_sorted = dict(sorted(dict2.items(), key=lambda item: item[1]))
    for i, x in enumerate(list(dict2_sorted)[0:100]):
        file1.write(f'{i+1}. {x} \n\t Delta: {dict2_sorted[x]}\n')

    file1.write('\n\ntop 100 for sp|P01275.3|GLUC_HUMAN\n')
    dict3_sorted = dict(sorted(dict3.items(), key=lambda item: item[1]))
    for i, x in enumerate(list(dict3_sorted)[0:100]):
        file1.write(f'{i+1}. {x} \n\t Delta: {dict3_sorted[x]}\n')

    print(f'algorithm took {(time.time() - seconds) / 60} minutes')
    file1.close()

if __name__ == '__main__':
    main()
