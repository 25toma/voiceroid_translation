# -*- coding: utf-8 -*-
import pywinauto
from abc import ABCMeta, abstractmethod

class VoiroAuto_Meta(metaclass=ABCMeta):
    @abstractmethod
    def talk(self, text):
        raise NotImplemented()

class Voiro_Pywinauto(VoiroAuto_Meta):
    def search_child_byclassname(self, class_name, uiaElementInfo, target_all = False):
        target = []
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():
            # ClassNameの一致確認
            if childElement.class_name == class_name:
                if target_all == False:
                    return childElement
                else:
                    target.append(childElement)
        if target_all == False:
            # 無かったらFalse
            return False
        else:
            return target


    def search_child_byname(self, name, uiaElementInfo):
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():
            # Nameの一致確認
            if childElement.name == name:
                return childElement
        # 無かったらFalse
        return False

    def talk(self, speakPhrase):
        # デスクトップのエレメント
        parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
        # voiceroidを捜索する
        voiceroid2 = self.search_child_byname("VOICEROID2",parentUIAElement)
        # *がついている場合
        if voiceroid2 == False:
            voiceroid2 = self.search_child_byname("VOICEROID2*",parentUIAElement)

        # テキスト要素のElementInfoを取得
        TextEditViewEle = self.search_child_byclassname("TextEditView",voiceroid2)
        textBoxEle      = self.search_child_byclassname("TextBox",TextEditViewEle)

        # コントロール取得
        textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(textBoxEle)

        # テキスト登録
        textBoxEditControl.set_edit_text(speakPhrase)


        # ボタン取得
        buttonsEle = self.search_child_byclassname("Button",TextEditViewEle,target_all = True)
        # 再生ボタンを探す
        playButtonEle = ""
        for buttonEle in buttonsEle:
            # テキストブロックを捜索
            textBlockEle = self.search_child_byclassname("TextBlock",buttonEle)
            if textBlockEle.name == "再生":
                playButtonEle = buttonEle
                break

        # ボタンコントロール取得
        playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(playButtonEle)

        # 再生ボタン押下
        playButtonControl.click()



    #----- In development functions ------------------
    def look_children(self, obj):
        for child in obj.children():
            print(child.class_name)
            #print(child.handle(),end=" ")
            #print(child.automation_id())


    def get_voiro2(self):
        # デスクトップのエレメント
        parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
        # voiceroidを捜索する
        voiceroid2 = self.search_child_byname("VOICEROID2",parentUIAElement)
        # *がついている場合
        if voiceroid2 == False:
            voiceroid2 = self.search_child_byname("VOICEROID2*",parentUIAElement)
        return voiceroid2

    def get_tuning_tab(self, tabName, voiro2=None):
        if voiro2==None:
            voiro2 = self.get_voiro2()
        tuning_tab = self.search_child_byclassname("TabControl", voiro2, target_all=True)[1]
        target = self.search_child_byname(tabName, tuning_tab)
        return target

if __name__=="__main__":
    pass
