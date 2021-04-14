import re, random


class SimilarWordReplace(object):
    def __init__(self,vocab_file):
        total_words = open(vocab_file, encoding='utf-8').read().splitlines()
        self.max_len, self.words_dict = self.handle_word_dict(total_words)

    def handle_word_dict(self, words_list: list) -> object:
        """
        读取txt文件，拿到替换此表，加工
        :rtype: list
        :return:
        """
        max_len = 0
        words_dict = {}
        special_word = []

        for i in words_list:
            # 判断此行是不是空行
            i = i.strip()
            if i:
                # 去除多余的空格
                i = re.sub('\t+', ' ', i)
                i = re.sub(" +", " ", i)
                i_list = i.split(" ")
                if len(i_list) > 1:

                    left_word = i_list[0]
                    right_word = " ".join(i_list[1:])

                    # 如果左词不在词表中，就新增key
                    if left_word not in words_dict:
                        words_dict[left_word] = [right_word]

                        # 更新最长替换词长度
                        max_len = len(left_word) if len(left_word) > max_len else max_len
                    else:
                        if right_word not in words_dict[left_word]:
                            words_dict[left_word] = words_dict[left_word] + [right_word]

                    # 找到特殊的替换词，字符首尾是英文或者数字的词
                    # if re.findall(u'[0-9a-zA-Z]+', left_word[0] + left_word[-1]):
                    #     special_word.append(left_word)

        return max_len, words_dict

    def cut(self, text):
        piece = ""
        result = []
        index = len(text)
        while index > 0:
            for size in range(index - self.max_len, index, ):
                piece = text[size:index]
                if piece in self.words_dict:
                    index = size + 1
                    break
            index = index - 1
            result.append(piece)
        result.reverse()
        return result

    def search_replace_word(self, text: str) -> tuple:
        """
        执行替换
        :param text:
        :return:
        """
        text = text + " " * self.max_len
        cut_list = self.cut(text)

        new_list = []
        sub_index = []

        # 先按照词表中的词分割
        for i in range(len(cut_list)):
            word = cut_list[i]
            # 词在词表中，且不在特殊词中，就替换
            if word in self.words_dict:
                # 拿到替换词的位置
                sub_index.append(i)

                # 词表查找替换词
                new_word = self.words_dict[word]

                # 如果替换的词只有一个那就直接替换
                if len(new_word) == 1:
                    new_list.append(new_word[0])
                # 如果有多个就随机的选一个
                else:
                    index = random.randint(0, len(new_word) - 1)
                    new_list.append(new_word[index])
            # 不在词表中就不替换
            else:
                new_list.append(word)
        return cut_list, new_list, sub_index

    def remove_repetition(self, new_list: list, new_index: list) -> list:
        """
        去除替换词两边重复的内容
        :param new_list:
        :param new_index:
        :return:
        """
        # 在替换词的位置，先向后看
        for i in new_index:
            # 拿到替换词
            word = new_list[i]
            # 替换词的长度
            word_len = len(word)
            # 从最长到1，逐渐拿替换词的右边字符和后面的对比
            for j in range(word_len, 0, -1):
                # 替换词右边的字符
                left_char = word[(word_len - j):]

                # 拿到替换词截取长度个数的后面字符拼接
                after_char = "".join(new_list[i + 1:i + 1 + j])

                # 选取后面跟左边相等个数的字符
                if left_char == after_char[:j]:
                    # 去重完字符的个数
                    after_len = 0
                    # 需要去重的字符位置
                    for k in range(i + 1, i + 1 + j):
                        # 加上本位置字符的长度
                        after_len = after_len + len(new_list[k])
                        # 如果长度还没到要去重的长度，就把这个位置变为空，然后接着去重
                        if after_len < j:
                            new_list[k] = ""
                        # 如果正好等于去重长度，就变为空，然后停止往下循环
                        elif after_len == j:
                            new_list[k] = ""
                            break
                        # 如果加上本位置字符后，大于长度，就说明，这个位置的字符不需要完全去重
                        elif after_len > j:
                            new_list[k] = new_list[k][:j - after_len]
                            break

        # 在替换词的位置，向前看
        for i in new_index:
            # 如果替换词不是第一个位置
            if i >= 1:
                # 拿到替换词
                word = new_list[i]
                # 替换词的长度
                word_len = len(word)
                # 选取替换词的局部
                for j in range(word_len, 0, -1):
                    # 替换词左边的字符
                    left_char = word[:j]
                    # 如果没有超出最前面
                    if i - j >= 0:
                        # 拿到替换词截取长度个数的后面字符拼接
                        befor_char = "".join(new_list[i - j: i])

                        # 选取前面跟替换词左边相等个数的字符
                        # 如果相等，就替换
                        if left_char == befor_char[-j:]:
                            # 去重完字符的个数
                            before_len = 0
                            # 需要去重的字符位置
                            for k in range(i - 1, i - 1 - j, -1):
                                # 加上本位置字符的长度
                                before_len = before_len + len(new_list[k])
                                # 如果长度还没到要去重的长度，就把这个位置变为空，然后接着去重
                                if before_len < j:
                                    new_list[k] = ""
                                # 如果正好等于去重长度，就变为空，然后停止往下循环
                                elif before_len == j:
                                    new_list[k] = ""
                                    break
                                # 如果加上本位置字符后，大于长度，就说明，这个位置的字符不需要完全去重
                                elif before_len > j:
                                    new_list[k] = new_list[k][:before_len - j]
                                    break

        return new_list

    def handle_replace_word(self, cut_list: list, new_list: list, sub_index: list) -> str:
        """
        两个任务：
        1.替换前：首尾是英文或者数字的替换词，且隔壁词也是相同的词性，就不替换。比如，1077中的077就不替换
        2.替换后，首尾是英文或者数字的替换词，且隔壁词也是相同的词性，就在替换词后面加个空格。
        如果是就增加一个空格
        :param cut_list:未替换的分词列表
        :param new_list:替换后的分词列表
        :param sub_index:替换词的位置
        :return:
        """
        new_index = []
        # 任务一：先看替换前是否值得替换
        for i in sub_index:

            # 当替换词位置在第一个的时候，只能检查尾字符
            if i == 0:
                # 如果待替换词的尾字符和下一个词的首字符都是数字，则不替换
                if re.findall(u'[0-9]', cut_list[i][-1]) and re.findall(u'[0-9]', cut_list[i + 1][0]):
                    new_list[i] = cut_list[i]

                # 如果待替换词的尾字符和下一个词的首字符都是英文，则不替换
                elif re.findall(u'[a-zA-Z]', cut_list[i][-1]) and re.findall(u'[a-zA-Z]', cut_list[i + 1][0]):
                    new_list[i] = cut_list[i]
                else:
                    new_index.append(i)

            # 当位置在末尾的时候，只能检查首字符
            elif i == len(cut_list) - 1:
                # 如果待替换词的首字符和上一个词的尾字符都是数字，则不替换
                if re.findall(u'[0-9]', cut_list[i][0]) and re.findall(u'[0-9]', cut_list[i - 1][-1]):
                    new_list[i] = cut_list[i]

                # 如果待替换词的首字符和上一个词的尾字符都是英文，则不替换
                elif re.findall(u'[a-zA-Z]', cut_list[i][0]) and re.findall(u'[a-zA-Z]', cut_list[i - 1][-1]):
                    new_list[i] = cut_list[i]
                else:
                    new_index.append(i)

            # 位置在中间的时候，两边都可以检查
            else:
                # 可以检查首尾字符

                # 如果待替换词的尾字符和下一个词的首字符都是数字，则不替换
                if re.findall(u'[0-9]', cut_list[i][-1]) and re.findall(u'[0-9]', cut_list[i + 1][0]):
                    new_list[i] = cut_list[i]

                # 如果待替换词的尾字符和下一个词的首字符都是英文，则不替换
                elif re.findall(u'[a-zA-Z]', cut_list[i][-1]) and re.findall(u'[a-zA-Z]', cut_list[i + 1][0]):
                    new_list[i] = cut_list[i]

                # 如果待替换词的首字符和上一个词的尾字符都是数字，则不替换
                elif re.findall(u'[0-9]', cut_list[i][0]) and re.findall(u'[0-9]', cut_list[i - 1][-1]):
                    new_list[i] = cut_list[i]

                # 如果待替换词的首字符和上一个词的尾字符都是英文，则不替换
                elif re.findall(u'[a-zA-Z]', cut_list[i][0]) and re.findall(u'[a-zA-Z]', cut_list[i - 1][-1]):
                    new_list[i] = cut_list[i]

                # 如果AABB的中间AB是替换词，则不替换
                elif cut_list[i - 1][-1] == cut_list[i][0] and cut_list[i + 1][0] == cut_list[i][-1]:
                    new_list[i] = cut_list[i]

                else:
                    new_index.append(i)

        # 任务二：再处理替换后的影响
        for i in new_index:
            # 拿到当前词
            now_word = new_list[i]

            # 如果当前词是第一个词，就只看后面的词
            if i == 0:
                # 拿到下一个词的首字符
                next_word = new_list[i + 1]

                # 如果替换词的末尾和下一个词都是数字或者英文，那就给前当前替换词后面加个空格
                if re.findall(u'[0-9a-zA-Z]+', now_word[-1]) and re.findall(u'[0-9a-zA-Z]+', next_word[0]):
                    new_list[i] = new_list[i] + " "

            # 如果当前词是最后一个词，就只看前面一个词
            elif i == len(new_list) - 1:
                # 拿到上一个词
                before_word = new_list[i - 1]

                # 如果替换词的末尾和上一个词都是数字或者英文，那就给前当前替换词前面加个空格
                if re.findall(u'[0-9a-zA-Z]+', now_word[0]) and re.findall(u'[0-9a-zA-Z]+', before_word[-1]):
                    new_list[i] = " " + new_list[i]

            # 如果当前词不是首尾，那就前后词都看
            else:
                # 拿到下一个词的首字符
                next_word = new_list[i + 1]

                # 如果替换词的末尾和下一个词都是数字或者英文，那就给前当前替换词后面加个空格
                if re.findall(u'[0-9a-zA-Z]+', now_word[-1]) and re.findall(u'[0-9a-zA-Z]+', next_word[0]):
                    new_list[i] = new_list[i] + " "

                # 拿到上一个词
                before_word = new_list[i - 1]

                # 如果替换词的末尾和上一个词都是数字或者英文，那就给前当前替换词前面加个空格
                if re.findall(u'[0-9a-zA-Z]+', now_word[0]) and re.findall(u'[0-9a-zA-Z]+', before_word[-1]):
                    new_list[i] = " " + new_list[i]

                    # 去除替换词周围相同的字符
        new_list = self.remove_repetition(new_list, new_index)

        return "".join(new_list).strip()

    def handle_text(self, text: str):
        """
        预处理人名，去除文本中全称名字的前部分
        :param text:
        :return:
        """
        text = re.sub(r"(?<=[^\x00-\xff])-(?=[^\x00-\xff])|·", "", text)
        # for i in full_name:
        #     if "-" in i:
        #         name_two = re.split('-', i)
        #         point_name = re.sub('-', '·', i)
        #         rule = "%s|%s" % (i, point_name)
        #         text = re.sub(rule, name_two[-1], text)
        return text

    def run(self, text) -> str:
        """
        核心处理模块
        :param text:
        :return:
        """

        text = self.handle_text(text)
        cut_list, new_list, sub_index = self.search_replace_word(text)
        # print(cut_list)
        # print(new_list)
        result = self.handle_replace_word(cut_list, new_list, sub_index)
        # 替换后再改写数值型
        return result


if __name__ == '__main__':
    vocab = "similar_words.txt"
    f = SimilarWordReplace(vocab)

    text = "我的作业比他的多"
    rep = f.run(text)
    print(rep)


