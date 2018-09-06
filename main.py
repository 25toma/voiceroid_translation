import recording
import voiro_auto
import translate

TEXT_CHECK = True #翻訳前後の内容をテキスト形式で表示する
transObj = translate.TranslateNormal()

while True:
    #英語を録音して、日本語にする
    speaksEN = recording.record()
    if speaksEN is None:
        continue
    speaksJP = transObj.trans(speaksEN)
    speaksJP = "\r\n".join(speaksJP)
    
    #ボイロの子に喋ってもらう
    voiro_auto.talkVOICEROID2(speaksJP)
    
    #デバッグ出力
    if TEXT_CHECK:
        print(speaksEN)
        print(speaksJP)
