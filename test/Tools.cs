using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Documents;
using System.Windows.Forms;
using System.Windows.Controls;
using System.Windows.Media;
using System.Text.RegularExpressions;
using System.Diagnostics;
using System.Windows;
using MSVB = Microsoft.VisualBasic.FileIO;

namespace UZIP2
{
	static class UTool
	{
		//检测路径是否可用，即使不存在
		public static bool CheckPath(string path)
		{
			// 检查路径是否为空
			if (path == null) return false;
			// 检测是否包含盘符和冒号
			try
			{
				if (!System.IO.Path.IsPathRooted(path)) return false;
			}
			catch
			{
				return false; // 使用了非法字符<>|会抛出错误
			}
			// 检测是否使用了非法字符<>|过不了上层,所以没放这 
			char[] invalidChars = { '*', '?', '\"', '/' };
			foreach (char c in invalidChars)
			{
				if (path.IndexOf(c) != -1) return false;
			}
			// 冒号:出现在其他位置
			if (path.Substring(2).IndexOf(':') != -1) return false;
			// 两层斜杠\\
			if (path.Contains("\\\\")) return false;
			return true;
		}

		// 路径补完，如果路径不带最后的\就补上一个
		public static string CompletionPath(string path)
		{
			if (path.Substring(path.Length - 1) == "\\") return path;
			return path + "\\";
		}

		// 使用分割标识符，切割字符串，用于从文件名提取密码
		public static string SplitString(string f,string s)
		{
			string p = f;
			
			int n1 = p.IndexOf(s);
			int n2 = -1;
			if (n1 >= 0)
			{
				p = p.Remove(0, n1 + s.Length);
				n2 = p.LastIndexOf(s);
				if (n2 >= 0)
				{
					p = p.Remove(n2);
				}
			}
			else
			{
				p = null;
			}
			
			return p;
		}

		// 分割字符串并清除空字符
		public static string[] Split(string s)
		{
			// 字符串为空 返回空
			if (s == "" || s == null) return null;
			// 清理所有空格,空白
			s = Regex.Replace(s, @"\s", "");
			// 清理重复的;;;
			string ss = null;
			do
			{
				ss = s;
				s = s.Replace(";;", ";");
			} while (s != ss);
			// 再次审查
			if (s == "") return null;
			// 删除字符串的分号结尾
			if (s.Substring(s.Length - 1, 1) == ";")
				s = s.Substring(0, s.Length - 1);
			// 再次审查
			if (s == "") return null;
			// 分割字符串
			return s.Split(';');

		}

		// 随机密码生成器
		public static string GetRandomString(int length, bool useNum = true
			, bool useLow = true, bool useUpp = true, bool useSpe = false, string custom = "")
		{
			byte[] b = new byte[4];
			new System.Security.Cryptography.RNGCryptoServiceProvider().GetBytes(b);
			Random r = new Random(BitConverter.ToInt32(b, 0));
			string s = null, str = custom;
			if (useNum == true) { str += "0123456789"; }
			if (useLow == true) { str += "abcdefghijklmnopqrstuvwxyz"; }
			if (useUpp == true) { str += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; }
			if (useSpe == true) { str += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"; }
			for (int i = 0; i < length; i++)
			{
				s += str.Substring(r.Next(0, str.Length - 1), 1);
			}
			return s;
		}

		// 检查文件真实格式
		public static string RealExtension(string path)
		{
			FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read);
			BinaryReader r = new BinaryReader(fs);
			string bx = " ";
			byte buffer;
			try
			{
				buffer = r.ReadByte();
				bx = buffer.ToString();
				buffer = r.ReadByte();
				bx += buffer.ToString();
			}
			catch (Exception exc)
			{
				System.Windows.MessageBox.Show("出现异常 " + exc.Message);
			}
			r.Close();
			fs.Close();
			//真实的文件类型
			switch (bx)
			{
				case "8297":	return ".rar";
				case "8075":	return ".zip";
				case "55122":	return ".7z";
				case "6690":	return ".bz2";
				case "31139":	return ".gz";
				case "30125":	return ".lzh";
				case "4950":	return ".tar";
				case "7783":	return ".wim";
				case "25355":	return ".xz";
				case "00":		return ".iso";
				default:		return null;
			}

			//string ZE = Enum.GetName(typeof(ZipExtension), int.Parse(bx));
			//MessageBox.Show("格式代码为 " + bx + "\n真实格式为 " + ZE);
		}



