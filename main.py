import recording
import voiro_auto
import translate
import config

#----------実行----------
transObj = translate.TranslateNormal()

while True:
    #英語を録音して、日本語にする
    raw_texts = recording.record()
    if raw_texts is None:
        continue
    trans_texts = transObj.trans(raw_texts)
    trans_texts = "\r\n".join(trans_texts)
    
    #ボイロの子に喋ってもらう
    voiro_auto.talkVOICEROID2(trans_texts)
    
    #デバッグ出力
    if config.TEXT_CHECK:
        print(raw_texts)
        print(trans_texts)
