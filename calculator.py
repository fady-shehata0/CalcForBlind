#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced Calculator for Blind Users
A bilingual calculator with NVDA screen reader support
Author: Fady Shehata
Version: 1.0.0
"""

import wx
import json
import os
from pathlib import Path
import math
from enum import Enum


class Theme(Enum):
    """Available themes for the calculator"""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"


class CalculatorSettings:
    """Manages calculator settings and persistence"""
    
    SETTINGS_FILE = "calculator_settings.json"
    DEFAULT_SETTINGS = {
        "language": "en",
        "theme": "light",
        "font_size": 12,
        "decimal_places": 10,
        "history_enabled": True,
        "sound_enabled": False
    }
    
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or return defaults"""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()


class Calculator:
    """Core calculator logic"""
    
    def __init__(self):
        self.reset()
        self.history = []
    
    def reset(self):
        """Reset calculator state"""
        self.display = "0"
        self.operator = None
        self.operand1 = None
        self.operand2 = None
        self.new_input = True
    
    def append_digit(self, digit):
        """Append a digit to display"""
        if self.new_input:
            self.display = str(digit)
            self.new_input = False
        else:
            if self.display == "0" and digit != ".":
                self.display = str(digit)
            elif digit == "." and "." not in self.display:
                self.display += str(digit)
            elif digit != ".":
                self.display += str(digit)
        return self.display
    
    def set_operator(self, op):
        """Set the operation to perform"""
        try:
            if self.operand1 is None:
                self.operand1 = float(self.display)
            else:
                self.calculate()
                self.operand1 = float(self.display)
            
            self.operator = op
            self.new_input = True
            return self.display
        except ValueError:
            return "Error"
    
    def calculate(self):
        """Perform the calculation"""
        if self.operator is None or self.operand1 is None:
            return self.display
        
        try:
            self.operand2 = float(self.display)
            result = self._perform_operation(
                self.operand1, 
                self.operator, 
                self.operand2
            )
            
            # Add to history
            calculation = f"{self.operand1} {self.operator} {self.operand2} = {result}"
            self.history.append(calculation)
            
            self.display = str(result)
            self.operator = None
            self.operand1 = None
            self.operand2 = None
            self.new_input = True
            
            return self.display
        except (ValueError, ZeroDivisionError) as e:
            return "Error"
    
    def _perform_operation(self, op1, operator, op2):
        """Perform basic arithmetic operations"""
        if operator == "+":
            return op1 + op2
        elif operator == "-":
            return op1 - op2
        elif operator == "×":
            return op1 * op2
        elif operator == "÷":
            if op2 == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return op1 / op2
        elif operator == "%":
            return op1 % op2
        elif operator == "^":
            return op1 ** op2
        else:
            return op1
    
    def square(self):
        """Calculate square of current number"""
        try:
            result = float(self.display) ** 2
            self.display = str(result)
            self.new_input = True
            return self.display
        except ValueError:
            return "Error"
    
    def sqrt(self):
        """Calculate square root"""
        try:
            num = float(self.display)
            if num < 0:
                return "Error"
            result = math.sqrt(num)
            self.display = str(result)
            self.new_input = True
            return self.display
        except ValueError:
            return "Error"
    
    def toggle_sign(self):
        """Toggle positive/negative sign"""
        try:
            result = -float(self.display)
            self.display = str(result)
            return self.display
        except ValueError:
            return "Error"
    
    def reciprocal(self):
        """Calculate reciprocal (1/x)"""
        try:
            num = float(self.display)
            if num == 0:
                return "Error"
            result = 1 / num
            self.display = str(result)
            self.new_input = True
            return self.display
        except ValueError:
            return "Error"
    
    def clear_display(self):
        """Clear display"""
        self.display = "0"
        self.new_input = True
        return self.display
    
    def backspace(self):
        """Remove last digit"""
        if len(self.display) > 1:
            self.display = self.display[:-1]
        else:
            self.display = "0"
        return self.display
    
    def get_history(self):
        """Get calculation history"""
        return self.history.copy()