		// 检查文件字符串后缀
		public static bool CanExtract(string FPath)
		{
			string Extension = Path.GetExtension(FPath).ToLower();
			switch (Extension)
			{
				// 压缩和解压
				case ".zip":
				case ".bz2":
				case ".gz":
				case ".tar":
				case ".wim":
				case ".7z":
				case ".xz":
				// 仅解压
				case ".rar":
				case ".arj":
				case ".cab":
				case ".chm":
				case ".cpio":
				case ".deb":
				case ".dmg":
				case ".fat":
				case ".hfs":
				case ".iso":
				case ".lzh":
				case ".lzma":
				case ".mbr":
				case ".msi":
				case ".nsis":
				case ".ntfs":
				case ".rpm":
					// 分卷
				case ".001":
					return true;
				case "": return false;
				default: return false;

			}
		}
		// 传入一个路径，检查是否存在，如存在，并返回加料的新路径
		public static string MoveFolderHelp(string sPath, string sName)
		{
			string oPath = sPath;
			int sNum = 1;
			while (File.Exists(oPath))
			{
				oPath = Path.GetDirectoryName(sPath) + "\\" + Path.GetFileNameWithoutExtension(sPath)
					+ sName + (sNum / 10 < 1 ? "0" + sNum : "" + sNum) + Path.GetExtension(sPath);
				sNum++;
			}
			return oPath;

		}
		

		// 移动文件
		public static void MoveFolder(string sourcePath, string destPath, string coverMode = null)
		{
			if (Directory.Exists(sourcePath))
			{
				if (!Directory.Exists(destPath))
				{
					//目标目录不存在则创建  
					try
					{
						Directory.CreateDirectory(destPath);
					}
					catch (Exception ex)
					{
						throw new Exception("创建目标目录失败：" + ex.Message);
					}
				}
				//获得源文件下所有文件  
				List<string> files = new List<string>(Directory.GetFiles(sourcePath));
				files.ForEach(c =>
				{
					string destFile = Path.Combine(new string[] { destPath, Path.GetFileName(c) });
					// 移动文件，检查文件是否存在，确定覆盖模式
					if (File.Exists(destFile))
					{
						if (coverMode == CoverMode.Pass || coverMode == null)
						{

						}
						if (coverMode == CoverMode.Cover)
						{
							File.Delete(destFile);
							File.Move(c, destFile);
						}
						if (coverMode == CoverMode.RenameNew)
						{
							File.Move(c, MoveFolderHelp(destFile, "-New"));
						}
						if (coverMode == CoverMode.RenameOld)
						{
							File.Move(destFile, MoveFolderHelp(destFile, "-Old"));
							File.Move(c, destFile);
						}
					}
					else
					{
						File.Move(c, destFile);
					}

				});
				//获得源文件下所有目录文件  
				List<string> folders = new List<string>(Directory.GetDirectories(sourcePath));

				folders.ForEach(c =>
				{
					string destDir = Path.Combine(new string[] { destPath, Path.GetFileName(c) });
					//Directory.Move必须要在同一个根目录下移动才有效，不能在不同卷中移动。  
					//Directory.Move(c, destDir);  

					//采用递归的方法实现  
					MoveFolder(c, destDir, coverMode);
				});
			}
		}

