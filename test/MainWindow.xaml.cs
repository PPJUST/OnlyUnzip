using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace UZIP2
{
	/// <summary>
	/// MainWindow.xaml 的交互逻辑
	/// </summary>
	public partial class MainWindow : Window
	{
		DebugWindow DBWin = null;
		public MainWindow()
		{
			InitializeComponent();
			WindowPosition();
			ControlInitialize();
		}

		// 窗体初始化Plus
		public void WindowPosition()
		{
			//屏幕尺寸
			double h = SystemParameters.PrimaryScreenHeight;
			double w = SystemParameters.PrimaryScreenWidth;
			double wl = USetting.WindowLeft;
			double wt = USetting.WindowTop;

			if (wl < 0 || wt < 0 || wl > w - 270 || wt > h - 270)
			{
				this.Left = w / 2 - 135;
				this.Top = h / 2 - 135;
			}
			else
			{
				this.Left = wl;
				this.Top = wt;
			}
			this.Topmost = USetting.WindowOnTop;
		}

		// 初始化控件
		public void ControlInitialize()
		{
			//以下为规整窗口，仅供测试时使用方便
			UBoard.Width = 250;
			//this.Width = 270;
			WSet.Visibility = Visibility.Hidden;
			WPassword.Visibility = Visibility.Hidden;

			//初始化控件开始
			switch (USetting.AppMode)
			{
				case (int)AppModes.Auto:BMenuAuto.IsChecked = true;break;
				case (int)AppModes.OnlyCompress: BMenuCompress.IsChecked = true; break;
				case (int)AppModes.OnlyExtract: BMenuExtract.IsChecked = true; break;
			}
			BMenuTipShowHelp(USetting.AppMode);
			BCustomize7z.IsChecked = USetting.Customize7z;
			BCustomize7zPath.Text = USetting.Customize7zPath;
			BTrimSpace.IsChecked = USetting.TrimSpace;
			BUseHotKey.IsChecked = USetting.UseHotKey;
			//热键
			BWindowOnTop.IsChecked = USetting.WindowOnTop;
			BDebugMode.Visibility = USetting.ShowDebug ? Visibility.Visible : Visibility.Hidden;
			BDebugMode.IsChecked = USetting.DebugMode;
			BExtractUnknow.IsChecked = USetting.ExtractUnknow;
			switch (USetting.ExtractOutMode)
			{
				case (int)ExtractPath.File: BExtractOutMode.SelectedIndex = 0; break;
				case (int)ExtractPath.Browse: BExtractOutMode.SelectedIndex = 1; break;
				case (int)ExtractPath.Customize1: BExtractOutMode.SelectedIndex = 3; break;
				case (int)ExtractPath.Customize2: BExtractOutMode.SelectedIndex = 4; break;
				case (int)ExtractPath.Customize3: BExtractOutMode.SelectedIndex = 5; break;
				case (int)ExtractPath.Customize4: BExtractOutMode.SelectedIndex = 6; break;
				case (int)ExtractPath.Customize5: BExtractOutMode.SelectedIndex = 7; break;
				case (int)ExtractPath.Customize6: BExtractOutMode.SelectedIndex = 8; break;
				case (int)ExtractPath.Customize7: BExtractOutMode.SelectedIndex = 9;  break;
				case (int)ExtractPath.Customize8: BExtractOutMode.SelectedIndex = 10; break;
			}
			BCombo03.Content = " " + USetting.CustomizeFolderName1;
			BCombo04.Content = " " + USetting.CustomizeFolderName2;
			BCombo05.Content = " " + USetting.CustomizeFolderName3;
			BCombo06.Content = " " + USetting.CustomizeFolderName4;
			BCombo07.Content = " " + USetting.CustomizeFolderName5;
			BCombo08.Content = " " + USetting.CustomizeFolderName6;
			BCombo09.Content = " " + USetting.CustomizeFolderName7;
			BCombo10.Content = " " + USetting.CustomizeFolderName8;
			
			switch (USetting.ExtractCoverMode)
			{
				case "-aos": BExtractCoverMode.SelectedIndex = 0; break;
				case "-aoa": BExtractCoverMode.SelectedIndex = 1; break;
				case "-aou": BExtractCoverMode.SelectedIndex = 2; break;
				case "-aot": BExtractCoverMode.SelectedIndex = 3; break;
			}
			BDeleteFinishFile.IsChecked = USetting.DeleteFinishFile;
			if (USetting.CreateNewFolder && USetting.CreateNameFolder)
			{
				USetting.CreateNewFolder = false;
				USetting.CreateNameFolder = false;
			}
			BCreateNewFolder.IsChecked = USetting.CreateNewFolder;
			BCreateNameFolder.IsChecked = USetting.CreateNameFolder;

			BResultWindow.IsChecked = USetting.ResultWindow;
			BCustomizeFolderPathName1.Content = USetting.CustomizeFolderName1;
			BCustomizeFolderPathPath1.Text = USetting.CustomizeFolderPath1;
			BCustomizeFolderPathName2.Content = USetting.CustomizeFolderName2;
			BCustomizeFolderPathPath2.Text = USetting.CustomizeFolderPath2;
			BCustomizeFolderPathName3.Content = USetting.CustomizeFolderName3;
			BCustomizeFolderPathPath3.Text = USetting.CustomizeFolderPath3;
			BCustomizeFolderPathName4.Content = USetting.CustomizeFolderName4;
			BCustomizeFolderPathPath4.Text = USetting.CustomizeFolderPath4;
			BCustomizeFolderPathName5.Content = USetting.CustomizeFolderName5;
			BCustomizeFolderPathPath5.Text = USetting.CustomizeFolderPath5;
			BCustomizeFolderPathName6.Content = USetting.CustomizeFolderName6;
			BCustomizeFolderPathPath6.Text = USetting.CustomizeFolderPath6;
			BCustomizeFolderPathName7.Content = USetting.CustomizeFolderName7;
			BCustomizeFolderPathPath7.Text = USetting.CustomizeFolderPath7;
			BCustomizeFolderPathName8.Content = USetting.CustomizeFolderName8;
			BCustomizeFolderPathPath8.Text = USetting.CustomizeFolderPath8;

			// 压缩面板
			BCompressType.SelectedIndex =  USetting.CompressType;
			switch (USetting.CompressLevel)
			{

				case (int)CompressLevels.No: BCompressLevel.SelectedIndex = 0;break;
				case (int)CompressLevels.Fastest: BCompressLevel.SelectedIndex = 1; break;
				case (int)CompressLevels.Fast: BCompressLevel.SelectedIndex = 2; break;
				case (int)CompressLevels.Normal: BCompressLevel.SelectedIndex = 3; break;
				case (int)CompressLevels.Maximum: BCompressLevel.SelectedIndex = 4; break;
				case (int)CompressLevels.Ultra: BCompressLevel.SelectedIndex = 5; break;
			}
			switch (USetting.CompressOutMode)
			{
				case (int)CompressPath.File: BCompressOutMode.SelectedIndex = 0; break;
				case (int)CompressPath.Browse: BCompressOutMode.SelectedIndex = 1; break;
			}

			switch (USetting.PasswordMode)
			{
				case (int)SetPasswords.No: BPasswordMode.SelectedIndex = 0; break;
				case (int)SetPasswords.Random8: BPasswordMode.SelectedIndex = 6; break;
				case (int)SetPasswords.Random16: BPasswordMode.SelectedIndex = 7; break;
				case (int)SetPasswords.Random32: BPasswordMode.SelectedIndex = 8; break;
				case (int)SetPasswords.Customize1: BPasswordMode.SelectedIndex = 2; break;
				case (int)SetPasswords.Customize2: BPasswordMode.SelectedIndex = 3; break;
				case (int)SetPasswords.Customize3: BPasswordMode.SelectedIndex = 4; break;
			}
			BDeleteCompressFinish.IsChecked = USetting.DeleteCompressFinish;
			BCompressAlone.IsChecked = USetting.CompressAlone;
			BHideZipContent.IsChecked = USetting.HideZipContent;
			BCustomizePassword1.Text = USetting.CustomizePassword1;
			BCustomizePassword2.Text = USetting.CustomizePassword2;
			BCustomizePassword3.Text = USetting.CustomizePassword3;

			// 更改背景图图片
			ChangeBackground("n");

			// 处理解压过滤
			BExtractFilter.Text = USetting.ExtractFilter;
			USetting.ExtractFilterArray = UTool.Split(USetting.ExtractFilter);
			// 处理压缩过滤
			BCompressFilter.Text = USetting.CompressFilter;
			USetting.CompressFilterArray = UTool.Split(USetting.CompressFilter);

			// 
			BNameFilter.Text = USetting.NameFilter;
			BNameFilter2.Text = USetting.NameFilter2;
			BNameToPassword.IsChecked = USetting.NameToPassword;
			BPasswordToName.IsChecked = USetting.PasswordToName;

			// 设置密码纸编辑面板为首选面板
			BPWPTab.IsSelected = true;
			// 读取密码
			USetting.PWNote.LoadPasswords();
			USetting.PWPaper.LoadPasswords();
			BPasswordPatse.Content = "密码纸(" + USetting.PWPaper.Count+")";

			// 准备Debug窗口
			if (USetting.DebugMode)
			{
				DBWin = new DebugWindow();
				DBWin.Top = SystemParameters.PrimaryScreenHeight / 2 - 260;
				DBWin.Left = SystemParameters.PrimaryScreenWidth / 2 - 260;
			}
			

			// 显示开屏信息
			TipShow(USetting.UZip);
			//备份密码
			USetting.BackConfigPage();
			USetting.BackConfigNote();

		}

		// 更改背景图片
		private void ChangeBackground(string s)
		{
			switch (s)
			{
				// setting 面板
				case "s": UBackImage.Source = new BitmapImage(new Uri("UBSetting.png", UriKind.Relative)); break;
				// password 面板
				case "p": UBackImage.Source = new BitmapImage(new Uri("UBPassword.png", UriKind.Relative)); break;
				// 正常面板
				case "n":
					switch (USetting.AppMode)
					{
						case (int)AppModes.Auto: UBackImage.Source = new BitmapImage(new Uri("UBAuto.png", UriKind.Relative)); break;
						case (int)AppModes.OnlyCompress: UBackImage.Source = new BitmapImage(new Uri("UBCompress.png", UriKind.Relative)); break;
						case (int)AppModes.OnlyExtract: UBackImage.Source = new BitmapImage(new Uri("UBExtract.png", UriKind.Relative)); break;
					}
					break;
			}
		}

		// 移动窗体
		private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			if (e.ButtonState == MouseButtonState.Pressed)
			{
				this.DragMove();
			}
		}

		// 关闭窗口
		private void WMain_BClose_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			if (USetting.RunState == RunStatus.Normal)
			{
				USetting.WindowLeft = this.Left;
				USetting.WindowTop = this.Top;
				Environment.Exit(0);
			}
		}
		private void WMain_BClose_MouseEnter(object sender, MouseEventArgs e)
		{
			BClose.Foreground = Brushes.Red;
			if (USetting.RunState == RunStatus.Normal) TipShow("「左击」关闭UZip应用\n「右击」最小化程序");
			if (USetting.RunState == RunStatus.EditSetting) TipShow("请先关闭设置面板");
			if (USetting.RunState == RunStatus.EditPassword) TipShow("请先关闭密码管理面板");
		}
		private void WMain_BClose_MouseLeave(object sender, MouseEventArgs e)
		{
			BClose.Foreground = Brushes.Black;
			TipShowEnd();
		}

		// 软件主菜单
		private void UTitle_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			if (USetting.RunState == RunStatus.Normal)
			{
				UMenu.Visibility = Visibility.Visible;
				USetting.RunState = RunStatus.ModeSelect;
				TipWarnToNormal();
				TipShowEnd();
				return;
			}
			if (USetting.RunState == RunStatus.ModeSelect)
			{
				UMenu.Visibility = Visibility.Hidden;
				USetting.RunState = RunStatus.Normal;
				return;
			}
		}
		private void UTitle_MouseEnter(object sender, MouseEventArgs e)
		{
			UTitle.Foreground = Brushes.Green;
			if (USetting.RunState == RunStatus.Normal) TipShow("选择软件的工作模式");
		}
		private void UTitle_MouseLeave(object sender, MouseEventArgs e)
		{
			UTitle.Foreground = Brushes.Black;
			TipShowEnd();
		}

		// 主菜单选项 解压
		private void BMenuExtract_Click(object sender, RoutedEventArgs e)
		{
			UMenu.Visibility = Visibility.Hidden;
			USetting.AppMode = (int)AppModes.OnlyExtract;
			USetting.RunState = RunStatus.Normal;
			ChangeBackground("n");
			TipShowEnd();
		}
		private void BMenuExtract_MouseEnter(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp((int)AppModes.OnlyExtract);
		}
		private void BMenuExtract_MouseLeave(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp(USetting.AppMode);
		}
		
		// 主菜单选项 压缩
		private void BMenuCompress_Click(object sender, RoutedEventArgs e)
		{
			UMenu.Visibility = Visibility.Hidden;
			USetting.AppMode = (int)AppModes.OnlyCompress;
			USetting.RunState = RunStatus.Normal;
			ChangeBackground("n");
			TipShowEnd();
		}
		private void BMenuCompress_MouseEnter(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp((int)AppModes.OnlyCompress);
		}
		private void BMenuCompress_MouseLeave(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp(USetting.AppMode);
		}

		// 主菜单选项 自动
		private void BMenuAuto_Click(object sender, RoutedEventArgs e)
		{
			UMenu.Visibility = Visibility.Hidden;
			USetting.AppMode = (int)AppModes.Auto;
			USetting.RunState = RunStatus.Normal;
			ChangeBackground("n");
			TipShowEnd();
		}
		private void BMenuAuto_MouseEnter(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp((int)AppModes.Auto);
		}
		private void BMenuAuto_MouseLeave(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp(USetting.AppMode);
		}

		// 主菜单选项 密码收集器
		private void BMenuCollection_Click(object sender, RoutedEventArgs e)
		{

			UMenu.Visibility = Visibility.Hidden;
			WMain.Visibility = Visibility.Hidden;
			WMini.Visibility = Visibility.Visible;
			USetting.RunState = RunStatus.MiniMode;
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(250, 60, TimeSpan.FromSeconds(.2)));
			UBoard.BeginAnimation(Border.HeightProperty, new DoubleAnimation(250, 60, TimeSpan.FromSeconds(.2)));
			BMiniPatse.Content = USetting.PWPaper.Count.ToString();
			BMiniPatse.ToolTip = "左击贴入密码，右击显示菜单\n最后贴入的密码：\n" + USetting.PWPaper.GetLastPassword();
			TipShowEnd();
			this.Topmost = true;
		}
		private void BMenuCollection_MouseEnter(object sender, MouseEventArgs e)
		{
			BUMenuTip.Text = ULanguage.MenuCollectionTip;
		}
		private void BMenuCollection_MouseLeave(object sender, MouseEventArgs e)
		{
			BMenuTipShowHelp(USetting.AppMode);
		}

		// 菜单的提示信息修正
		private void BMenuTipShowHelp(int m)
		{
			switch (m)
			{
				case (int)AppModes.Auto: BUMenuTip.Text = ULanguage.MenuAutoTip; break;
				case (int)AppModes.OnlyCompress: BUMenuTip.Text = ULanguage.MenuCompressTip; break;
				case (int)AppModes.OnlyExtract: BUMenuTip.Text = ULanguage.MenuExtractTip; break;
			}
		}


		// 密码收集器 打开菜单
		private void BMiniPatse_MouseRightButtonDown(object sender, MouseButtonEventArgs e)
		{
			USetting.RunState = RunStatus.MiniModeR;
			WMini.Visibility = Visibility.Hidden;
			WMiniR.Visibility = Visibility.Visible;
			BMiniDel.ToolTip = "删除最后贴入的密码:\n" + USetting.PWPaper.GetLastPassword();
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(60, 120, TimeSpan.FromSeconds(.1)));
			UBoard.BeginAnimation(Border.HeightProperty, new DoubleAnimation(60, 120, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.WidthProperty, new DoubleAnimation(60, 120, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.HeightProperty, new DoubleAnimation(60, 120, TimeSpan.FromSeconds(.1)));
		}

		// 密码收集器 取消
		private void BMiniCancel_Click(object sender, RoutedEventArgs e)
		{
			USetting.RunState = RunStatus.MiniMode;
			WMini.Visibility = Visibility.Visible;
			WMiniR.Visibility = Visibility.Hidden;
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			UBoard.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
		}

		// 密码收集器 贴入
		private void BMiniPatse_Click(object sender, RoutedEventArgs e)
		{
			PatsePassword();
		}

		// 密码收集器 删除
		private void BMiniDel_Click(object sender, RoutedEventArgs e)
		{
			string DelPW = USetting.PWPaper.DeleteLastPassword();
			BMiniPatse.Content = USetting.PWPaper.Count.ToString();
			BMiniPatse.Foreground = Brushes.DimGray;
			BMiniPatse.ToolTip = "左击贴入密码，右击显示菜单\n最后贴入的密码：\n" + USetting.PWPaper.GetLastPassword();
			USetting.RunState = RunStatus.MiniMode;
			USetting.PaperChange = true;
			WMini.Visibility = Visibility.Visible;
			WMiniR.Visibility = Visibility.Hidden;
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			UBoard.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));
			WMiniR.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 60, TimeSpan.FromSeconds(.1)));

		}

		// 密码收集器 退出
		private void BMiniReturn_Click(object sender, RoutedEventArgs e)
		{
			WMain.Visibility = Visibility.Visible;
			WMiniR.Visibility = Visibility.Hidden;
			USetting.RunState = RunStatus.Normal;
			BMiniPatse.Foreground = Brushes.DimGray;
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 250, TimeSpan.FromSeconds(.2)));
			UBoard.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 250, TimeSpan.FromSeconds(.2)));
			WMain.BeginAnimation(Border.WidthProperty, new DoubleAnimation(120, 250, TimeSpan.FromSeconds(.2)));
			WMain.BeginAnimation(Border.HeightProperty, new DoubleAnimation(120, 250, TimeSpan.FromSeconds(.2)));
			this.Topmost = USetting.WindowOnTop;
			BPasswordPatse.Content = "密码纸(" + USetting.PWPaper.Count + ")";
			TipShowEnd();
		}

		// 贴入密码
		public void PatsePassword()
		{
			string str = null;

			// 正常模式 贴入
			if (USetting.RunState == RunStatus.Normal)
			{
				str = GetClipboardHelp();
				if (str == null) return;
				str = USetting.PWPaper.AddPassword(str);
				if (str != null)
				{
					BPasswordPatse.Content = "密码纸(" + USetting.PWPaper.Count + ")";
					TipShow(str + "\n已写入密码纸",TipMods.WarmGray);
				}
				else
				{
					TipShow("密码纸已经满了，写不下更多密码了！", TipMods.WarnRed);
				}
			}
			if (USetting.RunState == RunStatus.MiniMode)
			{
				str = GetClipboardHelp();
				if (str == null) return;
				str = USetting.PWPaper.AddPassword(str);
				if (str != null)
				{
					BMiniPatse.Content = USetting.PWPaper.Count.ToString();
					BMiniPatse.ToolTip = "左击贴入密码，右击显示菜单\n最后贴入的密码：\n" + USetting.PWPaper.GetLastPassword();
				}
				else
				{
					BMiniPatse.Foreground = Brushes.Red;
				}
			}
			// 密码纸贴入标识开启，下次解压/压缩时会保存密码。
			USetting.PaperChange = true;
		}
		// 密码面板
		private void BPasswordPatse_Click(object sender, RoutedEventArgs e)
		{
			PatsePassword();

			// 工作中贴入，不会显示提示信息
			/*
			int PaperAndTempCount = 0;
			if (USetting.RunState == RunStatus.ExtractFile || 
				USetting.RunState == RunStatus.CompressFile ||
				USetting.RunState == RunStatus.AutoFile
				)
			{
				str = GetClipboardHelp();
				if (str == null) return;
				PaperAndTempCount = USetting.PWPaper.Count + USetting.PWTemp.Count;
				if (PaperAndTempCount >= Password.PWMAX)
				{
					TipShow("密码纸已经满了,写不下更多密码了！", TipMods.WarnRed);
				}
				else
				{
					BPasswordPatse.Content = "密码纸(" + PaperAndTempCount + ")";
					USetting.PWTemp.Add(str);
				}
				
			}
			*/
		}
		private void BPasswordPatse_MouseRightButtonDown(object sender, MouseButtonEventArgs e)
		{
			if (USetting.RunState == RunStatus.Normal)
			{
				WPassword.Visibility = Visibility.Visible;
				UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(250, 500, TimeSpan.FromSeconds(.2)));
				WPassword.BeginAnimation(Border.WidthProperty, new DoubleAnimation(0, 250, TimeSpan.FromSeconds(.2)));
				USetting.RunState = RunStatus.EditPassword;

				//填充密码到文本框
				BPWPageEditText.Text = Password.ListToString(USetting.PWPaper.Passwords);
				BPWNoteEditText.Text = Password.ListToString(USetting.PWNote.Passwords);
				BPWRecycleEditText.Text = Password.ListToString(USetting.PWRecycle);
				ChangeBackground("p");
				TipWarnToNormal();
				TipShowEnd();
				return;
			}
		}
		private void BPasswordPatse_MouseEnter(object sender, MouseEventArgs e)
		{
			
			if (USetting.RunState == RunStatus.Normal) TipShow("「左击」贴入密码\n「右击」管理密码");
			if (USetting.RunState == RunStatus.EditSetting) TipShow("请先关闭设置面板");
			if (USetting.RunState == RunStatus.EditPassword) TipShow("请先关闭密码管理面板");
		}



		// 设置面板
		private void BSetting_Click(object sender, RoutedEventArgs e)
		{
			if (USetting.RunState == RunStatus.EditSetting)
			{
				// 检查是否使用自定义输出目录，如自定义目录路径不存在，提示
				if (USetting.ExtractOutMode != (int)ExtractPath.File && USetting.ExtractOutMode != (int)ExtractPath.Browse)
				{
					string s = null;
					switch (USetting.ExtractOutMode)
					{
						case (int)ExtractPath.Customize1: s = USetting.CustomizeFolderPath1; break;
						case (int)ExtractPath.Customize2: s = USetting.CustomizeFolderPath2; break;
						case (int)ExtractPath.Customize3: s = USetting.CustomizeFolderPath3; break;
						case (int)ExtractPath.Customize4: s = USetting.CustomizeFolderPath4; break;
						case (int)ExtractPath.Customize5: s = USetting.CustomizeFolderPath5; break;
						case (int)ExtractPath.Customize6: s = USetting.CustomizeFolderPath6; break;
						case (int)ExtractPath.Customize7: s = USetting.CustomizeFolderPath7; break;
						case (int)ExtractPath.Customize8: s = USetting.CustomizeFolderPath8; break;
					}
					if (!UTool.CheckPath(s))
					{
						TipShow("您选择的 \"解压到\" 目录不可用", TipMods.WarnRed);
						return;
					}
				}
				BSetting.Content = "设置";
				WSet.Visibility = Visibility.Hidden;
				UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(500, 250, TimeSpan.FromSeconds(.2)));
				WSet.BeginAnimation(Border.WidthProperty, new DoubleAnimation(250, 0, TimeSpan.FromSeconds(.2)));
				USetting.RunState = RunStatus.Normal;

				// 文本框提示的审查
				BCustomize7zPath_Check(true);
				for (int i = 1; i <= 8; i++)
				{
					BCustomizeFolderPath_Check(i, true);
				}

				// 保存自定义的密码字符串
				USetting.CustomizePassword1 = BCustomizePassword1.Text;
				USetting.CustomizePassword2 = BCustomizePassword2.Text;
				USetting.CustomizePassword3 = BCustomizePassword3.Text;

				// 保存并处理过滤
				USetting.ExtractFilter = BExtractFilter.Text;
				USetting.ExtractFilterArray = UTool.Split(USetting.ExtractFilter);
				USetting.CompressFilter = BCompressFilter.Text;
				USetting.CompressFilterArray = UTool.Split(USetting.CompressFilter);
				ChangeBackground("n");
				return;
			}
			if (USetting.RunState == RunStatus.Normal)
			{
				BSetting.Content = "返回";
				WSet.Visibility = Visibility.Visible;
				UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(250, 500, TimeSpan.FromSeconds(.2)));
				WSet.BeginAnimation(Border.WidthProperty, new DoubleAnimation(0, 250, TimeSpan.FromSeconds(.2)));
				ChangeBackground("s");
				USetting.RunState = RunStatus.EditSetting;
				TipWarnToNormal();
				TipShowEnd();
				return;
			}
		}
		private void BSetting_MouseEnter(object sender, MouseEventArgs e)
		{
			if (USetting.RunState == RunStatus.Normal) TipShow("设置应用参数");
			if (USetting.RunState == RunStatus.EditSetting) TipShow("关闭设置面板");
			if (USetting.RunState == RunStatus.EditPassword) TipShow("请先关闭密码管理面板");

		}

		// 设置面板 重命名自定义文件夹名
		private int BenameBoxIn = 0;// 记录正在编辑的标签编号
		private Label BenameBoxInLabel = null;// 记录正在编辑的标签
		// 失去焦点，保存数据
		private void BRenameBox_LostFocus(object sender, RoutedEventArgs e)
		{
			RenameCustomizeFoderNameHelpEnd();
		}
		// 按下回车，保存数据
		private void BRenameBox_KeyDown(object sender, KeyEventArgs e)
		{
			if (e.Key == Key.Enter)
			{
				RenameCustomizeFoderNameHelpEnd();
			}
		}
		// 获取标签，及编号，存入中转数据。读取原有名称，打开编辑框，获取焦点。
		private void RenameCustomizeFoderNameHelp(Label l, int n)
		{
			if (BenameBoxIn != 0) return;
			BenameBoxIn = n;
			BenameBoxInLabel = l;
			Thickness margin = new Thickness();
			margin.Left = l.Margin.Left + 5;
			margin.Top = l.Margin.Top + 2;
			BRenameBox.Margin = margin;

			switch (BenameBoxIn)
			{
				case 1: BRenameBox.Text = USetting.CustomizeFolderName1; break;
				case 2: BRenameBox.Text = USetting.CustomizeFolderName2; break;
				case 3: BRenameBox.Text = USetting.CustomizeFolderName3; break;
				case 4: BRenameBox.Text = USetting.CustomizeFolderName4; break;
				case 5: BRenameBox.Text = USetting.CustomizeFolderName5; break;
				case 6: BRenameBox.Text = USetting.CustomizeFolderName6; break;
				case 7: BRenameBox.Text = USetting.CustomizeFolderName7; break;
				case 8: BRenameBox.Text = USetting.CustomizeFolderName8; break;
			}
			BRenameBox.Visibility = Visibility.Visible;
			BRenameBox.Focus();

		}
		// 中转数据中获取标签及编号。检查输入是否为空，储存新名称，同步到标签，关闭编辑框，转移焦点焦点。
		private void RenameCustomizeFoderNameHelpEnd()
		{
			string s = (BRenameBox.Text).Trim();
			if (s != "")
			{
				switch (BenameBoxIn)
				{
					case 1: USetting.CustomizeFolderName1 = s; BCombo03.Content = " " + USetting.CustomizeFolderName1; break;
					case 2: USetting.CustomizeFolderName2 = s; BCombo04.Content = " " + USetting.CustomizeFolderName2; break;
					case 3: USetting.CustomizeFolderName3 = s; BCombo05.Content = " " + USetting.CustomizeFolderName3; break;
					case 4: USetting.CustomizeFolderName4 = s; BCombo06.Content = " " + USetting.CustomizeFolderName4; break;
					case 5: USetting.CustomizeFolderName5 = s; BCombo07.Content = " " + USetting.CustomizeFolderName5; break;
					case 6: USetting.CustomizeFolderName6 = s; BCombo08.Content = " " + USetting.CustomizeFolderName6; break;
					case 7: USetting.CustomizeFolderName7 = s; BCombo09.Content = " " + USetting.CustomizeFolderName7; break;
					case 8: USetting.CustomizeFolderName8 = s; BCombo10.Content = " " + USetting.CustomizeFolderName8; break;
				}
				BenameBoxInLabel.Content = BRenameBox.Text;
			}

			BRenameBox.Visibility = Visibility.Hidden;
			BTabExtract.Focus();
			BenameBoxIn = 0;
		}


		private void BCustomizeFolderPathName1_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 1);
		}

		private void BCustomizeFolderPathName2_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 2);
		}

		private void BCustomizeFolderPathName3_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 3);
		}

		private void BCustomizeFolderPathName4_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 4);
		}

		private void BCustomizeFolderPathName5_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 5);
		}

		private void BCustomizeFolderPathName6_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 6);
		}

		private void BCustomizeFolderPathName7_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 7);
		}

		private void BCustomizeFolderPathName8_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
		{
			RenameCustomizeFoderNameHelp((Label)sender, 8);
		}

		private void BExtractOutMode_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			switch (BExtractOutMode.SelectedIndex)
			{
				case 0: USetting.ExtractOutMode = (int)ExtractPath.File; break;
				case 1: USetting.ExtractOutMode = (int)ExtractPath.Browse; break;
				case 3: USetting.ExtractOutMode = (int)ExtractPath.Customize1; break;
				case 4: USetting.ExtractOutMode = (int)ExtractPath.Customize2; break;
				case 5: USetting.ExtractOutMode = (int)ExtractPath.Customize3; break;
				case 6: USetting.ExtractOutMode = (int)ExtractPath.Customize4; break;
				case 7: USetting.ExtractOutMode = (int)ExtractPath.Customize5; break;
				case 8: USetting.ExtractOutMode = (int)ExtractPath.Customize6; break;
				case 9: USetting.ExtractOutMode = (int)ExtractPath.Customize7; break;
				case 10: USetting.ExtractOutMode = (int)ExtractPath.Customize8; break;
			}

		}
		private void Label_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("文件的解压位置");
		}

		private void BExtractCoverMode_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			switch (BExtractCoverMode.SelectedIndex)
			{
				case 0: USetting.ExtractCoverMode = CoverMode.Pass; break;
				case 1: USetting.ExtractCoverMode = CoverMode.Cover; break;
				case 2: USetting.ExtractCoverMode = CoverMode.RenameNew; break;
				case 3: USetting.ExtractCoverMode = CoverMode.RenameOld; break;
			}
		}
		private void Label_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("同名文件处理方式");
		}

		private void BDeleteFinishFile_Click(object sender, RoutedEventArgs e)
		{
			USetting.DeleteFinishFile = (bool)BDeleteFinishFile.IsChecked;
		}

		private void BCreateNewFolder_Click(object sender, RoutedEventArgs e)
		{
			USetting.CreateNewFolder = (bool)BCreateNewFolder.IsChecked;
			if (USetting.CreateNewFolder) 
			{
				BCreateNameFolder.IsChecked = false;
				USetting.CreateNameFolder = false;
			}
			
		}

		private void BResultWindow_Click(object sender, RoutedEventArgs e)
		{
			USetting.ResultWindow = (bool)BResultWindow.IsChecked;
		}

		private void BCustomize7z_Click(object sender, RoutedEventArgs e)
		{
			USetting.Customize7z = (bool)BCustomize7z.IsChecked;
		}
		private void BCustomize7z_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用您安装的7Zip程序\n默认提供：\n7-Zip 19.00 32bit");
		}

		private void BTrimSpace_Click(object sender, RoutedEventArgs e)
		{
			USetting.TrimSpace = (bool)BTrimSpace.IsChecked;
		}
		private void BTrimSpace_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("点击贴入密码纸时\n密码前后的空格将被去除");
		}

		private void BUseHotKey_Click(object sender, RoutedEventArgs e)
		{
			USetting.UseHotKey = (bool)BUseHotKey.IsChecked;
			if (USetting.UseHotKey) SetPasteHotKey();
			else
			{
				UnSetPastHotKey();
			}
		}
		private void BUseHotKey_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用热键贴入密码。\n注意，会覆盖剪切板的内容！");
		}

		private void BSetHotKey_Click(object sender, RoutedEventArgs e)
		{
			Window2 KBWin = new Window2();
			KBWin.Top = this.Top;
			KBWin.Left = this.Left + 7;
			KBWin.ShowDialog();
			if (KBWin.KNormal != 0)
			{
				USetting.HotKeyKey = KBWin.KNormal;
				USetting.HotKeyAlt = KBWin.KAlt;
				USetting.HotKeyShift = KBWin.KShift;
				USetting.HotKeyCtrl = KBWin.KCtrl;
			
				SetPasteHotKey();
			}

		}

		private void BExtractUnknow_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("仅解压模式时\n尝试解压未知格式的文件");
		}
		private void BExtractUnknow_Click(object sender, RoutedEventArgs e)
		{
			USetting.ExtractUnknow = (bool)BExtractUnknow.IsChecked;
		}

		private void BSetHotKey_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("设置热键");
		}

		private void BNameToPassword_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用标识符从文件名中提取密码\n分卷压缩文件无效\n请在右侧输入密码标识符");
		}

		private void BNameFilter_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("例:以#为标识符\n文件名#密码.zip\n 文件名#密码#(1).zip");
		}
		private void BNameFilter2_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("密码标识符，用以分割密码\n省略则为空格\n例如:文件名 密码.zip");
		}
		private void BPasswordToName_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("将密码写入到文件名\n将使用右侧标识符");
		}
		private void BNameToPassword_Click(object sender, RoutedEventArgs e)
		{
			USetting.NameToPassword = (bool)BNameToPassword.IsChecked;
		}

		private void BPasswordToName_Click(object sender, RoutedEventArgs e)
		{
			USetting.PasswordToName = (bool)BPasswordToName.IsChecked;
		}
		private void BNameFilter_LostFocus(object sender, RoutedEventArgs e)
		{
			USetting.NameFilter = BNameFilter.Text;
		}
		private void BNameFilter2_LostFocus(object sender, RoutedEventArgs e)
		{
			USetting.NameFilter2 = BNameFilter2.Text;
		}

		private void BWindowOnTop_Click(object sender, RoutedEventArgs e)
		{
			USetting.WindowOnTop = (bool)BWindowOnTop.IsChecked;
			this.Topmost = USetting.WindowOnTop;
		}
		private void BWindowOnTop_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("UZip始终置其他窗口之上");
		}

		private void BDebugMode_Click(object sender, RoutedEventArgs e)
		{
			USetting.DebugMode = (bool)BDebugMode.IsChecked;
			if (USetting.DebugMode)
			{
				if (USetting.DebugMode)
				{
					DBWin = new DebugWindow();
					DBWin.Top = SystemParameters.PrimaryScreenHeight / 2 - 260;
					DBWin.Left = SystemParameters.PrimaryScreenWidth / 2 - 260;
				}
			}
		}
		private void BDebugMode_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("传说中的Debug模式\n你居然找到了！");
		}

		private void BCustomize7zPath_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			var openFileDialog = new Microsoft.Win32.OpenFileDialog();
			openFileDialog.Title = "请选择您安装的7z.exe文件";
			openFileDialog.Filter = "7-Zip程序|7z.exe|应用程序 (*.exe)|*.exe|所有文件 (*.*)|*.*";
			var result = openFileDialog.ShowDialog();
			if (result == true)
			{
				BCustomize7zPath.Text = openFileDialog.FileName;
			}
		}
		private void BCustomize7zPath_MouseEnter(object sender, MouseEventArgs e)
		{

			if (BCustomize7zPath.Text == "") BCustomize7zPath.ToolTip = null;
			else BCustomize7zPath.ToolTip = BCustomize7zPath.Text;
			TipShow("选择您的7z.exe文件\n可以在7Zip安装目录寻找");
		}

		private void BCustomizeFolderPathPath1_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath2_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath3_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath4_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath5_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath6_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath7_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}

		private void BCustomizeFolderPathPath8_MouseDoubleClick(object sender, MouseButtonEventArgs e)
		{
			SelectFolder((TextBox)sender);
		}


		private void BCustomizeFolderPathName1_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath1.Text == "") BCustomizeFolderPathPath1.ToolTip = null;
			else BCustomizeFolderPathPath1.ToolTip = BCustomizeFolderPathPath1.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName2_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath2.Text == "") BCustomizeFolderPathPath2.ToolTip = null;
			else BCustomizeFolderPathPath2.ToolTip = BCustomizeFolderPathPath2.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName3_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath3.Text == "") BCustomizeFolderPathPath3.ToolTip = null;
			else BCustomizeFolderPathPath3.ToolTip = BCustomizeFolderPathPath3.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName4_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath4.Text == "") BCustomizeFolderPathPath4.ToolTip = null;
			else BCustomizeFolderPathPath4.ToolTip = BCustomizeFolderPathPath4.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName5_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath5.Text == "") BCustomizeFolderPathPath5.ToolTip = null;
			else BCustomizeFolderPathPath5.ToolTip = BCustomizeFolderPathPath5.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName6_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath6.Text == "") BCustomizeFolderPathPath6.ToolTip = null;
			else BCustomizeFolderPathPath6.ToolTip = BCustomizeFolderPathPath6.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName7_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath7.Text == "") BCustomizeFolderPathPath7.ToolTip = null;
			else BCustomizeFolderPathPath7.ToolTip = BCustomizeFolderPathPath7.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}

		private void BCustomizeFolderPathName8_MouseEnter(object sender, MouseEventArgs e)
		{
			if (BCustomizeFolderPathPath8.Text == "") BCustomizeFolderPathPath8.ToolTip = null;
			else BCustomizeFolderPathPath8.ToolTip = BCustomizeFolderPathPath8.Text;
			TipShow("双击选择 或 输入粘贴\n不存在的目录将被创建");
		}


		// 所有按钮的退出事件，恢复文本
		private void B_MouseLeave(object sender, MouseEventArgs e)
		{
			TipShowEnd();
		}

		// 选择目录
		private void SelectFolder(TextBox tb)
		{
			System.Windows.Forms.FolderBrowserDialog openFileDialog = new System.Windows.Forms.FolderBrowserDialog();  //选择文件夹
			openFileDialog.Description = "选择一个文件夹";
			if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK) //注意，此处一定要手动引入System.Window.Forms空间，否则你如果使用默认的DialogResult会发现没有OK属性
			{
				tb.Text = openFileDialog.SelectedPath + "\\";
			}
		}



		// 警告模式级别，0为最低，2最高，点击tip可归零，信息警告级低的提示 不能覆盖 警告级高的提示
		private int TipWarn = 0;
		// 警告模式级别归零
		public void TipWarnToNormal()
		{
			TipWarn = (int)TipMods.TipNormal;
		}
		// 根据参数，设置Tipss文本和颜色
		public void TipShow(string s,TipMods t = TipMods.TipNormal)
		{

			// 比较提示优先级，优先级低则返回
			if (TipWarn>(int)t) return;
			
			switch (t)
			{
				case TipMods.TipNormal: BTip.Foreground= Brushes.Gray; BTip.Text = s ; break;
				case TipMods.WarmGray:BTip.Foreground = Brushes.Gray;BTip.Text = s ; TipWarn = (int)TipMods.WarmGray; ; break;
				case TipMods.WarnGreen: BTip.Foreground = Brushes.Green; BTip.Text = s + "\n「确定」"; TipWarn = (int) TipMods.WarnGreen; break;
				case TipMods.WarnRed: BTip.Foreground = Brushes.Red; BTip.Text = s + "\n「确定」"; TipWarn = (int)TipMods.WarnRed; break;
				case TipMods.FixGray: BTip.Foreground = Brushes.Gray; BTip.Text = s; TipWarn = (int)TipMods.FixGray; break;

			}
			
		}
		// 用于恢复Tips文本
		public void TipShowEnd()
		{
			if (TipWarn!= (int)TipMods.TipNormal) return;
			switch (USetting.RunState)
			{
				case RunStatus.Normal:
					switch (USetting.AppMode)
					{
						case (int)AppModes.Auto: TipShow("「自动模式」\n拖拽文件自动压缩/解压", TipMods.TipNormal); break;
						case (int)AppModes.OnlyExtract: TipShow("「仅解压」\n拖拽压缩档案开始解压", TipMods.TipNormal); break;
						case (int)AppModes.OnlyCompress: TipShow("「仅压缩」\n拖拽文件/目录开始压缩", TipMods.TipNormal); break;
					}
					break;
					
				case RunStatus.EditSetting: TipShow("设置应用参数", TipMods.TipNormal); break;
				case RunStatus.EditPassword: TipShow("管理所有密码", TipMods.TipNormal); break;

			}
		}
		// 点击提示文本，退出提示模式
		private void BTip_MouseDown(object sender, MouseButtonEventArgs e)
		{
			//MessageBox.Show(USetting.RunState.ToString());
			if (USetting.RunState == RunStatus.ExtractFile)
			{
				
				YesNo ynWin = new YesNo();
				ynWin.WindowTips = "请确定是否中断解压";
				ynWin.Top = this.Top+75;
				ynWin.Left = this.Left+15;
				ynWin.ShowDialog();
				if (USetting.RunState == RunStatus.ExtractFile)
				{
					USetting.UCancel = ynWin.IsYes;
					UMessageTipCancelUpdata();
				}
				return;
			}

			if (USetting.RunState == RunStatus.CompressFile)
			{
				
				YesNo ynWin = new YesNo();
				ynWin.WindowTips = "请确定是否中断压缩";
				ynWin.Top = this.Top + 75;
				ynWin.Left = this.Left+15;
				ynWin.ShowDialog();
				if (USetting.RunState == RunStatus.CompressFile)
				{
					USetting.UCancel = ynWin.IsYes;
					UMessageTipCancelUpdata();
				}
				
				return;
			}
			TipWarnToNormal();
			TipShowEnd();
		}


		private void BDeleteFinishFile_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("解压成功后删除原文件\n解压失败不会有任何操作");
		}

		private void BCreateNewFolder_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("压缩档案内有多个文件\n且没有根文件夹时\n创建新文件夹容纳所有文件");
		}

		private void BResultWindow_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用独立窗口显示结果");
		}

		private void BFilter_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("不解压文件名包含以下关键字的文件\n不使用务必留空");
		}
		private void BExtractFilter_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用英文分号分隔关键词\n例: *.url;*.htm;*广告*");
		}




		// 获取剪切板内容
		private string GetClipboardHelp()
		{
			//从剪切板获取字符串
			string s = Clipboard.GetText();
			if (s == "")
			{
				TipShow("剪切板内没有密码可以贴入"); return null;
			}
			if (USetting.TrimSpace) s = s.Trim();
			s = s.Replace("\n", "").Replace("\t", "").Replace("\r", "");
			return s;
		}

		// 7z路径
		private void BCustomize7zPath_LostFocus(object sender, RoutedEventArgs e)
		{

			if (BCustomize7zPath.Text == "" || !File.Exists(BCustomize7zPath.Text))
			{
				BCustomize7zPath.BorderBrush = Brushes.Red;
				TipShow("7Z程序路径有误不会被保存", TipMods.WarnRed);
			}
			else
			{
				BCustomize7zPath.BorderBrush = Brushes.Gray;
			}

		}
		private void BCustomize7zPath_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomize7zPath_Check();
		}
		// 检查7z可用性
		private void BCustomize7zPath_Check(bool closeset = false)
		{
			string p = BCustomize7zPath.Text;
			bool filecheck = !(p == "" || p.Length < 7 || p.Substring(p.Length - 6) != "7z.exe" || !File.Exists(p));
			if (closeset)
			{
				if (!filecheck)
				{
					BCustomize7zPath.Text = null;
					USetting.Customize7zPath = null;
				}
				BCustomize7zPath.BorderBrush = Brushes.Gray;
				TipWarn = (int)TipMods.TipNormal;
				TipShowEnd();
			}
			else
			{
				if (filecheck)
				{
					USetting.Customize7zPath = p;
					BCustomize7zPath.BorderBrush = Brushes.Gray;
					TipWarn = (int)TipMods.TipNormal;
					TipShowEnd();
				}
				else
				{
					BCustomize7zPath.BorderBrush = Brushes.Red;
					TipShow("7Z路径有误，不会被保存", TipMods.WarnRed);
				}
			}

		}
		// 检查目录可用性
		private void BCustomizeFolderPath_Check(int s,bool closeset = false)
		{
			TextBox t = null; 
			switch (s)
			{
				case 1: t = BCustomizeFolderPathPath1; break;
				case 2: t = BCustomizeFolderPathPath2; break;
				case 3: t = BCustomizeFolderPathPath3; break;
				case 4: t = BCustomizeFolderPathPath4; break;
				case 5: t = BCustomizeFolderPathPath5; break;
				case 6: t = BCustomizeFolderPathPath6; break;
				case 7: t = BCustomizeFolderPathPath7; break;
				case 8: t = BCustomizeFolderPathPath8; break;
			}

			string p = t.Text;
			bool pathcheck = UTool.CheckPath(p);
			if (closeset)
			{
				if (!pathcheck)
				{
					t.Text = null;
					switch (s)
					{
						case 1: USetting.CustomizeFolderPath1 = null; break;
						case 2: USetting.CustomizeFolderPath2 = null; break;
						case 3: USetting.CustomizeFolderPath3 = null; break;
						case 4: USetting.CustomizeFolderPath4 = null; break;
						case 5: USetting.CustomizeFolderPath5 = null; break;
						case 6: USetting.CustomizeFolderPath6 = null; break;
						case 7: USetting.CustomizeFolderPath7 = null; break;
						case 8: USetting.CustomizeFolderPath8 = null; break;
					}
				}
				t.BorderBrush = Brushes.Gray;
				TipWarn = (int)TipMods.TipNormal;
				TipShowEnd();
			}
			else
			{
				if (pathcheck)
				{
					
					switch (s)
					{
						case 1: USetting.CustomizeFolderPath1 = UTool.CompletionPath(p); break;
						case 2: USetting.CustomizeFolderPath2 = UTool.CompletionPath(p); break;
						case 3: USetting.CustomizeFolderPath3 = UTool.CompletionPath(p); break;
						case 4: USetting.CustomizeFolderPath4 = UTool.CompletionPath(p); break;
						case 5: USetting.CustomizeFolderPath5 = UTool.CompletionPath(p); break;
						case 6: USetting.CustomizeFolderPath6 = UTool.CompletionPath(p); break;
						case 7: USetting.CustomizeFolderPath7 = UTool.CompletionPath(p); break;
						case 8: USetting.CustomizeFolderPath8 = UTool.CompletionPath(p); break;
					}
					t.BorderBrush = Brushes.Gray;
					TipWarn = (int)TipMods.TipNormal;
					TipShowEnd();
				}
				else
				{
					t.BorderBrush = Brushes.Red;
					TipShow("非可用目录，不会被保存", TipMods.WarnRed);
				}
			}
		}

		private void BCustomizeFolderPathPath1_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(1, false);
		}


		private void BCustomizeFolderPathPath2_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(2, false);
		}
		private void BCustomizeFolderPathPath3_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(3, false);
		}
		private void BCustomizeFolderPathPath4_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(4, false);
		}
		private void BCustomizeFolderPathPath5_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(5, false);
		}
		private void BCustomizeFolderPathPath6_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(6, false);
		}
		private void BCustomizeFolderPathPath7_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(7, false);
		}
		private void BCustomizeFolderPathPath8_TextChanged(object sender, TextChangedEventArgs e)
		{
			BCustomizeFolderPath_Check(8, false);
		}

		private void BRenameBox_MouseMove(object sender, MouseEventArgs e)
		{
			TipShow("左击其他位置或回车确定输入");
		}
		private void BCustomizeFolderPathName1_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置1\n右击重命名标签");
		}
		private void BCustomizeFolderPathName2_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置2\n右击重命名标签");
		}
		private void BCustomizeFolderPathName3_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置3\n右击重命名标签");
		}
		private void BCustomizeFolderPathName4_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置4\n右击重命名标签");
		}
		private void BCustomizeFolderPathName5_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置5\n右击重命名标签");
		}
		private void BCustomizeFolderPathName6_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置6\n右击重命名标签");
		}
		private void BCustomizeFolderPathName7_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置7\n右击重命名标签");
		}
		private void BCustomizeFolderPathName8_MouseEnter_1(object sender, MouseEventArgs e)
		{
			TipShow("自定义位置8\n右击重命名标签");
		}

		private void BSetPWOk_Click(object sender, RoutedEventArgs e)
		{
			// 关闭密码管理窗口
			BSetPWCloseHelp();
			// 备份密码文件
			USetting.BackConfigPage();
			USetting.BackConfigNote();
			// 清空密码库并储存新密码，注意 超量的密码将被抛弃
			USetting.PWPaper.ClearPassword();
			USetting.PWPaper.AddPassword(Password.StringToList(BPWPageEditText.Text));
			// 修正密码纸数量
			BPasswordPatse.Content = "密码纸(" + USetting.PWPaper.Count + ")";
			// 清空密码库并储存新密码，注意 超量的密码将被抛弃
			USetting.PWNote.ClearPassword();
			USetting.PWNote.AddPassword(Password.StringToList(BPWNoteEditText.Text));
			// 储存废纸篓
			USetting.PWRecycle = Password.StringToList(BPWRecycleEditText.Text);
			ChangeBackground("n");
			TipShow("所有密码已保存");
		}

		private void BSetPWCancel_Click(object sender, RoutedEventArgs e)
		{
			BSetPWCloseHelp();
			ChangeBackground("n");
		}
		private void BSetPWCloseHelp()
		{
			WPassword.Visibility = Visibility.Hidden;
			UBoard.BeginAnimation(Border.WidthProperty, new DoubleAnimation(500, 250, TimeSpan.FromSeconds(.2)));
			WPassword.BeginAnimation(Border.WidthProperty, new DoubleAnimation(250, 0, TimeSpan.FromSeconds(.2)));
			USetting.RunState = RunStatus.Normal;
		}

		private void BSetPWCancel_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("取消修改\n所有的修改不会被保存");
		}

		private void BSetPWOk_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("保存所有的修改");
		}

		private void BPWNoteEditText_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("常用密码，上限200个\n储存的密码不会被删除");
		}

		private void BPWPageEditText_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("一次性密码，上限200个\n密码被解压使用后会将删除");
		}

		private void BPWRecycleEditText_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("解压缩成功后被删除的密码纸\n关闭程序后将被清空");
		}

		private void TabItem_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("废纸篓\n解压缩使用过的临时密码");
		}

		private void BCompressType_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("压缩文件格式\n暂时只支持以下通用格式");
		}

		private void BCompressLevel_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("文件压缩级别\n从上至下，速度越慢，文件越小");
		}

		private void BCompressOutMode_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("文件压缩到的位置");
		}

		private void PasswordMode_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("压缩档案的密码");
		}

		private void BSetHotKey_Copy_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("压缩文件日志\n查看压缩位置及其密码");
		}

		private void BDeleteCompressFinish_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("成功压缩后，删除原文件");
		}

		private void BCompressAlone_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("拖入多个文件或文件夹时\n单独压缩每个文件或文件夹");
		}

		private void BCompressFilter_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("使用英文分号分隔关键词\n例: *.txt;*.lnk;*temp*");
		}

		private void BCompressFilter1(object sender, MouseEventArgs e)
		{
			TipShow("忽略文件名包含以下关键字的文件(测试)\n不使用务必留空");
		}
		private void BExtractFilter1(object sender, MouseEventArgs e)
		{
			TipShow("清理文件名包含以下关键字的文件\n不使用务必留空");
		}
		private void BCustomizePassword1_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("自定义的压缩密码1\n只支持英文、数字或部分符号");
		}

		private void BCustomizePassword2_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("自定义的压缩密码2\n只支持英文、数字或部分符号");
		}

		private void BCustomizePassword3_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("自定义的压缩密码3\n只支持英文、数字或部分符号");
		}

		private void BCompressType_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			USetting.CompressType = BCompressType.SelectedIndex;
		}

		private void BCompressLevel_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			switch (BCompressLevel.SelectedIndex)
			{
				case 0: USetting.CompressLevel = (int)CompressLevels.No;break;
				case 1: USetting.CompressLevel = (int)CompressLevels.Fastest; break;
				case 2: USetting.CompressLevel = (int)CompressLevels.Fast; break;
				case 3: USetting.CompressLevel = (int)CompressLevels.Normal; break;
				case 4: USetting.CompressLevel = (int)CompressLevels.Maximum; break;
				case 5: USetting.CompressLevel = (int)CompressLevels.Ultra; break;
			}
		}

		private void BCompressOutMode_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			switch (BCompressOutMode.SelectedIndex)
			{
				case 0: USetting.CompressOutMode = (int)CompressPath.File; break;
				case 1: USetting.CompressOutMode = (int)CompressPath.Browse; break;
			}
		}


		private void BPasswordMode_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			switch (BPasswordMode.SelectedIndex)
			{
				case 0: USetting.PasswordMode = (int)SetPasswords.No; break;
				case 2: USetting.PasswordMode = (int)SetPasswords.Customize1; break;
				case 3: USetting.PasswordMode = (int)SetPasswords.Customize2; break;
				case 4: USetting.PasswordMode = (int)SetPasswords.Customize3; break;
				case 6: USetting.PasswordMode = (int)SetPasswords.Random8; break;
				case 7: USetting.PasswordMode = (int)SetPasswords.Random16; break;
				case 8: USetting.PasswordMode = (int)SetPasswords.Random32; break;

			}
		}

		private void BDeleteCompressFinish_Click(object sender, RoutedEventArgs e)
		{
			USetting.DeleteCompressFinish = (bool)BDeleteCompressFinish.IsChecked;
		}

		private void BCompressAlone_Click(object sender, RoutedEventArgs e)
		{
			USetting.CompressAlone = (bool)BCompressAlone.IsChecked;
		}



		
		// 定义用于修改提示信息的委托，Debug窗口显示
		private delegate void UMessageBug(string m);
		// 定义用于修改提示信息的委托，主窗口提示信息
		private delegate void UMessage(string m,TipMods t);
		// 定义用于修改提示信息的委托，密码纸按钮
		private delegate void UMessagePaper();
		// 定义用于输出结果窗口的委托
		private delegate void UMessageResult(List<string> ls, List<string> lf,bool isExtract);
		
		// 取消标识
		string TipCancel
		{
			get
			{return USetting.UCancel ? "\n「正在取消」" : "\n「取消」";}
		}

		// 用于修改提示信息并且带取消提示的委托的实现
		string TempTip = null;
		private void UMessageTipCancel(string m,TipMods t)
		{
			TempTip = m;
			TipShow(m+TipCancel, t);
		}
		// 正常的更新提示信息委托的实现
		private void UMessageTip(string m, TipMods t)
		{
			TipShow(m, t);
		}
		// 用于更新提示信息的取消信息
		private void UMessageTipCancelUpdata()
		{
			UMessageTipCancel(TempTip, TipMods.FixGray);
		}
		// 用于输出debug窗口委托的实现
		private void UMessageDebugWindow(string m)
		{
			DBWin.message = m;
			DBWin.Show();
		}
		// 用于更正 密码纸按钮的实现
		private void UMessagePaperNum()
		{
			BPasswordPatse.Content = "密码纸(" + USetting.PWPaper.Count + ")";
		}
		// 用于显示结果窗口的实现
		private void UMessageResultWindow(List<string> ls,List<string> lf,bool isExtract)
		{
			ResultWindow RWin = new ResultWindow();
			RWin.Left = this.Left;
			RWin.Top = this.Top + 25;
			RWin.Show();

			if (isExtract)
				RWin.OutExtractResult(ls, lf);
			else
			{
				// 成功列表有s 则启动单文件压缩的，失败列表有f 就启动单文件压缩的，
				if (ls!=null && ls.Count>0 && ls[0] == "s") RWin.OutCompressAloneResult(true);
				else if (lf!=null && lf.Count>0 && lf[0] == "f") RWin.OutCompressAloneResult(false);
				// 以上都不是 就琼那个多文件压缩的
				else RWin.OutCompressResult(ls, lf);
			}				
		}

		// 拖拽文件开始工作
		private void BDropBox_Drop(object sender, DragEventArgs e)
		{
			// 程序非空闲状态时直接返回
			if (USetting.RunState != RunStatus.Normal) return;

			// 读取拖拽的文件列表
			if (e.Data.GetDataPresent(System.Windows.DataFormats.FileDrop))
			{
				USetting.FileList = (string[])e.Data.GetData(System.Windows.DataFormats.FileDrop);
			}
			else return;
			// 确定文件列表可用性
			if (USetting.FileList == null) return;
			
			// 仅解压
			if (USetting.AppMode == (int)AppModes.OnlyExtract)
			{
				// 是否需要弹出路径选择窗口窗口
				if (USetting.ExtractOutMode == (int)ExtractPath.Browse)
				{
					// 弹出解压路径选择窗口,窗口取消，则中断
					if (!ShowExtractSelectWindow()) return;
				}
				// 更改工作状态
				USetting.RunState = RunStatus.ExtractFile;
				MainProcess(true);
			}
			// 仅压缩
			if (USetting.AppMode == (int)AppModes.OnlyCompress)
			{
				// 是否需要弹出路径选择窗口窗口
				if (USetting.CompressOutMode == (int)CompressPath.Browse)
				{
					// 弹出压缩路径选择窗口
					if (!ShowCompressSelectWindow()) return;
				}
				// 更改工作状态
				USetting.RunState = RunStatus.CompressFile;
				MainProcess(false);
			}

			// 自动模式，文件可解压是解压模式，不可则都是压缩模式
			// 具体工作方式由最后选中并拖拽的文件决定
			if (USetting.AppMode == (int)AppModes.Auto)
			{
				bool ce = UTool.CanExtract(USetting.FileList[0]);
				VolumesFile vf = new VolumesFile(USetting.FileList[0]);
				// 检查最后选择的文件是否能解压,或者是否为分卷
				if ( ce || vf.IsVolumes())
				{
					// 检查是否为手动选择解压位置
					if (USetting.ExtractOutMode == (int)ExtractPath.Browse)
					{
						// 弹出解压路径选择窗口，若取消窗口则直接中断工作
						if (!ShowExtractSelectWindow()) return;
					}

					USetting.RunState = RunStatus.ExtractFile;
					MainProcess(true);
				}
				else
				{
					if (USetting.CompressOutMode == (int)CompressPath.Browse)
					{
						// 弹出压缩路径选择窗口，若取消窗口则直接中断工作
						if (!ShowCompressSelectWindow()) return;
					}

					USetting.RunState = RunStatus.CompressFile;
					MainProcess(false);
				}
			}
		}

		// 解压选择窗口 弹出
		private bool ShowExtractSelectWindow()
		{
			SelectOut UEWin = new SelectOut();
			UEWin.Top = this.Top + 25;
			UEWin.Left = this.Left;
			UEWin.ShowDialog();
			// 窗口被取消，结束并返回，
			if (UEWin.SelectPath == null) return false;
			// 否则，选择路径被导入 usetting.lastoutpath，选择路径成功
			return true;
		}

		// 压缩选择窗口 弹出
		private bool ShowCompressSelectWindow()
		{
			SelectOut2 UCWin = new SelectOut2();
			UCWin.Top = this.Top + 25;
			UCWin.Left = this.Left;
			UCWin.ShowDialog();
			// 窗口被取消，结束并返回，
			if (UCWin.SelectPath == null) return false;
			// 否则，选择路径被导入 usetting.lastoutpath，选择路径成功
			return true;
		}

		// 用于区分压压缩和解压的主进程
		private void MainProcess(bool isExtract = true)
		{
			// 备份密码纸
			if (USetting.PaperChange)
			{
				USetting.BackConfigPage();
				USetting.BackConfigNote();
				USetting.PaperChange = false;
			}

			// 解压
			if (isExtract)
			{
				// 解压
				ExtractProcessAsync();
			}
			else
			{
				// 压缩，压缩到每个文件
				if (USetting.CompressAlone) CompressProcessAsync();
				// 压缩，压缩到一个文件
				else CompressProcessAsync(true);
			}

			
		}


		// 解压主进程
		private void ExtractProcessAsync()
		{
			// 成功列表
			List<string> SuccessList = new List<string>();
			// 失败列表
			List<string> FailureList = new List<string>();
			// 密码纸已用列表
			List<string> PWPSuccessList = new List<string>();
			// 分卷文件列表
			List<string> VolumesList = new List<string>();
			// 是否使用文件过滤
			bool FilterFile = false;
			List<string> FilterList = null;
			if (USetting.ExtractFilterArray != null && USetting.ExtractFilterArray.Length > 0)
			{
				FilterFile = true;
			}
			Task t = Task.Run(() => {
				// 创建debug窗口
				UCmd Cmd = new UCmd(true);
				// 用于接收解压/测试结果字符串
				string uMessage = null;
				// 用于储存正确的密码
				string uPassword = null;
				// 用于确定密码的来源是否为Page
				bool uIsPaper = false;
				// 用于确定是否找到正确的密码，测试通过，可以开始解压
				bool uOk = false;
				// 是否是分卷
				VolumesFile uVolumes = null;

				
				// 文件计数
				int fn = 0;
				int fs = USetting.FileList.Length;
				// 输出文本
				string str = null;
				// 用于智能解压，读取子目录信息
				DirectoryInfo di = null;
				// 从文件名提取的密码
				string NamePassword = null;
				// 标识，用于标识文件是否曾被（分卷）解压过
				bool vhas = false;
				// 多文件操作 解压
				foreach (var fi in USetting.FileList)
				{
					// 检查是否取消
					if (USetting.UCancel) continue;

					// 文件名另存，便于后续修改
					string f = fi;
					// 计数器归零
					uMessage = null;uPassword = null; uIsPaper = false;uOk = false;
					FilterList = null;NamePassword = null;uVolumes = null;vhas = false;
					// 文件输出目录 临时
					string FOutTemp = UCmdPathHelp.UExtractPath(f);
					// 文件输出目录 真
					string FOut = UCmdPathHelp.UExtractPath();
					// 提取文件名
					string FName = System.IO.Path.GetFileNameWithoutExtension(f);
					
					str = "正在解压（" + ++fn + "/" + fs + "）\n";
					this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "检查压缩档案...", TipMods.FixGray);
					// 检查是否为分卷,返回主分卷
					uVolumes = new VolumesFile(f);

					// 检测文件是 否不可解压，且不使用解压未知格式，且不是分卷，直接跳过
					if (!UTool.CanExtract(f) && !USetting.ExtractUnknow && !uVolumes.IsVolumes())
					{
						FailureList.Add(f);
						// 删除临时文件夹
						if (Directory.Exists(FOutTemp))
						{
							Directory.Delete(FOutTemp);
						}
						continue;
					}
					// 检查卷，如果为zip，检测是否被作为分卷解压
					if ((System.IO.Path.GetExtension(f)).ToLower() == ".zip")
					{
						// 成功解压列表
						if (!vhas)
						{
							for (int i = 0; i < SuccessList.Count; i++)
							{
								if (SuccessList[i] == f)
								{
									vhas = true; break;
								}
							}
						}
						// 检查失败列表
						if (!vhas)
						{
							for (int i = 0; i < FailureList.Count; i++)
							{
								if (FailureList[i] == f)
								{
									vhas = true; break;
								}
							}
						}
						// 检查标识，判定是否被解压过
						if (vhas)
						{
							// 如果在分卷列表中找到，跳过
							if (Directory.Exists(FOutTemp))
							{
								Directory.Delete(FOutTemp);
							}
							continue;
						}

					}
					// 检查卷，如果是分卷，检测是否被作为分卷解压
					if (uVolumes.IsVolumes() )
					{
						string MainVolumes = uVolumes.GetMainVolumes();
						// 成功解压列表
						if (!vhas)
						{
							for (int i = 0; i < SuccessList.Count; i++)
							{
								if (SuccessList[i] == MainVolumes)
								{
									vhas = true; break;
								}
							}
						}
						// 检查失败列表
						if (!vhas)
						{
							for (int i = 0; i < FailureList.Count; i++)
							{
								if (FailureList[i] == MainVolumes)
								{
									vhas = true; break;
								}
							}
						}
						// 检查标识，判定是否被解压过
						if (vhas)
						{
							// 如果在分卷列表中找到，跳过
							if (Directory.Exists(FOutTemp))
							{
								Directory.Delete(FOutTemp);
							}
							continue;
						}
						// 标识检查通过，为被解压，且为分卷，则使用主卷替换
						if (MainVolumes != null) f = MainVolumes;
					}

					//MessageBox.Show(uVolumes.gogo());
					//USetting.RunState = RunStatus.Normal;
					//return;

					// 测试无密码
					uMessage = Cmd.TestFile(f);
					if (UCmd.IsOK(uMessage))
					{
						uOk = true;
					}


					// 通过其他方式提取密码(读取内置密码)，此段可直接删除。同时移除mypassword.cs
					
					if (!uOk && USetting.ReadPasswordMode !=0)
					{
						this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "提取内置解压密码...", TipMods.FixGray);
						Mypassword myps = new Mypassword();
						if (myps.myp != null) 
						{
							foreach (string op in myps.myp)
							{
								uMessage = Cmd.TestFile(f, op);
								if (UCmd.IsOK(uMessage))
								{
									uPassword = op;
									uOk = true;
								}
							}
						}

					}


					// 尝试从文件名提取密码
					if (!uOk && USetting.NameToPassword && USetting.NameFilter != null 
						&& USetting.NameFilter != "" && !uVolumes.IsVolumes())
					{
						this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "从文件名提取密码...", TipMods.FixGray);
						NamePassword = UTool.SplitString(FName,USetting.NameFilter);
						// 分卷则使用其他方式
						//NamePassword = UTool.SplitString(uVolumes.FileName, USetting.NameFilter);
						if (NamePassword != null)
						{
							uMessage = Cmd.TestFile(f, NamePassword);
							if (UCmd.IsOK(uMessage))
							{
								uPassword = NamePassword;
								// 提纯文件名
								string rep = USetting.NameFilter + NamePassword + USetting.NameFilter;
								string fname2 = FName.Replace(rep, "");
								if (FName == fname2)
								{
									rep = USetting.NameFilter + NamePassword;
									fname2 = FName.Replace(rep, "");
								}
								if (FName != fname2)
								{
									FName = fname2;
								}
								uOk = true;
							}
						}
					}


					
					this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "查找可用密码...", TipMods.FixGray);

					// 在密码本中查找密码
					if (!uOk)
					{
						uPassword = USetting.PWNote.CmdTestPassword(Cmd, f);
						if (uPassword != null)
						{
							uOk = true;
						}
					}
					
					// 在密码纸中查找密码
					if (!uOk)
					{
						uPassword = USetting.PWPaper.CmdTestPassword(Cmd, f);
						if (uPassword != null)
						{
							uOk = true;
							uIsPaper = true;
						}
					}
					
					// 如果无法解压，且没有找到密码，加入失败列表，并跳过
					if (!uOk)
					{
						//MessageBox.Show("没有找到密码");
						FailureList.Add(f);
						// 删除临时文件夹
						if (Directory.Exists(FOutTemp))
						{
							Directory.Delete(FOutTemp);
						}
						continue;
					}
					this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "正在提取文件..." , TipMods.FixGray);

					// 开始解压 // 解压新临时文件夹以实现特殊功能
					uMessage = Cmd.ExtractFileNewForder(f, uPassword);

					// Debug模式显示结果
					if (USetting.DebugMode)
					{
						this.Dispatcher.Invoke(new UMessageBug(UMessageDebugWindow), uMessage);
					}

					// 查看解压结果,处理后事
					if (UCmd.IsOK(uMessage))
					{
						SuccessList.Add(f);
						// 删除密码纸
						if (uIsPaper)
						{
							// 将密码纸已用密码加入废纸篓
							if (USetting.PWRecycle == null) USetting.PWRecycle = new List<string>();
							USetting.PWRecycle.Add(uPassword);
							// 删除密码纸已用密码
							USetting.PWPaper.DeletePassword(uPassword);
							// 修正密码纸计数
							this.Dispatcher.Invoke(new UMessagePaper(UMessagePaperNum));
						}

						//if (uIsPaper) PWPSuccessList.Add(uPassword);

						// 处理文件过滤，删除过滤的文件
						if (FilterFile)
						{
							foreach (string filter in USetting.ExtractFilterArray)
							{
								FilterList = UTool.FindFile(FOutTemp, filter);
								// 删除文件
								foreach (string ff in FilterList)
								{
									File.Delete(ff);
								}
							}
						}

						// 读取临时目录信息
						di = new DirectoryInfo(FOutTemp);
						
						// 还原临时目录的文件 
						// 处理多文件情况,或处理解压到同名文件夹
						if (USetting.CreateNewFolder || USetting.CreateNameFolder)
						{
							
							
							// 读取根目录内文件或文件夹数量是否为1，为1时，移动到解压根目录
							if (di.GetDirectories().Length + di.GetFiles().Length <= 1 && !USetting.CreateNameFolder)
							{
								UTool.MoveFolder(FOutTemp, FOut,USetting.ExtractCoverMode);
								di.Delete(true);
							}
							// 根目录有多个文件，为防止混乱，创建压缩文件同名文件夹
							else
							{
								// 如果同名文件夹已存在，更改一个新名字
								string newpath = System.IO.Path.GetDirectoryName(FOut)
									+ "\\" + FName ;
								string newpath2 = newpath + "\\";
								int newpathnum = 1;
								while (Directory.Exists(newpath2))
								{
									newpath2 = newpath + "-New"+ newpathnum + "\\";
									newpathnum++;
								}
								Directory.CreateDirectory(newpath2);

								UTool.MoveFolder(FOutTemp,newpath2);
								try
								{
									di.Delete(true);
								}
								catch
								{
									// UTool.DeleteDirectory(f);
								}
							}
						}
						// 不处理多文件情况
						else
						{
							// 不处理多文件，则直接移动到解压输出目录
							UTool.MoveFolder(FOutTemp, FOut,USetting.ExtractCoverMode);
							//MessageBox.Show(di.ToString());
							try
							{
								di.Delete(true);
							}
							catch
							{
								// UTool.DeleteDirectory(f);
							}
							
						}
						
						// 删除原文件
						if (USetting.DeleteFinishFile && File.Exists(f))
						{
							// 检查是否是分卷，处理分卷
							if (UCmd.IsVolumes(uMessage))
							{
								// 分卷删除程序
								uVolumes.DeleteVolumesFile();

							}
							else
							{
								//File.Delete(f);
								UTool.DeleteFile(f, USetting.DeleteToRecycle);

							}
							
						}

					}
					else
					{
						FailureList.Add(f);
					}
					// 处理后事
				}
				/*
				// 检查是否使用了密码纸，加入废纸篓
				if(PWPSuccessList.Count > 0)
				{
					// 将密码纸已用密码加入废纸篓
					if (USetting.PWRecycle == null)
					{
						// 有时候会莫名其妙为空引用
						USetting.PWRecycle = PWPSuccessList;
					}
					else
					{
						foreach (string pw in PWPSuccessList)
						{
							USetting.PWRecycle.Add(pw);
						}
					}

					// 删除密码纸已用密码
					USetting.PWPaper.DeletePassword(PWPSuccessList);
				}
				// 修正密码纸计数
				this.Dispatcher.Invoke(new UMessagePaper(UMessagePaperNum));
				*/

				// 恢复软件状态，恢复提示状态
				USetting.RunState = RunStatus.Normal;
				TipWarnToNormal();
				// 整理成功失败数据
				int fl = FailureList.Count;
				int sl = SuccessList.Count;
				// 使用结果窗 则只在结果窗显示结果
				if (USetting.ResultWindow)
				{
					this.Dispatcher.Invoke(new UMessage(UMessageTip), "拖拽一个压缩档案到这里",TipMods.TipNormal);
					this.Dispatcher.Invoke(new UMessageResult(UMessageResultWindow), SuccessList, FailureList,true);
					
				}
				// 不使用结果窗，在提示面板显示结果
				else
				{
					if (fl != 0)
						this.Dispatcher.Invoke(new UMessage(UMessageTip), "解压已完成,其中 " + fl + " 个失败", TipMods.WarnRed);
					else
						this.Dispatcher.Invoke(new UMessage(UMessageTip), "解压全部完成", TipMods.WarnGreen);
				}
				
				// 清空文件列表
				USetting.FileList = null;
				// 复位中断数据
				USetting.UCancel = false;
			});
			return;
		}

		// 压缩主进程
		private void CompressProcessAsync(bool alone  = false)
		{
			// 成功列表
			List<string> SuccessList = new List<string>();
			// 失败列表
			List<string> FailureList = new List<string>();
			// 是否使用文件过滤
			string[] FilterFile = null;
			if (USetting.CompressFilterArray != null && USetting.CompressFilterArray.Length > 0)
			{
				FilterFile = USetting.CompressFilterArray;
			}
			
			Task t = Task.Run(()=>{
				// 创建CMD
				UCmd Cmd = new UCmd(false);
				// 储存压缩结果
				CompressResultToTxt RToTxt = new CompressResultToTxt(USetting.CompressLog);
				// 用于接收解压/测试结果字符串
				string uMessage = null;
				// 用于储存压缩的密码
				string uPassword = null;
				// 0 不使用随机密码，8，16，32位随机密码
				int RandomPassword = 0;
				switch ((SetPasswords)USetting.PasswordMode)
				{
					case SetPasswords.No:break;
					case SetPasswords.Random8: RandomPassword = 8; break;
					case SetPasswords.Random16: RandomPassword = 16; break;
					case SetPasswords.Random32: RandomPassword = 32; break;
					case SetPasswords.Customize1: uPassword = USetting.CustomizePassword1;break;
					case SetPasswords.Customize2: uPassword = USetting.CustomizePassword2; break;
					case SetPasswords.Customize3: uPassword = USetting.CustomizePassword3; break;
				}
				// 文件计数
				int fn = 0;
				int fs = USetting.FileList.Length;
				// 输出文本
				string str = null;
				// 密码标识，用于将密码写入文件名
				string PWSign = null;
				// 是否将密码写入文件名
				if (USetting.PasswordToName)
				{
					PWSign = USetting.NameFilter2;
					if (USetting.NameFilter2 == "" || USetting.NameFilter2 == null)
						PWSign = " ";
				}
					

				// 单文件操作 压缩、、 压缩为一个文件
				if (alone)
				{
					// 如使用随机密码则生成随机密码
					if (RandomPassword != 0) uPassword = UTool.GetRandomString(RandomPassword);
					// 输出提示文本
					str = "正在压缩（" + ++fn + "/" + fs + "）\n";
					this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "创建压缩档案..." , TipMods.FixGray);
					
					// 开始压缩
					uMessage = Cmd.CompressFile(USetting.FileList, uPassword, FilterFile,USetting.HideZipContent,PWSign);
					// Debug模式显示
					if (USetting.DebugMode)
					{
						this.Dispatcher.Invoke(new UMessageBug(UMessageDebugWindow), uMessage);
					}
					// 查看压缩结果,处理后事
					if (UCmd.IsOK(uMessage))
					{
						SuccessList.Add("s");
						// 删除原文件
						if (USetting.DeleteCompressFinish)
						{
							foreach (string fr in USetting.FileList)
							{
								if (Directory.Exists(fr))
									UTool.DeleteDirectory(fr, USetting.DeleteToRecycle);
								
								if (File.Exists(fr))
									UTool.DeleteFile(fr,USetting.DeleteToRecycle); 
								
							}
						}
						// 写入日志
						RToTxt.Write(Cmd.GetOutFilePath(), uPassword);
						RToTxt.Close();
					}
					else
					{
						FailureList.Add("f");
					}
				}
				// 多文件操作 压缩
				else
				{
					foreach (var f in USetting.FileList)
					{
						// 检查是否取消
						if (USetting.UCancel) continue;

						// 计数器归零
						uMessage = null; 
						// 如使用随机密码则生成随机密码
						if (RandomPassword != 0) uPassword = UTool.GetRandomString(RandomPassword);
						// 输出提示文本
						str = "正在压缩（" + ++fn + "/" + fs + "）\n";
						this.Dispatcher.Invoke(new UMessage(UMessageTipCancel), str + "创建压缩档案...", TipMods.FixGray);
						// 开始压缩
						uMessage = Cmd.CompressFile(f, uPassword, FilterFile, USetting.HideZipContent, PWSign);
						// Debug模式显示
						if (USetting.DebugMode)
						{
							this.Dispatcher.Invoke(new UMessageBug(UMessageDebugWindow), uMessage);
						}
						// 查看压缩结果,处理后事
						if (UCmd.IsOK(uMessage))
						{
							SuccessList.Add(f);
							// 删除原文件
							if (USetting.DeleteCompressFinish)
							{
								if (Directory.Exists(f))
									UTool.DeleteDirectory(f, USetting.DeleteToRecycle);
								if (File.Exists(f))
									UTool.DeleteFile(f, USetting.DeleteToRecycle);
							}
							// 写入日志
							RToTxt.Write(Cmd.GetOutFilePath(),uPassword);
						}
						else
						{
							FailureList.Add(f);
						}
						
					}
					RToTxt.Close();
				}
				// 恢复软件状态，恢复提示状态
				USetting.RunState = RunStatus.Normal;
				TipWarnToNormal();
				// 如使用结果窗 则只在结果窗显示结果
				// 否则使用提示面板显示结果
				if (USetting.ResultWindow)
				{
					this.Dispatcher.Invoke(new UMessage(UMessageTip), "拖拽一个压缩档案到这里", TipMods.TipNormal);
					this.Dispatcher.Invoke(new UMessageResult(UMessageResultWindow), SuccessList, FailureList, false);
				}
				else
				{
					if (FailureList.Count != 0)
						if (FailureList[0] == "f")
							this.Dispatcher.Invoke(new UMessage(UMessageTip), "压缩失败\n请检查文件是否被占用", TipMods.WarnRed);
						else
							this.Dispatcher.Invoke(new UMessage(UMessageTip), "压缩已完成,其中 " + FailureList.Count + " 个失败", TipMods.WarnRed);
					else
						if(SuccessList[0]=="s")
						this.Dispatcher.Invoke(new UMessage(UMessageTip), "压缩完成", TipMods.WarnGreen);
					else
						this.Dispatcher.Invoke(new UMessage(UMessageTip), "压缩全部完成", TipMods.WarnGreen);
				}

				// 清空文件列表
				USetting.FileList = null;
				// 复位中断数据
				USetting.UCancel = false;
			});
		}

		// 打开压缩日志文件
		private void BShowCompressLog_Click(object sender, RoutedEventArgs e)
		{
			if(File.Exists(USetting.CompressLog))
				CompressResultToTxt.OpenLog(USetting.CompressLog);
		}



		// 定义热键
		UHotKey UKPatse;

		// 覆写以加入快捷键
		protected override void OnSourceInitialized(EventArgs e)
		{
			base.OnSourceInitialized(e);

			UKPatse = new UHotKey(this);
			//UKPatse.SetHotKey(UKey.Key_F5, true);
			//UKPatse.Register();
			// 设置热键
			SetPasteHotKey();
			// 获取消息的事件，传入处理程序
			HwndSource source = PresentationSource.FromVisual(this) as HwndSource;
			source.AddHook(WndProc);
		}
		
		// 设置并注册热键
		public void SetPasteHotKey()
		{

			if (USetting.HotKeyKey != 0)
			{
				BSetHotKey.Content = (USetting.HotKeyCtrl ? "Ctrl + " : "") +
					(USetting.HotKeyShift ? "Shift + " : "") +
					(USetting.HotKeyAlt ? "Alt + " : "") +
					Enum.GetName(typeof(UKey), USetting.HotKeyKey).Remove(0, 4);
				if (USetting.UseHotKey)
				{
					UKPatse.SetHotKey((UKey)USetting.HotKeyKey, USetting.HotKeyAlt,
						USetting.HotKeyShift, USetting.HotKeyCtrl);
					UKPatse.Register();
				};

			}
		}
		// 去掉注册热键
		public void UnSetPastHotKey()
		{
			UKPatse.Unregister();
		}



		// 用于获取鼠标所在窗口句柄
		[DllImport("user32.dll")]
		internal static extern IntPtr WindowFromPoint(System.Drawing.Point Point);
		[DllImport("user32.dll")]
		internal static extern bool GetCursorPos(out System.Drawing.Point lpPoint);
		private IntPtr GetCursorWindow()
		{
			System.Drawing.Point p;
			GetCursorPos(out p);//获取鼠标坐标
			//InputHitTest(p);
			
			return WindowFromPoint(p);
			//WindowFromPoint(p);

		}

		
		//设置此窗体为活动窗体
		[DllImport("user32.dll", EntryPoint = "SetForegroundWindow")]
		public static extern bool SetForegroundWindow(IntPtr hWnd);

		// 热键处理程序
		IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handle)
		{
			if (wParam.ToInt32() == UKPatse.ID)
			{
				// 全局快捷键要执行的命令
				// 读取剪切板的内容
				// 模拟热键 ctrl+c 复制到剪切板

				//System.Windows.Forms.SendKeys.SendWait("%{tab}");

				//.Focus();
				//IntPtr HWND2 = GetCursorWindow();
				//SetForegroundWindow(HWND2);

				Keyboard.Release(Key.LeftShift);
				Keyboard.Release(Key.LeftAlt);
				Keyboard.Release(Key.LeftCtrl);
				Thread.Sleep(100);
				
				Keyboard.Press(Key.LeftCtrl);
				Keyboard.Press(Key.C);
				Keyboard.Release(Key.C);
				Keyboard.Release(Key.LeftCtrl);
				Thread.Sleep(100);
				// 贴入剪切板内密码
				PatsePassword();
				// 恢复剪切板内容

			}
			return IntPtr.Zero;
		}

		private void BClose_MouseRightButtonDown(object sender, MouseButtonEventArgs e)
		{
			Thread.Sleep(200);
			this.WindowState = WindowState.Minimized;
			if (USetting.RunState == RunStatus.Normal)
			{
				TipWarnToNormal();
				TipShowEnd();
			}
			

		}

		private void BTip_MouseEnter(object sender, MouseEventArgs e)
		{
			if (USetting.RunState != RunStatus.Normal) return;
			if(TipWarn == (int)TipMods.WarmGray) TipWarn = (int)TipMods.TipNormal;
			TipShowEnd();
		}

		private void BCreateNameFolder_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("解压到压缩档案同名目录\n注意：本选项和自动创建文件夹互斥");
		}

		private void BCreateNameFolder_Click(object sender, RoutedEventArgs e)
		{
			USetting.CreateNameFolder = (bool)BCreateNameFolder.IsChecked;
			if (USetting.CreateNameFolder)
			{
				BCreateNewFolder.IsChecked = false;
				USetting.CreateNewFolder = false;
			}
		}

		private void BHideZipContent_MouseEnter(object sender, MouseEventArgs e)
		{
			TipShow("隐藏加密压缩文件内的文件列表，\n解压前将无法看到其中包含的内容。\n（ 仅限7z格式 ）");
		}

		private void BHideZipContent_Click(object sender, RoutedEventArgs e)
		{
			USetting.HideZipContent = (bool)BHideZipContent.IsChecked;
		}
	}
}
