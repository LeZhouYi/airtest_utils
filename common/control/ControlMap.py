from appium import webdriver
from common.run import RunEnv

class ControlType(object):
    CheckBox = 'check_box'
    TextOther = 'text_other'
    TextView = 'text_static'
    ImageView = 'imgage_view'
    ImagePanel = 'image_panel'
    Button = 'button'
    EditField = 'edit_field'
    EditText = 'edit_text'
    Content = 'content_desc'

mapping = {
    ControlType.CheckBox: ['android.widget.CheckBox','XCUIElementTypeSwitch'],
    ControlType.TextOther: ['android.view.View','XCUIElementTypeOther'],
    ControlType.TextView: ['android.view.View','XCUIElementTypeStaticText'],
    ControlType.ImageView: ['android.widget.ImageView','XCUIElementTypeButton'],
    ControlType.ImagePanel: ['android.widget.ImageView','XCUIElementTypeImage'],
    ControlType.Button: ['android.widget.Button','XCUIElementTypeButton'],
    ControlType.EditField: ['android.widget.EditText','XCUIElementTypeTextField'],
    ControlType.EditText: ['text','name'],
    ControlType.Content: ['content-desc','name']
}

def value(driver:webdriver,key:str)->str:
    '''获取控件关键字'''
    index = 0 if RunEnv.isAndroid(driver) else 1
    return mapping[key][index]