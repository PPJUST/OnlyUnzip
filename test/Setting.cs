using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace UZIP2
{


	public static class USetting
	{
		// 程序信息
		public static string UZip = "UZip2.22 by Farkaway\nFrom 52pojie.cn";
		// 程序状态
		public static RunStatus RunState = RunStatus.Normal;
		// 解压压缩中断
		public static bool UCancel = false;
		// 密码纸是否已改动，如改动了，解压时备份密码
		public static bool PaperChange = false;
		// 程序目录
		public static string BasePath = System.AppDomain.CurrentDomain.SetupInformation.ApplicationBase;
		// 配置目录名
		public static string ConfigFileForder = "Config\\";
		// 配置文件工具
		public static Config UConfig = new Config(BasePath + ConfigFileForder + "UZip.config");
		// 配置密码工具
		public static Config UPageConfig = new Config(BasePath + ConfigFileForder + "PasswordPage.config");
		// 配置密码工具2
		public static Config UNoteConfig = new Config(BasePath + ConfigFileForder + "PasswordNote.config");
		// 压缩记录文件
		public static string CompressLog = BasePath + "Compress.log";

		// 文件列表
		public static string[] FileList = null;
		// 密码纸
		public static Password PWPaper = new Password("PWPaper", UPageConfig);
		// 密码本
		public static Password PWNote = new Password("PWNote",UNoteConfig);
		// 废纸篓，密码回收站，关闭软件清除
		public static List<string> PWRecycle = new List<string>();
		// 草稿纸，解压时贴入的密码
		// public static List<string> PWTemp = new List<string>();

		// 文件解压过滤
		public static string[] ExtractFilterArray = null;
		// 文件压缩过滤
		public static string[] CompressFilterArray = null;

		// 文件删除到回收站
		public static bool DeleteToRecycle = true;

		// 读取外部密码
		public static string PWUrl 
		{
			get { return UConfig.GetConfig("PWUrl", ""); }
			set { UConfig.SetConfig("PWUrl", ""); }
		}
		// 
		public static int ReadPasswordMode 
		{
			get {return SConvert.ToInt(UConfig.GetConfig("ReadPasswordMode"),0); }
			set { UConfig.SetConfig("ReadPasswordMode", value.ToString()); }
		} 
		// 窗口位置y
		public static double WindowTop
		{
			get { return SConvert.ToDouble(UConfig.GetConfig("WindowTop"), -1); }
			set { UConfig.SetConfig("WindowTop", value.ToString()); }
		}
		// 窗口位置x
		public static double WindowLeft
		{
			get { return SConvert.ToDouble(UConfig.GetConfig("WindowLeft"), -1); }
			set { UConfig.SetConfig("WindowLeft", value.ToString()); }
		}
		// 程序工作模式
		public static int AppMode
		{
			get { return SConvert.ToInt(UConfig.GetConfig("AppMode"), (int)AppModes.Auto); }
			set { UConfig.SetConfig("AppMode", value.ToString()); }
		}

		// 主窗口始终置顶
		public static bool WindowOnTop
		{
			get { return SConvert.ToBool(UConfig.GetConfig("WindowOnTop"), true); }
			set { UConfig.SetConfig("WindowOnTop", value.ToString()); }
		}
		// 贴入密码时去除空格
		public static bool TrimSpace
		{
			get { return SConvert.ToBool(UConfig.GetConfig("TrimSpace"), false); }
			set { UConfig.SetConfig("TrimSpace", value.ToString()); }
		}
		// 使用自定义热键
		public static bool UseHotKey
		{
			get { return SConvert.ToBool(UConfig.GetConfig("UseHotKey"), false); }
			set { UConfig.SetConfig("UseHotKey", value.ToString()); }
		}
		// 自定义的热键
		public static uint HotKeyKey
		{
			get { return (uint)SConvert.ToInt(UConfig.GetConfig("HotKeyKey"), 0); }
			set { UConfig.SetConfig("HotKeyKey", value.ToString()); }
		}
		public static bool HotKeyAlt
		{
			get { return SConvert.ToBool(UConfig.GetConfig("HotKeyAlt"), false); }
			set { UConfig.SetConfig("HotKeyAlt", value.ToString()); }
		}
		public static bool HotKeyShift
		{
			get { return SConvert.ToBool(UConfig.GetConfig("HotKeyShift"), false); }
			set { UConfig.SetConfig("HotKeyShift", value.ToString()); }
		}
		public static bool HotKeyCtrl
		{
			get { return SConvert.ToBool(UConfig.GetConfig("HotKeyCtrl"), false); }
			set { UConfig.SetConfig("HotKeyCtrl", value.ToString()); }
		}
		

		// 独立窗口显示结果
		public static bool ResultWindow
		{
			get { return SConvert.ToBool(UConfig.GetConfig("ResultWindow"), false); }
			set { UConfig.SetConfig("ResultWindow", value.ToString()); }
		}
		// 显示Debug模式，仅通过修改配置文件开启，开启后显示Debug模式选项
		public static bool ShowDebug
		{
			get { return SConvert.ToBool(UConfig.GetConfig("ShowDebug"), false); }
			set { UConfig.SetConfig("ShowDebug", value.ToString()); }
		}
		// 使用Debug模式，开发者模式
		public static bool DebugMode
		{
			get { return SConvert.ToBool(UConfig.GetConfig("DebugMode"), false); }
			set { UConfig.SetConfig("DebugMode", value.ToString()); }
		}
		// 使用自定义7z.exe路径
		public static bool Customize7z
		{
			get { return SConvert.ToBool(UConfig.GetConfig("Customize7z"), false); }
			set { UConfig.SetConfig("Customize7z", value.ToString()); }
		}
		// 自定义的7z路径
		public static string Customize7zPath
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("Customize7zPath"), null); }
			set { UConfig.SetConfig("Customize7zPath", value); }
		}
		// 解压目录选项，设置面板
		public static int ExtractOutMode
		{
			get { return SConvert.ToInt(UConfig.GetConfig("ExtractOutMode"), (int)ExtractPath.File); }
			set { UConfig.SetConfig("ExtractOutMode", value.ToString()); }
		}
		// 解压目录选项，弹窗面板
		public static int ExtractOutModePop
		{
			get { return SConvert.ToInt(UConfig.GetConfig("ExtractOutModePop"), (int)ExtractPath.Last); }
			set { UConfig.SetConfig("ExtractOutModePop", value.ToString()); }
		}
		// 上次弹窗时，选择的解压目录
		public static string LastExtractPath
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("LastExtractPath"), null); }
			set { UConfig.SetConfig("LastExtractPath", value); }
		}
		// 解压目录选项，覆盖模式
		public static string ExtractCoverMode
		{
			get {
				string c = UConfig.GetConfig("ExtractCoverMode");
				return CoverMode.HasIt(c) ? c : CoverMode.Pass;
			}
			set { UConfig.SetConfig("ExtractCoverMode", value); }
		}
		// 尝试解压未知格式
		public static bool ExtractUnknow
		{
			get { return SConvert.ToBool(UConfig.GetConfig("ExtractUnknow"), true); }
			set { UConfig.SetConfig("ExtractUnknow", value.ToString()); }
		}
		// 解压成功删除文件
		public static bool DeleteFinishFile
		{
			get { return SConvert.ToBool(UConfig.GetConfig("DeleteFinishFile"), false); }
			set { UConfig.SetConfig("DeleteFinishFile", value.ToString()); }
		}
		// 包内文件较多时创建新文件夹
		public static bool CreateNewFolder
		{
			get { return SConvert.ToBool(UConfig.GetConfig("CreateNewFolder"), false); }
			set { UConfig.SetConfig("CreateNewFolder", value.ToString()); }
		}
		// 解压到压缩档案同名目录
		public static bool CreateNameFolder
		{
			get { return SConvert.ToBool(UConfig.GetConfig("CreateNameFolder"), false); }
			set { UConfig.SetConfig("CreateNameFolder", value.ToString()); }
		}



		// 自定义文件夹1
		public static string CustomizeFolderName1
		{
			get { return UConfig.GetConfig("CustomizeFolderName1", "自定义位置1"); }
			set { UConfig.SetConfig("CustomizeFolderName1", value); }
		}
		// 自定义文件夹路径1
		public static string CustomizeFolderPath1
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath1"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath1", value); }
		}
		// 自定义文件夹2
		public static string CustomizeFolderName2
		{
			get { return UConfig.GetConfig("CustomizeFolderName2", "自定义位置2"); }
			set { UConfig.SetConfig("CustomizeFolderName2", value); }
		}
		// 自定义文件夹路径2
		public static string CustomizeFolderPath2
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath2"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath2", value); }
		}
		// 自定义文件夹3
		public static string CustomizeFolderName3
		{
			get { return UConfig.GetConfig("CustomizeFolderName3", "自定义位置3"); }
			set { UConfig.SetConfig("CustomizeFolderName3", value); }
		}
		// 自定义文件夹路径3
		public static string CustomizeFolderPath3
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath3"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath3", value); }
		}
		// 自定义文件夹4
		public static string CustomizeFolderName4
		{
			get { return UConfig.GetConfig("CustomizeFolderName4", "自定义位置4"); }
			set { UConfig.SetConfig("CustomizeFolderName4", value); }
		}
		// 自定义文件夹路径4
		public static string CustomizeFolderPath4
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath4"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath4", value); }
		}
		// 自定义文件夹5
		public static string CustomizeFolderName5
		{
			get { return UConfig.GetConfig("CustomizeFolderName5", "自定义位置5"); }
			set { UConfig.SetConfig("CustomizeFolderName5", value); }
		}
		// 自定义文件夹路径5
		public static string CustomizeFolderPath5
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath5"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath5", value); }
		}
		// 自定义文件夹6
		public static string CustomizeFolderName6
		{
			get { return UConfig.GetConfig("CustomizeFolderName6", "自定义位置6"); }
			set { UConfig.SetConfig("CustomizeFolderName6", value); }
		}
		// 自定义文件夹路径6
		public static string CustomizeFolderPath6
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath6"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath6", value); }
		}
		// 自定义文件夹7
		public static string CustomizeFolderName7
		{
			get { return UConfig.GetConfig("CustomizeFolderName7", "自定义位置7"); }
			set { UConfig.SetConfig("CustomizeFolderName7", value); }
		}
		// 自定义文件夹路径7
		public static string CustomizeFolderPath7
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath7"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath7", value); }
		}
		// 自定义文件夹8
		public static string CustomizeFolderName8
		{
			get { return UConfig.GetConfig("CustomizeFolderName8", "自定义位置8"); }
			set { UConfig.SetConfig("CustomizeFolderName8", value); }
		}
		// 自定义文件夹路径8
		public static string CustomizeFolderPath8
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("CustomizeFolderPath8"), null); }
			set { UConfig.SetConfig("CustomizeFolderPath8", value); }
		}
		// 从文件名提取密码
		public static bool NameToPassword
		{
			get { return SConvert.ToBool(UConfig.GetConfig("NameToPassword"), false); }
			set { UConfig.SetConfig("NameToPassword", value.ToString()); }
		}
		// 从文件名提取标识符
		public static string NameFilter
		{
			get { return UConfig.GetConfig("NameFilter", null); }
			set { UConfig.SetConfig("NameFilter", value); }
		}

		// 从文件名提取标识符
		public static string NameFilter2
		{
			get { return UConfig.GetConfig("NameFilter2", null); }
			set { UConfig.SetConfig("NameFilter2", value); }
		}


		// 将密码写入文件名
		public static bool PasswordToName
		{
			get { return SConvert.ToBool(UConfig.GetConfig("PasswordToName"), false); }
			set { UConfig.SetConfig("PasswordToName", value.ToString()); }
		}


		// 解压文件过滤
		public static string ExtractFilter
		{
			get { return UConfig.GetConfig("ExtractFilter", null); }
			set { UConfig.SetConfig("ExtractFilter", value); }
		}
		// 压缩文件过滤
		public static string CompressFilter
		{
			get { return UConfig.GetConfig("CompressFilter", null); }
			set { UConfig.SetConfig("CompressFilter", value); }
		}
		// 压缩格式
		public static int CompressType
		{
			get { return SConvert.ToInt(UConfig.GetConfig("CompressType"), (int)CompressTypes.zip); }
			set { UConfig.SetConfig("CompressType", value.ToString());}
		}
		// 压缩级别
		public static int CompressLevel
		{
			get { return SConvert.ToInt(UConfig.GetConfig("CompressLevel"), (int)CompressLevels.Normal); }
			set { UConfig.SetConfig("CompressLevel", value.ToString()); }
		}
		// 压缩目录选项
		public static int CompressOutMode
		{
			get { return SConvert.ToInt(UConfig.GetConfig("CompressOutMode"), (int)CompressPath.File); }
			set { UConfig.SetConfig("CompressOutMode", value.ToString()); }
		}
		// 压缩目录选项，弹窗面板
		public static int CompressOutModePop
		{
			get { return SConvert.ToInt(UConfig.GetConfig("CompressOutModePop"), (int)CompressPath.Last); }
			set { UConfig.SetConfig("CompressOutModePop", value.ToString()); }
		}
		// 上次弹窗时，选择的压缩目录
		public static string LastCompressPath
		{
			get { return SConvert.ToPathString(UConfig.GetConfig("LastCompressPath"), null); }
			set { UConfig.SetConfig("LastCompressPath", value); }
		}
		// 压缩密码选项
		public static int PasswordMode
		{
			get { return SConvert.ToInt(UConfig.GetConfig("PasswordMode"), (int)SetPasswords.No); }
			set { UConfig.SetConfig("PasswordMode", value.ToString()); }
		}
		// 隐藏压缩文件内容
		public static bool HideZipContent
		{
			get { return SConvert.ToBool(UConfig.GetConfig("HideZipContent"), false); }
			set { UConfig.SetConfig("HideZipContent", value.ToString()); }
		}
		// 压缩密码选项，弹窗面板
		public static int PasswordModePop
		{
			get { return SConvert.ToInt(UConfig.GetConfig("PasswordModePop"), (int)SetPasswords.No); }
			set { UConfig.SetConfig("PasswordModePop", value.ToString()); }
		}
		// 每个都压缩的到单独文件
		public static bool CompressAlone
		{
			get { return SConvert.ToBool(UConfig.GetConfig("CompressAlone"), true); }
			set { UConfig.SetConfig("CompressAlone", value.ToString()); }
		}
		// 删除压缩完成文件
		public static bool DeleteCompressFinish
		{
			get { return SConvert.ToBool(UConfig.GetConfig("DeleteCompressFinish"), false); }
			set { UConfig.SetConfig("DeleteCompressFinish", value.ToString()); }
		}
		// 自定义密码1
		public static string CustomizePassword1
		{
			get { return UConfig.GetConfig("CustomizePassword1", null); }
			set { UConfig.SetConfig("CustomizePassword1", value); }
		}
		// 自定义密码2
		public static string CustomizePassword2
		{
			get { return UConfig.GetConfig("CustomizePassword2", null); }
			set { UConfig.SetConfig("CustomizePassword2", value); }
		}
		// 自定义密码3
		public static string CustomizePassword3
		{
			get { return UConfig.GetConfig("CustomizePassword3", null); }
			set { UConfig.SetConfig("CustomizePassword3", value); }
		}


		// 最大备份数
		const int MAXBACK = 5;
		// 备份密码配置
		public static void BackConfigPage()
		{
			int BFileNumber = SConvert.ToInt(UConfig.GetConfig("BackPageNum"), 1);
			UConfig.SetConfig("BackPageNum", (BFileNumber >= MAXBACK ? 1 : BFileNumber+1 ).ToString());
			string BackConfigPage = BasePath + ConfigFileForder + "PasswordPage.config";
			string BackConfigForder = BasePath + ConfigFileForder + "Backup\\";
			string BackConfigPageTo = BackConfigForder + "PasswordPage.config" + ".backup0" + BFileNumber;
			if (Directory.Exists(BackConfigForder) == false) Directory.CreateDirectory(BackConfigForder);
			if (File.Exists(BackConfigPage)) File.Copy(BackConfigPage, BackConfigPageTo , true);
		}
		public static void BackConfigNote()
		{
			int BFileNumber = SConvert.ToInt(UConfig.GetConfig("BackNoteNum"), 1);
			UConfig.SetConfig("BackNoteNum", (BFileNumber >= MAXBACK ? 1 : BFileNumber + 1).ToString());
			string BackConfigNote = BasePath + ConfigFileForder + "PasswordNote.config";
			string BackConfigForder = BasePath + ConfigFileForder + "Backup\\";
			string BackConfigNoteTo = BackConfigForder + "PasswordNote.config" + ".backup0" + BFileNumber;
			if (Directory.Exists(BackConfigForder) == false) Directory.CreateDirectory(BackConfigForder);
			if (File.Exists(BackConfigNote)) File.Copy(BackConfigNote, BackConfigNoteTo, true);
		}
	}
	public class Password
	{
		// 密码上限
		public const int PWMAX = 200;
		// 密码数据
		public List<string> Passwords = new List<string>();
		// 密码字段名
		public string PasswordName = null;
		// 配置文件操作工具
		private Config PWConfig = null;
		// 获取密码数
		public int Count
		{
			get { return Passwords.Count; }
		}
		public Password(string name,Config c)
		{
			PasswordName = name;
			PWConfig = c;
		}
		// 载入所有密码数据
		public void LoadPasswords()
		{
			string p = null;
			for (int i = 0; i < PWMAX; i++)
			{
				p = PWConfig.GetConfig(PasswordName + i, null);
				if (p == null||p=="") break;
				Passwords.Add(p);
			}

		}
		// 储存所有密码
		public void SavePasswords()
		{
			int i = 0;
			foreach (string p in Passwords)
			{
				PWConfig.SetConfig(PasswordName + i, p);
				i++;
			}
			// 添加结尾标记
			PWConfig.SetConfig(PasswordName + i, null);
		}

		// 添加一个密码，并写入配置。容量超过返回Null 否则返回字符串
		public string AddPassword(string pw)
		{
			if (Count >= PWMAX) return null;
			else
			{
				Passwords.Add(pw);
				PWConfig.SetConfig(PasswordName + (Count - 1), pw);
				// 重新添加结尾标记
				PWConfig.SetConfig(PasswordName + (Count), null);
				return pw;
			}
		}

		// 删除一个密码，并保存所有密码,返回删除的密码，以便放入临时回收站，
		public string DeletePassword(string pw)
		{
			Passwords.Remove(pw);
			SavePasswords();
			return pw;
		}
		// 获取最后的输入
		public string GetLastPassword()
		{
			if (Count <= 0) return null;
			return Passwords[Count - 1];
		}
		// 删除最后输入的，并保存所有密码,返回删除的密码，以便放入临时回收站，
		public string DeleteLastPassword()
		{
			int c = Count;
			if (c <= 0) return null;
			string deletepw = GetLastPassword();
			Passwords.RemoveAt(c - 1);
			PWConfig.SetConfig(PasswordName + (c-1), null);
			//SavePasswords();
			return deletepw;
		}

		// 添加若干密码,超过上限则忽略
		public bool AddPassword(List<string> li)
		{
			if (li == null) return false;
			if (Count + li.Count() >= PWMAX) return false;
			foreach (string l in li)
			{
				if(Count<PWMAX) Passwords.Add(l);
			}
			SavePasswords();
			return true;
		}
		// 删除若干密码
		public List<string> DeletePassword(List<string> li)
		{
			if (li == null) return null;
			foreach (string l in li)
			{
				Passwords.Remove(l);
			}
			SavePasswords();
			return li;
		}
		// 清空密码库
		public void ClearPassword()
		{
			Passwords = new List<string>();
			PWConfig.SetConfig(PasswordName + 0, null);
		}
		// 带回车的字符串段 转换为 列表list
		public static List<string> StringToList(string str)
		{
			if (str == null || str == "") return null;
			// 使用换行符切割字符串
			string[] sArray = str.Split('\n');
			List<string> list = new List<string>();

			string s2 = "";
			foreach (string s in sArray)
			{
				// 剔除空行
				if (s != "\n" && s != "\r" && s != "\t" && s != "" && s != " " && s != null)
				{
					// 剔除特殊字符
					s2 = s.Replace("\n", "").Replace("\t", "").Replace("\r", "");
					list.Add(s2);
				}

			}
			return list;
		}
		// 列表list 转换为 带回车的字符串段 
		public static string ListToString(List<string> li)
		{
			if (li == null) return null;
			return string.Join("\n", li.ToArray());
		}
		// 传入一个cmd对象，以检测密码
		public string CmdTestPassword(UCmd cmd,string f)
		{
			for (int i = 0; i < Passwords.Count; i++)
			{
				string uMessage = cmd.TestFile(f, Passwords[i]);
				//MessageBox.Show(uMessage);
				if (UCmd.IsOK(uMessage))
				{
					return Passwords[i];
				}
			}
			return null;
		}

	}

	// 字符串 转为 INT DOUBLE BOOL转换，防止异常,可设置默认值
	public static class SConvert
	{
		public static int ToInt(string i,int i0 = 0)
		{
			if (i == null) return i0;
			try
			{
				return int.Parse(i);
			}
			catch
			{
				return i0;
			}
		}
		public static double ToDouble(string d,double d0 = 0)
		{
			if (d == null) return d0;
			try
			{
				return double.Parse(d);
			}
			catch
			{
				return d0;
			}
		}
		public static bool ToBool(string b,bool b0 = false)
		{
			if (b == null) return b0;
			try
			{
				return bool.Parse(b);
			}
			catch
			{
				return b0;
			}
		}
		public static string ToPathString(string p, string p0 = null)
		{
			// null 或 非路径 UTool.CheckPath 都已经处理
			return UTool.CheckPath(p) ? p : p0;
		}
	}
	// App 工作模式
	public enum AppModes
	{
		Auto = 0,					// 自动选择解压
		OnlyExtract = 1,			// 仅解压
		OnlyCompress = 2			// 仅压缩

	}
	// 运行状态
	public enum RunStatus
	{
		Normal = 0,					// 待机中
		EditSetting = 1,			// 设置中，不可解压，不可贴入密码，不可编辑密码
		EditPassword = 2,			// 密码设置中，不可解压，不可贴入密码，不可编辑设置
		MiniMode = 3,				// 迷你模式，密码收集器
		MiniModeR = 4,              // 迷你模式，右键菜单
		ModeSelect = 5,				// 软件模式选择
		ExtractFile = 6,            // 解压中，不可解压，可以贴入密码，不可设置，不可编辑密码。
		CompressFile = 7,           // 压缩中
		AutoFile = 8,				// 自动解压和压缩
		Finish = 9,					// 完成
		Error = 10					// 错误，不可解压，不可贴入密码，不可编辑设置
	}

	// 解压位置，此位置应和SelectOut窗口 列表框相同
	public enum ExtractPath
	{
		Last = 0,           // 上次位置，设置面板里没有
		File = 1,           // 文件所在位置
							// ----------
		Browse = 3,         // 浏览的临时自定义位置
							// ----------
		Customize1 = 5,     // 自定义位置1
		Customize2 = 6,     // 自定义位置2
		Customize3 = 7,     // 自定义位置3
		Customize4 = 8,     // 自定义位置4
		Customize5 = 9,     // 自定义位置5
		Customize6 = 10,    // 自定义位置6
		Customize7 = 11,    // 自定义位置7
		Customize8 = 12,    // 自定义位置8

	}

	// 覆盖模式
	public struct CoverMode
	{
		public static string Cover = "-aoa"; // 覆盖现有文件
		public static string Pass = "-aos"; // 跳过现有文件
		public static string RenameNew = "-aou"; // 重命名新的文件
		public static string RenameOld = "-aot"; // 重命名旧的文件
		public static bool HasIt(string s)
		{
			if (s == Cover || s == Pass || s == RenameNew || s == RenameOld) return true;
			return false;
		}
	}
	// 压缩级别
	public enum CompressLevels
	{
		No = 0,				// 不压缩
		Fastest = 1,		// 极速
		Fast = 3,			// 快速
		Normal = 5,			// 标准
		Maximum = 7,		// 最大
		Ultra = 9			// 极限

	}
	// 压缩到目录
	public enum CompressPath
	{
		Last = 0,           // 上次位置，设置面板里没有
		File = 1,           // 文件所在位置
							// --------------------
		Browse = 3,         // 浏览的临时自定义位置
	}
	// 设置密码
	public enum SetPasswords
	{
		No = 0,             // 不设置密码
							// --------------------
		Customize1 = 2,     // 自定义1
		Customize2 = 3,     // 自定义2
		Customize3 = 4,     // 自定义3
							// --------------------
		Random8 = 6,        // 随机密码
		Random16 = 7,       // 随机密码
		Random32 = 8        // 随机密码

	}
	// 压缩格式
	public enum CompressTypes
	{
		zip = 0,        // zip 0,1,3,5,7,9
		zip7 = 1,       // 7z 0,1,3,5,7,9
		bzip2 = 2,		// bz 1,3,5,7,9
		gzip =3,		// gz 1,5,7,9
		tar = 4,		// tar 0
		wim = 5,		// wim 0
		xz = 6,			// xz 1,3,5,7,9
	}

	// 提示模式
	public enum TipMods
	{
		TipNormal = 0,      // 普通提示，工具提示
		WarmGray = 1,		// 灰色提示，贴入密码
		WarnGreen = 2,		// 绿色示意，解压成功
		WarnRed = 3,		// 红色警告，错误提示
		FixGray = 4			// 固定模式，不会被点击清除，工具提示
	}

}
