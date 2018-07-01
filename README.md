
## フォルダ構成

```sh
./python_template
├── app.py                  - Flaskによるサーバー起動
├── requirements.txt        - 依存関係モジュールの定義
├── modules                 - pythonファイル
│   ├── domain              - 業務ロジック
│   ├── models              - DB関係
│   ├── tests               - テスト用ファイル
│   └── utils               - ユーティリティファイル
├── static                  - css,jsなどの静的ファイル
│   ├── assets              - 画像ファイルなど
│   ├── css                 - CSSファイル
│   └── js                  - JSファイル
└── templetes               - htmlファイル

```

## リファレンス

[Flask1](https://www.yoheim.net/blog.php?q=20160505)

[Flask2](http://python.zombie-hunting-club.com/entry/2017/11/03/223503)

[FlaskをVSCodeでデバッグできるようにする](https://ohke.hateblo.jp/entry/2017/09/01/230000)
→FlaskはAnacondaからインストールする必要がある。pipでインストールすると「ImportError: No module named flask」が表示される

[O/R Mapper - SQLAlchemy1](https://qiita.com/zakuro9715/items/7e393ef1c80da8811027)


[O/R Mapper - SQLAlchemy2](http://st-hakky.hatenablog.com/entry/2017/08/13/130202)
→ちょくちょく記載ミスがある点に注意

[Materialized CSS - Google](https://materializecss.com/)

[PythonをAzureWebServiceにデプロイする](https://docs.microsoft.com/ja-jp/azure/app-service/app-service-web-get-started-python)