		// 查找目录中的指定格式文件
		public static List<string> FindFile(string SourcePath, string ffilter)
		{
			List<String> FList = new List<string>();
			FindFileHelp(SourcePath, ffilter, FList);
			return FList;
		}
		static void FindFileHelp(string SourcePath, string ffilter, List<string> Flist)
		{
			// 规整目录后斜杠
			string sSourcePath = UTool.CompletionPath(SourcePath);

			//在指定目录及子目录下查找文件,在list中列出子目录及文件
			DirectoryInfo Dir = new DirectoryInfo(sSourcePath);
			DirectoryInfo[] DirSub = Dir.GetDirectories();
			//查找文件,返回文件
			foreach (FileInfo f in Dir.GetFiles(ffilter, SearchOption.TopDirectoryOnly)) //查找文件
			{
				Flist.Add(Dir + f.ToString());
			}
			//查找子目录，并递归
			foreach (DirectoryInfo d in DirSub)//查找子目录
			{
				FindFileHelp(Dir + d.ToString(), ffilter, Flist);
			}
		}

		// 删除文件或文件夹
		public static void DeleteFileOrDirectory(string f,bool Recycle=false)
		{
			
			if (File.Exists(f))
			{
				DeleteFile(f, Recycle);
			}
			else if (Directory.Exists(f))
			{
				DeleteDirectory(f, Recycle);

			}


		}
		public static void DeleteFile(string f, bool Recycle = false)
		{
			if (Recycle)
				MSVB.FileSystem.DeleteFile(f, MSVB.UIOption.OnlyErrorDialogs, MSVB.RecycleOption.SendToRecycleBin);
			else
				File.Delete(f);
		}
		public static void DeleteDirectory(string f, bool Recycle = false)
		{
			if (Recycle)
				MSVB.FileSystem.DeleteDirectory(f, MSVB.UIOption.OnlyErrorDialogs, MSVB.RecycleOption.SendToRecycleBin);
			else
				(new DirectoryInfo(f)).Delete(true);
		}

	}
	public class VolumesFile
	{
		string Extension;
		string Extension2;
		string ZipType;
		bool Volumes = false;
		string Forder ;
		public string FileName;
		int s;
		public VolumesFile(string FilePath)
		{
			// 文件一级后缀
			Extension = Path.GetExtension(FilePath).ToLower();
			// 文件所在目录
			Forder = Path.GetDirectoryName(FilePath)+"\\";
			// 提取文件名
			FileName = Path.GetFileNameWithoutExtension(FilePath);

			// 判断分卷信息，提取二级后缀，更正压缩类型，更新文件名
			if (Extension.Length > 3)
			{
				// .part1.rar
				if (Extension == ".rar")
				{
					ZipType = "rar";
					// 提取二级后缀
					Extension2 = Path.GetExtension(FileName).ToLower();
					// 检查二级后缀
					if (Extension2.Length > 5)
					{
						if (Extension2.Substring(0, 5) == ".part")
						{
							Volumes = true;
							// 重新提取文件名
							FileName = Path.GetFileNameWithoutExtension(FileName);
						}
					}
					return;
				}
				// .zip
				if (Extension == ".zip")
				{
					ZipType = "zip-zip";
					return;
				}
				// .z01
				if (Extension.Substring(0, 2) == ".z")
				{
					// 检查后缀
					if (int.TryParse(Extension.Remove(0, 2), out s))
					{
						ZipType = "zip-z";
						Volumes = true;
					}
					return;
				}
				// zip.001 7z.001 判断是否可以转换为整型 再判断第二级后缀
				if (int.TryParse(Extension.Remove(0, 1), out s))
				{
					// 提取二级后缀
					Extension2 = Path.GetExtension(FileName).ToLower();

					switch (Extension2)
					{
						case ".zip": ZipType = "zip"; Volumes = true; break;
						case ".bz2": ZipType = "bz2"; Volumes = true; break;
						case ".gz": ZipType = "gz"; Volumes = true; break;
						case ".tar": ZipType = "tar"; Volumes = true; break;
						case ".wim": ZipType = "wim"; Volumes = true; break;
						case ".7z": ZipType = "7z"; Volumes = true; break;
						case ".xz": ZipType = "xz"; Volumes = true; break;
					}
					// 重新提取文件名
					if(Volumes) FileName = Path.GetFileNameWithoutExtension(FileName);
					return;
				}
			}
		}
		// 获取主分卷
		public string GetMainVolumes()
		{
			if (ZipType == null) return null;

			switch (ZipType)
			{
				case "zip-zip":return null;
				case "zip-z":return Forder + FileName + ".zip";
				case "zip":return Forder + FileName + ".zip.001";
				case "bz2": return Forder + FileName + ".bz2.001";
				case "gz": return Forder + FileName + ".gz.001";
				case "tar": return Forder + FileName + ".tar.001";
				case "wim": return Forder + FileName + ".wim.001";
				case "7z": return Forder + FileName + ".7z.001";
				case "xz": return Forder + FileName + ".xz.001";
				case "rar":return Forder + FileName + ".part1.rar";
			}
			return null;
		}
		// 是否为分卷
		public bool IsVolumes()
		{
			//if(ZipType == "rar")
			return Volumes;
		}
		// 删除分卷文件
		public void DeleteVolumesFile()
		{
			bool go = false;
			int num = 1;
			if (ZipType == null) return;
			switch (ZipType)
			{
				case "zip-zip": 
				case "zip-z":
					{
						DeleteFile(Forder + FileName + ".zip");
						do
						{
							go = DeleteFile(Forder + FileName + ".z" + num.ToString().PadLeft(2, '0'));
							num++;
						} while (go);
						break;
					}
				case "rar":
					{
						do
						{
							go = DeleteFile(Forder + FileName + ".part" + num +".rar");
							num++;
						} while (go);
						break;
					}
				case "zip":
				case "bz2": 
				case "gz": 
				case "tar": 
				case "wim": 
				case "7z": 
				case "xz":
					{
						do
						{
							go = DeleteFile(Forder + FileName + Extension2 +"."+ num.ToString().PadLeft(3, '0'));
							
							num++;
						} while (go);
						break;
					}
			}
		}
		// 删除文件，不存在则跳过
		private bool DeleteFile(string f)
		{
			
			if (File.Exists(f))
			{
				//File.Delete(f);
				UTool.DeleteFile(f, USetting.DeleteToRecycle);
				return true;
			}
			return false;
		}
	}
	public static class UCmdPathHelp
	{
		// 返回7Z路径
		public static string Get7zParh()
		{
			if (USetting.Customize7z == true && File.Exists(USetting.Customize7zPath))
			{
				return "\"" + USetting.Customize7zPath + "\" ";
			}
			else
			{
				return "\"" + USetting.BasePath + "7-Zip\\7z.exe" + "\""; ;
			}
		}

