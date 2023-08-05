import setuptools

setuptools.setup(
    name="pytive",
    version="0.0.1",
    author="koaf",
    author_email="koafff@aol.com",
    description="Mirrativ PythonApi",
    long_description="このプロジェクトはRabies様のフォークでございます。気が向いた時に更新をします。\n 現在使える機能\n配信情報の取得\nコメント読み込み/送信\nフォロー/フォロー解除\n配信リクエスト",
    long_description_content_type="text/markdown",
    url="https://github.com/koaf/pytive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)