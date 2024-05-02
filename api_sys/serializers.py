from rest_framework import serializers
from .models import *
from django.utils import timezone
from datetime import timedelta

#通常英単語
class english_wordSerializer(serializers.ModelSerializer):
   class Meta:
       model = English_word
       fields = ('eng_word', 'eng_word_mean', 'eng_part_of_speech','eng_level')

#ユーザーリスト
class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('user_id', 'password')

#トークンリスト
class TokenSerializer(serializers.ModelSerializer):
   class Meta:
       model = AccessToken
       fields = ('user_id', 'token','access_datetime')

#不正解データシリアライザ
class AnswearSerializer(serializers.ModelSerializer):
   class Meta:
       model = Answer_data
       fields = ('user_id', 'eng_word')

#トークンシリアライザ
class Token_check_Serializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, style={'input_type': 'token'})
    def validate(self, data):
        token = data.get('token')
        tokenlist = AccessToken.objects.get(token=token)
        dt = timezone.now()
        if dt.date()== tokenlist.access_datetime.date() and token ==tokenlist.token:#IDが一致かつトークンハッシュ値が一致かつ日付が今日のトークンを抽出
            return data
        raise serializers.ValidationError('fail')

#ログインシリアライザ
class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=10, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')
        userid = User.objects.get(user_id=user_id)
        if user_id == userid.user_id:
            if password ==userid.password:
                return data
            else:
                raise serializers.ValidationError('ログイン失敗')
            
#ミスリスト
class MissSerializer(serializers.ModelSerializer):
   class Meta:
       model = Miss
       fields = ('user_id', 'num')

#ロックリスト
class LockSerializer(serializers.ModelSerializer):
   class Meta:
       model = Lock
       fields = '__all__'