		public static string GetExtractPath(string file = null)
		{
			return "\"" + UExtractPath(file) + "\"";
		}
		// 返回解压输出路径,如输入文件路径，则提取其名称，则创建该名称的文件夹
		public static string UExtractPath(string file = null)
		{
			string path = null;
			// 检查是否使用浏览路径面板
			if (USetting.ExtractOutMode != (int)ExtractPath.Browse)
			{
				switch (USetting.ExtractOutMode)
				{
					case (int)ExtractPath.File: path = Path.GetDirectoryName(USetting.FileList[0]) + "\\"; break;
					case (int)ExtractPath.Customize1: path = USetting.CustomizeFolderPath1; break;
					case (int)ExtractPath.Customize2: path = USetting.CustomizeFolderPath2; break;
					case (int)ExtractPath.Customize3: path = USetting.CustomizeFolderPath3; break;
					case (int)ExtractPath.Customize4: path = USetting.CustomizeFolderPath4; break;
					case (int)ExtractPath.Customize5: path = USetting.CustomizeFolderPath5; break;
					case (int)ExtractPath.Customize6: path = USetting.CustomizeFolderPath6; break;
					case (int)ExtractPath.Customize7: path = USetting.CustomizeFolderPath7; break;
					case (int)ExtractPath.Customize8: path = USetting.CustomizeFolderPath8; break;
				}
			}
			
			// 如使用浏览路径面板，并确定，选择的路径存入 USetting.LastExtractPath
			// 如取消，则不会进入此程序，因此不留处理程序
			else path = USetting.LastExtractPath;
			//System.Windows.MessageBox.Show(path);
			// 是否需要新建文件夹
			if (file != null) path = path + "UZipTempForder\\";

			// 检查解压输出目录是否存在，不存在就创建
			if (Directory.Exists(path) == false) Directory.CreateDirectory(path);
			return UTool.CompletionPath(path);
		}

