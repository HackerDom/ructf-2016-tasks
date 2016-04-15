using System;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

namespace winme
{
	class Program
	{
		public static string playersId;
		static void Main(string[] args)
		{
			Console.WriteLine("Hello, I want to play a game with you!");
			Console.WriteLine("It's oldy-moldy rock-paper-scissors-lizard-Spock");
			Console.WriteLine("Here are the rules: \n\r Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors, scissors decapitate lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock. And as it always has, rock crushes scissors.");
			Console.WriteLine("Please, type your number:");
			playersId = Console.ReadLine();
			while (true)
			{
				Console.WriteLine("Type your gesture:");
				var gesture = Console.ReadLine() ?? "";
				string myChoice;
				switch (gesture.Trim().ToLower())
				{
					case "rock":
						myChoice = "paper";
						break;
					case "paper":
						myChoice = "scissors";
						break;
					case "lizard":
						myChoice = "rock";
						break;
					case "spock":
						myChoice = "lizard";
						break;
					case "scissors":
						myChoice = "spock";
						break;
					default:
						{
							Console.WriteLine("I do not understand you");
							continue;
						}
				}
				Console.WriteLine("My choice is {0}, aaand... I win!", myChoice);
				Console.WriteLine("I make my move after you've made yours, do you really believe you can win? But you can always try again! :-P");
			}
		}

		public static string GenerateFlag(string playersId)
		{
			var appName = AppDomain.CurrentDomain.FriendlyName;
			var appVersion = Assembly.GetExecutingAssembly().GetName().Version;
			var today = DateTime.Now.DayOfWeek.ToString();
			var os = Environment.OSVersion.VersionString;
			byte[] suffix;
			var result = ConfuseEm(playersId, appName, today, appVersion, os, Environment.ProcessorCount,
				Environment.Is64BitOperatingSystem, Environment.MachineName, out suffix);
			Console.WriteLine(result);

			if (!string.IsNullOrEmpty(playersId))
			{
				var flag = Xor(result, suffix);
				return BitConverter.ToString(flag);
			}
			return "";
		}

		public static byte[] ConfuseEm(string playersId, string appName, string today, Version appVersion, string os,
			int processorCount, bool is64BitOperatingSystem, string machineName, out byte[] rightPart)
		{
			rightPart = new byte[processorCount*2];
			if (is64BitOperatingSystem)
			{
				var rv = Encoding.UTF8.GetBytes(os)
					.Concat(Encoding.UTF8.GetBytes(machineName))
					.Concat(Encoding.UTF8.GetBytes(appName));
				rightPart = rv.ToArray();
			}
			else
			{
				for (var i = 0; i < processorCount*2; i += sizeof (char))
				{
					if (appVersion.MajorRevision > 1)
						BitConverter.GetBytes(appName[i%appName.Length]).CopyTo(rightPart, i);
					else
						BitConverter.GetBytes(machineName[i%machineName.Length]).CopyTo(rightPart, i);
				}
			}
			var strings = Encoding.UTF8.GetBytes(string.Format("{0}{1}{2}",playersId, appName, today));

			var md5 = MD5.Create();
			var leftPart = md5.ComputeHash(strings);

			var resultBytes = Xor(leftPart, rightPart);
			return resultBytes;
		}

		public static byte[] Xor(byte[] l, byte[] r)
		{
			var length = Math.Max(l.Length, r.Length);
			var leftPart = new byte[length];
			var rightPart = new byte[length];
			l.CopyTo(leftPart, 0);
			r.CopyTo(rightPart, 0);
			

			var result = new byte[length];
			for (var i = 0; i < length; i++)
			{
				result[i] = (byte)(leftPart[i] ^ rightPart[i]);
			}
			return result;
		}
	}
}
