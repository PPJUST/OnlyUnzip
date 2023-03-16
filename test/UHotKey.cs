using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Interop;

namespace UZIP2
{
	class UHotKey
	{
		static IntPtr Handle;
		static Int32 AutoHotKeys = 0x9999;
		public Int32 ID;
		public bool isRegister = false;
		UInt32 KMod = 0x0000;
		UInt32 KKey = 0x0000;

		public UHotKey(MainWindow mw)
		{
			// 获取窗口句柄
			Handle = new WindowInteropHelper(mw).Handle;
			ID = AutoHotKeys;
			AutoHotKeys--;

		}

		[DllImport("user32.dll")]
		public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);
		[DllImport("user32.dll")]
		public static extern bool UnregisterHotKey(IntPtr hWnd, int id);
		// 自定义快捷键事件
		//public const Int32 HOTKEY_PASTE = 0x9999;
		public void SetHotKey(UKey Key, bool Alt = false, bool Shift = false, bool Ctrl = false)
		{
			KMod = 0;
			if (Alt) KMod |= 0x0001;
			if (Shift) KMod |= 0x0004;
			if (Ctrl) KMod |= 0x0002;
			KKey = (UInt32)Key;
		}
		// 注册快捷键
		public void Register()
		{
			if (IsOK())
			{
				if (isRegister) Unregister();
				
				RegisterHotKey(Handle, ID, KMod, KKey);
				isRegister = true;
			}
				
		}
		// 取消注册快捷键
		public void Unregister()
		{
			UnregisterHotKey(Handle, ID);
		}
		// 检查快捷键是否可用
		public bool IsOK()
		{
			if (KMod == 0x0000) return false;
			if (KKey == 0x0000) return false;
			return true;
		}
	}
	// 建码
	public enum UKey
	{
		Key_0 = 0x30,
		Key_1 = 0x31,
		Key_2 = 0x32,
		Key_3 = 0x33,
		Key_4 = 0x34,
		Key_5 = 0x35,
		Key_6 = 0x36,
		Key_7 = 0x37,
		Key_8 = 0x38,
		Key_9 = 0x39,
		Key_A = 0x41,
		Key_B = 0x42,
		Key_C = 0x43,
		Key_D = 0x44,
		Key_E = 0x45,
		Key_F = 0x46,
		Key_G = 0x47,
		Key_H = 0x48,
		Key_I = 0x49,
		Key_J = 0x4A,
		Key_K = 0x4B,
		Key_L = 0x4C,
		Key_M = 0x4D,
		Key_N = 0x4E,
		Key_O = 0x4F,
		Key_P = 0x50,
		Key_Q = 0x51,
		Key_R = 0x52,
		Key_S = 0x53,
		Key_T = 0x54,
		Key_U = 0x55,
		Key_V = 0x56,
		Key_W = 0x57,
		Key_X = 0x58,
		Key_Y = 0x59,
		Key_Z = 0x5A,

		Key_F1 = 0x70,
		Key_F2 = 0x71,
		Key_F3 = 0x72,
		Key_F4 = 0x73,
		Key_F5 = 0x74,
		Key_F6 = 0x75,
		Key_F7 = 0x76,
		Key_F8 = 0x77,
		Key_F9 = 0x78,
		Key_F10 = 0x79,
		Key_F11 = 0x7A,
		Key_F12 = 0x7B,

		Key_Tilde = 0xC0,       // 波浪号
		Key_Minus = 0xBD,       // 减号
		Key_Plus = 0xBB,        // 加号

		Key_BraceOpen = 0xDB,   // 左花括号
		Key_BraceClose = 0xDD,  // 右花括号
		Key_Backslash = 0xDC,   // 反斜杠

		Key_Semicolon = 0xBA,   // 分号
		Key_Quote = 0xDE,       // 引号

		Key_Comma = 0xBC,       // 逗号
		Key_Period = 0xBE,      // 句号
		Key_Question = 0xBF,    // 问号
	}
}