		public static string UCompressPath()
		{
			string path = null;
			// 确定压缩输出目录
			if (USetting.CompressOutMode == (int)CompressPath.File)
			{
				path = Path.GetDirectoryName(USetting.FileList[0]);
			}
			if (USetting.CompressOutMode == (int)CompressPath.Browse)
			{
				path = USetting.LastCompressPath;
			}

			// 检查压缩输出目录是否存在，不存在就创建
			if (Directory.Exists(path) == false) Directory.CreateDirectory(path);
			return UTool.CompletionPath(path);
		}
		// 返回压缩输出路径
		public static string GetCompressPath()
		{
			//System.Windows.MessageBox.Show("\"" + UCompressPath() + "\"");
			return "\"" + UCompressPath() + "\"";
		}
	}

	public class UCmd
	{
		Process p = new Process();
		// 7zip程序目录
		string Z7Path = "";
		// 输出目录
		string OutPath = "";
		// 压缩覆盖模式
		string ECover = null;
		// 压缩级别
		string CLevel = null;
		// 压缩文件格式
		string CType = null;

		// 记录输出的文件
		private string OFPath = null;
		public string GetOutFilePath()
		{
			return OFPath;
		}

		// true 表示压缩 false 表示解压
		public UCmd(bool isExtract)
		{
			//设置要启动的应用程序
			p.StartInfo.FileName = "cmd.exe";
			//是否使用操作系统shell启动
			p.StartInfo.UseShellExecute = false;
			// 接受来自调用程序的输入信息
			p.StartInfo.RedirectStandardInput = true;
			// 输出信息
			p.StartInfo.RedirectStandardOutput = true;
			//不显示程序窗口
			p.StartInfo.CreateNoWindow = true;
			// 确定7Z目录
			Z7Path = UCmdPathHelp.Get7zParh();
			// 根据工作模式 初始化对象
			if (isExtract)
			{
				// 确定解压输出目录
				OutPath = UCmdPathHelp.GetExtractPath();
				// 解压覆盖模式
				ECover = USetting.ExtractCoverMode;
			}
			else
			{
				// 确定压缩输出目录
				OutPath = UCmdPathHelp.GetCompressPath();
				// 压缩级别
				CLevel = USetting.CompressLevel.ToString();
				// 压缩类型
				switch (USetting.CompressType)
				{
					case (int)CompressTypes.zip: CType = ".zip"; break;
					case (int)CompressTypes.zip7: CType = ".7z"; break;
				}
			}
		}


		// 读取目录信息（测试有问题 不要用了）
		public string ListFile(string FilePath, string Password = null)
		{
			// 拼接目录用字符串
			string StrInput = Z7Path + " l " + "\"" + FilePath + "\"" + " -p" + "\"" + Password + "\"";
			// System.Windows.MessageBox.Show(StrInput);
			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}
		// 测试密码
		public string TestFile(string FilePath, string Password = null)
		{

			// 拼接测试用字符串
			string StrInput = Z7Path + " t " + "\"" + FilePath + "\"" + " -p" + "\"" + Password + "\"";
			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}

