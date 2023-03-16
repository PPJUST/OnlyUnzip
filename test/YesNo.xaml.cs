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
	/// YesNo.xaml 的交互逻辑
	/// </summary>
	public partial class YesNo : Window
	{
		public string YesContext
		{
			set { BOk.Content = value; } 
		} 
		public string NoContext
		{
			set { BCancel.Content = value; }
		} 
		public string WindowTitle
		{
			set { this.Title = value; }
		} 
		public string WindowTips
		{
			set { BTips.Content = value; }
		}
		public bool IsYes = false;
		public YesNo()
		{
			InitializeComponent();
			
		}

		private void BOk_Click(object sender, RoutedEventArgs e)
		{
			IsYes = true;
			this.Close();
		}

		private void BCancel_Click(object sender, RoutedEventArgs e)
		{
			IsYes = false;
			this.Close();
		}
	}
}
