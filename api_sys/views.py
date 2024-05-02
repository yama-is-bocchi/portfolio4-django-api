from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
import json
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from .form import * 
from django.shortcuts import *
from .learning_data import *



#管理者か確認するメソッド
def Check_admin(p_token):
    actoken = AccessToken.objects.get(token=p_token)
    if actoken.user.user_id=="admin":
        return True
    else:
        return False
    
#発行されているトークンとJSONの利用者IDが一致するか確認
def Check_token(p_user_id,p_token):
    actoken=AccessToken.objects.get(token=p_token)
    if actoken.user.user_id==p_user_id:
        return True
    return False

#管理者画面ロックリスト取得
class Admin_defuse_lock(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            temp_user=User.objects.get(user_id=datas["user_id"])
            lock = Lock.objects.get(user=temp_user)
            lock.delete()
            miss=Miss.objects.get(user=temp_user)
            miss.num="0"
            miss.save()
            return Response(status=HTTP_200_OK)



#管理者画面ロックリスト取得
class Admin_get_lock_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            lock_list = Lock.objects.all()
            serializer = LockSerializer(lock_list, many=True)
            return Response(serializer.data)



#管理者画面ミスリスト取得
class Admin_get_miss_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            miss_list = Miss.objects.all()
            serializer = MissSerializer(miss_list, many=True)
            return Response(serializer.data)



#管理者画面トークンリスト取得
class Admin_get_token_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            token_list = AccessToken.objects.all()
            serializer = TokenSerializer(token_list, many=True)
            return Response(serializer.data)


#管理者画面アンサーリスト取得
class Admin_get_answer_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            user_list = Answer_data.objects.all()
            serializer = AnswearSerializer(user_list, many=True)
            return Response(serializer.data)


#ランダム英単語取得
class GetRandomEnglish(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        if Check_token(datas["user_id"],datas["token"])==True:
            #トークンが正しい
           temp = English_word.objects.all()
           queryset=temp.order_by('?')[:4]
           if len(queryset)>=4:
                serializer = english_wordSerializer(queryset, many=True)
                return Response(data=serializer.data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

#不正解リスト
class AddAnswear(GenericAPIView):
    #トークンチェック
    def post(self, request):
        datas = json.loads(request.body)
        if Check_token(datas["user_id"],datas["token"])==True:
            #トークンが正しい
            temp_user=User.objects.get(user_id=datas["user_id"])
            new_data=Answer_data(user_id=temp_user,eng_word=datas["eng_word"])
            new_data.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

#後で
#管理者画面ユーザー登録  
class Admin_add_word(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            #管理者である
            temp_word = English_word(eng_word=datas["eng_word"],eng_word_mean=datas["eng_word_mean"],
                                     eng_part_of_speech=datas["eng_part_of_speech"],eng_level=datas["eng_level"])
            temp_word.save()
            return Response(status=HTTP_200_OK)


#学習型サービス
class LearnEnglishView(GenericAPIView):
    def post(self,request):
        datas = json.loads(request.body)
        
        #トークンチェック
        if Check_token(datas["user_id"],datas["token"])==True:
            queryset = Answer_data.objects.filter(user_id=datas["user_id"])
            if len(queryset)>0:
                serializer_list = AnswearSerializer(queryset,many=True)
                level=Learning_data_list.Calc_best_problem(serializer_list.data)
                serializer = english_wordSerializer(level, many=True)
                if level is None:
                    temp = English_word.objects.all()
                    set=temp.order_by('?')[:4]
                    serialized = english_wordSerializer(set, many=True)
                    return Response(data=serialized.data)
                else:
                    return Response(data=serializer.data)
            else:
                temp = English_word.objects.all()
                set=temp.order_by('?')[:4]
                serialized = english_wordSerializer(set, many=True)
                return Response(data=serialized.data)
        else:
            return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)

#管理者画面ユーザー削除      
class Add_user(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        temp_user=User.objects.filter(user_id=datas["user_id"])
        if(len(temp_user)==0):
            new_user=User(user_id=datas["user_id"],password=datas["password"])
            new_user.save()
            #ミステーブルに作成
            new_miss=Miss(user=new_user,num="0")
            new_miss.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

#ユーザーリスト
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('password',)

#トークンリスト
class TokenViewSet(viewsets.ModelViewSet):
    queryset = AccessToken.objects.all()
    serializer_class = TokenSerializer
    filter_fields = ('',)



#ログイン対象のユーザーを捜す
class CheckloginView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        #ロックリストに追加されていないか確認
        datas = json.loads(request.body)
        temp_user=User.objects.get(user_id=datas["user_id"])
        temp_lock=Lock.objects.filter(user=temp_user)
        if len(temp_lock)!=0:
            #ロックリストにある
            return Response( {'error': 1}, status=HTTP_403_FORBIDDEN)
        
        if temp_user.user_id==datas["user_id"] and temp_user.password==datas["password"]:
            #異常なし&ミステーブル_NUMを初期化する
            init_miss=Miss(user=temp_user,num="0")
            init_miss.save()
            return Response({'error': 0})
        else:
            #ミステーブルに追加&確認して5回以上ならロックする
            if temp_user is None:
                #利用者IDが存在しない
                return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)
            else:
                #利用者IDが存在する
                if temp_user.user_id=="admin":
                    return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)
                miss_tbl=Miss.objects.get(user=temp_user)
                sum_num=int(miss_tbl.num)+1
                if sum_num>5:
                    #ロックリストに追加
                    new_lock=Lock(user=temp_user)
                    new_lock.save()
                    return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)
                else:
                    new_miss=Miss(user=temp_user,num=str(sum_num))
                    new_miss.save()
                    return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)

