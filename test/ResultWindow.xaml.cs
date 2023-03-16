using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;


namespace UZIP2
{
	/// <summary>
	/// ResultWindow.xaml 的交互逻辑
	/// </summary>

	
	public partial class ResultWindow : Window
	{
		public RichBoxEdit RichEdit;
		public string FilePath;
		public string OutPath;
		public ResultWindow()
		{
			InitializeComponent();
			this.Topmost = USetting.WindowOnTop;
			FilePath = Path.GetDirectoryName(USetting.FileList[0]) + "\\";
			RichEdit = new RichBoxEdit(BResults);

		}

		private void BClose_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			this.Close();
		}

		private void BClose_MouseEnter(object sender, MouseEventArgs e)
		{
			BClose.Foreground = Brushes.Red;
		}

		private void BClose_MouseLeave(object sender, MouseEventArgs e)
		{
			BClose.Foreground = Brushes.Black;
		}

		private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			if (e.ButtonState == MouseButtonState.Pressed)
			{
				this.DragMove();
			}
		}
		// 用于输出压缩成果的程序，
		public void OutCompressResult(List<string> LS, List<string> LF)
		{
			OutPath = UCmdPathHelp.UCompressPath();
			string g = "-\n";
			string del = USetting.DeleteCompressFinish ? "，原文件已删除\n" : "\n";
			RichEdit.Clear();
			RichEdit.AddText("文件目录 " + FilePath + "\n");
			
			RichEdit.AddText("输出目录 " + OutPath + "\n");
			RichEdit.AddText(g);
			RichEdit.AddText("文件总计 " + (LS.Count) + "个\n");
			RichEdit.AddText(g);
			if (LS.Count > 0) RichEdit.AddText("压缩成功 " + LS.Count + "个  ", Brushes.Green);
			if (LF.Count > 0) RichEdit.AddText("压缩失败 " + LF.Count + "个\n", Brushes.Red);
			else RichEdit.AddText("\n");
			RichEdit.AddText(g);

			if (LS.Count > 0)
			{
				RichEdit.AddText("压缩成功的文件" + del, Brushes.Green);
				// 成功列表输出
				foreach (string f in LS)
				{
					RichEdit.AddText("✔ " + Path.GetFileName(f) + "\n", Brushes.Green);
				}
				RichEdit.AddText(g);
			}
			if (LF.Count > 0)
			{
				RichEdit.AddText("压缩失败的文件\n", Brushes.Red);
				foreach (string f in LF)
				{
					RichEdit.AddText("✖ " + Path.GetFileName(f) + "\n", Brushes.Red);
				}
				RichEdit.AddText(g);
			}
		}
		// 用于输出压缩成果的程序(压为一个)
		public void OutCompressAloneResult(bool isOK)
		{
			OutPath = UCmdPathHelp.UCompressPath();
			string g = "-\n";
			string del = USetting.DeleteCompressFinish ? "，原文件已删除\n" : "\n";
			RichEdit.Clear();
			RichEdit.AddText("文件目录 " + FilePath + "\n");
			RichEdit.AddText("输出目录 " + OutPath + "\n");
			RichEdit.AddText(g);
			if (isOK)
				RichEdit.AddText("所有文件已成功压缩为一个档案\n ", Brushes.Green);
			else
				RichEdit.AddText("压缩失败或可能有错误\n请检查文件是否被其他程序占用\n ", Brushes.Green);
		}

		// 用于输出解压成果的程序，
		public void OutExtractResult(List<string> LS,List<string> LF)
		{
			OutPath = UCmdPathHelp.UExtractPath();
			string g = "-\n";
			string del = USetting.DeleteFinishFile ? "，原文件已删除\n" : "\n";

			RichEdit.Clear();
			RichEdit.AddText("文件目录 " + FilePath + "\n");
			RichEdit.AddText("输出目录 " + OutPath + "\n");
			RichEdit.AddText(g);

			RichEdit.AddText("文件总计 " + ( LS.Count + LF.Count ) + "个\n");
			if (LS.Count > 0) RichEdit.AddText("解压成功 " + LS.Count + "个  ", Brushes.Green);
			if (LF.Count > 0) RichEdit.AddText("解压失败 " + LF.Count + "个\n", Brushes.Red);
			else RichEdit.AddText("\n");



			RichEdit.AddText(g);

			if (LS.Count > 0)
			{
				RichEdit.AddText("解压成功的文件" + del, Brushes.Green);
				// 成功列表输出
				foreach (string f in LS)
				{
					RichEdit.AddText("✔ " + Path.GetFileName(f)  + "\n", Brushes.Green);
				}
				RichEdit.AddText(g);
			}
			if (LF.Count > 0)
			{
				RichEdit.AddText("解压失败的文件\n", Brushes.Red);
				foreach (string f in LF)
				{
					RichEdit.AddText("✖ " + Path.GetFileName(f)  + "\n", Brushes.Red);
				}
				RichEdit.AddText(g);
			}


		}

		private void OpenOutPath_Click(object sender, RoutedEventArgs e)
		{
			Process.Start("explorer.exe", OutPath);
		}

		private void OpenFilePath_Click(object sender, RoutedEventArgs e)
		{
			Process.Start("explorer.exe", FilePath);
		}
	}
}
