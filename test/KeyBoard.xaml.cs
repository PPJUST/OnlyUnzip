using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace UZIP2
{
	/// <summary>
	/// KeyBoard.xaml 的交互逻辑
	/// </summary>
	/// 

    public partial class Window2 : Window
    {
		List<ToggleButton> TBtns;
		//KBoard KB = new KBoard();
		public UInt32 KNormal = 0;
		public bool KShift = false;
		public bool KCtrl = false;
		public bool KAlt = false;
		public bool KCap = false;

		public Window2()
        {
            InitializeComponent();
			TBtns = GetChildObjects<ToggleButton>(WKB_A, typeof(ToggleButton));
			this.Topmost = USetting.WindowOnTop;
		}

		private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			// 禁用窗口可移动
			/*
			if (e.ButtonState == MouseButtonState.Pressed)
			{
				this.DragMove();
			}
			*/
		}

		//检查设定是否正确，如正确显示保存按钮
		public void IsOK()
		{
			if (KNormal != 0 && (KShift || KCtrl || KAlt))
			{
				UOk.Visibility = Visibility.Visible;
				UTip.Visibility = Visibility.Hidden;
			}
			else
			{
				UOk.Visibility = Visibility.Hidden;
				UTip.Visibility = Visibility.Visible;
			}
		}

		//查找子控件
		public List<T> GetChildObjects<T>(DependencyObject obj, Type typename) where T : FrameworkElement
		{
			DependencyObject child = null;
			List<T> childList = new List<T>();

			for (int i = 0; i <= VisualTreeHelper.GetChildrenCount(obj) - 1; i++)
			{
				child = VisualTreeHelper.GetChild(obj, i);

				if (child is T && (((T)child).GetType() == typename))
				{
					childList.Add((T)child);
				}
				childList.AddRange(GetChildObjects<T>(child, typename));
			}
			return childList;
		}

		// 普通按钮被按下
		private void ToggleButton_Click(object sender, RoutedEventArgs e)
		{
			ToggleButton t = (ToggleButton)sender;
			if ((bool)t.IsChecked)
			{
				foreach (ToggleButton tb in TBtns)
				{
					tb.IsChecked = false;
				}
				((ToggleButton)sender).IsChecked = true;
				// 返回当前按键代码
				KNormal = (UInt32)int.Parse(t.Name.Remove(0, 2));

				//MessageBox.Show(KNormal.ToString("x"));
			}
			else
			{
				KNormal = 0;
			}
			IsOK();
		}

		private void BC_LShift_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_LShift.IsChecked)
			{
				BC_RShift.IsChecked = false;
				KShift = true;
			}
			else
			{
				KShift = false;
			}
			IsOK();
		}

		private void BC_RShift_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_RShift.IsChecked)
			{
				BC_LShift.IsChecked = false;
				KShift = true;
			}
			else
			{
				KShift = false;
			}
			IsOK();
		}

		private void BC_LCtrl_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_LCtrl.IsChecked)
			{
				BC_RCtrl.IsChecked = false;
				KCtrl = true;
			}
			else
			{
				KCtrl = false;
			}
			IsOK();
		}

		private void BC_RCtrl_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_RCtrl.IsChecked)
			{
				BC_LCtrl.IsChecked = false;
				KCtrl = true;
			}
			else
			{
				KCtrl = false;
			}
			IsOK();
		}

		private void BC_LAlt_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_LAlt.IsChecked)
			{
				BC_RAlt.IsChecked = false;
				KAlt = true;
			}
			else
			{
				KAlt = false;
			}
			IsOK();
		}

		private void BC_RAlt_Click(object sender, RoutedEventArgs e)
		{
			BC_Cap.IsChecked = false;
			KCap = false;
			if ((bool)BC_RAlt.IsChecked)
			{
				BC_LAlt.IsChecked = false;
				KAlt = true;
			}
			else
			{
				KAlt = false;
			}
			IsOK();
		}

		private void BC_Cap_Click(object sender, RoutedEventArgs e)
		{
			if ((bool)BC_Cap.IsChecked)
			{
				BC_RCtrl.IsChecked = false;
				BC_LCtrl.IsChecked = false;
				BC_LShift.IsChecked = false;
				BC_RShift.IsChecked = false;
				BC_LAlt.IsChecked = false;
				BC_RAlt.IsChecked = false;

				KCap = true;
				KAlt = false;
				KShift = false;
				KCtrl = false;
			}
			else
			{
				KCap = false;
			}
			IsOK();
		}


		private void UOk_Click(object sender, RoutedEventArgs e)
		{
			//KCheck();
			//MessageBox.Show(KNormal.ToString("x"));
			//MessageBox.Show("Normal:\t" + KB.KNormal + " \nShift:\t" + KB.KShift + " \nCtrl:\t" + KB.KCtrl + " \nAlt:\t" + KB.KAlt + " \nCap:\t" + KB.KCap);
			this.Close();
		}

		private void WMain_BClose_MouseEnter(object sender, MouseEventArgs e)
		{

		}

		private void WMain_BClose_MouseLeave(object sender, MouseEventArgs e)
		{

		}

		private void WMain_BClose_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
		{
			KNormal = 0;
			this.Close();
		}
	}
}