#トークンを発行
class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(user_id=serializer.validated_data["user_id"])
            token = AccessToken.create(user)
            return Response({'token':token.token})
        else:
            return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)


#トークンを確認and発行されているユーザーIDを返す
class ChecktokenView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = Token_check_Serializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=AccessToken.objects.get(token=serializer.validated_data["token"])
            return Response({'user_id': user.user_id})
        else:
            return Response( {'error': 1}, status=HTTP_400_BAD_REQUEST)


#管理者画面ユーザーリスト取得
class Admin_get_user_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            user_list = User.objects.all()
            serializer = UserSerializer(user_list, many=True)
            return Response(serializer.data)

#管理者画面ユーザーパスワード変更
class Admin_update_user_pass(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            #管理者である
            user=User.objects.get(user_id=datas["user_id"])
            user.password=datas["password"]
            user.save()
            return Response(status=HTTP_200_OK)

#管理者画面ユーザー削除      
class Admin_delete_user(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            #管理者である
            obj = get_object_or_404(User, user_id=datas["user_id"])
            obj.delete() 
            return Response(status=HTTP_200_OK)
        
    
#管理者画面ワードリスト取得
class Admin_get_word_data(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            word_list = English_word.objects.all()
            serializer = english_wordSerializer(word_list, many=True)
            return Response(serializer.data)
        
    #管理者画面ユーザーパスワード変更
class Admin_update_word(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            #管理者である
            word=English_word.objects.get(eng_word=datas["eng_word"])
            word.eng_word_mean=datas["eng_word_mean"]
            word.eng_part_of_speech=datas["eng_part_of_speech"]
            word.eng_level=datas["eng_level"]
            word.save()
            return Response(status=HTTP_200_OK)
        

#管理者画面ユーザー削除      
class Admin_delete_word(GenericAPIView):
    def post(self, request):
        datas = json.loads(request.body)
        #管理者か確認する
        if Check_admin(datas["token"])==False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            #管理者である
            obj = get_object_or_404(English_word, eng_word=datas["eng_word"])
            obj.delete() 
            return Response(status=HTTP_200_OK)