		// 解压文件
		public string ExtractFile(string FilePath, string Password = null)
		{
			// 重写输出目录
			OutPath = UCmdPathHelp.GetExtractPath();
			// 拼接解压缩用字符串
			string StrInput = Z7Path + " x " + "\"" + FilePath + "\"" + " -o" + OutPath +
				" " + ECover + " -p" + "\"" + Password + "\"";
			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}
		// 解压文件，在新文件夹中
		public string ExtractFileNewForder(string FilePath, string Password = null)
		{

			// 拼接输出
			// 拼接解压缩用字符串
			string StrInput = Z7Path + " x " + "\"" + FilePath + "\"" + " -o" + UCmdPathHelp.GetExtractPath(FilePath) +
				" " + ECover + " -p" + "\"" + Password + "\"";
			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}
		// 压缩文件
		public string CompressFile(string FilePath, string Password = null, 
			string[] filter = null, bool hidecontent = false, string sign = null)
		{
			// 拼接输出文件
			string OutFilePath = "";
			string OutFileName = Path.GetFileNameWithoutExtension(FilePath);
			// 在文件名藏入密码
			string SignPW = "";
			if (sign != null && Password != null) SignPW = sign + Password;

			// 查看文件名是否包含-new
			int n = OutFileName.IndexOf("-New");
			if (n > 0)
			{
				OutFileName = OutFileName.Remove(n);
			}
			int OutFileNum = 0;
			// 检查输出文件是否存在
			do {
				OutFilePath = OutPath.Substring(1, OutPath.Length - 2) +
					 OutFileName + (OutFileNum == 0 ? "" : "-New" + OutFileNum) + SignPW + CType;

				OutFileNum++;
			} while (File.Exists(OutFilePath));
			// 储存当前输出的目录
			OFPath = OutFilePath;
			// 格式化输出目录
			OutFilePath = "\"" + OutFilePath + "\"";

			// 拼接压缩用字符串
			string StrInput = Z7Path + " a " + OutFilePath + " \"" + FilePath + "\"";
			// 加入密码
			if (Password != null) StrInput = StrInput + " -p" + "\"" + Password + "\"" ;
			// 判断是否需要隐藏文件内容 仅限7z
			if (hidecontent && CType == ".7z") 
			{
				StrInput = StrInput + " -mhe";
			}
			// 拼接过滤字符串
			if (filter != null && filter.Length > 0)
			{
				foreach (string fil in filter)
				{
					StrInput = StrInput + " -xr!" + fil;
				}
			}

			//System.Windows.MessageBox.Show(StrInput);
			//return "null";
			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}

		// 压缩若干文件
		public string CompressFile(string[] FileList, string Password = null, 
			string[] filter = null,bool hidecontent = false, string sign = null)
		{
			// 拼接输出文件
			string OutFileForder = Path.GetFileNameWithoutExtension(Path.GetDirectoryName(FileList[0]));
			if (OutFileForder == "")
			{
				OutFileForder = "NewArchive";
			}

			// 在文件名藏入密码
			string SignPW = "";
			if (sign != null && Password != null) SignPW = sign + Password; 

			// 拼接输出文件
			string OutFilePath = "";
			int OutFileNum = 0;
			// 检查输出文件是否存在
			do
			{
				OutFilePath = OutPath.Substring(1, OutPath.Length - 2) + OutFileForder +
					(OutFileNum == 0 ? "" : "-New" + OutFileNum) + SignPW + CType;
				OutFileNum++;
			} while (File.Exists(OutFilePath));
			// 储存当前输出的目录
			OFPath = OutFilePath;
			// 格式化输出目录
			OutFilePath = "\"" + OutFilePath + "\"";

			// 拼接输入文件串
			string InFilePaths = null;
			foreach (string s in FileList)
			{
				InFilePaths = InFilePaths + " \"" + s + "\"";
			}
			// 拼接压缩用字符串 
			string StrInput = Z7Path + " a " + OutFilePath + InFilePaths;

			// 加入密码
			if (Password != null) StrInput = StrInput + " -p" + "\"" + Password + "\"";
			// 判断是否需要隐藏文件内容 仅限7z
			if (hidecontent && CType == ".7z")
			{
				StrInput = StrInput + " -mhe";
			}

			// 添加过滤字符串
			// 拼接过滤字符串
			if (filter != null && filter.Length > 0)
			{
				foreach (string fil in filter)
				{
					StrInput = StrInput + " -xr!" + fil;
				}
			}

			// 启动CMD程序并读取结果
			string StrOutPut = Cmd(StrInput);
			return StrOutPut;
		}
		// 返回是否成功，即包含Everything 
		public static bool IsOK(string s)
		{
			return s.Contains("Everything is Ok");
		}
		// 返回是否分卷
		public static bool IsVolumes(string s)
		{
			// 排除RAR单卷
			if (s.Contains("Volumes = 1")) return false;
			// 正常分卷检查
			if (s.Contains("Volumes =")) return true;
			return false;
		}
		// 主进程
		private string Cmd(string StrInput)
		{
			// 启动命令行
			p.Start();
			// 向cmd窗口发送输入信息
			p.StandardInput.WriteLine(StrInput + "&exit");
			p.StandardInput.AutoFlush = true;
			// 等待执行完退出进程
			p.WaitForExit();

			// 接收结果
			string StrOutput = p.StandardOutput.ReadToEnd();

			// 返回输出
			return StrOutput;
		}
	}
	public class RichBoxEdit
	{
		System.Windows.Controls.RichTextBox RichBox;
		Run r = null;
		Paragraph Para = null;
		//para.Inlines.Add(r);
		//richtxtbox.Document.Blocks.Clear();
		//richtxtbox.Document.Blocks.Add(para);
		public RichBoxEdit(System.Windows.Controls.RichTextBox rtbox)
		{
			RichBox = rtbox;
			//r = new Run();
			Para = new Paragraph();
		}

