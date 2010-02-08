#from constants import *
THEME_FILE = "default.edj"

import evas
import ecore
import ecore.evas
import ecore.x
import edje
import elementary

class Popup(elementary.InnerWindow):
    default_width = 500
    default_height = 500
    default_group = "amsn2/popup"

    def __init__(self, parent, width=None, height=None, group=None):
        elementary.InnerWindow.__init__(self, parent)

        self._parent = parent
        self.style_set("minimal") # size fallbacks to __layout's min/max

        self.__edje = edje.Edje(self.evas)
        self.__width = height or self.default_width
        self.__height = height or self.default_height
        _group = group or self.default_group
        self.__edje.file_set(THEME_FILE, _group)
        self.__edje.size_hint_min_set(self.__width, self.__height)
        self.__edje.size_hint_max_set(self.__width, self.__height)

        self.__action_btns = []
        self.__action_list = {}

        self.__edje.show()
        elementary.InnerWindow.content_set(self, self.__edje)

    def _title_text_set(self, value):
        if not value:
            self.__layout.part_text_set("title.text", "")
        else:
            self.__layout.part_text_set("title.text", value)

    title_text = property(fset=_title_text_set)

    def action_add(self, label, func_cb, data=None, icon=None):
        btn = elementary.Button(self._parent)
        btn.label_set(label)
        btn.callback_clicked_add(self.__action_btn_clicked)
        btn.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                 evas.EVAS_HINT_EXPAND)
        btn.size_hint_align_set(evas.EVAS_HINT_FILL,
                                evas.EVAS_HINT_FILL)
        btn.data["clicked"] = (func_cb, data)

        if icon:
            btn.icon_set(icon)
            icon.show()

        self.__actions_list[label] = btn

        btn.show()
        self.__edje.part_box_append("actions", btn)

    def content_set(self, content):
        content.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                     evas.EVAS_HINT_EXPAND)
        content.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.__layout.content_set("content", content)
        content.show()

    def open(self):
        self._parent.block(True)
        self.show()

    def close(self):
        self.hide()
        self._parent.block(False)
        self.delete()

