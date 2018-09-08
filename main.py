import recording
import voiro_auto
import translate
import config

#----------実行----------
trans_obj = translate.TranslateNormal()
voiro_obj = voiro_auto.Voiro_Pywinauto()

while True:
    #英語を録音して、日本語にする
    raw_texts = recording.record()
    if raw_texts is None:
        continue
    trans_texts = trans_obj.trans(raw_texts)
    trans_texts = "\r\n".join(trans_texts)
    
    #ボイロの子に喋ってもらう
    voiro_obj.talk(trans_texts)
    
    #デバッグ出力
    if config.TEXT_CHECK:
        print(raw_texts)
        print(trans_texts)