class CalculatorFrame(wx.Frame):
    """Main calculator window"""
    
    TRANSLATIONS = {
        "en": {
            "title": "Advanced Calculator",
            "menu_file": "&File",
            "menu_exit": "E&xit",
            "menu_view": "&View",
            "menu_theme": "&Theme",
            "menu_light": "&Light",
            "menu_dark": "&Dark",
            "menu_high_contrast": "&High Contrast",
            "menu_language": "&Language",
            "menu_english": "&English",
            "menu_arabic": "&Arabic",
            "menu_help": "&Help",
            "menu_about": "&About",
            "menu_history": "&History",
            "clear_history": "Clear History",
            "close": "Close",
        },
        "ar": {
            "title": "آلة حاسبة متقدمة",
            "menu_file": "&ملف",
            "menu_exit": "&خروج",
            "menu_view": "&عرض",
            "menu_theme": "&المظهر",
            "menu_light": "فا&تح",
            "menu_dark": "&غامق",
            "menu_high_contrast": "&تباين عالي",
            "menu_language": "&اللغة",
            "menu_english": "&الإنجليزية",
            "menu_arabic": "&العربية",
            "menu_help": "&مساعدة",
            "menu_about": "&عن البرنامج",
            "menu_history": "&السجل",
            "clear_history": "مسح السجل",
            "close": "إغلاق",
        }
    }
    
    THEMES = {
        "light": {
            "bg": wx.Colour(255, 255, 255),
            "fg": wx.Colour(0, 0, 0),
            "btn_bg": wx.Colour(230, 230, 230),
            "btn_fg": wx.Colour(0, 0, 0),
            "display_bg": wx.Colour(240, 240, 240),
            "display_fg": wx.Colour(0, 0, 0),
        },
        "dark": {
            "bg": wx.Colour(30, 30, 30),
            "fg": wx.Colour(255, 255, 255),
            "btn_bg": wx.Colour(50, 50, 50),
            "btn_fg": wx.Colour(255, 255, 255),
            "display_bg": wx.Colour(20, 20, 20),
            "display_fg": wx.Colour(0, 255, 0),
        },
        "high_contrast": {
            "bg": wx.Colour(0, 0, 0),
            "fg": wx.Colour(255, 255, 0),
            "btn_bg": wx.Colour(255, 255, 0),
            "btn_fg": wx.Colour(0, 0, 0),
            "display_bg": wx.Colour(0, 0, 0),
            "display_fg": wx.Colour(255, 255, 0),
        }
    }
    
    def __init__(self):
        wx.Frame.__init__(self, None, title="Advanced Calculator", size=(400, 600))
        
        self.settings = CalculatorSettings()
        self.calculator = Calculator()
        self.history_frame = None
        
        # Setup UI
        self.SetBackgroundColour(self.THEMES["light"]["bg"])
        self.init_ui()
        self.apply_theme(self.settings.get("theme", "light"))
        self.apply_language(self.settings.get("language", "en"))
        
        # Bind close event
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Center window on screen
        self.Centre()
        
        # Accessibility
        self.SetAccessible(wx.Accessible(self))
    
    def init_ui(self):
        """Initialize user interface"""
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Menu bar
        self.create_menu_bar()
        
        # Display
        self.display = wx.TextCtrl(
            panel,
            value="0",
            size=(-1, 60),
            style=wx.TE_READONLY | wx.TE_RIGHT
        )
        self.display.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(self.display, 0, wx.EXPAND | wx.ALL, 5)
        
        # Buttons layout
        buttons_data = [
            [("C", "clear"), ("←", "backspace"), ("Hist", "history"), ("÷", "divide")],
            [("7", "7"), ("8", "8"), ("9", "9"), ("×", "multiply")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("-", "minus")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("+", "plus")],
            [("0", "0"), (".", "decimal"), ("=", "equals"), ("√", "sqrt")],
            [("x²", "square"), ("±", "toggle_sign"), ("1/x", "reciprocal"), ("%", "modulo")],
        ]
        
        # Create buttons
        self.buttons = {}
        for row in buttons_data:
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            for label, name in row:
                btn = wx.Button(panel, label=label, size=(80, 50))
                btn.SetAccessible(wx.Accessible(btn))
                self.buttons[name] = btn
                self.Bind(wx.EVT_BUTTON, self.on_button_click, btn)
                row_sizer.Add(btn, 1, wx.EXPAND | wx.ALL, 2)
            sizer.Add(row_sizer, 0, wx.EXPAND)
        
        panel.SetSizer(sizer)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = wx.MenuBar()
        
        # File menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q")
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        menubar.Append(file_menu, "&File")
        
        # View menu
        view_menu = wx.Menu()
        
        # Theme submenu
        theme_menu = wx.Menu()
        theme_menu.AppendRadioItem(1, "&Light")
        theme_menu.AppendRadioItem(2, "&Dark")
        theme_menu.AppendRadioItem(3, "&High Contrast")
        self.Bind(wx.EVT_MENU, lambda e: self.change_theme("light"), id=1)
        self.Bind(wx.EVT_MENU, lambda e: self.change_theme("dark"), id=2)
        self.Bind(wx.EVT_MENU, lambda e: self.change_theme("high_contrast"), id=3)
        view_menu.AppendSubMenu(theme_menu, "&Theme")
        
        # Language submenu
        lang_menu = wx.Menu()
        lang_menu.AppendRadioItem(4, "&English")
        lang_menu.AppendRadioItem(5, "&العربية")
        self.Bind(wx.EVT_MENU, lambda e: self.change_language("en"), id=4)
        self.Bind(wx.EVT_MENU, lambda e: self.change_language("ar"), id=5)
        view_menu.AppendSubMenu(lang_menu, "&Language")
        
        menubar.Append(view_menu, "&View")
        
        # Help menu
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About")
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        menubar.Append(help_menu, "&Help")
        
        self.SetMenuBar(menubar)
    
    def on_button_click(self, event):
        """Handle button clicks"""
        btn = event.GetEventObject()
        
        for name, button in self.buttons.items():
            if button == btn:
                self.handle_button(name)
                break
    
    def handle_button(self, name):
        """Handle button actions"""
        try:
            if name in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                result = self.calculator.append_digit(name)
            elif name == "decimal":
                result = self.calculator.append_digit(".")
            elif name == "clear":
                result = self.calculator.clear_display()
            elif name == "backspace":
                result = self.calculator.backspace()
            elif name == "plus":
                result = self.calculator.set_operator("+")
            elif name == "minus":
                result = self.calculator.set_operator("-")
            elif name == "multiply":
                result = self.calculator.set_operator("×")
            elif name == "divide":
                result = self.calculator.set_operator("÷")
            elif name == "modulo":
                result = self.calculator.set_operator("%")
            elif name == "equals":
                result = self.calculator.calculate()
            elif name == "square":
                result = self.calculator.square()
            elif name == "sqrt":
                result = self.calculator.sqrt()
            elif name == "toggle_sign":
                result = self.calculator.toggle_sign()
            elif name == "reciprocal":
                result = self.calculator.reciprocal()
            elif name == "history":
                self.show_history()
                return
            else:
                return
            
            self.display.SetValue(result)
            self.display.SetInsertionPointEnd()
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Calculator Error", wx.OK | wx.ICON_ERROR)
    
    def show_history(self):
        """Show calculation history"""
        history = self.calculator.get_history()
        if not history:
            wx.MessageBox("No history available", "History", wx.OK | wx.ICON_INFORMATION)
            return
        
        if self.history_frame is None or not self.history_frame:
            self.history_frame = HistoryFrame(self, history)
        else:
            self.history_frame.update_history(history)
        
        self.history_frame.Show()
    
    def apply_theme(self, theme_name):
        """Apply theme to calculator"""
        if theme_name not in self.THEMES:
            theme_name = "light"
        
        theme = self.THEMES[theme_name]
        
        self.SetBackgroundColour(theme["bg"])
        self.display.SetBackgroundColour(theme["display_bg"])
        self.display.SetForegroundColour(theme["display_fg"])
        
        for btn in self.buttons.values():
            btn.SetBackgroundColour(theme["btn_bg"])
            btn.SetForegroundColour(theme["btn_fg"])
    
    def change_theme(self, theme_name):
        """Change calculator theme"""
        self.apply_theme(theme_name)
        self.settings.set("theme", theme_name)
        self.Refresh()
    
    def change_language(self, lang):
        """Change calculator language"""
        self.apply_language(lang)
        self.settings.set("language", lang)
    
    def apply_language(self, lang):
        """Apply language translations"""
        if lang not in self.TRANSLATIONS:
            lang = "en"
        
        self.current_language = lang
        # Update title
        self.SetTitle(self.TRANSLATIONS[lang]["title"])
    
    def on_about(self, event):
        """Show about dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("Advanced Calculator")
        info.SetVersion("1.0.0")
        info.SetDescription(
            "A bilingual calculator with NVDA screen reader support.\n"
            "Supports English and Arabic with multiple themes."
        )
        info.SetCopyright("© 2026 Fady Shehata")
        info.AddDeveloper("Fady Shehata")
        info.SetLicense("MIT License")
        
        wx.adv.AboutBox(info)
    
    def on_exit(self, event):
        """Exit application"""
        self.Close(True)
    
    def on_close(self, event):
        """Handle window close"""
        self.settings.save_settings()
        self.Destroy()


class HistoryFrame(wx.Frame):
    """History window"""
    
    def __init__(self, parent, history):
        wx.Frame.__init__(self, parent, title="Calculation History", size=(400, 300))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # List control
        self.history_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.history_list.InsertColumn(0, "Calculations", width=-1)
        
        for item in history:
            self.history_list.InsertItem(0, item)
        
        sizer.Add(self.history_list, 1, wx.EXPAND | wx.ALL, 5)
        
        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clear_btn = wx.Button(panel, label="Clear History")
        close_btn = wx.Button(panel, label="Close")
        
        self.Bind(wx.EVT_BUTTON, self.on_clear, clear_btn)
        self.Bind(wx.EVT_BUTTON, self.on_close, close_btn)
        
        btn_sizer.Add(clear_btn, 0, wx.ALL, 5)
        btn_sizer.Add(close_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND)
        panel.SetSizer(sizer)
    
    def update_history(self, history):
        """Update history list"""
        self.history_list.DeleteAllItems()
        for item in history:
            self.history_list.InsertItem(0, item)
    
    def on_clear(self, event):
        """Clear history"""
        self.history_list.DeleteAllItems()
    
    def on_close(self, event):
        """Close window"""
        self.Close()


class CalculatorApp(wx.App):
    """Main application class"""
    
    def OnInit(self):
        self.frame = CalculatorFrame()
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = CalculatorApp()
    app.MainLoop()
