using System.Collections.Generic;
using System.Configuration;
using System.Linq;

namespace UZIP2
{

	// 此类需要手动引用 框架 System.Configuration
	// 用于读写配置文件
	public class Config
	{
		public Configuration configObject;

		/// <summary>
		/// 根据路径获取配置文件
		/// </summary>
		/// <param name="key">键值</param>
		/// <returns></returns>
		public Config(string configPath)
		{
			ExeConfigurationFileMap fileMap = new ExeConfigurationFileMap();
			fileMap.ExeConfigFilename = configPath;
			this.configObject = ConfigurationManager.OpenMappedExeConfiguration(fileMap, ConfigurationUserLevel.None);
		}

		public string GetConfig(string key)
		{
			string val = string.Empty;

			if (this.configObject.AppSettings.Settings.AllKeys.Contains(key))
				val = this.configObject.AppSettings.Settings[key].Value;

			return val;
		}

		/// <summary>
		/// 获取所有配置文件
		/// </summary>
		/// <returns></returns>
		public Dictionary<string, string> GetConfig()
		{
			Dictionary<string, string> dict = new Dictionary<string, string>();
			foreach (string key in this.configObject.AppSettings.Settings.AllKeys)
				dict.Add(key, this.configObject.AppSettings.Settings[key].Value);

			return dict;
		}

		/// <summary>
		/// 根据键值获取配置文件
		/// </summary>
		/// <param name="key">键值</param>
		/// <param name="defaultValue">默认值</param>
		/// <returns></returns>
		public string GetConfig(string key, string defaultValue)
		{
			string val = defaultValue;
			if (this.configObject.AppSettings.Settings.AllKeys.Contains(key))
				val = this.configObject.AppSettings.Settings[key].Value;

			if (val == null)
				val = defaultValue;

			return val;
		}

		/// <summary>
		/// 写配置文件,如果节点不存在则自动创建
		/// </summary>
		/// <param name="key">键值</param>
		/// <param name="value">值</param>
		/// <returns></returns>
		public bool SetConfig(string key, string value)
		{
			try
			{
				//Configuration conf = ConfigurationManager.OpenExeConfiguration(ConfigurationUserLevel.None);
				if (!this.configObject.AppSettings.Settings.AllKeys.Contains(key))
					this.configObject.AppSettings.Settings.Add(key, value);
				else
					this.configObject.AppSettings.Settings[key].Value = value;
				this.configObject.Save(ConfigurationSaveMode.Modified);
				//ConfigurationManager.RefreshSection("appSettings");

				return true;
			}

			catch { return false; }
		}

		/// <summary>
		/// 写配置文件(用键值创建),如果节点不存在则自动创建
		/// </summary>
		/// <param name="dict">键值集合</param>
		/// <returns></returns>
		public bool SetConfig(Dictionary<string, string> dict)
		{
			try
			{
				if (dict == null || dict.Count == 0)
					return false;

				//Configuration conf = ConfigurationManager.OpenExeConfiguration(ConfigurationUserLevel.None);
				foreach (string key in dict.Keys)
				{
					if (!this.configObject.AppSettings.Settings.AllKeys.Contains(key))
						this.configObject.AppSettings.Settings.Add(key, dict[key]);
					else
						this.configObject.AppSettings.Settings[key].Value = dict[key];
				}

				this.configObject.Save(ConfigurationSaveMode.Modified);

				return true;
			}
			catch { return false; }
		}
	}

	public class ItemsSection : ConfigurationSection
	{
		[ConfigurationProperty("items", IsRequired = true)]
		public string Category
		{
			get
			{
				return (string)base["Category"];
			}

			set
			{
				base["Category"] = value;
			}
		}
		[ConfigurationProperty("", IsDefaultCollection = true)]
		public ItemElementCollection Books
		{
			get
			{
				return (ItemElementCollection)base[""];
			}
		}
	}

	public class ItemElementCollection : ConfigurationElementCollection
	{
		protected override ConfigurationElement CreateNewElement()
		{
			return new ItemElement();
		}

		protected override object GetElementKey(ConfigurationElement element)
		{
			return ((ItemElement)element).Name;
		}

		public override ConfigurationElementCollectionType CollectionType
		{
			get
			{
				return ConfigurationElementCollectionType.BasicMap;
			}
		}
		protected override string ElementName
		{
			get
			{
				return "item";
			}
		}
		public ItemElement this[int index]
		{
			get
			{
				return (ItemElement)BaseGet(index);
			}
			set
			{
				if (BaseGet(index) != null)
				{
					BaseRemoveAt(index);
				}
				BaseAdd(index, value);
			}

		}
	}

	public class ItemElement : ConfigurationElement
	{
		[ConfigurationProperty("name", IsRequired = true)]
		public string Name
		{
			get
			{
				return (string)base["name"];
			}

			set
			{
				base["name"] = value;
			}
		}

		[ConfigurationProperty("icon", IsRequired = true)]

		public string Icon
		{
			get
			{
				return (string)base["icon"];
			}

			set
			{
				base["icon"] = value;
			}
		}

		[ConfigurationProperty("assembly", IsRequired = true)]
		public string Assembly
		{
			get
			{
				return (string)base["assembly"];
			}

			set
			{
				base["assembly"] = value;
			}
		}

		[ConfigurationProperty("target", IsRequired = true)]
		public string Target
		{
			get
			{
				return (string)base["target"];
			}

			set
			{
				base["target"] = value;
			}
		}

		[ConfigurationProperty("kind", IsRequired = true)]
		public string Kind
		{
			get
			{
				return (string)base["kind"];
			}

			set
			{
				base["name"] = value;
			}
		}
	}
}

//库来源
//https://blog.csdn.net/qq_29844879/article/details/80207619?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.control
