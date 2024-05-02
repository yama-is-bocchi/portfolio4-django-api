from rest_framework import routers
from .views import *
from django.urls import path, include


urlpatterns = [
    path('eng_word/', GetRandomEnglish.as_view(), name='eng-word'), # 英単語取得
    path('add_answear/', AddAnswear.as_view(), name='add-answear'), # サインアップ
    path('add_user/', Add_user.as_view(), name='add-user'), # サインアップ
    path('login/', LoginView.as_view(), name='user-login'), # ログイン処理
    path('learn_eng/', LearnEnglishView.as_view(), name='learn-eng-word'), # 学習サービスワード取得
    path('checklogin/', CheckloginView.as_view(), name='check-user-login'), # パスワード確認
    path('checktoken/', ChecktokenView.as_view(), name='check-token-login'), # トークン確認
    path('get_user_data/', Admin_get_user_data.as_view(), name='user-list'), # 管理者画面ユーザーリスト取得
    path('update_user_pass/', Admin_update_user_pass.as_view(), name='update-user-pass'), # 管理者画面ユーザーパスワード変更
    path('delete_user/', Admin_delete_user.as_view(), name='delete-user'), # 管理者画面ユーザー削除
    path('get_word_data/', Admin_get_word_data.as_view(), name='word-list'), # 管理者画面ワードリスト取得
    path('update_word/', Admin_update_word.as_view(), name='update-word'), # 管理者画面ワード変更
    path('delete_word/', Admin_delete_word.as_view(), name='delete-word'), # 管理者画面ワード削除
    path('add_word/', Admin_add_word.as_view(), name='add-word'), # 管理者画面ワード追加
    path('get_answer_data/', Admin_get_answer_data.as_view(), name='answer-list'), # 管理者画面ユーザーリスト取得
    path('get_token_data/', Admin_get_token_data.as_view(), name='token-list'), # 管理者画面トークンリスト取得
    path('get_miss_data/', Admin_get_miss_data.as_view(), name='miss-list'), # 管理者画面トークンリスト取得
    path('get_lock_data/', Admin_get_lock_data.as_view(), name='lock-list'), # 管理者画面ロックリスト取得
    path('defuse_lock/', Admin_defuse_lock.as_view(), name='defuse-lock'), # 管理者画面ロック解除
]