using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace UZIP2
{
	class Mypassword
	{
		public string[] myp;
		// 启用下方设置的密码，请将false 改为 true

		public Mypassword()
		{


			// 你也可以使用其他的方式，如文件读取、网络读取等等，当然这需要自行编程
			// 只需要将其组装为字符串数组并存入myp字段即可。
			// 最不要忘记将 UseOtherPassword = false; 改为 UseOtherPassword = true;

			// 设置外部密码来源
			// 0 不启用
			// 1 内置密码
			// 2 网络网址
			// 3 文件路径

			int ReadPasswordMode = USetting.ReadPasswordMode;
			
			// 不启用
			if (ReadPasswordMode == 0) 
			{

			}
			
			// 内置密码
			if (ReadPasswordMode == 1) 
			{
				myp = new string[]
				{
					// 在这里设置内置的解压密码
					"password1",
					"password2",
					"password3",
					"password4",
					"password5",
					"password6"
				};
			}

			// 从文件读取密码
			if (ReadPasswordMode == 2 && USetting.PWUrl != "")
			{
				
				myp = ReadFileTxt(USetting.PWUrl);
				
			}

			// 通过网络读取密码,https暂不支持
			if (ReadPasswordMode == 3 && USetting.PWUrl != "") 
			{
				myp = ReadWebTxt(USetting.PWUrl);
			}

			// 通过隐藏的网络读取密码
			if (ReadPasswordMode == 4) 
			{
				// 如果你希望将网址隐藏起来，请参考下面的方式修改代码
				// 需要注意https暂不支持
				myp = ReadWebTxt(@"http://password.com/pw.txt");
			}

		}


		// 从网路读取数据
		public string[] ReadWebTxt(string Webtxt)
		{
			List<string> lp = new List<string>();

			try
			{
				HttpWebRequest r = (HttpWebRequest)WebRequest.Create(Webtxt);
				WebResponse wr = r.GetResponse();
				Stream s = wr.GetResponseStream();

				using (StreamReader sr = new StreamReader(s, Encoding.UTF8))
				{
					string line = string.Empty;
					while ((line = sr.ReadLine()) != null)
					{
						
						lp.Add(line);
					}
				}
			}
			catch (Exception ex)
			{
				//MessageBox.Show("网络错误");
			}
			if (lp.Count >0)
			{
				return lp.ToArray();
			}
			else
			{
				return null;
			}
		}

		// 从文件读取密码
		public string[] ReadFileTxt(string filetxt) 
		{
			List<string> lp = new List<string>();
			if (!File.Exists(filetxt)) return null;
			try
			{
				StreamReader sr = new StreamReader(filetxt);
				string line = null;
				while (!sr.EndOfStream)
				{
					line = sr.ReadLine();
					lp.Add(line);
				}
			}
			catch (Exception ex)
			{
				//MessageBox.Show("网络错误");
			}
			if (lp.Count > 0)
			{
				return lp.ToArray();
			}
			else
			{
				return null;
			}
		}
	
	}
}
