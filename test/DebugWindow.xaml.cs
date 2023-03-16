using System;
using System.Collections.Generic;
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
using System.Windows.Shapes;

namespace UZIP2
{
	/// <summary>
	/// DebugWindow.xaml 的交互逻辑
	/// </summary>
	public partial class DebugWindow : Window
	{
		public string message
		{
			set
			{
				BResults.Text = value;
			}
		}
		public DebugWindow()
		{
			InitializeComponent();
			this.Topmost = USetting.WindowOnTop;
		}

		private void BClose_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			this.Hide();
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

		private void BOk_Click(object sender, RoutedEventArgs e)
		{
			this.Hide();
		}
	}
}