		public void AddText(string s)
		{
			AddText(s, Brushes.DimGray);
		}
		public void AddText(string s, SolidColorBrush BForeground)
		{
			r = new Run();
			r.Text = s;
			r.Foreground = BForeground;

			Para.Inlines.Add(r);
			RichBox.Document.Blocks.Add(Para);
		}

		public void Clear()
		{
			Para.Inlines.Clear();
			RichBox.Document.Blocks.Clear();
		}
		public string GetText()
		{
			TextRange TRange = new TextRange(RichBox.Document.ContentStart, RichBox.Document.ContentEnd);
			return TRange.Text;
		}
		// 保存为文件 ，未测试
		// 详见
		// https://blog.csdn.net/hanwb2010/article/details/17165103

		public void SaveFile(string filename)
		{
			if (string.IsNullOrEmpty(filename))
			{
				throw new ArgumentNullException();
			}
			using (FileStream stream = File.OpenWrite(filename))
			{
				TextRange DTextRange = new TextRange(RichBox.Document.ContentStart, RichBox.Document.ContentEnd);
				string dataFormat = System.Windows.DataFormats.Text;
				string ext = Path.GetExtension(filename);
				if (String.Compare(ext, ".rtf", true) == 0)
				{
					dataFormat = System.Windows.DataFormats.Rtf;
				}
				DTextRange.Save(stream, dataFormat);
			}
		}
	}
	

	public class CompressResultToTxt
	{
		string txt;
		FileStream fs;
		StreamWriter sw;
		public CompressResultToTxt(string TxtPath)
		{
			txt = TxtPath;
			if (!File.Exists(TxtPath))
			{
				File.Create(TxtPath).Close();
			}
			fs= new FileStream(TxtPath, FileMode.Append);
			sw = new StreamWriter(fs);
		}
		public void Write(string filepath,string password = null)
		{
			string t = DateTime.Now.ToString();
			string f = Path.GetFileName(filepath);
			string p = null;
			if (password == null || password == "") p = "-";
			else p = password;
			WriteLine(t + "    文件名称：" + f + "    解压密码：" + p + "\n输出目录：" + filepath+"\n");
		}
		private void WriteLine(string s)
		{
			sw.WriteLine(s);
			sw.Flush();
		}
		public void Close()
		{

			sw.Close();
			fs.Close();
		}
		public static void OpenLog(string txtfile)
		{
			Process.Start("notepad.exe", txtfile);
		}
	}

}
