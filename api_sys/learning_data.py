import collections
import random
from .models import *
from django.db.models.functions import Length

class Learning_data_list():
    def Calc_best_problem(p_list):
        word_list=[]
        for_list=list(p_list)
        #解答データに対応する英単語モデルリストを抽出
        for item in for_list:
            word_model=English_word.objects.get(eng_word=item["eng_word"])
            word_list.append(word_model)

        level_list=[]
        speech_list=[]
        length_list=[]
        #英単語リストのレベル,品詞,長さのリストを取得
        for item in word_list:
            level_list.append(item.eng_level)
            speech_list.append(item.eng_part_of_speech)
            length_list.append(len(item.eng_word))
        #最も間違えやすいレベルを抽出
        most_level=Learning_data_list.extract_most_item(level_list)
        #最も間違えやすい品詞を抽出
        most_speech=Learning_data_list.extract_most_item(speech_list)
        #最も間違えやすい長さのワードを抽出
        avg_length=Learning_data_list.calc_list_average(length_list)
        case=random.randint(0,3)

        #レベル
        if case==0:
            #該当するレベルのデータをすべて取得後ランダムで4つ取得する
            filtered_objects = English_word.objects.filter(eng_level=most_level)
            ret1=filtered_objects.order_by('?')[:4]
            if len(ret1)<4:
                obj=English_word.objects.all()
                inc1=obj.order_by('?')[:4]
                return inc1
            else:
                return ret1
        #品詞
        elif case==1:
            #該当する品詞のデータをすべて取得後ランダムで4つ取得する
            filtered_objects = English_word.objects.filter(eng_part_of_speech=most_speech)
            ret2=filtered_objects.order_by('?')[:4]
            if len(ret2)<4:
                obj=English_word.objects.all()
                inc2=obj.order_by('?')[:4]
                return inc2
            else:
                return ret2
        #長さ
        elif case==2:
            #該当する文字数のデータをすべて取得後ランダムで4つ取得する
            ret3 = English_word.objects.annotate(eng_word_length=Length("eng_word")).filter(eng_word_length=avg_length)
            if len(ret3)<4:
                obj=English_word.objects.all()
                inc3=obj.order_by('?')[:4]
                return inc3
            else:
                return ret3


    #リストの平均値を算出
    def calc_list_average(p_list):
        sum_num=0
        for item in p_list:
            sum_num+=item
        average=sum_num/len(p_list)
        return average
    
    #リストから最も多い要素を抽出する
    def extract_most_item(p_list):
        a=list(p_list)
        b=collections.Counter(a)
        c=b.most_common()
        return c[0][0]