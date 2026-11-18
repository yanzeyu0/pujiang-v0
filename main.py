# -*- coding: utf-8 -*-
"""
蒲江房产带看作战系统 - V0 原生渲染验证 APK
================================================
目的：只回答一个问题 —— Kivy 写的原生界面，能不能在
      鸿蒙 7「卓易通」Android 容器里正常渲染并交互。

本版本特性：
  - 不连任何服务器
  - 不发任何网络请求
  - 不含任何业务逻辑
  - 只用 Kivy 官方组件（不引第三方 UI 库，降低打包风险）

五个验证点：
  1. 中文是否正常显示（字体）
  2. 文本 / 按钮 / 输入框是否正常渲染（SDL2 文本层）
  3. 色块能否绘制（OpenGL ES 画布）
  4. 点击按钮有无反应（触摸事件）
  5. 横竖屏切换界面是否自适应
"""

import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.utils import platform
from kivy.graphics import Color, Rectangle

kivy.require('2.0.0')

# 注册中文字体为全局默认字体，解决 Kivy 默认字体不含中文导致乱码的问题。
# 字体文件 chinese_font.ttf 随 APK 一起打包（buildozer.spec 已含 ttf 扩展）。
_FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'chinese_font.ttf')
if os.path.exists(_FONT_PATH):
    LabelBase.register(name='Roboto', fn_regular=_FONT_PATH)
    LabelBase.register(name='RobotoItalic', fn_regular=_FONT_PATH)
    LabelBase.register(name='RobotoMedium', fn_regular=_FONT_PATH)
    LabelBase.register(name='RobotoMediumItalic', fn_regular=_FONT_PATH)
    LabelBase.register(name='RobotoBold', fn_regular=_FONT_PATH)
    LabelBase.register(name='RobotoBoldItalic', fn_regular=_FONT_PATH)
    LabelBase.register(name='DejaVuSans', fn_regular=_FONT_PATH)


class ColorBand(Widget):
    """用 Kivy canvas 画的色带，专门验证 OpenGL ES 画布是否工作。"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(52)
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.09, 0.30, 0.55, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.95, 0.62, 0.18, 1)
            Rectangle(pos=(self.x + dp(10), self.y + dp(10)),
                      size=(dp(72), max(1, self.height - dp(20))))
            Color(0.16, 0.62, 0.50, 1)
            Rectangle(pos=(self.x + dp(92), self.y + dp(10)),
                      size=(dp(72), max(1, self.height - dp(20))))


class V0Screen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(16),
                         spacing=dp(10), **kwargs)
        self.tap_count = 0
        self._build()

    def _build(self):
        self.add_widget(Label(
            text='[b]蒲江房产带看作战系统[/b]\nV0 原生渲染验证',
            markup=True, font_size='21sp', size_hint_y=None,
            height=dp(74), halign='center', valign='middle'))

        self.add_widget(ColorBand())

        info_text = (
            '平台: {}\n'
            '窗口: {} x {}\n'
            'Kivy: {}\n'
            '当前方向: {}'
        ).format(
            platform, int(Window.width), int(Window.height),
            kivy.__version__,
            '横屏' if Window.width > Window.height else '竖屏'
        )
        info = Label(text=info_text, font_size='14sp', halign='left',
                     valign='top', size_hint_y=None, height=dp(96))
        info.bind(width=lambda w, val: setattr(w, 'text_size', (val - dp(8), None)))
        self.add_widget(info)

        row = BoxLayout(orientation='horizontal', size_hint_y=None,
                        height=dp(48), spacing=dp(8))
        self.name_input = TextInput(text='蒲江测试', font_size='16sp',
                                    multiline=False)
        row.add_widget(self.name_input)
        btn = Button(text='点我验证', font_size='16sp')
        btn.bind(on_press=self.on_tap)
        row.add_widget(btn)
        self.add_widget(row)

        self.result = Label(text='状态: 等待点击', font_size='15sp',
                            size_hint_y=None, height=dp(42),
                            halign='center', valign='middle')
        self.add_widget(self.result)

        scroll = ScrollView(size_hint=(1, 1))
        notes = Label(
            text=(
                '验证清单（请逐项对照）\n'
                '1. 标题中文正常显示，没有方块/乱码 -> 字体层 OK\n'
                '2. 蓝/橙/绿三条色块显示 -> OpenGL 画布 OK\n'
                '3. 点"点我验证"，下面状态文字变化 -> 触摸事件 OK\n'
                '4. 点输入框能弹出键盘并改字 -> 输入层 OK\n'
                '5. 横过来竖过来布局不乱 -> 自适应 OK\n'
                '6. 连续开合 10 次不闪退 -> 稳定性 OK\n\n'
                '本包不联网、不留数据。测完卸载即可。'
            ),
            font_size='13sp', halign='left', valign='top',
            size_hint_y=None, height=dp(430), line_height=1.35)
        notes.bind(width=lambda w, val: setattr(w, 'text_size', (val - dp(6), None)))
        scroll.add_widget(notes)
        self.add_widget(scroll)

    def on_tap(self, instance):
        self.tap_count += 1
        self.result.text = '[{}] 触摸正常 / 第 {} 次 / 输入="{}"'.format(
            'OK' if self.tap_count else 'NO',
            self.tap_count, self.name_input.text)


class V0App(App):
    title = '蒲江房产 V0 渲染验证'

    def build(self):
        Window.softinput_mode = 'below_target'
        return V0Screen()


if __name__ == '__main__':
    V0App().run()
