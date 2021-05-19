# 開発環境 構築手順
```
docker-compose up -d
docker-compose exec web bash
python manage.py runserver 0.0.0.0:8000
```

http://localhost:8000にアクセスする。

# シークレットファイルの準備
settingsフォルダと同階層にsecretsフォルダを作成しその中にsecrets.yamlを作成する
```
├─secrets
│　└─secrets.yaml
├─settings
│  └─__pycache__
```

secrets.yamlの中身は以下の通りにする
```
# PAY.JP
PAYJP_SECRET_KEY: 'シークレットキー'
PAYJP_PUBLIC_KEY: 'パブリックキー'

# reCAPTCHA
RECAPTCHA_SITE_KEY: 'サイトキー'
RECAPTCHA_SECRET_KEY: 'シークレットキー'

# メール(GMAIL)
EMAIL_HOST_USER: 'メールアドレス'
EMAIL_HOST_PASSWORD: 'アプリパスワード'
```
