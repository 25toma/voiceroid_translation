import recording
import voiro_auto
import translate
import config

#----------実行----------
transObj = translate.TranslateNormal()

while True:
    #英語を録音して、日本語にする
    raw_text = recording.record()
    if raw_text is None:
        continue
    trans_text = transObj.trans(raw_text)
    trans_text = "\r\n".join(trans_text)
    
    #ボイロの子に喋ってもらう
    voiro_auto.talkVOICEROID2(trans_text)
    
    #デバッグ出力
    if config.TEXT_CHECK:
        print(raw_text)
        print(trans_text)
