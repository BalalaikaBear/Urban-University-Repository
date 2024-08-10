class WordsFinder:
    def __init__(self, *args):
        self.file_names = args

    def get_all_words(self):
        all_words = {}
        for file_name in self.file_names:
            try:
                with open(file_name, encoding="utf-8") as file:
                    words_in_file = self.del_punctuation(file.read().lower().split())  # создание списка со всеми словами
                all_words[file_name] = words_in_file
            except FileNotFoundError:  # не учитывать отсутствующий файл
                pass
        return all_words

    def del_punctuation(self, words):
        """
        Убирает знаки пунктуации в конце слова
        """
        for i, word in enumerate(words):
            if word == "-":  # отдельное тире учитывается как отдельное слово
                continue
            if word[-1] in ",.=!?;:-_'":
                words[i] = word[:-1]
        return words

    def find(self, word):
        """
        Поиск первого встречаемого слова в файлах
        """
        word = word.lower()
        output = {}
        for file_name, words_in_file in (self.get_all_words().items()):  # просмотр файлов
            output[file_name] = 0
            for i, word_in_file in enumerate(words_in_file):  # разбиение на отдельные слова в файле
                if word == word_in_file:
                    output[file_name] = i + 1
                    break
        return output

    def count(self, word):
        """
        Количество встречаемых слов в файлах
        """
        word = word.lower()
        output = {}
        for file_name, words_in_file in (self.get_all_words().items()):  # просмотр файлов
            count = 0
            for word_in_file in words_in_file:  # разбиение на отдельные слова в файле
                if word == word_in_file:
                    count += 1
            output[file_name] = count
        return output


finder2 = WordsFinder("module_7_3_file1.txt", "module_7_3_file2.txt")
print(finder2.get_all_words())
print(finder2.find("text"))
print(finder2.count("Text"))
