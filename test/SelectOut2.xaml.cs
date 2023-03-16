using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.IO;

namespace UZIP2
{
	/// <summary>
	/// SelectOutAndPassword.xaml 的交互逻辑
	/// </summary>
	public partial class SelectOut2 : Window
	{
		// 标记选择路径是否成功，返回失败就不会执行解压 
		public string SelectPath = null;

		public SelectOut2()
		{
			InitializeComponent();
			// 读取上次的 列表框选项，并设置界面元素
			ReadPathLast();
			//USetting.LastOutPath;
			// 根据路径现状，初始化按钮可用性和文字
			TPath_TextChanged_Help();
			this.Topmost = USetting.WindowOnTop;
		}

		// 读取上一回的面板设置，并同步到控件
		public void ReadPathLast()
		{
			BSelectPath.SelectedIndex = USetting.CompressOutModePop;
			switch (USetting.CompressOutModePop)
			{
				case 0:
					TPath.Text = USetting.LastCompressPath; break;
				case 1:
					if (USetting.FileList == null) TPath.Text = null;
					else TPath.Text = UTool.CompletionPath(Path.GetDirectoryName(USetting.FileList[0]));
					break;
				case 3:
					BSelectPath.SelectedIndex = 0;
					TPath.Text = USetting.LastCompressPath; break;
			}

		}
		private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			// 窗口不可移动故省略以下代码
			/*
			if (e.ButtonState == MouseButtonState.Pressed)
			{
				this.DragMove();
			}
			*/
		}

		// 列表框选项及处理，没有使用SelectionChange，因为重复选择按钮不能重置执行事件
		// 列表框-上次位置
		private void ComboBoxItem_PreviewMouseLeftButtonDown_0(object sender, MouseButtonEventArgs e)
		{
			TPath.Text = USetting.LastCompressPath;
		}
		// 列表框-文件位置
		private void ComboBoxItem_PreviewMouseLeftButtonDown_1(object sender, MouseButtonEventArgs e)
		{
			if (USetting.FileList == null) TPath.Text = null;
			else TPath.Text = UTool.CompletionPath(Path.GetDirectoryName(USetting.FileList[0]));
		}
		// 列表框-浏览
		private void ComboBoxItem_PreviewMouseLeftButtonDown_3(object sender, MouseButtonEventArgs e)
		{
			BSelectPath.SelectedIndex = 3;
			System.Windows.Forms.FolderBrowserDialog openFileDialog = new System.Windows.Forms.FolderBrowserDialog();  //选择文件夹
			openFileDialog.Description = "选择一个文件夹";
			if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
			//注意，此处一定要手动引入System.Window.Forms空间，否则你如果使用默认的DialogResult会发现没有OK属性
			{
				TPath.Text = openFileDialog.SelectedPath + "\\";
			}
			else
			{
				TPath.Text = "";
			}
		}

		private void TPath_TextChanged(object sender, TextChangedEventArgs e)
		{
			//界面加载时候会报错BOK不存在
			if (BOk == null) return;
			// 检测字符串可用性并处理界面元素
			TPath_TextChanged_Help();
		}
		// 检测字符串可用性并处理界面元素
		void TPath_TextChanged_Help()
		{
			//检测文本框内容是否可用
			if (UTool.CheckPath(TPath.Text))
			{
				BOk.IsEnabled = true;
				BOk.Content = "确定";
			}
			else
			{
				BOk.IsEnabled = false;
				BOk.Content = "目录错误";
			}
		}

		private void BOk_Click(object sender, RoutedEventArgs e)
		{
			// 检查路径可用性，文本框检查过，不通过按钮不可用，所以这里省略
			// 路径补完，检查路径是否有\没有就加一个,把路径写输出参数
			string Path = UTool.CompletionPath(TPath.Text);

			// 储存到最后储存的路径
			USetting.LastCompressPath = Path;
			// 储存当前列表框选项
			USetting.CompressOutModePop = BSelectPath.SelectedIndex;
			// 储存当前路径，以备调用
			SelectPath = Path;
			// 关闭窗口
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

		private void BClose_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			SelectPath = null;
			this.Close();
		}

		private void BSelectPath_PreviewMouseWheel(object sender, MouseWheelEventArgs e)
		{
			// 如果选择框没有展开，禁用选择框鼠标滚轮
			if (!BSelectPath.IsDropDownOpen) e.Handled = true;
		}
	}
}

