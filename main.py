import recording
import voiro_auto
import translate
import config

#----------実行----------
phone_obj = recording.Microphone()
trans_obj = translate.TranslateNMT()
voiro_obj = voiro_auto.Voiro_Pywinauto()

while True:
    #英語を録音して、日本語にする
    raw_texts = phone_obj.record()
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
