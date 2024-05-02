from django.db import models
from datetime import timedelta
from django.utils import timezone
import hashlib

# Create your models here.
#ユーザーモデル
class User(models.Model): 
    user_id = models.CharField(max_length=10, verbose_name="利用者ID",primary_key=True) 
    password = models.CharField(max_length=15, verbose_name="パスワード") 
    def __str__(self): 
        return self.user_id,self.password
    
#解答データモデル
class Answer_data(models.Model): 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 
    eng_word = models.CharField(max_length=30, verbose_name="英単語ワード") 
    def __str__(self): 
        return self.user_id,self.eng_word
    
#英単語リスト
class English_word(models.Model): 
    eng_word = models.CharField(max_length=30, verbose_name="英単語ワード",primary_key=True) 
    eng_word_mean = models.CharField(max_length=30, verbose_name="英単語の意味") 
    eng_part_of_speech = models.CharField(max_length=10,verbose_name="品詞")
    eng_level = models.CharField(max_length=2,verbose_name="英単語レベル")
    def __str__(self): 
        return self.eng_word,self.eng_word_mean,self.eng_part_of_speech,self.eng_level

#トークン有効期限
def in_30_days():
    return timezone.now() + timedelta(days=30)

#トークンモデル
class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    access_datetime = models.DateTimeField(default=in_30_days)
    def str(self):
        # メールアドレスとアクセス日時、トークンが見えるように設定
        dt = timezone.localtime(self.access_datetime).strftime("%Y/%m/%d %H:%M:%S")
        return self.user.user_id + '(' + dt + ') - ' + self.token
    @staticmethod
    def create(user: User):
        if AccessToken.objects.filter(user=user).exists():
            AccessToken.objects.get(user=user).delete()
        dt = timezone.now()
        str = user.user_id + user.password + dt.strftime('%Y%m%d%H%M%S%f')
        hash = hashlib.sha1(str.encode('utf-8')).hexdigest()
        token = AccessToken.objects.create(
            user=user,
            token=hash,
            access_datetime=dt)
        return token
    
#ミステーブル
class Miss(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,primary_key=True,verbose_name="試行ユーザー")
    num=  models.CharField(max_length=2,verbose_name="試行回数")
    def __str__(self): 
        return self.user.user_id,self.num
        
    

#アカウント停止テーブル
class Lock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,primary_key=True,verbose_name="停止ユーザー")
    def __str__(self): 
        return self.user.user_id
